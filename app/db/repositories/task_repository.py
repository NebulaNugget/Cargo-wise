# Task repository for task operations
from typing import List, Optional, Dict, Any
from app.models.task import Task, TaskState, TaskStatus
from app.db.repositories.base_respository import BaseRepository
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TaskRepository(BaseRepository[Task]):
    """Repository for task operations with HITL support"""
    
    def __init__(self, db_session):
        super().__init__(db_session, Task, "tasks")
    
    async def create_task(self, task: Task) -> Task:
        """Create a new task"""
        # Set initial state
        if task.current_state is None:
            task.current_state = TaskState(task_id=task.id)
        
        # Store in database
        return await self.create(task)
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return await self.get(task_id)
    
    # async def update_task_state(self, task_id: str, state: TaskState) -> bool:
    #     """Update task state"""
    #     return await self.update(
    #         task_id,
    #         {
    #             "current_state": state.dict(),
    #             "updated_at": datetime.now().isoformat()
    #         }
    #     )
    async def update_task_state(self, task_id: str, state: TaskState) -> bool:
        """Update task state"""
        task = await self.get_task(task_id)
        if not task:
            return False
            
        # Update the task state
        task.current_state = state
        
        # Check if the task is completed and update completed_at if needed
        if state.status == TaskStatus.COMPLETED and not task.completed_at:
            task.completed_at = datetime.utcnow().isoformat()
            
        # Update the task
        return await self.update_task(task)
    
    async def mark_task_completed(self, task_id: str, result: Dict[str, Any] = None) -> bool:
        """Mark a task as completed with results"""
        task = await self.get_task(task_id)
        if not task:
            return False
            
        # Update task state to completed
        task.current_state.status = TaskStatus.COMPLETED
        task.current_state.updated_at = datetime.utcnow()
        task.completed_at = datetime.utcnow() 
        
        # Add result data if provided
        if result:
            task.current_state.outputs.update(result.get("outputs", {}))
            task.current_state.error = result.get("error")
            
        # Save the updated task
        return await self.update_task(task)
    
    async def update_task(self, task: Task) -> bool:
        """Update entire task"""
        task.updated_at = datetime.now().isoformat()
        return await self.update(task.id, task.dict())
    
    async def pause_task(self, task_id: str, reason: str, confidence: float = None) -> bool:
        """Pause task for human approval"""
        task = await self.get_task(task_id)
        if not task:
            return False
        
        # Update state to paused
        task.current_state.status = TaskStatus.PAUSED
        task.current_state.requires_approval = True
        task.current_state.approval_requested_at = datetime.now().isoformat()
        task.current_state.metadata["pause_reason"] = reason
        
        if confidence is not None:
            task.current_state.metadata["confidence"] = confidence
        
        # Save updated state
        return await self.update_task_state(task_id, task.current_state)
    
    async def approve_task(self, task_id: str, approval_data: Dict[str, Any] = None) -> bool:
        """Approve a task that is pending human approval"""
        task = await self.get_task(task_id)
        if not task:
            return False
            
        # Check if task is pending approval
        if task.current_state.status != TaskStatus.PAUSED or not task.current_state.requires_approval:
            return False
            
        # Update task state
        task.current_state.status = TaskStatus.RUNNING
        task.current_state.requires_approval = False
        
        # Add approval metadata
        if not task.current_state.metadata:
            task.current_state.metadata = {}
            
        task.current_state.metadata["approved_at"] = datetime.utcnow().isoformat()
        
        if approval_data:
            task.current_state.metadata["approval_data"] = approval_data
            
        # Update task
        return await self.update_task(task)
    
    async def reject_task(self, task_id: str, rejection_data: Dict[str, Any] = None) -> bool:
        """Reject a task that is pending human approval"""
        task = await self.get_task(task_id)
        if not task:
            return False
            
        # Check if task is pending approval
        if task.current_state.status != TaskStatus.PAUSED:
            return False
            
        # Update task state
        task.current_state.status = TaskStatus.REJECTED
        task.current_state.requires_approval = False
        
        # Add rejection metadata
        if not task.current_state.metadata:
            task.current_state.metadata = {}
            
        task.current_state.metadata["rejected_at"] = datetime.utcnow().isoformat()
        
        if rejection_data:
            rejection_reason = rejection_data.get("reason", "Task rejected by user")
            task.current_state.metadata["rejection_reason"] = rejection_reason
            task.current_state.metadata["rejection_data"] = rejection_data
        
        # Update task
        return await self.update_task(task)
        
    async def count(self, query: Dict[str, Any] = None) -> int:
        """Count tasks matching the query"""
        return await self.collection.count_documents(query or {})
    
    async def listAll(self, query: Dict[str, Any] = None, limit: int = 100, offset: int = 0, sort=None) -> List[Task]:
        """List tasks with pagination and optional sorting - FIXED date handling"""
        # Default sort by created_at in descending order if not specified
        if sort is None:
            sort = [("created_at", -1)]
    
        # Use the query directly - no need for complex date processing
        # since we're now passing datetime objects from the API layer
        final_query = query or {}
        
        # Log the final query for debugging
        logger.debug(f"Final MongoDB query: {final_query}")
        
        # Get raw documents from MongoDB
        docs = await self.collection.find(final_query).sort(sort).skip(offset).limit(limit).to_list(length=limit)
        
        # Log the number of documents found
        logger.debug(f"Found {len(docs)} documents matching query")
        
        # Convert documents to Task objects
        return [Task(**doc) for doc in docs]
        
    async def get_pending_approval_tasks(self, limit: int = 100) -> List[Task]:
        """Get tasks pending human approval"""
        query = {
            "current_state.status": TaskStatus.PAUSED,
            "current_state.requires_approval": True
        }
        return await self.listAll(query, limit, 0, sort=[("created_at", -1)])
    
    async def add_feedback(self, task_id: str, feedback_data: Dict[str, Any]) -> bool:
        """Add feedback to a task"""
        task = await self.get_task(task_id)
        if not task:
            return False
        
        # Store feedback in task metadata
        if "feedback" not in task.metadata:
            task.metadata["feedback"] = []
        
        feedback_data["timestamp"] = datetime.now().isoformat()
        task.metadata["feedback"].append(feedback_data)
        
        # Save the updated task
        return await self.update_task(task)