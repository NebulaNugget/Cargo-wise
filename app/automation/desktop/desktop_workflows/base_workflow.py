from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DesktopWorkflow(ABC):
    """Base class for all desktop automation workflows"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.steps = []
        self._initialize_steps()
    
    @abstractmethod
    def _initialize_steps(self) -> None:
        """Define the workflow steps - must be implemented by subclasses"""
        pass
    
    async def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the entire workflow with the given context"""
        context = context or {}
        results = []
        
        logger.info(f"Starting workflow: {self.name}")
        
        for i, step in enumerate(self.steps):
            try:
                logger.info(f"Executing step {i+1}/{len(self.steps)}: {step.get('description', 'No description')}")
                
                # Execute the step
                step_result = await self._execute_step(step, context)
                
                # Update context with step results
                if step.get('output_key') and step_result.get('success'):
                    context[step['output_key']] = step_result.get('outputs', {})
                
                results.append({
                    "step": i+1,
                    "description": step.get('description', ''),
                    "success": step_result.get('success', False),
                    "outputs": step_result.get('outputs', {}),
                    "error": step_result.get('error')
                })
                
                # Stop workflow if step failed and abort_on_failure is True
                if not step_result.get('success', False) and step.get('abort_on_failure', True):
                    logger.error(f"Workflow aborted at step {i+1} due to failure")
                    break
                    
            except Exception as e:
                logger.exception(f"Error in workflow step {i+1}")
                results.append({
                    "step": i+1,
                    "description": step.get('description', ''),
                    "success": False,
                    "error": str(e)
                })
                
                if step.get('abort_on_failure', True):
                    break
        
        return {
            "workflow_name": self.name,
            "success": all(step.get('success', False) for step in results),
            "steps": results,
            "context": context
        }
    
    async def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        from app.core.marc1.tool_registry import get_tool_registry
        
        tool_name = step.get('tool')
        if not tool_name:
            return {"success": False, "error": "No tool specified for step"}
        
        # Get tool from registry
        registry = get_tool_registry()
        tool_cls = registry.get_tool(tool_name)
        
        # Prepare parameters with context variables
        params = self._prepare_parameters(step.get('parameters', {}), context)
        
        # Execute tool
        tool_instance = tool_cls()
        return await tool_instance.execute(params)
    
    def _prepare_parameters(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Replace parameter placeholders with context values"""
        result = {}
        
        for key, value in params.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                # Extract context key
                context_key = value[2:-1]
                if context_key in context:
                    result[key] = context[context_key]
                else:
                    result[key] = value  # Keep as is if context key not found
            else:
                result[key] = value
                
        return result