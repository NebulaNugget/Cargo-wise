# NEW: Graph construction helpers
from typing import Dict, Any, List, Callable, Optional, Type, Union, Tuple
from pydantic import BaseModel, Field, create_model
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import inspect
import logging
from app.ai.tools.base_tool import Marc1Tool
from app.core.marc1.tool_registry import get_tool_registry
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

logger = logging.getLogger(__name__)

class AgentState(BaseModel):
    """Base state model for LangGraph agents"""
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(default_factory=list)
    current_tool: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    task_id: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    status: str = "RUNNING"  # RUNNING, COMPLETED, ERROR, PAUSED
    
    class Config:
        arbitrary_types_allowed = True

def create_agent_state_model(additional_fields: Dict[str, Tuple[Type, Any]] = None) -> Type[AgentState]:
    """Create a custom agent state model with additional fields"""
    if additional_fields is None:
        return AgentState
        
    return create_model(
        "CustomAgentState",
        __base__=AgentState,
        **additional_fields
    )

def create_tool_node(tool_name: str) -> ToolNode:
    """Create a ToolNode for a registered Marc1Tool"""
    registry = get_tool_registry()
    tool_cls = registry.get_tool(tool_name)
    
    if not tool_cls:
        raise ValueError(f"Tool '{tool_name}' not found in registry")
    
    async def tool_executor(state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with the current state"""
        try:
            # Create tool instance
            tool = tool_cls()
            
            # Execute tool with input from state
            result = await tool.execute(state.get("tool_input", {}))
            
            # Update state with tool output
            new_state = state.copy()
            new_state["tool_output"] = result
            new_state["current_tool"] = None
            
            # Add tool execution message
            new_state["messages"].append(
                AIMessage(content=f"Tool {tool_name} executed with result: {result}")
            )
            
            # Check for errors
            if result.get("status") == "ERROR":
                new_state["error"] = result.get("error")
                new_state["status"] = "ERROR"
            
            return new_state
            
        except Exception as e:
            logger.exception(f"Error executing tool {tool_name}")
            new_state = state.copy()
            new_state["error"] = str(e)
            new_state["status"] = "ERROR"
            new_state["messages"].append(
                AIMessage(content=f"Error executing tool {tool_name}: {str(e)}")
            )
            return new_state
    
    return ToolNode(tool_executor)

def create_llm_node(llm, system_prompt: str = None):
    """Create a node that uses an LLM to decide the next action"""
    
    async def llm_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state with the LLM"""
        messages = state.get("messages", [])
        
        # Add system prompt if provided and not already present
        if system_prompt and not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        # Get LLM response
        response = await llm.ainvoke(messages)
        
        # Update state with LLM response
        new_state = state.copy()
        new_state["messages"] = messages + [response]
        
        # Parse tool calls if any
        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_call = response.tool_calls[0]
            new_state["current_tool"] = tool_call["name"]
            new_state["tool_input"] = tool_call["args"]
        
        return new_state
    
    return llm_node

def create_human_approval_node():
    """Create a node that pauses execution for human approval"""
    
    async def human_approval_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Pause execution for human approval"""
        new_state = state.copy()
        new_state["status"] = "PAUSED"
        new_state["messages"].append(
            AIMessage(content="Waiting for human approval to continue.")
        )
        return new_state
    
    return human_approval_node

def create_decision_node(decision_fn: Callable[[Dict[str, Any]], str]):
    """Create a node that decides which path to take next"""
    
    async def decision_node(state: Dict[str, Any]) -> str:
        """Decide which path to take next"""
        return decision_fn(state)
    
    return decision_node

def build_workflow_graph(
    state_model: Type[AgentState],
    llm,
    system_prompt: str,
    tools: List[str],
    human_approval_steps: List[str] = None,
    max_iterations: int = 10
) -> StateGraph:
    """Build a workflow graph with the given components"""
    # Create the graph with the state model
    graph = StateGraph(state_model)
    
    # Add LLM node
    graph.add_node("llm", create_llm_node(llm, system_prompt))
    
    # Add tool nodes
    for tool_name in tools:
        graph.add_node(tool_name, create_tool_node(tool_name))
    
    # Add human approval nodes if specified
    if human_approval_steps:
        for step in human_approval_steps:
            graph.add_node(f"approve_{step}", create_human_approval_node())
    
    # Add iteration counter node
    def check_iterations(state: Dict[str, Any]) -> Dict[str, Any]:
        new_state = state.copy()
        iterations = new_state.get("iterations", 0) + 1
        new_state["iterations"] = iterations
        
        if iterations >= max_iterations:
            new_state["status"] = "COMPLETED"
            new_state["messages"].append(
                AIMessage(content=f"Maximum iterations ({max_iterations}) reached.")
            )
        
        return new_state
    
    graph.add_node("check_iterations", check_iterations)
    
    # Add router node to decide next step
    def route(state: Dict[str, Any]) -> str:
        # Check for completion or error
        if state.get("status") in ["COMPLETED", "ERROR"]:
            return END
        
        # Check for human approval pause
        if state.get("status") == "PAUSED":
            return END
        
        # Check if a tool needs to be executed
        current_tool = state.get("current_tool")
        if current_tool:
            # Check if this tool requires human approval
            if human_approval_steps and current_tool in human_approval_steps:
                return f"approve_{current_tool}"
            return current_tool
        
        # Default to LLM for next action
        return "llm"
    
    # Connect the nodes
    graph.add_node("router", create_decision_node(route))
    
    # Set up the edges
    graph.set_entry_point("llm")
    
    # From LLM to router
    graph.add_edge("llm", "router")
    
    # From tools to check_iterations
    for tool_name in tools:
        graph.add_edge(tool_name, "check_iterations")
    
    # From check_iterations to router
    graph.add_edge("check_iterations", "router")
    
    # From human approval nodes to router
    if human_approval_steps:
        for step in human_approval_steps:
            graph.add_edge(f"approve_{step}", "router")
    
    return graph

def create_cargowise_workflow(
    llm,
    workflow_name: str,
    tools: List[str],
    system_prompt: Optional[str] = None,
    human_approval_steps: List[str] = None,
    max_iterations: int = 10
) -> StateGraph:
    """Create a CargoWise-specific workflow graph"""
    # Default system prompt if not provided
    if system_prompt is None:
        system_prompt = (
            "You are an AI assistant that helps automate CargoWise operations. "
            "Your goal is to complete the requested task by using the available tools. "
            f"You are executing the '{workflow_name}' workflow."
        )
    
    # Create state model with workflow-specific fields
    state_model = create_agent_state_model({
        "workflow_name": (str, workflow_name),
        "iterations": (int, 0),
    })
    
    # Build and return the graph
    return build_workflow_graph(
        state_model=state_model,
        llm=llm,
        system_prompt=system_prompt,
        tools=tools,
        human_approval_steps=human_approval_steps,
        max_iterations=max_iterations
    )

# Helper function to run a workflow with initial input
async def run_workflow(
    workflow_graph: StateGraph,
    initial_input: str,
    task_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run a workflow with the given input"""
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=initial_input)],
        "task_id": task_id,
        "context": context or {},
        "status": "RUNNING"
    }
    
    # Compile the graph
    app = workflow_graph.compile()
    
    # Run the workflow
    result = await app.ainvoke(initial_state)
    
    return result