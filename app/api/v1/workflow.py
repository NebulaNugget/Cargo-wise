# Workflow management endpoints
from fastapi import APIRouter, Depends, HTTPException, Body
from app.core.marc1.execution_engine import ExecutionEngine
from app.models.task import Task, TaskState
from app.models.hitl import HITLApproval, HITLRejection
from app.db.repositories.task_repository import TaskRepository
from app.dependencies import get_db
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
router = APIRouter()

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/execute", response_model=Task)
async def execute_workflow(
    workflow_request: dict,
    db=Depends(get_db)
) -> Task:
    """Execute a new automation workflow"""
    try:
        # Create task record
        task = Task(
            workflow_id=workflow_request.get("workflow_id"),
            parameters=workflow_request.get("parameters", {}),
            tools=workflow_request.get("tools", []),
            hitl_enabled=workflow_request.get("hitl_enabled", True),
            confidence_threshold=workflow_request.get("confidence_threshold", 0.7),
            critical_operations=workflow_request.get("critical_operations", [])
        )
        # Save to database
        await task_repo.create_task(task)
        
        # Start execution
        engine = ExecutionEngine(task_registry=db)
        
        return task
    except Exception as e:
        logger.exception("Workflow execution failed")
        raise HTTPException(500, f"Execution failed: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskState)
async def get_task_state(
    task_id: str,
    db=Depends(get_db)
) -> TaskState:
    """Get current state of a running task"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    return task.current_state

@router.get("/tasks/pending-approval", response_model=List[Task])
async def get_pending_approval_tasks(
    db=Depends(get_db)
) -> List[Task]:
    """Get all tasks pending human approval"""
    task_repo = TaskRepository(db)
    return await task_repo.get_pending_approval_tasks()

@router.post("/tasks/{task_id}/approve")
async def approve_task_step(
    task_id: str,
    approval_data: HITLApproval = Body(...),
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Approve a step in a paused task with optional modifications"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task.current_state.status != TaskStatus.PAUSED:
        raise HTTPException(400, "Task not in paused state")
    
    # Update task with approval
    success = await task_repo.approve_task(task_id, approval_data)
    
    if not success:
        raise HTTPException(500, "Failed to update task state")
    
    # Get updated task
    task = await task_repo.get_task(task_id)
    
    # Resume execution
    engine = ExecutionEngine(task_registry=db)
    
    # In a real implementation, you'd resume the task in a background process
    # For now, we'll just return success
    
    return {
        "status": "approved",
        "task_id": task_id,
        "message": "Task approved and resumed"
    }

@router.post("/tasks/{task_id}/reject")
async def reject_task_step(
    task_id: str,
    rejection_data: HITLRejection = Body(...),
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Reject a step in a paused task"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task.current_state.status != TaskStatus.PAUSED:
        raise HTTPException(400, "Task not in paused state")
    
    # Update task with rejection
    success = await task_repo.reject_task(task_id, rejection_data)
    
    if not success:
        raise HTTPException(500, "Failed to update task state")
    
    # Handle rejection (cleanup, alternative flows, etc.)
    engine = ExecutionEngine(task_registry=db)
    await engine.handle_rejection(task, rejection_data.dict())
    
    return {
        "status": "rejected",
        "task_id": task_id,
        "message": "Task rejected and terminated"
    }

    
@router.post("/tasks/{task_id}/resume")
async def resume_paused_task(
    task_id: str,
    approval_data: dict,
    db=Depends(get_db)
):
    """Resume a HITL-paused task"""
    task = await db.get(Task, task_id)
    if task.current_state.status != "PAUSED":
        raise HTTPException(400, "Task not in paused state")
    
    # Update task with human input
    task.current_state.context.update(approval_data)
    task.current_state.status = "RUNNING"
    await db.commit()
    
    # Resume execution
    engine = ExecutionEngine(task_registry=db)
    await engine.resume_task(task)
    
    return {"status": "resumed"}

@router.post("/tasks/{task_id}/approve")
async def approve_task_step(
    task_id: str,
    approval_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Approve a step in a paused task with optional modifications"""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task.current_state.status != "PAUSED":
        raise HTTPException(400, "Task not in paused state")
    
    # Update task with human input and approval
    task.current_state.context.update(approval_data.get("context", {}))
    task.current_state.status = "APPROVED"
    task.current_state.metadata["human_approved"] = True
    task.current_state.metadata["approval_timestamp"] = datetime.now().isoformat()
    task.current_state.metadata["approval_notes"] = approval_data.get("notes", "")
    
    await db.commit()
    
    # Resume execution
    engine = ExecutionEngine(task_registry=db)
    await engine.resume_task(task)
    
    return {
        "status": "approved",
        "task_id": task_id,
        "message": "Task approved and resumed"
    }

@router.post("/tasks/{task_id}/reject")
async def reject_task_step(
    task_id: str,
    rejection_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Reject a step in a paused task"""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task.current_state.status != "PAUSED":
        raise HTTPException(400, "Task not in paused state")
    
    # Update task with rejection status
    task.current_state.status = "REJECTED"
    task.current_state.metadata["human_rejected"] = True
    task.current_state.metadata["rejection_timestamp"] = datetime.now().isoformat()
    task.current_state.metadata["rejection_reason"] = rejection_data.get("reason", "")
    task.current_state.metadata["rejection_notes"] = rejection_data.get("notes", "")
    
    await db.commit()
    
    # Optionally terminate the task or handle rejection
    engine = ExecutionEngine(task_registry=db)
    await engine.handle_rejection(task, rejection_data)
    
    return {
        "status": "rejected",
        "task_id": task_id,
        "message": "Task rejected and terminated"
    }

@router.post("/tasks/{task_id}/modify")
async def modify_task_step(
    task_id: str,
    modification_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Modify parameters of a paused task before resuming"""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task.current_state.status != "PAUSED":
        raise HTTPException(400, "Task not in paused state")
    
    # Update task parameters with human modifications
    if "parameters" in modification_data:
        task.parameters.update(modification_data["parameters"])
    
    # Update context if provided
    if "context" in modification_data:
        task.current_state.context.update(modification_data["context"])
    
    task.current_state.metadata["human_modified"] = True
    task.current_state.metadata["modification_timestamp"] = datetime.now().isoformat()
    task.current_state.metadata["modification_notes"] = modification_data.get("notes", "")
    
    await db.commit()
    
    return {
        "status": "modified",
        "task_id": task_id,
        "message": "Task parameters modified"
    }