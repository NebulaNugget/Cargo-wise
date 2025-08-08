from typing import Dict, Any, List, Optional, AsyncGenerator
# Add import at the top
from app.utils.task_status_utils import TaskStatusUtils
from langchain.agents import AgentExecutor
from langchain.schema import AgentAction, AgentFinish
import logging
from app.models.task import TaskStatus

logger = logging.getLogger(__name__)

class LinearWorkflowBuilder:
    """
    Builds a linear workflow from a list of tools
    
    This class creates a simple linear workflow that executes tools in sequence.
    In Phase 2, this will be replaced with a more sophisticated LangGraph implementation.
    """
    
    def __init__(self, tools: List[Dict[str, Any]]):
        self.tools = tools
        
    def compile(self):
        """Compile the workflow into an executable object"""
        return LinearWorkflow(self.tools)

class LinearWorkflow:
    """
    Simple linear workflow that executes tools in sequence
    
    This is a placeholder for the LangGraph implementation in Phase 2.
    """
    
    def __init__(self, tools: List[Dict[str, Any]]):
        self.tools = tools
        
    # In the astream method, replace the complex cancellation checks:
    async def astream(self, initial_state: Dict[str, Any], start_at:int = 0) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream execution events"""
        from app.core.marc1.tool_registry import get_tool_registry
        
        state = initial_state.copy()
        registry = get_tool_registry()
        total_steps = len(self.tools)

        # Get task ID for cancellation checking
        task_id = state.get("context", {}).get("task_id") or state.get("task_id")

        # Check if this is a resumed task that was already approved
        is_resumed = state.get("metadata", {}).get("approved_at") is not None
        
        for step, tool_config in enumerate(self.tools[start_at:], start=start_at):
            # **SIMPLIFIED: Direct database cancellation check**
            if task_id and TaskStatusUtils.is_task_cancelled(task_id):
                logger.info(f"Task {task_id} cancelled before executing tool {tool_config.get('name', 'unknown')}")
                state["status"] = TaskStatus.CANCELED
                state["error"] = "Task was cancelled by user"
                yield state
                return
                
            # Update state with current step
            state["step"] = step
            state["total_steps"] = total_steps
            
            # Get tool from registry
            tool_name = tool_config.get("name")
            if not tool_name:
                state["status"] = TaskStatus.FAILED
                state["error"] = f"No tool name specified for step {step}"
                yield state
                return
                
            tool_cls = registry.get_tool(tool_name)
            if not tool_cls:
                state["status"] = TaskStatus.FAILED
                state["error"] = f"Tool not found: {tool_name}"
                yield state
                return
                
            # Prepare tool parameters
            parameters = tool_config.get("parameters", {})
            
            # Update current tool info in state
            state["current_tool"] = {
                "name": tool_name,
                "parameters": parameters
            }
            
            # Check if this tool requires HITL approval - skip this check if task was already approved
            if not is_resumed and self._requires_approval(tool_name, state):
                state["status"] = TaskStatus.PAUSED
                state["requires_approval"] = True
                yield state
                return
            
            # Execute tool
            try:
                # Create tool instance
                tool = tool_cls()
                
                # Prepare input
                from app.ai.tools.base_tool import ToolNodeInput
                tool_input = ToolNodeInput(
                    task_id=state.get("task_id"),
                    parameters=parameters,
                    context=state.get("context", {})
                )
                
                # Execute tool
                logger.info(f"Executing tool: {tool_name}")
                result = await tool.execute(tool_input)
                
                # **SIMPLIFIED: Check if tool returned cancellation status**
                if result.get("status") == "CANCELED":
                    state["status"] = TaskStatus.CANCELED
                    state["error"] = result.get("error", "Task was cancelled")
                    yield state
                    return
                
                # Update state with result
                tool_status = result.get("status", TaskStatus.RUNNING)
                
                # Only update state status if tool failed, otherwise keep it as RUNNING
                if tool_status == TaskStatus.FAILED:
                    state["status"] = TaskStatus.FAILED
                else:
                    # Keep status as RUNNING until all tools complete
                    state["status"] = TaskStatus.RUNNING
                
                if "outputs" not in state:
                    state["outputs"] = {}
                if result.get("outputs"):
                    state["outputs"].update(result["outputs"])
                state["error"] = result.get("error")
                
                # Yield updated state
                yield state
                
                # If tool execution failed, stop workflow
                if state["status"] == TaskStatus.FAILED:
                    return
                    
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                state["status"] = TaskStatus.FAILED
                state["error"] = str(e)
                yield state
                return
        
        # **SIMPLIFIED: Final cancellation check before completion**
        if task_id and TaskStatusUtils.is_task_cancelled(task_id):
            logger.info(f"Task {task_id} cancelled before completion")
            state["status"] = TaskStatus.CANCELED
            state["error"] = "Task was cancelled by user"
            yield state
            return
        
        # All tools completed successfully
        state["status"] = TaskStatus.COMPLETED
        yield state

    def _requires_approval(self, tool_name: str, state: Dict[str, Any]) -> bool:
        """
        Check if a tool requires HITL approval
        
        This is a placeholder for the actual implementation.
        In a real implementation, this would check the HITL policy.
        """
        # Get task parameters
        task_id = state.get("task_id")
        hitl_enabled = state.get("hitl_enabled", True)
        critical_operations = state.get("critical_operations", [])
        confidence_threshold = state.get("confidence_threshold", 0.7)
        confidence = state.get("context", {}).get("confidence", 0.0)
        
        # If HITL is disabled, no approval required
        if not hitl_enabled:
            return False
        
        # If this is a critical operation, require approval
        if tool_name in critical_operations:
            return True
        
        # If confidence is below threshold, require approval
        if confidence < confidence_threshold:
            return True
        
        return False

# For Phase 2: Keep this commented out until ready to implement LangGraph
"""
class LangGraphWorkflowBuilder:
    '''Builds workflows using LangGraph for Phase 2'''
    
    def __init__(self, tools: List[Type[Marc1Tool]]):
        self.tools = tools
        self.graph = Graph()
        
        # Build graph structure
        self._build_nodes()
        self._connect_linear_flow()
        
        # Add HITL checkpoint node
        self._add_hitl_checkpoint()

    def _build_nodes(self):
        '''Register all tools as LangGraph nodes'''
        for tool_cls in self.tools:
            node = tool_cls.as_node()
            self.graph.add_node(node.name, node.func)

    def _connect_linear_flow(self):
        '''Connect nodes in sequential order'''
        nodes = [tool_cls.name for tool_cls in self.tools]
        for i in range(len(nodes)-1):
            self.graph.add_edge(nodes[i], nodes[i+1])
        self.graph.add_edge(nodes[-1], END)
    
    def _add_hitl_checkpoint(self):
        '''Add HITL checkpoint node to the graph'''
        def hitl_check(state: Dict[str, Any]) -> str:
            '''Check if human approval is needed'''
            # Get current tool and task parameters
            current_tool = state.get("current_tool", "")
            hitl_enabled = state.get("hitl_enabled", True)
            critical_operations = state.get("critical_operations", [])
            confidence = state.get("confidence", 1.0)
            confidence_threshold = state.get("confidence_threshold", 0.7)
            
            # If HITL is disabled, continue execution
            if not hitl_enabled:
                return "continue"
            
            # If this is a critical operation, require approval
            if current_tool in critical_operations:
                return "pause_for_approval"
            
            # If confidence is below threshold, require approval
            if confidence < confidence_threshold:
                return "pause_for_approval"
            
            # Otherwise, continue execution
            return "continue"
        
        # Add HITL checkpoint node
        self.graph.add_node("hitl_checkpoint", hitl_check)
        
        # Insert HITL checkpoint before each tool node
        nodes = [tool_cls.name for tool_cls in self.tools]
        for i in range(len(nodes)):
            # Add edge from previous node to HITL checkpoint
            if i > 0:
                self.graph.add_edge(nodes[i-1], "hitl_checkpoint")
            
            # Add conditional edges from HITL checkpoint
            self.graph.add_conditional_edges(
                "hitl_checkpoint",
                lambda state, result: result,
                {
                    "continue": nodes[i],
                    "pause_for_approval": END  # End execution and wait for approval
                }
            )

    def compile(self) -> Graph:
        '''Finalize workflow graph'''
        return self.graph.compile()
    
    async def execute_with_hitl(self, task_id: str, initial_state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        '''
        Execute workflow with HITL checkpoints
        
        This method handles the execution of the workflow with HITL checkpoints,
        pausing execution when human approval is required.
        '''
        # Compile the graph
        graph = self.compile()
        
        # Add task ID to state
        state = initial_state.copy()
        state["task_id"] = task_id
        
        # Execute the graph
        async for event in graph.astream(state):
            # Check if execution paused for approval
            if event.get("status") == "pause_for_approval":
                # Update event with HITL metadata
                event["status"] = TaskStatus.PAUSED
                event["requires_approval"] = True
                event["metadata"] = {
                    "pause_reason": "Human approval required",
                    "current_tool": event.get("current_tool", ""),
                    "confidence": event.get("confidence", 0.0)
                }
                
                yield event
                return  # Stop execution until approved
            
            # Otherwise, yield the event
            yield event
"""