# Task API endpoints
from fastapi import APIRouter,Body, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from app.models.task import Task, TaskStatus, TaskState, TaskCreate, TaskUpdate
from app.db.repositories.task_repository import TaskRepository
from app.core.marc1.execution_engine import ExecutionEngine
from app.core.marc1.task_manager import TaskManager
from app.core.marc1.tool_registry import get_tool_registry
from app.dependencies import get_db
# Add this import at the top of the file
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any, List, Optional
import logging
import glob
import json
import traceback
import asyncio
from datetime import datetime
import uuid
import os
import time
from pathlib import Path
import base64
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.core.webSocket.screenshot_manager import (
    connect_client, 
    disconnect_client, 
    register_task, 
    initialize_screenshot_watcher,
    active_connections,
    task_user_mappings
)
from app.core.auth.jwt_handler import JWTHandler
# from app.automation.robot.robot_driver import set_ws_broadcast_function as set_robot_ws_broadcast

logger = logging.getLogger(__name__)
router = APIRouter()
# Initialize screenshot watcher
screenshot_watcher = initialize_screenshot_watcher()

# set_robot_ws_broadcast(broadcast_to_task_clients)
# Get task manager instance
def get_task_manager(db=Depends(get_db)):
    task_repo = TaskRepository(db)
    execution_engine = ExecutionEngine(task_repo)
    return TaskManager(task_repo, execution_engine)

@router.get("/{task_id}/summary")
async def get_task_summary(
    task_id: str,
    db=Depends(get_db)
):
    """Get a summary of a completed task"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    # Check if task is completed or failed
    if task.current_state.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        return {
            "task_id": task_id,
            "status": task.current_state.status,
            "message": "Task is still in progress or awaiting approval"
        }
    
    # Get completion or failure summary
    if task.current_state.status == TaskStatus.COMPLETED:
        summary = task.current_state.metadata.get("completion_summary", {})
        summary_type = "completion"
    elif task.current_state.status == TaskStatus.FAILED:
        summary = task.current_state.metadata.get("failure_summary", {})
        summary_type = "failure"
    else:  # REJECTED
        summary = {
            "rejection_reason": task.current_state.metadata.get("rejection_reason", "Unknown reason"),
            "rejected_at": task.current_state.metadata.get("rejected_at", datetime.utcnow().isoformat())
        }
        summary_type = "rejection"
    
    # Prepare response
    response = {
        "task_id": task_id,
        "status": task.current_state.status,
        "summary_type": summary_type,
        "summary": summary,
        "outputs": task.current_state.outputs,
        "errors": task.current_state.errors,
        "duration_seconds": summary.get("duration_seconds"),
        "timestamp": summary.get("end_time")
    }
    
    return response

@router.post("/{task_id}/feedback")
async def submit_task_feedback(
    task_id: str,
    feedback: Dict[str, Any] = Body(...),
    db=Depends(get_db)
):
    """Submit feedback for a completed task"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    # Check if task is completed or failed
    if task.current_state.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        raise HTTPException(400, "Cannot submit feedback for tasks that are not completed or failed")
    
    # Update task with feedback
    if "feedback" not in task.current_state.metadata:
        task.current_state.metadata["feedback"] = []
    
    # Add timestamp to feedback
    feedback["timestamp"] = datetime.utcnow().isoformat()
    
    # Add feedback to task
    task.current_state.metadata["feedback"].append(feedback)
    
    # Update task in database
    await task_repo.update_task(task)
    
    # Log feedback
    from app.utils.logging import log_task_event
    await log_task_event(
        task_id=task_id,
        event=f"Feedback submitted: {feedback.get('rating', 'N/A')}/5",
        metadata={"feedback": feedback}
    )
    
    return {"message": "Feedback submitted successfully"}

