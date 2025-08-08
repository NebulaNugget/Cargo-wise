# Base tool implementation
from pydantic import BaseModel, Field
from app.utils.task_status_utils import TaskStatusUtils
from typing import Dict, Any, Optional, List, Type, ClassVar
import logging
import inspect
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class ToolNodeInput(BaseModel):
    """Input for tool execution"""
    task_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

class ToolNodeOutput(BaseModel):
    """Output from tool execution"""
    status: str
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    confidence: float = 1.0
    
    # Add execution metadata
    execution_time: Optional[float] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    screenshot: Optional[str] = None  # Base64 encoded screenshot

class Marc1Tool:
    """Base class for all MARC-1 tools"""
    name: ClassVar[str] = "base_tool"
    description: ClassVar[str] = "Base tool class"
    required_params: ClassVar[Dict[str, Type]] = {}
    optional_params: ClassVar[Dict[str, Type]] = {}
    
    def __init__(self):
        self.execution_start_time = None
    
    async def execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """
        Execute the tool with the given input
        
        Args:
            input: Tool input parameters
            
        Returns:
            Tool execution result
        """
        # Convert dict to ToolNodeInput if needed
        if isinstance(input, dict):
            # Create a ToolNodeInput from the dict
            task_id = input.get("task_id")
            parameters = input.get("parameters", {})
            context = input.get("context", {})
            input = ToolNodeInput(task_id=task_id, parameters=parameters, context=context)
        # **NEW: Check if task is cancelled before execution**
        if input.task_id and TaskStatusUtils.is_task_cancelled(input.task_id):
            logger.info(f"Task {input.task_id} is cancelled, stopping tool {self.name}")
            return {
                "status": "CANCELED",
                "outputs": {},
                "error": "Task was cancelled by user",
                "timestamp": datetime.utcnow().isoformat()
            }
        # Validate required parameters
        validation_errors = self.validate_parameters(input.parameters)
        if validation_errors:
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Parameter validation failed: {validation_errors}",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Start execution timer
        self.execution_start_time = datetime.utcnow()
        
        try:
            # Execute the tool
            logger.info(f"Executing tool {self.name} for task {input.task_id}")
            result = await self._execute(input)

            # **NEW: Check if task was cancelled during execution**
            if input.task_id and TaskStatusUtils.is_task_cancelled(input.task_id):
                logger.info(f"Task {input.task_id} was cancelled during tool {self.name} execution")
                return {
                    "status": "CANCELED",
                    "outputs": {},
                    "error": "Task was cancelled by user",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Calculate execution time
            execution_time = (datetime.utcnow() - self.execution_start_time).total_seconds()
            
            # Add execution metadata
            if isinstance(result, dict):
                result["execution_time"] = execution_time
                result["timestamp"] = datetime.utcnow().isoformat()
                
                # Log success
                logger.info(f"Tool {self.name} executed successfully in {execution_time:.2f} seconds")
                return result
            else:
                # Convert to dict if not already
                return {
                    "status": "SUCCESS",
                    "outputs": {"result": result},
                    "execution_time": execution_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            # Calculate execution time
            execution_time = (datetime.utcnow() - self.execution_start_time).total_seconds()
            
            # Log error
            logger.error(f"Error executing tool {self.name}: {str(e)}")
            
            # Return error result
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """
        Tool-specific execution logic
        
        This method should be overridden by subclasses.
        
        Args:
            input: Tool input parameters
            
        Returns:
            Tool execution result
        """
        raise NotImplementedError("Tool must implement _execute method")
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> List[str]:
        """
        Validate parameters against required and optional parameters
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            List of validation errors, or empty list if valid
        """
        errors = []
        
        # Check required parameters
        for param_name, param_type in self.required_params.items():
            if param_name not in parameters:
                errors.append(f"Missing required parameter: {param_name}")
            elif not self._is_valid_type(parameters[param_name], param_type):
                errors.append(f"Parameter {param_name} has invalid type. Expected {param_type.__name__}")
        
        # Check optional parameters
        for param_name, param_value in parameters.items():
            if param_name in self.required_params:
                continue  # Already checked
                
            if param_name in self.optional_params:
                param_type = self.optional_params[param_name]
                if not self._is_valid_type(param_value, param_type):
                    errors.append(f"Parameter {param_name} has invalid type. Expected {param_type.__name__}")
        
        return errors
    
    def _is_valid_type(self, value: Any, expected_type: Type) -> bool:
        """Check if a value is of the expected type"""
        # Handle special cases
        if expected_type == list:
            return isinstance(value, list)
        elif expected_type == dict:
            return isinstance(value, dict)
        elif expected_type == str:
            return isinstance(value, str)
        elif expected_type == int:
            return isinstance(value, int)
        elif expected_type == float:
            return isinstance(value, (int, float))
        elif expected_type == bool:
            return isinstance(value, bool)
        
        # Default case
        return isinstance(value, expected_type)
    
    def _get_parameters(self, input) -> dict:
        """
        Safely extract parameters from input regardless of type
        
        Args:
            input: Either a ToolNodeInput object or a dictionary
            
        Returns:
            Dictionary of parameters
        """
        if input is None:
            return {}
        elif isinstance(input, dict):
            return input.get("parameters", {})
        elif hasattr(input, "parameters"):
            return input.parameters
        else:
            return {}
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get tool schema for documentation and validation"""
        return {
            "name": cls.name,
            "description": cls.description,
            "required_params": {
                name: param_type.__name__ 
                for name, param_type in cls.required_params.items()
            },
            "optional_params": {
                name: param_type.__name__
                for name, param_type in cls.optional_params.items()
            }
        }
    
    @classmethod
    def as_node(cls):
        """Convert tool to LangGraph node (for Phase 2)"""
        async def node_func(state: Dict[str, Any]) -> Dict[str, Any]:
            # Create tool instance
            tool = cls()
            
            # Extract parameters from state
            parameters = state.get("parameters", {})
            context = state.get("context", {})
            task_id = state.get("task_id")
            
            # Create input
            tool_input = ToolNodeInput(
                task_id=task_id,
                parameters=parameters,
                context=context
            )
            
            # Execute tool
            result = await tool.execute(tool_input)
            
            # Update state with result
            state.update(result)
            return state
            
        # Set node name and description
        node_func.__name__ = cls.name
        node_func.__doc__ = cls.description
        
        return node_func