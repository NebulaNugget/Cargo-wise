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
    
    async def approve_task(self, task_id: str, approval_data: Dict[str, Any], user_id: str = None) -> bool:
        """Approve a paused task"""
        task = await self.get_task(task_id)
        if not task or task.current_state.status != TaskStatus.PAUSED:
            return False
        
        # Update state with approval
        task.current_state.status = TaskStatus.APPROVED
        task.current_state.requires_approval = False
        task.current_state.approved_at = datetime.now().isoformat()
        task.current_state.approved_by = user_id
        
        # Apply any parameter modifications
        if "modified_parameters" in approval_data and approval_data["modified_parameters"]:
            task.parameters.update(approval_data["modified_parameters"])
        
        # Apply any tool modifications
        if "modified_tools" in approval_data and approval_data["modified_tools"]:
            task.tools = approval_data["modified_tools"]
        
        # Update context with human input
        if "context" in approval_data:
            task.current_state.context.update(approval_data["context"])
        
        # Add approval metadata
        task.current_state.metadata["approval_notes"] = approval_data.get("notes", "")
        if "override_confidence" in approval_data:
            task.current_state.metadata["override_confidence"] = approval_data["override_confidence"]
        
        # Save updated state
        return await self.update_task(task)
    
    async def reject_task(self, task_id: str, rejection_data: Dict[str, Any], user_id: str = None) -> bool:
        """Reject a paused task"""
        task = await self.get_task(task_id)
        if not task or task.current_state.status != TaskStatus.PAUSED:
            return False
        
        # Update state with rejection
        task.current_state.status = TaskStatus.REJECTED
        task.current_state.requires_approval = False
        task.current_state.rejection_reason = rejection_data.get("reason", "")
        
        # Add rejection metadata
        task.current_state.metadata["rejection_timestamp"] = datetime.now().isoformat()
        task.current_state.metadata["rejected_by"] = user_id
        task.current_state.metadata["rejection_notes"] = rejection_data.get("notes", "")
        task.current_state.metadata["trigger_alternative"] = rejection_data.get("trigger_alternative", False)
        task.current_state.metadata["alternative_flow"] = rejection_data.get("alternative_flow")
        
        # Save updated state
        return await self.update_task(task)
    
    async def get_pending_approval_tasks(self, limit: int = 100) -> List[Task]:
        """Get tasks pending human approval"""
        return await self.list({
            "current_state.status": TaskStatus.PAUSED,
            "current_state.requires_approval": True
        }, limit)
    
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