@router.post("/", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    current_user: dict = Depends(JWTHandler.get_current_user)
):
    """Create a new task"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Validate tools
    tool_registry = get_tool_registry()
    for tool_config in task_create.tools:
        errors = tool_registry.validate_tool_config(tool_config)
        if errors:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid tool configuration: {', '.join(errors)}"
            )
    
    # Create task
    task = Task(
        id=str(uuid.uuid4()),
        name=task_create.name,
        description=task_create.description,
        workflow_type=task_create.workflow_type,
        tools=task_create.tools,
        parameters=task_create.parameters,
        context=task_create.context,
        metadata=task_create.metadata,
        created_at=datetime.utcnow().isoformat(),
        current_state=TaskState(
            task_id=None,  # Will be set after task is created
            status=TaskStatus.PENDING,
            parameters=task_create.parameters,
            context=task_create.context
        )
    )
    
    # Set task ID in current state
    task.current_state.task_id = task.id
    
    # Save task
    await task_repo.create_task(task)
    
    # Register task with screenshot manager
    register_task(task.id, current_user["user_id"])

    # Start execution in background if auto_execute is enabled
    if task_create.auto_execute:
        background_tasks.add_task(execute_task_background, task.id, db)
    
    return task

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    db=Depends(get_db)
):
    """Get a task by ID"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    return task



@router.get("/", response_model=List[Task])
async def list_tasks(
    limit: int = 100,
    offset: int = 0,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db=Depends(get_db)
):
    """
    List tasks with pagination, sorted by recency (newest first)
    
    Parameters:
    - limit: Maximum number of tasks to return (default: 100)
    - offset: Number of tasks to skip (default: 0)
    - status: Filter tasks by status
    - start_date: Filter tasks created on or after this date (ISO format: YYYY-MM-DD)
    - end_date: Filter tasks created on or before this date (ISO format: YYYY-MM-DD)
    """
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Build query
    query = {}
    if status:
        query["current_state.status"] = status
    
    # Add date filters if provided - FIXED: Use datetime objects instead of strings
    if start_date or end_date:
        query["created_at"] = {}
        
        if start_date:
            try:
                # Convert to datetime object for MongoDB comparison
                start_datetime = datetime.fromisoformat(f"{start_date}T00:00:00")
                query["created_at"]["$gte"] = start_datetime  # Use datetime object directly
                logger.debug(f"Added start_date filter: {start_datetime}")
            except ValueError:
                raise HTTPException(400, "Invalid start_date format. Use YYYY-MM-DD")
                
        if end_date:
            try:
                # Set time to end of day and use datetime object
                end_datetime = datetime.fromisoformat(f"{end_date}T23:59:59")
                query["created_at"]["$lte"] = end_datetime  # Use datetime object directly
                logger.debug(f"Added end_date filter: {end_datetime}")
            except ValueError:
                raise HTTPException(400, "Invalid end_date format. Use YYYY-MM-DD")
    
    # Log the query for debugging
    logger.debug(f"MongoDB query: {json.dumps(query, default=str)}")
    print("Query:", query)
    
    # For debugging, get all tasks first
    all_tasks_count = await task_repo.count({})
    logger.debug(f"Total tasks in database: {all_tasks_count}")
    print("Total tasks:", all_tasks_count)
    
    # Get total count for pagination metadata
    total_count = await task_repo.count(query)
    print("Matching tasks:", total_count)
    logger.debug(f"Tasks matching query: {total_count}")
    
    # Get tasks with pagination, sorted by created_at in descending order (newest first)
    tasks = await task_repo.listAll(query, limit, offset, sort=[("created_at", -1)])
    print("Retrieved tasks:", len(tasks))
    logger.debug(f"Retrieved {len(tasks)} tasks")
    
    # Add pagination metadata to response
    pagination = {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + len(tasks)) < total_count
    }
    
    # Use FastAPI's jsonable_encoder to handle datetime serialization
    serialized_tasks = jsonable_encoder(tasks)
    
    # Return tasks with pagination metadata
    return JSONResponse(
        content={
            "items": serialized_tasks,
            "pagination": pagination,
            "filters_applied": {
                "status": status,
                "start_date": start_date,
                "end_date": end_date
            }
        }
    )

@router.post("/{task_id}/resume", response_model=Task)
async def resume_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Resume a paused task"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is paused
    if task.current_state.status != TaskStatus.PAUSED:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not paused: {task_id}"
        )
    
    # Update task status to RUNNING
    task.current_state.status = TaskStatus.RUNNING
    task.current_state.requires_approval = False
    task.current_state.metadata["resumed_at"] = datetime.utcnow().isoformat()
    await task_repo.update_task(task)
    
    # Start execution in background
    background_tasks.add_task(resume_task_background, task_id, db)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

