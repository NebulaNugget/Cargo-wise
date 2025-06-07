# Workflow execution tools
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from typing import Dict, Any, List
import logging
import importlib
import inspect

logger = logging.getLogger(__name__)

class ExecuteWorkflowTool(Marc1Tool):
    name = "execute_workflow"
    description = "Execute a predefined workflow of multiple tools"
    required_params = {"workflow_name": str}
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        workflow_name = input.parameters["workflow_name"]
        
        try:
            # Get workflow definition
            workflow = self._get_workflow(workflow_name)
            if not workflow:
                return {
                    "status": "ERROR",
                    "outputs": {},
                    "error": f"Workflow '{workflow_name}' not found"
                }
            
            # Execute workflow steps
            context = {k: v for k, v in input.parameters.items() if k != "workflow_name"}
            results = []
            
            for i, step in enumerate(workflow["steps"]):
                try:
                    logger.info(f"Executing workflow step {i+1}/{len(workflow['steps'])}: {step.get('description', 'No description')}")
                    
                    # Get tool class
                    tool_cls = self._get_tool_class(step["tool"])
                    if not tool_cls:
                        results.append({
                            "step": i+1,
                            "description": step.get("description", ""),
                            "success": False,
                            "error": f"Tool '{step['tool']}' not found"
                        })
                        if step.get("abort_on_failure", True):
                            break
                        continue
                    
                    # Prepare parameters with context variables
                    params = self._prepare_parameters(step.get("parameters", {}), context)
                    
                    # Execute tool
                    tool_instance = tool_cls()
                    step_input = ToolNodeInput(parameters=params, context=context)
                    step_result = await tool_instance.execute(step_input)
                    
                    # Update context with step results
                    if step.get("output_key") and step_result.get("status") == "SUCCESS":
                        context[step["output_key"]] = step_result.get("outputs", {})
                    
                    results.append({
                        "step": i+1,
                        "description": step.get("description", ""),
                        "success": step_result.get("status") == "SUCCESS",
                        "outputs": step_result.get("outputs", {}),
                        "error": step_result.get("error")
                    })
                    
                    # Stop workflow if step failed and abort_on_failure is True
                    if step_result.get("status") != "SUCCESS" and step.get("abort_on_failure", True):
                        logger.error(f"Workflow aborted at step {i+1} due to failure")
                        break
                        
                except Exception as e:
                    logger.exception(f"Error in workflow step {i+1}")
                    results.append({
                        "step": i+1,
                        "description": step.get("description", ""),
                        "success": False,
                        "error": str(e)
                    })
                    
                    if step.get("abort_on_failure", True):
                        break
            
            return {
                "status": "SUCCESS" if all(step["success"] for step in results) else "ERROR",
                "outputs": {
                    "workflow_name": workflow_name,
                    "steps_completed": len(results),
                    "steps_successful": sum(1 for step in results if step["success"]),
                    "results": results,
                    "context": context
                },
                "error": None if all(step["success"] for step in results) else "Workflow execution failed"
            }
            
        except Exception as e:
            logger.exception(f"Error executing workflow '{workflow_name}'")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
    
    def _get_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Get workflow definition by name"""
        # This would typically come from a database or configuration file
        # For now, we'll define some example workflows
        import yaml
        import os
        
        workflows_dir = os.path.join(os.getcwd(), "app", "workflows")
        # Check if the workflow file exists
        workflow_file = os.path.join(workflows_dir, f"{workflow_name}.yaml")
        if not os.path.exists(workflow_file):
            logger.error(f"Workflow file not found: {workflow_file}")
            return None
            # Load the workflow definition
        try:
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)
            return workflow
        except Exception as e:
            logger.exception(f"Error loading workflow file: {workflow_file}")
            return None
    
    def _get_tool_class(self, tool_name: str):
        """Get tool class by name"""
        # Import all tool modules
        tool_modules = [
            "app.ai.tools.cargowise_tools",
            "app.ai.tools.desktop_tools",
            "app.ai.tools.browser_tools"
        ]
        
        for module_name in tool_modules:
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Marc1Tool) and 
                        hasattr(obj, "name") and 
                        obj.name == tool_name):
                        return obj
            except ImportError:
                continue
        
        return None
    
    def _prepare_parameters(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Replace parameter placeholders with context values"""
        result = {}
        
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Extract context key
                context_key = value[2:-1]
                if context_key in context:
                    result[key] = context[context_key]
                else:
                    result[key] = value  # Keep as is if context key not found
            else:
                result[key] = value
                
        return result