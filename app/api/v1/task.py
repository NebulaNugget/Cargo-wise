# Task API endpoints
from fastapi import APIRouter,Body, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from app.models.task import Task, TaskStatus, TaskState, TaskCreate, TaskUpdate
from app.db.repositories.task_repository import TaskRepository
from app.core.marc1.execution_engine import ExecutionEngine
from app.core.marc1.tool_registry import get_tool_registry
from app.dependencies import get_db
# Add this import at the top of the file
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any, List, Optional
import logging
import json
import asyncio
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

# Active WebSocket connections for task status updates
active_connections: Dict[str, List[WebSocket]] = {}

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
    else:
        summary = task.current_state.metadata.get("failure_summary", {})
        summary_type = "failure"
    
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
    db=Depends(get_db)
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
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    # Check if task is running
    if task.current_state.status not in [TaskStatus.RUNNING, TaskStatus.QUEUED, TaskStatus.PAUSED]:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not running: {task_id}"
        )
    
    # Update task status
    task.current_state.status = TaskStatus.CANCELLED
    task.current_state.metadata["cancelled_at"] = datetime.utcnow().isoformat()
    await task_repo.update_task(task)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

@router.post("/{task_id}/approve", response_model=Task)
async def approve_task(
    task_id: str,
    approval_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Approve a task that is pending human approval"""
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
    
    # Resume execution in background
    background_tasks.add_task(resume_task_background, task_id, db)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

@router.post("/{task_id}/reject", response_model=Task)
async def reject_task(
    task_id: str,
    rejection_data: Dict[str, Any],
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
    if task.current_state.status != TaskStatus.PAUSED or not task.current_state.requires_approval:
        raise HTTPException(
            status_code=400,
            detail=f"Task is not pending approval: {task_id}"
        )
    
    # Reject task
    success = await task_repo.reject_task(task_id, rejection_data)
    if not success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reject task: {task_id}"
        )
    
    # Get updated task
    task = await task_repo.get_task(task_id)
    
    # Notify WebSocket clients
    await notify_task_update(task)
    
    return task

@router.websocket("/ws/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: str,
    db=Depends(get_db)
):
    """WebSocket endpoint for task status updates"""
    await websocket.accept()
    
    # Add connection to active connections
    if task_id not in active_connections:
        active_connections[task_id] = []
    active_connections[task_id].append(websocket)
    
    try:
        # Send initial task state
        task_repo = TaskRepository(db)
        task = await task_repo.get_task(task_id)
        if task:
            await websocket.send_json(task.dict())
        
        # Keep connection open
        while True:
            # Wait for client messages (ping/pong)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
            
    except WebSocketDisconnect:
        # Remove connection from active connections
        if task_id in active_connections:
            active_connections[task_id].remove(websocket)
            if not active_connections[task_id]:
                del active_connections[task_id]

async def notify_task_update(task: Task):
    """Notify WebSocket clients of task update"""
    if task.id in active_connections:
        for connection in active_connections[task.id]:
            try:
                await connection.send_json(task.dict())
            except Exception as e:
                logger.error(f"Error sending WebSocket update: {str(e)}")

async def execute_task_background(task_id: str, db):
    """Execute a task in the background"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return
    
    # Create execution engine
    execution_engine = ExecutionEngine()
    
    try:
        # Execute task
        async for state in execution_engine.execute_task(task):
            # Update task state
            task.current_state = state
            await task_repo.update_task(task)
            
            # Notify WebSocket clients
            await notify_task_update(task)
            
            # If execution paused or completed, break
            if state.status in [TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                break
                
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {str(e)}")
        
        # Update task status to failed
        task.current_state.status = TaskStatus.FAILED
        task.current_state.error = str(e)
        task.current_state.metadata["error_details"] = {
            "exception_type": type(e).__name__,
            "timestamp": datetime.utcnow().isoformat()
        }
        await task_repo.update_task(task)
        
        # Notify WebSocket clients
        await notify_task_update(task)

async def resume_task_background(task_id: str, db):
    """Resume a paused task in the background"""
    # Create task repository
    task_repo = TaskRepository(db)
    
    # Get task
    task = await task_repo.get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return
    
    # Check if task is approved
    if task.current_state.status != TaskStatus.APPROVED:
        logger.error(f"Task is not approved: {task_id}")
        return
    
    # Create execution engine
    execution_engine = ExecutionEngine()
    
    try:
        # Resume task execution
        async for state in execution_engine.resume_task(task_id):
            # Update task state
            task.current_state = state
            await task_repo.update_task(task)
            
            # Notify WebSocket clients
            await notify_task_update(task)
            
            # If execution paused or completed, break
            if state.status in [TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                break
                
    except Exception as e:
        logger.error(f"Error resuming task {task_id}: {str(e)}")
        
        # Update task status to failed
        task.current_state.status = TaskStatus.FAILED
        task.current_state.error = str(e)
        task.current_state.metadata["error_details"] = {
            "exception_type": type(e).__name__,
            "timestamp": datetime.utcnow().isoformat()
        }
        await task_repo.update_task(task)
        
        # Notify WebSocket clients
        await notify_task_update(task)