@router.post("/{task_id}/edit", response_model=Task)
async def edit_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    edited_data: Dict[str, Any] = Body(...)
    
):
    """Edit a paused task and restart it with new parameters"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is paused
    if task.current_state.status != TaskStatus.PAUSED:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not paused: {task_id}"
        )
    
    # Update task parameters
    if "parameters" in edited_data:
        task.parameters.update(edited_data["parameters"])
        # Also update parameters in each tool configuration
        for tool in task.tools:
            # Only update parameters that exist in the tool
            for param_key, param_value in edited_data["parameters"].items():
                if param_key in tool.get("parameters", {}):
                    tool["parameters"][param_key] = param_value

        # Also update parameters in current state if they exist
        if hasattr(task.current_state, 'parameters') and task.current_state.parameters is not None:
            task.current_state.parameters.update(edited_data["parameters"])        
        # Update MARC1 parameters in context if they exist
        if "context" in task.__dict__ and task.context:
            # Update parameters in marc1_intent if it exists
            if "marc1_intent" in task.context:
                if "parameters" in task.context["marc1_intent"]:
                    for param_key, param_value in edited_data["parameters"].items():
                        if param_key in task.context["marc1_intent"]["parameters"]:
                            task.context["marc1_intent"]["parameters"][param_key] = param_value
    # Add edit metadata
    if "edit_history" not in task.metadata:
        task.metadata["edit_history"] = []
    
    # Record edit in history
    task.metadata["edit_history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "edited_parameters": edited_data.get("parameters", {})
    })
    
    # Update task status to indicate it's been edited
    task.current_state.status = TaskStatus.PAUSED
    task.current_state.requires_approval = True
    task.current_state.metadata["edited"] = True
    task.current_state.metadata["edit_timestamp"] = datetime.utcnow().isoformat()
    task.current_state.metadata["pause_reason"] = "Task edited, awaiting approval"
    await task_repo.update_task(task)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

# Update the existing reject_task function to handle rejection with reason
@router.post("/{task_id}/reject", response_model=Task)
async def reject_task(
    task_id: str,
    rejection_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
):
    """Reject a task that is pending human approval"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is pending approval
    if task.current_state.status != TaskStatus.PAUSED:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not paused: {task_id}"
        )
    
    # Get rejection reason
    rejection_reason = rejection_data.get("reason", "No reason provided")
    
    # Update task status to REJECTED
    task.current_state.status = TaskStatus.REJECTED
    task.current_state.requires_approval = False
    
    task.current_state.metadata["rejection_reason"] = rejection_reason
    task.current_state.metadata["rejected_at"] = datetime.utcnow().isoformat()
    # Update task in database
    await task_repo.update_task(task)
    
    # Log rejection event - Fix the NoneType error by checking if log_task_event is properly imported
    try:
        from app.utils.logging import log_task_event, LogLevel
        await log_task_event(
            task_id=task_id,
            event=f"Task rejected: {reason}",
            level=LogLevel.INFO,
            metadata={"rejection_reason": reason}
        )
    except Exception as e:
        # Log the error but don't fail the request
        logger.error(f"Error logging task rejection: {str(e)}")
    
    # Notify WebSocket clients if the function exists
    if 'notify_task_update' in globals():
        try:
            await notify_task_update(task)
        except Exception as e:
            logger.error(f"Error notifying task update: {str(e)}")


    return task

