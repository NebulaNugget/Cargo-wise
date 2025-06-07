import re
import logging
from typing import Dict, Any, List, Optional, Union, Callable
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error"""
    pass

class Validator:
    """Utility for validating data in the application"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Validate that all required fields are present and not empty"""
        missing = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing.append(field)
        return missing
    
    @staticmethod
    def validate_workflow_definition(workflow: Dict[str, Any]) -> List[str]:
        """Validate workflow definition structure"""
        errors = []
        
        # Check required top-level fields
        required_fields = ["name", "description", "steps"]
        for field in required_fields:
            if field not in workflow:
                errors.append(f"Missing required field: {field}")
        
        # If no steps, return early
        if "steps" not in workflow or not isinstance(workflow["steps"], list):
            errors.append("Steps must be a list")
            return errors
        
        # Validate each step
        for i, step in enumerate(workflow["steps"]):
            step_errors = Validator.validate_workflow_step(step)
            for error in step_errors:
                errors.append(f"Step {i+1}: {error}")
        
        return errors
    
    @staticmethod
    def validate_workflow_step(step: Dict[str, Any]) -> List[str]:
        """Validate a single workflow step"""
        errors = []
        
        # Check required step fields
        required_fields = ["description", "tool"]
        for field in required_fields:
            if field not in step:
                errors.append(f"Missing required field: {field}")
        
        # Validate tool exists
        if "tool" in step:
            from app.core.marc1.tool_registry import get_tool_registry
            registry = get_tool_registry()
            if not registry.has_tool(step["tool"]):
                errors.append(f"Unknown tool: {step['tool']}")
        
        # Validate parameters if present
        if "parameters" in step and not isinstance(step["parameters"], dict):
            errors.append("Parameters must be a dictionary")
        
        return errors
    
    @staticmethod
    def validate_with_model(data: Dict[str, Any], model_class: type) -> Union[BaseModel, List[str]]:
        """Validate data against a Pydantic model"""
        try:
            return model_class(**data)
        except ValidationError as e:
            errors = []
            for error in e.errors():
                errors.append(f"{'.'.join(error['loc'])}: {error['msg']}")
            return errors
    
    @staticmethod
    def validate_booking_reference(reference: str) -> bool:
        """Validate CargoWise booking reference format"""
        # Example: ABCD-123456 or ABCD123456
        pattern = r'^[A-Z]{2,4}[-]?\d{6,8}$'
        return bool(re.match(pattern, reference))
    
    @staticmethod
    def validate_container_number(container: str) -> bool:
        """Validate container number format"""
        # ISO 6346 format: 4 letters + 6 digits + 1 check digit
        pattern = r'^[A-Z]{4}\d{7}$'
        return bool(re.match(pattern, container))