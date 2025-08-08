# Task lifecycle management
# Task lifecycle management
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.models.task import Task, TaskState, TaskStatus
from app.core.marc1.execution_engine import ExecutionEngine
from app.db.repositories.task_repository import TaskRepository
import logging
from datetime import datetime
import asyncio
import uuid

logger = logging.getLogger(__name__)

class TaskManager:
    """
    Manages the lifecycle of tasks including creation, execution, 
    pausing, resuming, editing, and rejection
    """
    
    def __init__(self, task_repository: TaskRepository, execution_engine: ExecutionEngine):
        self.task_repository = task_repository
        self.execution_engine = execution_engine
        self._active_tasks = {}  # Track active task executions
        
    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task"""
        # Generate task ID if not provided
        if "id" not in task_data:
            task_data["id"] = str(uuid.uuid4())
            
        # Set created_at timestamp
        task_data["created_at"] = datetime.utcnow().isoformat()
        
        # Create initial state
        initial_state = TaskState(
            task_id=task_data["id"],
            status=TaskStatus.PENDING,
            parameters=task_data.get("parameters", {}),
            context=task_data.get("context", {})
        )
        
        # Create task object
        task = Task(
            id=task_data["id"],
            name=task_data.get("name", f"Task {task_data['id']}"),
            description=task_data.get("description", ""),
            workflow_type=task_data.get("workflow_type", "default"),
            tools=task_data.get("tools", []),
            parameters=task_data.get("parameters", {}),
            context=task_data.get("context", {}),
            metadata=task_data.get("metadata", {}),
            created_at=task_data["created_at"],
            current_state=initial_state
        )
        
        # Save task to repository
        await self.task_repository.create_task(task)
        
        # Auto-execute if specified
        if task_data.get("auto_execute", False):
            asyncio.create_task(self.execute_task(task.id))
            
        return task
        
    async def execute_task(self, task_id: str) -> None:
        """Execute a task and update its state"""
        # Get task from repository
        task = await self.task_repository.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
            
        # Update task status to RUNNING
        task.current_state.status = TaskStatus.RUNNING
        await self.task_repository.update_task_state(task_id, task.current_state)
        
        # Execute task
        execution_task = asyncio.create_task(self._execute_and_update(task))
        self._active_tasks[task_id] = execution_task
        
        # Wait for execution to complete
        try:
            await execution_task
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {str(e)}")
        finally:
            # Remove from active tasks
            if task_id in self._active_tasks:
                del self._active_tasks[task_id]
                
    async def _execute_and_update(self, task: Task) -> None:
        """Execute task and update state in repository"""
        async for state in self.execution_engine.execute_task(task):
            # Update task state in repository
            await self.task_repository.update_task_state(task.id, state)
            
    async def resume_task(self, task_id: str) -> None:
        """Resume a paused task"""
        # Get task from repository
        task = await self.task_repository.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
            
        # Check if task is paused
        if task.current_state.status != TaskStatus.PAUSED:
            logger.error(f"Cannot resume task {task_id} that is not paused")
            return
            
        # Resume task execution
        execution_task = asyncio.create_task(self._resume_and_update(task))
        self._active_tasks[task_id] = execution_task
        
        # Wait for execution to complete
        try:
            await execution_task
        except Exception as e:
            logger.error(f"Error resuming task {task_id}: {str(e)}")
        finally:
            # Remove from active tasks
            if task_id in self._active_tasks:
                del self._active_tasks[task_id]
                
    async def _resume_and_update(self, task: Task) -> None:
        """Resume task and update state in repository"""
        async for state in self.execution_engine.resume_task(task):
            # Update task state in repository
            await self.task_repository.update_task_state(task.id, state)
            
    async def edit_task(self, task_id: str, edited_parameters: Dict[str, Any]) -> None:
        """Edit and restart a task with new parameters"""
        # Get task from repository
        task = await self.task_repository.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
            
        # Check if task is paused
        if task.current_state.status != TaskStatus.PAUSED:
            logger.error(f"Cannot edit task {task_id} that is not paused")
            return
            
        # Edit and restart task
        execution_task = asyncio.create_task(self._edit_and_update(task, edited_parameters))
        self._active_tasks[task_id] = execution_task
        
        # Wait for execution to complete
        try:
            await execution_task
        except Exception as e:
            logger.error(f"Error editing task {task_id}: {str(e)}")
        finally:
            # Remove from active tasks
            if task_id in self._active_tasks:
                del self._active_tasks[task_id]
                
    async def _edit_and_update(self, task: Task, edited_parameters: Dict[str, Any]) -> None:
        """Edit task and update state in repository"""
        async for state in self.execution_engine.edit_task(task, edited_parameters):
            # Update task state in repository
            await self.task_repository.update_task_state(task.id, state)
            
    async def reject_task(self, task_id: str, rejection_reason: str) -> None:
        """Reject and cancel a task"""
        # Get task from repository
        task = await self.task_repository.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
            
        # Check if task is paused
        if task.current_state.status != TaskStatus.PAUSED:
            logger.error(f"Cannot reject task {task_id} that is not paused")
            return
            
        # Reject task
        state = await self.execution_engine.reject_task(task, rejection_reason)
        
        # Update task state in repository
        await self.task_repository.update_task_state(task_id, state)
        
        # Cancel active execution if exists
        if task_id in self._active_tasks:
            self._active_tasks[task_id].cancel()
            del self._active_tasks[task_id]
            
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return await self.task_repository.get_task(task_id)
        
    async def list_tasks(self, query: Dict[str, Any] = None, limit: int = 100, offset: int = 0) -> List[Task]:
        """List tasks with pagination"""
        return await self.task_repository.listAll(query, limit, offset)
        
    async def get_pending_approval_tasks(self, limit: int = 100) -> List[Task]:
        """Get tasks pending human approval"""
        return await self.task_repository.get_pending_approval_tasks(limit)
        
    def is_task_active(self, task_id: str) -> bool:
        """Check if task is currently being executed"""
        return task_id in self._active_tasks