@router.get("/pending-approval", response_model=List[Task])
async def get_pending_approval_tasks(
    limit: int = 100,
    db=Depends(get_db)
):
    """Get tasks that are pending human approval"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get tasks pending approval
    query = {"current_state.status": TaskStatus.PAUSED, "current_state.requires_approval": True}
    tasks = await task_repo.listAll(query, limit, 0, sort=[("created_at", -1)])
    
    return tasks

@router.post("/{task_id}/execute", response_model=Task)
async def execute_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Execute a task"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is already running
    if task.current_state.status in [TaskStatus.RUNNING, TaskStatus.QUEUED]:
        raise HTTPException(
            status_code=400,
            detail=f"Task is already running: {task_id}"
        )
    
    # Update task status
    task.current_state.status = TaskStatus.QUEUED
    await task_repo.update_task(task)
    
    # Start execution in background
    background_tasks.add_task(execute_task_background, task_id, db)
    
    return task


@router.post("/{task_id}/cancel", response_model=Task)
async def cancel_task(
    task_id: str,
    db=Depends(get_db)
):
    """Cancel a running task"""
    # Create task repository and execution engine
    task_repo = TaskRepository(db)
    execution_engine = ExecutionEngine(task_repo)
    # **ADD: Mark as cancelled FIRST, before any other operations**
    cancel_state = await execution_engine.cancel_task(task_id)

    

    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Update task state
    task.current_state = cancel_state
    await task_repo.update_task(task)
    
    # **ADD: Force cleanup of any running processes**
    try:
        from app.automation.robot.cargowise_automation import CargoWiseAutomation
        from app.ai.tools.browser_tools import BrowserSessionManager
        
        # Cancel CargoWise automation with task_id
        cw_automation = CargoWiseAutomation(task_id=task_id)
        #await cw_automation.cancel_automation()
        
        # Close browser sessions
        await BrowserSessionManager.cleanup()
    except Exception as e:
        logger.error(f"Error during automation cancellation: {str(e)}")

    # # Check if task can be cancelled
    # if task.current_state.status not in [TaskStatus.RUNNING, TaskStatus.PAUSED]:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Task cannot be cancelled: {task_id} (status: {task.current_state.status})"
    #     )
    
    # # Cancel task
    # cancel_state = await execution_engine.cancel_task(task_id)
    
    
    
    # # Notify WebSocket clients
    # await notify_task_update(task)
    
    # # Also try to cancel any running automation
    # try:
    #     # Import automation components
    #     from app.automation.robot.cargowise_automation import CargoWiseAutomation
    #     from app.ai.tools.browser_tools import BrowserSessionManager
        
    #     # Cancel CargoWise automation
    #     cw_automation = CargoWiseAutomation(task_id=task_id)
    #     await cw_automation.cancel_automation()
        
    #     # Close browser sessions
    #     await BrowserSessionManager.cleanup()
    # except Exception as e:
    #     logger.error(f"Error during automation cancellation: {str(e)}")
    # Notify WebSocket clients
    await notify_task_update(task)
    return task
@router.post("/{task_id}/approve", response_model=Task)
async def approve_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    approval_data: Dict[str, Any] = Body(...)
):
    """Approve a task that is pending human approval"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    logger.info(f"Approving task {task_id}")
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is pending approval
    if task.current_state.status != TaskStatus.PAUSED or not task.current_state.requires_approval:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not pending approval: {task_id}"
        )
    
    # Approve task
    success = await task_repo.approve_task(task_id, approval_data)
    if not success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to approve task: {task_id}"
        )
    
    # Get updated task
    task = await task_repo.get_task(task_id)
    
    # Explicitly set task to RUNNING state
    task.current_state.status = TaskStatus.RUNNING
    task.current_state.requires_approval = False
    task.current_state.metadata["resumed_at"] = datetime.utcnow().isoformat()
    task.current_state.metadata["approved_at"] = datetime.utcnow().isoformat()
    task.current_state.metadata["approved_by"] = approval_data.get("user", "unknown")
    await task_repo.update_task(task)
    
    # Resume execution in background
    background_tasks.add_task(resume_task_background, task_id, db)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

# Add this new endpoint after the existing endpoints
@router.get("/{task_id}/screenshots")
async def get_task_screenshots(
    task_id: str,
    db=Depends(get_db)
):
    """Get all PNG screenshots for a specific task"""
    # Verify task exists
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    # Define screenshot directory path
    screenshot_base_dir = Path("C:/Users/UK-PC/Desktop/AI driven cargo-wise automation framework/cargowise-ai-backend/screenshots")
    task_screenshot_dir = screenshot_base_dir / task_id
    
    # Check if task screenshot directory exists
    if not task_screenshot_dir.exists():
        return {
            "task_id": task_id,
            "screenshots": [],
            "message": "No screenshots found for this task"
        }
    
    # Get all PNG files in the task directory
    png_files = list(task_screenshot_dir.glob("*.png"))
    
    if not png_files:
        return {
            "task_id": task_id,
            "screenshots": [],
            "message": "No PNG files found for this task"
        }
    
    # Sort by creation time (newest first)
    png_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    
    # Prepare response with file information
    screenshots = []
    for png_file in png_files:
        screenshots.append({
            "filename": png_file.name,
            "path": str(png_file),
            "size_bytes": png_file.stat().st_size,
            "created_at": datetime.fromtimestamp(png_file.stat().st_mtime).isoformat(),
            "download_url": f"/api/v1/tasks/{task_id}/screenshots/{png_file.name}"
        })
    
    return {
        "task_id": task_id,
        "screenshots": screenshots,
        "total_count": len(screenshots)
    }

