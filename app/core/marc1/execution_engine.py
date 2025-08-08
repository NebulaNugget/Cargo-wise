# Now uses LangGraph underneath
from typing import Optional, AsyncGenerator, Dict, Any, List
from app.core.marc1.langgraph.base_graph import LinearWorkflowBuilder
from app.models.task import Task, TaskState, TaskStatus
import logging
import asyncio
from datetime import datetime
import traceback
from app.utils.logging import log_task_event, LogLevel, log_exception, log_to_file, LogSource
logger = logging.getLogger(__name__)

class ExecutionEngine:
    def __init__(self, task_registry=None):
        self.task_registry = task_registry
        self._paused_tasks = {}  # Store paused task states
        self._cancelled_tasks = set()  # **ADD THIS: Track cancelled tasks**
        
    async def execute_task(self, task: Task) -> AsyncGenerator[TaskState, None]:
        """Main execution entrypoint"""
        # **ADD: Pass execution engine reference to workflow**
        if not state.context:
            state.context = {}
        state.context["task_id"] = task.id
        state.context["_execution_engine"] = self  # **ADD THIS**
        # Check if this is an NLP query task
        if task.workflow_type == "nlp_query":
            # For NLP queries, we use the tools determined by the NLP processor
            logger.info(f"Executing NLP query task: {task.id}")
        
        # Convert MARC-1 task to LangGraph workflow
        try:
            workflow = LinearWorkflowBuilder(task.tools).compile()
            
            # Check if workflow is None
            if workflow is None:
                raise ValueError(f"Failed to compile workflow for task {task.id}")
        except Exception as e:
            logger.error(f"Error creating workflow for task {task.id}: {str(e)}")
            state = TaskState(
                task_id=task.id,
                parameters=task.parameters,
                context=task.context,
                status=TaskStatus.FAILED,
                error=f"Failed to create workflow: {str(e)}",
                metadata={"error_type": type(e).__name__}
            )
            yield state
            return
        
        # Initialize execution state
        state = TaskState(
            task_id=task.id,
            parameters=task.parameters,
            context=task.context,
            status=TaskStatus.RUNNING,
            metadata={}  # Initialize metadata as empty dict
        )
        # Add task_id to context for tools to use
        if not state.context:
            state.context = {}
        state.context["task_id"] = task.id
        
        yield state  # Initial state
        
        # Check if we need to pause for HITL approval before starting
        if self._requires_pre_execution_approval(task):
            state.status = TaskStatus.PAUSED
            state.requires_approval = True
            state.metadata["pause_reason"] = "Pre-execution approval required"
            state.metadata["pause_timestamp"] = datetime.utcnow().isoformat()
            yield state
            return  # Stop execution until approved
        # Start execution timer
        execution_start_time = datetime.utcnow()
        state.metadata["execution_start_time"] = execution_start_time.isoformat()
        
        # Stream execution events
        try:
            # Check if workflow is None
            if workflow is None:
                raise ValueError(f"Failed to compile workflow for task {task.id}")
                
            # Initialize outputs in state if not present
            if not hasattr(state, 'outputs') or state.outputs is None:
                state.outputs = {}
            
            # Check if this is a resumed task
            is_resumed = task.id in self._paused_tasks
            if is_resumed:
                logger.info(f"Resuming paused task {task.id}")
                # Restore state from paused tasks
                paused_state = self._paused_tasks[task.id]
                # Update state with paused state data
                state.outputs = paused_state.get("outputs", {})
                state.metadata["resumed_from"] = paused_state.get("step", 0)
                state.metadata["resumed_at"] = datetime.utcnow().isoformat()
                # Remove from paused tasks
                del self._paused_tasks[task.id]

            async for event in workflow.astream(state.dict()):
                # **ADD THIS: Check for cancellation before processing each event**
                if task.id in self._cancelled_tasks:
                    logger.info(f"Task {task.id} was cancelled, stopping execution")
                    state.status = TaskStatus.CANCELED
                    state.error = "Task was cancelled by user"
                    yield state
                    return
                # Check if event is None
                if event is None:
                    logger.warning(f"Received None event from workflow for task {task.id}")
                    continue
                # Process the event
                state = self._update_state_from_event(state, event)
                
                # Log execution progress
                current_tool = event.get("current_tool", {})
                # Add null check for current_tool
                if current_tool is not None:
                    tool_name = current_tool.get("name", "unknown")
                else:
                    tool_name = "unknown"
                
                step_num = event.get("step", 0) + 1  # 1-based for display
                total_steps = event.get("total_steps", 0)
                
                logger.info(f"Task {task.id}: Executing step {step_num}/{total_steps} - Tool: {tool_name}")

                # Check confidence level for HITL pause
                confidence = event.get("confidence", 1.0)
                confidence_threshold = task.metadata.get("confidence_threshold", 0.8)
                
                # Pause if confidence is below threshold
                if confidence < confidence_threshold:
                    state.status = TaskStatus.PAUSED
                    state.requires_approval = True
                    state.metadata["pause_reason"] = f"Low confidence ({confidence:.2f} < {confidence_threshold:.2f})"
                    state.metadata["pause_timestamp"] = datetime.utcnow().isoformat()
                    state.metadata["current_tool"] = current_tool
                    state.metadata["confidence"] = confidence
                    state.metadata["step"] = step_num
                    
                    # Store state for potential resume
                    self._paused_tasks[task.id] = {
                        "step": step_num,
                        "outputs": state.outputs,
                        "paused_at": datetime.utcnow().isoformat()
                    }
                    
                    yield state
                    return  # Stop execution until approved
                
                # Check if we need to pause for human approval during execution
                if self._requires_approval_for_tool(task, tool_name):
                    state.status = TaskStatus.PAUSED
                    state.requires_approval = True
                    state.metadata["pause_reason"] = f"Approval required for tool: {tool_name}"
                    state.metadata["pause_timestamp"] = datetime.utcnow().isoformat()
                    state.metadata["current_tool"] = current_tool
                    state.metadata["step"] = step_num
                    
                    # Store state for potential resume
                    self._paused_tasks[task.id] = {
                        "step": step_num,
                        "outputs": state.outputs,
                        "paused_at": datetime.utcnow().isoformat()
                    }
                    yield state
                    return  # Stop execution until approved
                # If execution completed, set completed_at timestamp
                if state.status == TaskStatus.COMPLETED and not task.completed_at:
                    task.completed_at = datetime.utcnow()
                    # Update the task in the database if task_registry exists
                    if self.task_registry:
                        await self.task_registry.update_task(task)
                # # Yield updated state
                # yield state
                
                # # If execution completed or failed, break
                # if state.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                #     break
                
                # **FIX: Additional cancellation check after each tool execution**
                if task.id in self._cancelled_tasks:
                    logger.info(f"Task {task.id} was cancelled after tool execution")
                    state.status = TaskStatus.CANCELED
                    state.error = "Task was cancelled by user"
                    yield state
                    return  # Exit the generator completely
                
                yield state
                
                # **FIX: Exit immediately if cancelled**
                if state.status == TaskStatus.CANCELED:
                    return
                
                if state.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    break
                # **FIX: Clean up cancelled tasks when execution ends**
                if task.id in self._cancelled_tasks:
                    self._cancelled_tasks.discard(task.id)
                    logger.info(f"Cleaned up cancelled task {task.id} from tracking")
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            # Check if task was cancelled before setting FAILED status
            if task.id in self._cancelled_tasks:
                logger.info(f"Task {task.id} was cancelled, preserving CANCELED status despite exception")
                state.status = TaskStatus.CANCELED
                state.error = "Task was cancelled by user"
            else:
                state.status = TaskStatus.FAILED
                state.error = str(e)
            # Calculate execution time
            execution_end_time = datetime.utcnow()
            execution_time_seconds = (execution_end_time - execution_start_time).total_seconds()

            # Create failure summary
            failure_summary = {
                "status": "FAILED",
                "duration_seconds": execution_time_seconds,
                "start_time": execution_start_time.isoformat(),
                "end_time": execution_end_time.isoformat(),
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exception(type(e), e, e.__traceback__)
            }
            
            # Update state with failure details
            state.metadata["error_details"] = {
                "exception_type": type(e).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
            state.metadata["failure_summary"] = failure_summary
            state.metadata["failure_timestamp"] = execution_end_time.isoformat()
            
            # Log failure with detailed information
            logger.error(f"Task {task.id} failed after {execution_time_seconds:.2f} seconds: {str(e)}")
            await log_task_event(
                task_id=task.id,
                event=f"Task failed: {str(e)}",
                level=LogLevel.ERROR,
                metadata=failure_summary
            )
            await log_exception(e, task_id=task.id)
            
            yield state
            return

        # Calculate execution time
        execution_end_time = datetime.utcnow()
        execution_time_seconds = (execution_end_time - execution_start_time).total_seconds()
        
        # Create completion summary
        completion_summary = {
            "status": "COMPLETED",
            "duration_seconds": execution_time_seconds,
            "start_time": execution_start_time.isoformat(),
            "end_time": execution_end_time.isoformat(),
            "tools_executed": [tool.get("name", tool.get("type", "unknown")) for tool in task.tools],
            "result_summary": self._generate_result_summary(state)
        }
        # Update final state with execution metrics and completion summary
        state.metadata["execution_end_time"] = execution_end_time.isoformat()
        state.metadata["execution_time_seconds"] = execution_time_seconds
        state.metadata["completion_summary"] = completion_summary
        state.metadata["completion_timestamp"] = execution_end_time.isoformat()
        
        # Log completion with detailed information
        if state.status == TaskStatus.COMPLETED:
            task.completed_at = execution_end_time
            # Also add completed_at to the state for consistency
            state.metadata["completed_at"] = execution_end_time.isoformat()
            logger.info(f"Task {task.id} completed successfully in {execution_time_seconds:.2f} seconds")
            
         # Log completion   with detailed information
        if state.status == TaskStatus.COMPLETED:
            logger.info(f"Task {task.id} completed successfully in {execution_time_seconds:.2f} seconds")    
            await log_task_event(
                task_id=task.id,
                event=f"Task completed successfully in {execution_time_seconds:.2f} seconds",
                metadata=completion_summary
            )
        else:
            logger.error(f"Task {task.id} failed after {execution_time_seconds:.2f} seconds")
        
        yield state  # Final state

    def _generate_result_summary(self, state: TaskState) -> str:
        """Generate a human-readable summary of the task results"""
        outputs = state.outputs or {}
        
        # Extract key information from outputs
        if not outputs:
            return "Task completed with no output data."
        
        # Try to create a meaningful summary based on output data
        summary_parts = []
        
        # Check for common output fields
        if "message" in outputs:
            summary_parts.append(outputs["message"])
        
        if "result" in outputs:
            result = outputs["result"]
            if isinstance(result, str):
                summary_parts.append(result)
            elif isinstance(result, dict):
                for key, value in result.items():
                    summary_parts.append(f"{key}: {value}")
        
        # Add any other relevant output fields
        for key, value in outputs.items():
            if key not in ["message", "result", "screenshots"] and isinstance(value, (str, int, float, bool)):
                summary_parts.append(f"{key}: {value}")
        
        if summary_parts:
            return " ".join(summary_parts)
        else:
            return "Task completed successfully."

    def _update_state_from_event(self, state: TaskState, event: Dict[str, Any]) -> TaskState:
        """Update task state from execution event"""
        # Check if event is None
        if event is None:
            logger.warning(f"Received None event for task {state.task_id}")
            return state
            
        # Update outputs if present
        if "outputs" in event and event["outputs"]:
            if not hasattr(state, "outputs") or state.outputs is None:
                state.outputs = {}
            state.outputs.update(event["outputs"])
            
        # Update status if present
        if "status" in event:
            # Only update status if current status is not CANCELED
            if state.status != TaskStatus.CANCELED:
                state.status = event["status"]
            else:
                logger.info(f"Preserving CANCELED status for task {state.task_id}, ignoring event status: {event['status']}")
            
        # Update error if present
        if "error" in event and event["error"]:
            if state.status != TaskStatus.CANCELED:
                state.error = event["error"]
            else:
                logger.info(f"Preserving cancellation error for task {state.task_id}, ignoring event error: {event['error']}")
            
        # Update metadata
        if not hasattr(state, "metadata") or state.metadata is None:
            state.metadata = {}
            
        # Add event metadata to state metadata
        if "metadata" in event and event["metadata"]:
            state.metadata.update(event["metadata"])
            
        # Add step information
        if "step" in event:
            state.metadata["current_step"] = event["step"]
            
        # Add total steps
        if "total_steps" in event:
            state.metadata["total_steps"] = event["total_steps"]
            
        # Add current tool
        if "current_tool" in event:
            state.metadata["current_tool"] = event["current_tool"]
            
        # Add confidence if present
        if "confidence" in event:
            state.metadata["confidence"] = event["confidence"]
            
        return state    
    
    def _process_event(self, event: dict, task: Task) -> TaskState:
        """Convert LangGraph event to MARC-1 task state"""
        return TaskState(
            task_id=task.id,
            status=event.get("status", TaskStatus.RUNNING),
            outputs=event.get("outputs", {}),
            errors=event.get("errors", []),
            metadata={
                "current_node": event.get("node"),
                "retry_count": event.get("retry_count", 0),
                "confidence": event.get("confidence", 1.0)  # Default high confidence
            }
        )
    
    async def resume_task_with_approval(self, task_id: str, approved: bool = True) -> AsyncGenerator[TaskState, None]:
        """Resume a paused task after human approval"""
        if task_id not in self._paused_tasks:
            logger.error(f"Cannot resume task {task_id}: not found in paused tasks")
            yield TaskState(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error="Task not found in paused tasks"
            )
            return
            
        paused_info = self._paused_tasks[task_id]
        workflow = paused_info["workflow"]
        task = paused_info["task"]
        
        if not approved:
            # Task was rejected
            yield TaskState(
                task_id=task_id,
                status=TaskStatus.REJECTED,
                metadata={
                    "rejected_at": datetime.now().isoformat(),
                    "paused_at": paused_info["paused_at"]
                }
            )
            # Clean up
            del self._paused_tasks[task_id]
            return
            
        # Task was approved, continue execution
        last_event = paused_info["last_event"]
        
        # Mark as approved and continue
        yield TaskState(
            task_id=task_id,
            status=TaskStatus.APPROVED,
            metadata={
                "approved_at": datetime.now().isoformat(),
                "paused_at": paused_info["paused_at"]
            }
        )
        
        # Continue execution from where we left off
        async for event in workflow.aresume(last_event):
            processed_event = self._process_event(event, task)
            
            # Check if we need to pause again
            if self._should_pause_for_approval(processed_event, task):
                # Update paused state
                self._paused_tasks[task_id]["last_event"] = event
                self._paused_tasks[task_id]["paused_at"] = datetime.now().isoformat()
                
                # Update state to PAUSED
                processed_event.status = TaskStatus.PAUSED
                processed_event.requires_approval = True
                
                yield processed_event
                break  # Stop execution until human approval again
                
            yield processed_event
            
        # If we completed without pausing again, clean up
        if task_id in self._paused_tasks and not self._should_pause_for_approval(processed_event, task):
            del self._paused_tasks[task_id]
    
    def _should_pause_for_approval(self, state: TaskState, task: Task) -> bool:
        """Determine if execution should pause for human approval"""
        # Check if HITL is enabled for this task
        hitl_enabled = getattr(task, "hitl_enabled", True)
        if not hitl_enabled:
            return False
            
        # Get HITL config from task if available
        hitl_config = getattr(task, "hitl_config", None)
        
        # Use either the config object or fallback to task attributes
        if hitl_config:
            critical_ops = hitl_config.critical_operations
            confidence_threshold = hitl_config.confidence_threshold
            auto_approve_tools = hitl_config.auto_approve_tools
        else:
            critical_ops = getattr(task, "critical_operations", [])
            confidence_threshold = getattr(task, "confidence_threshold", 0.7)
            auto_approve_tools = getattr(task, "auto_approve_tools", [])
        
        current_node = state.metadata.get("current_node", "")
        
        # Skip approval for auto-approved tools
        if current_node in auto_approve_tools:
            return False
            
        # Check if current operation is in critical list
        if current_node in critical_ops:
            return True
        
        # Check confidence threshold
        confidence = state.metadata.get("confidence", 1.0)
        
        if confidence < confidence_threshold:
            logger.info(f"Pausing task {task.id} for approval: confidence {confidence} below threshold {confidence_threshold}")
            return True
        
        return False
    
    def _requires_pre_execution_approval(self, task: Task) -> bool:
        """
        Determine if a task requires human approval before execution starts
        
        Args:
            task: The task to check
            
        Returns:
            True if pre-execution approval is required, False otherwise
        """
        # Check if HITL is enabled for this task
        hitl_enabled = getattr(task, "hitl_enabled", True)
        if not hitl_enabled:
            return False
            
        # Get HITL config from task if available
        hitl_config = getattr(task, "hitl_config", None)
        
        # Check for high-risk operations
        high_risk_tools = ["cargowise_delete_booking", "cargowise_cancel_booking", 
                          "cargowise_modify_payment", "cargowise_submit_customs"]
        
        for tool in task.tools:
            tool_name = tool.get("name", "")
            if tool_name in high_risk_tools:
                logger.info(f"Task {task.id} requires pre-execution approval due to high-risk tool: {tool_name}")
                return True
        
        # For now, we'll only require pre-execution approval for high-risk operations
        return False
    
    def _requires_approval_for_tool(self, task: Task, tool_name: str) -> bool:
        """
        Determine if a specific tool requires human approval before execution
        
        Args:
            task: The task being executed
            tool_name: The name of the tool to check
            
        Returns:
            True if approval is required for this tool, False otherwise
        """
        # Check if HITL is enabled for this task
        hitl_enabled = getattr(task, "hitl_enabled", True)
        if not hitl_enabled:
            return False
            
        # Get HITL config from task if available
        hitl_config = getattr(task, "hitl_config", None)
        
        # Use either the config object or fallback to task attributes
        if hitl_config:
            critical_ops = hitl_config.critical_operations
            auto_approve_tools = hitl_config.auto_approve_tools
        else:
            critical_ops = getattr(task, "critical_operations", [])
            auto_approve_tools = getattr(task, "auto_approve_tools", [])
        
        # Skip approval for auto-approved tools
        if tool_name in auto_approve_tools:
            return False
            
        # Check if tool is in critical list
        if tool_name in critical_ops:
            return True
        
        # Default high-risk tools that always require approval
        high_risk_tools = ["cargowise_delete_booking", "cargowise_cancel_booking", 
                          "cargowise_modify_payment", "cargowise_submit_customs"]
        
        if tool_name in high_risk_tools:
            return True
        
        return False
    
    async def edit_task(self, task: Task, edited_parameters: Dict[str, Any]) -> AsyncGenerator[TaskState, None]:
            """Edit and restart a task with new parameters"""
            logger.info(f"Editing task {task.id} with new parameters")
            
            # Update task parameters
            task.parameters.update(edited_parameters)
            
            # Add edit metadata
            if not task.metadata:
                task.metadata = {}
            
            if "edit_history" not in task.metadata:
                task.metadata["edit_history"] = []
                
            # Record edit in history
            task.metadata["edit_history"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "edited_parameters": edited_parameters
            })
            
            # Reset task state
            task.current_state = TaskState(
                task_id=task.id,
                parameters=task.parameters,
                context=task.context,
                status=TaskStatus.RUNNING,
                metadata={"edited": True, "edit_timestamp": datetime.utcnow().isoformat()}
            )
            
            # Remove from paused tasks if present
            if task.id in self._paused_tasks:
                del self._paused_tasks[task.id]
                
            # Execute the task with new parameters
            async for state in self.execute_task(task):
                yield state
            
    async def reject_task(self, task: Task, rejection_reason: str) -> TaskState:
        """Reject and cancel a task"""
        logger.info(f"Rejecting task {task.id}: {rejection_reason}")
        
        # Update task state
        state = TaskState(
            task_id=task.id,
            parameters=task.parameters,
            context=task.context,
            status=TaskStatus.REJECTED,
            error=f"Task rejected: {rejection_reason}",
            metadata={
                "rejection_reason": rejection_reason,
                "rejected_at": datetime.utcnow().isoformat()
            }
        )
        
        # Remove from paused tasks if present
        if task.id in self._paused_tasks:
            del self._paused_tasks[task.id]
            
        # Log rejection
        await log_task_event(
            task_id=task.id,
            event=f"Task rejected: {rejection_reason}",
            level=LogLevel.WARNING,
            metadata={"rejection_reason": rejection_reason}
        )
        
        return state

    # # Add a new method to cancel a task
    # async def cancel_task(self, task_id: str) -> TaskState:
    #     """Cancel a running task"""
    #     logger.info(f"Cancelling task {task_id}")
    #     # **ADD THIS: Mark task as cancelled in memory**
    #     self._cancelled_tasks.add(task_id)
    #     # Check if task is in paused tasks
    #     if task_id in self._paused_tasks:
    #         del self._paused_tasks[task_id]
    #         logger.info(f"Removed paused task {task_id}")
        
    #     # Create cancellation state
    #     cancellation_time = datetime.utcnow()
        
    #     # Try to cancel any running automation processes
    #     try:
    #         # Import here to avoid circular imports
    #         from app.automation.robot.cargowise_automation import CargoWiseAutomation
    #         from app.ai.tools.browser_tools import BrowserSessionManager
            
    #         # Cancel CargoWise automation if running
    #         cw_automation = CargoWiseAutomation()
    #         await cw_automation.cancel_automation()
            
    #         # Close any browser sessions
    #         await BrowserSessionManager.cleanup()
            
    #         logger.info(f"Successfully cancelled automation processes for task {task_id}")
    #     except Exception as e:
    #         logger.error(f"Error cancelling automation processes for task {task_id}: {str(e)}")
        
    #     # Create cancellation state
    #     cancel_state = TaskState(
    #         task_id=task_id,
    #         status=TaskStatus.CANCELED,  # Make sure this status exists in your TaskStatus enum
    #         metadata={
    #             "cancelled_at": cancellation_time.isoformat(),
    #             "cancellation_reason": "User requested cancellation"
    #         }
    #     )
    #     # **FIX: Schedule cleanup after a delay to ensure cancellation is processed**
    #     async def cleanup_after_delay():
    #         await asyncio.sleep(5)  # Wait 5 seconds
    #         if task_id in self._cancelled_tasks:
    #             self._cancelled_tasks.discard(task_id)
    #             logger.info(f"Cleaned up cancelled task {task_id} after delay")
        
    #     asyncio.create_task(cleanup_after_delay())
    #     return cancel_state
    # g
    async def cancel_task(self, task_id: str) -> TaskState:
        """Cancel a running task"""
        logger.info(f"Cancelling task {task_id}")
        
        # Update task status in database immediately
        from app.db.repositories.task_repository import TaskRepository
        from app.db.database import get_db_session
        
        async with get_db_session() as db:
            task_repo = TaskRepository(db)
            task = await task_repo.get_task(task_id)
            
            if task:
                # Create cancelled state
                cancel_state = TaskState(
                    task_id=task_id,
                    status=TaskStatus.CANCELED,
                    error="Task was cancelled by user",
                    metadata={
                        "cancelled_at": datetime.utcnow().isoformat(),
                        "cancellation_reason": "User requested cancellation"
                    }
                )
                
                # Update in database
                await task_repo.update_task_state(task_id, cancel_state)
                logger.info(f"Task {task_id} marked as cancelled in database")
                
                return cancel_state
        
        # Return default cancelled state if task not found
        return TaskState(
            task_id=task_id,
            status=TaskStatus.CANCELED,
            error="Task was cancelled by user"
        )
    # Add or update this method in the ExecutionEngine class
    async def resume_task(self, task: Task) -> AsyncGenerator[TaskState, None]:
        """Resume a paused task"""
        logger.info(f"Resuming task {task.id}")
        # **FIX: Check if task was cancelled before resuming**
        if task.id in self._cancelled_tasks:
            logger.info(f"Task {task.id} was cancelled, cannot resume")
            cancel_state = TaskState(
                task_id=task.id,
                status=TaskStatus.CANCELED,
                error="Task was cancelled by user",
                metadata={
                    "cancelled_at": datetime.utcnow().isoformat(),
                    "cancellation_reason": "Task was previously cancelled"
                }
            )
            yield cancel_state
            return
    
        # Initialize execution state from current state
        state = task.current_state
        state.metadata["resumed_at"] = datetime.utcnow().isoformat()


        
        yield state  # Initial state
        
        # Start execution timer
        execution_start_time = datetime.utcnow()
        state.metadata["execution_start_time"] = execution_start_time.isoformat()
        
        # Convert MARC-1 task to LangGraph workflow
        try:
            workflow = LinearWorkflowBuilder(task.tools).compile()
            
            # Check if workflow is None
            if workflow is None:
                raise ValueError(f"Failed to compile workflow for task {task.id}")
        except Exception as e:
            logger.error(f"Error creating workflow for task {task.id}: {str(e)}")
            state.status = TaskStatus.FAILED
            state.error = f"Failed to create workflow: {str(e)}"
            state.metadata["error_type"] = type(e).__name__
            yield state
            return
        
        # Stream execution events
        try:
            # Initialize outputs in state if not present
            if not hasattr(state, 'outputs') or state.outputs is None:
                state.outputs = {}
                
            # Get the current step from metadata if available
            # current_step = state.metadata.get("current_step", 0)
            current_step = state.metadata.get("step", 0)
            
            async for event in workflow.astream(state.dict(), start_at=current_step):
                # **FIX: Add cancellation check at the beginning of each iteration**
                if task.id in self._cancelled_tasks:
                    logger.info(f"Task {task.id} was cancelled during resume, stopping execution")
                    state.status = TaskStatus.CANCELED
                    state.error = "Task was cancelled by user"
                    yield state
                    return
                # Check if event is None
                if event is None:
                    logger.warning(f"Received None event from workflow for task {task.id}")
                    continue
                    
                # Process the event
                state = self._update_state_from_event(state, event)
                
                # Log execution progress
                current_tool = event.get("current_tool", {})
                # Add null check for current_tool
                if current_tool is not None:
                    tool_name = current_tool.get("name", "unknown")
                else:
                    tool_name = "unknown"
                
                step_num = event.get("step", 0) + 1  # 1-based for display
                total_steps = event.get("total_steps", 0)
                
                logger.info(f"Task {task.id}: Executing step {step_num}/{total_steps} - Tool: {tool_name}")
                
                # Check confidence level for HITL pause
                confidence = event.get("confidence", 1.0)
                confidence_threshold = task.metadata.get("confidence_threshold", 0.8)
                
                # Pause if confidence is below threshold
                if confidence < confidence_threshold:
                    state.status = TaskStatus.PAUSED
                    state.requires_approval = True
                    state.metadata["pause_reason"] = f"Low confidence ({confidence:.2f} < {confidence_threshold:.2f})"
                    state.metadata["pause_timestamp"] = datetime.utcnow().isoformat()
                    state.metadata["current_tool"] = current_tool
                    state.metadata["confidence"] = confidence
                    state.metadata["current_step"] = step_num
                    
                    yield state
                    return  # Stop execution until approved
                
                # Check if we need to pause for human approval during execution
                if self._requires_approval_for_tool(task, tool_name):
                    state.status = TaskStatus.PAUSED
                    state.requires_approval = True
                    state.metadata["pause_reason"] = f"Approval required for tool: {tool_name}"
                    state.metadata["pause_timestamp"] = datetime.utcnow().isoformat()
                    state.metadata["current_tool"] = current_tool
                    state.metadata["current_step"] = step_num
                    
                    yield state
                    return  # Stop execution until approved
                    
                # Yield updated state
                yield state
                
                # If execution completed or failed, break
                if state.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    break
                    
        except Exception as e:
            # **FIX: Check if task was cancelled before setting FAILED status**
            if task.id in self._cancelled_tasks:
                logger.info(f"Task {task.id} was cancelled, preserving CANCELED status despite exception: {str(e)}")
                state.status = TaskStatus.CANCELED
                state.error = "Task was cancelled by user"
                state.metadata["cancelled_at"] = datetime.utcnow().isoformat()
                state.metadata["cancellation_reason"] = "Task was cancelled during execution"
            else:
                logger.error(f"Error executing task {task.id}: {str(e)}")
                state.status = TaskStatus.FAILED
                state.error = str(e)
            
            # Calculate execution time
            execution_end_time = datetime.utcnow()
            execution_time_seconds = (execution_end_time - execution_start_time).total_seconds()

            # Create failure summary
            failure_summary = {
                "status": "FAILED",
                "duration_seconds": execution_time_seconds,
                "start_time": execution_start_time.isoformat(),
                "end_time": execution_end_time.isoformat(),
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exception(type(e), e, e.__traceback__)
            }
            
            # Update state with failure details
            state.metadata["error_details"] = {
                "exception_type": type(e).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
            state.metadata["failure_summary"] = failure_summary
            state.metadata["failure_timestamp"] = execution_end_time.isoformat()
            
            # Log failure with detailed information
            logger.error(f"Task {task.id} failed after {execution_time_seconds:.2f} seconds: {str(e)}")
            log_task_event(
                task_id=task.id,
                event=f"Task failed: {str(e)}",
                level=LogLevel.ERROR,
                metadata=failure_summary
            )
            log_exception(e, task_id=task.id)
            
            yield state
            return
            
        # Calculate execution time
        execution_end_time = datetime.utcnow()
        execution_time_seconds = (execution_end_time - execution_start_time).total_seconds()
        
        # Create completion summary
        completion_summary = {
            "status": "COMPLETED",
            "duration_seconds": execution_time_seconds,
            "start_time": execution_start_time.isoformat(),
            "end_time": execution_end_time.isoformat(),
            "tools_executed": [tool.get("name", tool.get("type", "unknown")) for tool in task.tools],
            "result_summary": self._generate_result_summary(state)
        }
        
        # Update final state with execution metrics and completion summary
        state.metadata["execution_end_time"] = execution_end_time.isoformat()
        state.metadata["execution_time_seconds"] = execution_time_seconds
        state.metadata["completion_summary"] = completion_summary
        state.metadata["completion_timestamp"] = execution_end_time.isoformat()
        
        # Log completion with detailed information
        if state.status == TaskStatus.COMPLETED:
            logger.info(f"Task {task.id} completed successfully in {execution_time_seconds:.2f} seconds")    
            await log_task_event(
                task_id=task.id,
                event=f"Task completed successfully in {execution_time_seconds:.2f} seconds",
                metadata=completion_summary
            )
        else:
            logger.error(f"Task {task.id} failed after {execution_time_seconds:.2f} seconds")
        
        yield state  # Final state