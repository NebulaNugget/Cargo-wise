from typing import Dict, Type, List
from app.automation.desktop.desktop_workflow.base_workflow import DesktopWorkflow
from app.automation.desktop.desktop_workflow.cargowise_desktop import (
    CargoWiseLoginWorkflow,
    CargoWiseCreateBookingWorkflow
)

class WorkflowRegistry:
    """Registry for desktop automation workflows"""
    
    def __init__(self):
        self._workflows: Dict[str, Type[DesktopWorkflow]] = {}
        self._register_default_workflows()
    
    def _register_default_workflows(self) -> None:
        """Register built-in workflows"""
        self.register_workflow(CargoWiseLoginWorkflow)
        self.register_workflow(CargoWiseCreateBookingWorkflow)
    
    def register_workflow(self, workflow_cls: Type[DesktopWorkflow]) -> None:
        """Register a workflow class"""
        # Create an instance to get the name
        instance = workflow_cls()
        self._workflows[instance.name] = workflow_cls
    
    def get_workflow(self, name: str) -> DesktopWorkflow:
        """Get a workflow instance by name"""
        if name not in self._workflows:
            raise ValueError(f"Workflow '{name}' not registered")
        
        return self._workflows[name]()
    
    def list_workflows(self) -> List[Dict[str, str]]:
        """List all registered workflows"""
        result = []
        for name, workflow_cls in self._workflows.items():
            instance = workflow_cls()
            result.append({
                "name": instance.name,
                "description": instance.description
            })
        return result

# Singleton instance
_registry = None

def get_workflow_registry() -> WorkflowRegistry:
    """Get the workflow registry singleton"""
    global _registry
    if _registry is None:
        _registry = WorkflowRegistry()
    return _registry