@router.get("/{task_id}/screenshots/{filename}")
async def download_task_screenshot(
    task_id: str,
    filename: str,
    db=Depends(get_db)
):
    """Download a specific PNG screenshot for a task"""
    # Verify task exists
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    # Define screenshot directory path
    screenshot_base_dir = Path("C:/Users/UK-PC/Desktop/AI driven cargo-wise automation framework/cargowise-ai-backend/screenshots")
    task_screenshot_dir = screenshot_base_dir / task_id
    
    # Construct full file path
    file_path = task_screenshot_dir / filename
    
    # Security check: ensure the file is within the task directory
    try:
        file_path = file_path.resolve()
        task_screenshot_dir = task_screenshot_dir.resolve()
        if not str(file_path).startswith(str(task_screenshot_dir)):
            raise HTTPException(403, "Access denied")
    except Exception:
        raise HTTPException(403, "Invalid file path")
    
    # Check if file exists and is a PNG
    if not file_path.exists():
        raise HTTPException(404, "Screenshot not found")
    
    if not file_path.suffix.lower() == '.png':
        raise HTTPException(400, "Only PNG files are supported")
    
    # Return the file
    return FileResponse(
        path=str(file_path),
        media_type="image/png",
        filename=filename
    )

# WebSocket endpoint for task screenshots
@router.websocket("/ws/{task_id}")
async def websocket_task_endpoint(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time task screenshots"""
    # Get token from query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        return
    
    # Validate token
    try:
        payload = JWTHandler.decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    try:
        # Connect client with task_id
        await connect_client(websocket, user_id, task_id)
        
        # Keep connection alive until client disconnects
        while True:
            # Wait for messages (ping/pong handled automatically)
            data = await websocket.receive_text()
            # Process any client messages if needed
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: user_id={user_id}, task_id={task_id}")
        await disconnect_client(user_id, task_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await disconnect_client(user_id, task_id) 

# WebSocket endpoint for user's general connection
@router.websocket("/ws/user")
async def websocket_user_endpoint(websocket: WebSocket):
    """WebSocket endpoint for user's general connection"""
    # Get token from query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        return
    
    # Validate token
    try:
        payload = JWTHandler.decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    try:
        # Connect client without task_id (general connection)
        await connect_client(websocket, user_id)
        
        # Keep connection alive until client disconnects
        while True:
            # Wait for messages (ping/pong handled automatically)
            data = await websocket.receive_text()
            # Process any client messages if needed
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: user_id={user_id}")
        await disconnect_client(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await disconnect_client(user_id)

async def notify_task_update(task: Task):
    """Notify WebSocket clients of task updates"""
    try:
        # Convert task to JSON-serializable format
        # Use FastAPI's jsonable_encoder to handle datetime objects
        task_data = jsonable_encoder(task)
        
        # Get user_id for this task
        user_id = task_user_mappings.get(task.id)
        if not user_id:
            logger.debug(f"No user mapped for task {task.id}")
            return
        
        # Check if user has active connections
        if user_id not in active_connections:
            logger.debug(f"No active connections for user {user_id}")
            return
        
        # Send to all connections for this user
        user_connections = active_connections[user_id]
        for connection_key, websocket in user_connections.items():
            try:
                await websocket.send_json({
                    "type": "task_update",
                    "data": task_data
                })
                logger.debug(f"Task update sent to user {user_id}, connection {connection_key}")
            except Exception as e:
                logger.error(f"Error sending WebSocket update to {user_id}/{connection_key}: {str(e)}")
                # Connection might be closed, but we'll let the disconnect handler clean it up
    except Exception as e:
        logger.error(f"Error in notify_task_update: {str(e)}", exc_info=True)

# Add at module level
_running_tasks = set()
async def execute_task_background(task_id: str, db):
    """Execute a task in the background"""
    # **FIX: Prevent multiple instances of the same task**
    if task_id in _running_tasks:
        logger.warning(f"Task {task_id} is already running, skipping duplicate execution")
        return
    
    _running_tasks.add(task_id)
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return

    execution_engine = ExecutionEngine()
    
    try:
        async for state in execution_engine.execute_task(task):
            # **FIX: Check cancellation BEFORE processing state**
            if task_id in execution_engine._cancelled_tasks:
                logger.info(f"Task {task_id} was cancelled, stopping background execution")
                # Ensure final cancelled state is saved
                task.current_state.status = TaskStatus.CANCELED
                task.current_state.error = "Task was cancelled by user"
                await task_repo.update_task(task)
                await notify_task_update(task)
                return  # Exit immediately
            
            # **FIX: Double-check database state**
            current_task = await task_repo.get_task(task_id)
            if current_task and current_task.current_state.status == TaskStatus.CANCELED:
                logger.info(f"Task {task_id} was cancelled (database check), stopping execution")
                return  # Exit immediately
            
            # Update task state
            task.current_state = state
            await task_repo.update_task(task)
            
            # Ensure task_id is in context for tools to use
            if not task.current_state.context:
                task.current_state.context = {}
            task.current_state.context["task_id"] = task_id
            
            # Notify WebSocket clients
            await notify_task_update(task)
            
            # **FIX: Exit immediately on cancellation**
            if state.status == TaskStatus.CANCELED:
                logger.info(f"Task {task_id} reached CANCELED status, stopping execution")
                return
            
            # If execution paused or completed, break
            if state.status in [TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED]:
                break
                
    except Exception as e:
        # **FIX: Check if cancellation caused the exception**
        if task_id in execution_engine._cancelled_tasks:
            logger.info(f"Task {task_id} exception due to cancellation, preserving CANCELED status")
            task.current_state.status = TaskStatus.CANCELED
            task.current_state.error = "Task was cancelled by user"
        else:
            logger.error(f"Error executing task {task_id}: {str(e)}")
            task.current_state.status = TaskStatus.FAILED
            task.current_state.error = str(e)
            task.current_state.metadata["error_details"] = {
                "exception_type": type(e).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        await task_repo.update_task(task)
        await notify_task_update(task)
    finally:
        # **FIX: Remove task from running set**
        _running_tasks.remove(task_id)


# Update the resume_task_background function to properly handle task resumption
async def resume_task_background(task_id: str, db):
    """Resume a paused task in the background"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return
    
    # Create execution engine
    execution_engine = ExecutionEngine(task_repo)
    
    try:
        # Ensure task_id is in context for tools to use
        if not task.current_state.context:
            task.current_state.context = {}
        task.current_state.context["task_id"] = task_id
        await task_repo.update_task(task)
        # Resume task execution
        async for state in execution_engine.resume_task(task):
            # Update task state
            task.current_state = state
            # Ensure task_id is in context for tools to use
            if not task.current_state.context:
                task.current_state.context = {}
            task.current_state.context["task_id"] = task_id
            await task_repo.update_task(task)
            
            # Notify WebSocket clients
            await notify_task_update(task)
            
            # If execution paused or completed, break
            if state.status in [TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELED]:
                break
                
    except asyncio.CancelledError:
        logger.error(f"Task resumption was canceled for task {task_id}")
        # Don't update task state here, as it might be a normal cancellation
        
    except Exception as e:
        logger.error(f"Error resuming task {task_id}: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Update task status to failed
        task.current_state.status = TaskStatus.FAILED
        task.current_state.error = f"Error resuming task: {str(e)}"
        task.current_state.metadata["error_details"] = {
            "exception_type": type(e).__name__,
            "timestamp": datetime.utcnow().isoformat(),
            "traceback": traceback.format_exc()
        }
        await task_repo.update_task(task)
        
        # Notify WebSocket clients
        await notify_task_update(task)