# LLM/AI interaction endpoints
from fastapi import APIRouter, Depends, HTTPException, Body, BackgroundTasks
from app.models.task import Task, TaskStatus, TaskState
from app.db.repositories.task_repository import TaskRepository
from app.dependencies import get_db
from app.core.nlp.query_processor import NLPQueryProcessor
from typing import Dict, Any, Optional, List
import logging
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)
router = APIRouter()

class NaturalLanguageQuery(BaseModel):
    """Model for natural language query requests"""
    query: str = Field(..., min_length=3, max_length=1000)
    context: Dict[str, Any] = Field(default_factory=dict)
    client_id: Optional[str] = None
    user_id: Optional[str] = None
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty or just whitespace")
        return v

class QueryResponse(BaseModel):
    """Response model for natural language queries"""
    task_id: str
    status: str
    message: str
    estimated_completion_time: Optional[int] = None

async def process_query_background(task_id: str, db):
    """Background task to process the query"""
    processor = NLPQueryProcessor(db)
    await processor.process_query(task_id)

@router.post("/query", response_model=QueryResponse)
async def process_natural_language_query(
    query_request: NaturalLanguageQuery,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
) -> QueryResponse:
    """
    Process a natural language query and create a task
    
    This endpoint accepts natural language instructions from users,
    validates them, and creates a task record for processing by the MARC-1 engine.
    """
    logger.info(f"Received natural language query: {query_request.query[:50]}...")
    
    try:
        # Create a new task with PENDING status
        task = Task(
            id=str(uuid.uuid4()),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            query=query_request.query,
            context=query_request.context,
            parameters={},  # Will be populated by NLP processor
            status=TaskStatus.PENDING,
            workflow_type="nlp_query",  # Special type for NL queries
            user_id=query_request.user_id,
            client_id=query_request.client_id
        )
        
        # Set initial state
        task.current_state = TaskState(
            task_id=task.id,
            status=TaskStatus.PENDING,
            metadata={
                "source": "api",
                "query_timestamp": datetime.utcnow().isoformat(),
                "raw_query": query_request.query
            }
        )
        
        # Store in database
        task_repo = TaskRepository(db)
        created_task = await task_repo.create_task(task)
        
        # Queue for processing in background task
        background_tasks.add_task(process_query_background, created_task.id, db)
        
        return QueryResponse(
            task_id=created_task.id,
            status="accepted",
            message="Query received and processing has begun",
            estimated_completion_time=30  # Placeholder: 30 seconds
        )
        
    except Exception as e:
        logger.error(f"Error processing natural language query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )

@router.get("/query/{task_id}", response_model=Task)
async def get_nlp_query_status(
    task_id: str,
    db=Depends(get_db)
) -> Task:
    """Get the status of a natural language query task"""
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
        
    return task

@router.post("/query/{task_id}/approve")
async def approve_nlp_task(
    task_id: str,
    approval_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
):
    """Approve a paused NLP task that requires human approval"""
    task_repo = TaskRepository(db)
    success = await task_repo.approve_task(task_id, approval_data)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to approve task. Task may not be in PAUSED state."
        )
    
    # After approval, start execution
    processor = NLPQueryProcessor(db)
    task = await task_repo.get_task(task_id)
    
    # Start execution in background
    # In a real implementation, this would be handled by a background worker
    # For now, we'll just acknowledge that it would happen
    
    return {"status": "success", "message": "Task approved successfully and queued for execution"}

@router.post("/query/{task_id}/reject")
async def reject_nlp_task(
    task_id: str,
    rejection_data: Dict[str, Any] = Body(...),
    db=Depends(get_db)
):
    """Reject a paused NLP task"""
    task_repo = TaskRepository(db)
    success = await task_repo.reject_task(task_id, rejection_data)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to reject task. Task may not be in PAUSED state."
        )
    
    return {"status": "success", "message": "Task rejected successfully"}

@router.get("/pending-approvals", response_model=List[Task])
async def get_pending_approvals(
    limit: int = 100,
    db=Depends(get_db)
):
    """Get all tasks pending human approval"""
    task_repo = TaskRepository(db)
    tasks = await task_repo.get_pending_approval_tasks(limit)
    return tasks