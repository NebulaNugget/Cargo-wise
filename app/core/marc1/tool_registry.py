# Tool registry for MARC-1 platform
from typing import Dict, Type, List, Any, Optional
# Add this import at the top
# Update imports to include both old and new tools
from app.ai.tools.cargowise_tools import (
    CargoWiseLoginTool as OldCargoWiseLoginTool,
    CargoWiseSearchBookingTool as OldCargoWiseSearchBookingTool,
    
    CargoWiseUpdateBookingTool,
    CargoWiseCreateShipmentTool,
    CargoWiseCreateConsolidationTool,
    CargoWiseSearchShipmentByHousebillTool,
    CargoWiseSearchConsolidationByReferenceNumberTool,
    CargoWiseGenerateReportTool
)
# Import the new Robot Framework-based tools
from app.automation.robot import (
    CargoWiseLoginTool,
    
    CargoWiseSearchBookingTool
)
import logging
import importlib
import inspect
import os
import pkgutil
from app.ai.tools.base_tool import Marc1Tool

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    Registry for all available tools in the MARC-1 platform
    
    This class maintains a registry of all available tools and provides
    methods to discover, register, and retrieve tools.
    """
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance._tools = {}  # Initialize empty registry
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._tools = {}  # Map of tool name to tool class
            self._initialized = True
    
    def register_tool(self, tool_cls: Type[Marc1Tool]) -> None:
        """
        Register a tool class with the registry
        
        Args:
            tool_cls: The tool class to register
        """
        try:
            if not issubclass(tool_cls, Marc1Tool):
                logger.warning(f"Cannot register {tool_cls.__name__}: not a Marc1Tool subclass")
                return False
                
            tool_name = getattr(tool_cls, "name", tool_cls.__name__)
            if tool_name in self._tools:
                logger.warning(f"Tool {tool_name} already registered, overwriting")

                
            self._tools[tool_name] = tool_cls
            logger.debug(f"Registered tool: {tool_name}")
            return True
        except Exception as e:
            logger.error(f"Error registering tool {tool_cls.__name__}: {str(e)}")
            return False
    
    def get_tool(self, tool_name: str) -> Optional[Type[Marc1Tool]]:
        """
        Get a tool class by name
        
        Args:
            tool_name: The name of the tool to retrieve
            
        Returns:
            The tool class, or None if not found
        """
        return self._tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all registered tools
        
        Returns:
            A list of tool metadata dictionaries
        """
        return [
            {
                "name": tool_name,
                "description": getattr(tool_cls, "description", ""),
                "required_params": getattr(tool_cls, "required_params", {}),
                "optional_params": getattr(tool_cls, "optional_params", {})
            }
            for tool_name, tool_cls in self._tools.items()
        ]
    
    def discover_tools(self, package_name: str = "app.ai.tools") -> int:
        """
        Discover and register all tools in a package
        
        Args:
            package_name: The name of the package to scan for tools
            
        Returns:
            Number of tools registered
        """
        registered_count = 0
        try:
            package = importlib.import_module(package_name)
            package_path = getattr(package, "__path__", [])
            
            for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
                if is_pkg:
                    # Recursively discover tools in subpackages
                    registered_count += self.discover_tools(f"{package_name}.{module_name}")
                else:
                    try:
                        module = importlib.import_module(f"{package_name}.{module_name}")
                        
                        # Find all Marc1Tool subclasses in the module
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, Marc1Tool) and 
                                obj != Marc1Tool and
                                getattr(obj, "name", None)):
                                if self.register_tool(obj):
                                    registered_count += 1
                                
                    except Exception as e:
                        logger.error(f"Error loading module {module_name}: {str(e)}")
            
            logger.info(f"Discovered {registered_count} tools in {package_name}")
            return registered_count
                        
        except Exception as e:
            logger.error(f"Error discovering tools in {package_name}: {str(e)}")
            return registered_count
    
    def get_tools_for_intent(self, intent_name: str) -> List[Dict[str, Any]]:
        """
        Get tools that can handle a specific intent
        
        Args:
            intent_name: The name of the intent
            
        Returns:
            A list of tool configurations
        """
        # This is a simple mapping for Phase 1
        # In Phase 2, this will be more sophisticated with LLM-based tool selection
        intent_to_tools = {
            "cargowise_login": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "${environment}"
                    }
                }
            ],
           
            "search_booking": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_booking",
                    "description": "Search for a booking in CargoWise",
                    "parameters": {
                        "booking_reference": "${booking_reference}"
                    }
                }
            ],
            "create_shipment": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${login_password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_shipment",
                    "description": "Create a new shipment in CargoWise",
                    "parameters": {
                        "weight": "${weight}",
                        "consignor": "${consignor}",
                        "transport_method": "${transport_method}",
                        "description": "${description}"
                    }
                }
            ],
            "search_shipment_by_housebill": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${login_password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_shipment_by_housebill",
                    "description": "Search for a shipment by housebill number",
                    "parameters": {
                        "housebill": "${housebill}"
                    }
                }
            ],

            "search_consolidation_by_referencenumber": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${login_password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_consolidation_by_referencenumber",
                    "description": "Search for a consolidation by reference number",
                    "parameters": {
                        "referencenumber": "${referencenumber}"
                    }
                }
            ],
            "create_consolidation": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${login_password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_consolidation",
                    "description": "Create a new consolidation in CargoWise",
                    "parameters": {
                        "transport": "${transport}",
                        "container_mode": "${container_mode}",
                        "first_load": "${first_load}",
                        "last_load": "${last_load}",
                        "voyage": "${voyage}",
                        "eta": "${eta}",
                        "etd": "${etd}",
                        "bol": "${bol}",
                        "vessel": "${vessel}"
                    }
                }
            ],
            "track_shipment": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_track_shipment",
                    "description": "Track a shipment in CargoWise",
                    "parameters": {
                        "tracking_number": "${tracking_number}",
                        "container_number": "${container_number}"
                    }
                }
            ]
        }
        
        return intent_to_tools.get(intent_name, [])
    
    def validate_tool_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate parameters for a tool
        
        Args:
            tool_name: The name of the tool
            parameters: The parameters to validate
            
        Returns:
            A dictionary of validation errors, or an empty dict if valid
        """
        tool_cls = self.get_tool(tool_name)
        if not tool_cls:
            return {"tool": [f"Tool {tool_name} not found"]}
            
        errors = {}
        
        # Check required parameters
        required_params = getattr(tool_cls, "required_params", {})
        for param_name, param_type in required_params.items():
            if param_name not in parameters:
                if not errors.get("required"):
                    errors["required"] = []
                errors["required"].append(f"Missing required parameter: {param_name}")
            elif not isinstance(parameters[param_name], param_type):
                if not errors.get("type"):
                    errors["type"] = []
                errors["type"].append(f"Parameter {param_name} should be of type {param_type.__name__}")
                
        # Check optional parameters
        optional_params = getattr(tool_cls, "optional_params", {})
        for param_name, param_value in parameters.items():
            if param_name not in required_params and param_name in optional_params:
                param_type = optional_params[param_name]
                if not isinstance(param_value, param_type):
                    if not errors.get("type"):
                        errors["type"] = []
                    errors["type"].append(f"Parameter {param_name} should be of type {param_type.__name__}")
                    
        return errors

    def validate_tool_config(self, tool_config: Dict[str, Any]) -> List[str]:
            """
            Validate a complete tool configuration
            
            Args:
                tool_config: Tool configuration to validate
                
            Returns:
                List of validation errors, or empty list if valid
            """
            errors = []
            
            # Check if tool name is provided
            if "name" not in tool_config:
                errors.append("Tool name is required")
                return errors
            
            # Get tool name
            tool_name = tool_config["name"]
            
            # Check if tool exists
            tool_cls = self.get_tool(tool_name)
            if not tool_cls:
                errors.append(f"Tool not found: {tool_name}")
                return errors
            
            # Get parameters
            parameters = tool_config.get("parameters", {})
            
            # Validate parameters
            param_errors = self.validate_tool_parameters(tool_name, parameters)
            
            # Convert parameter errors to flat list
            for error_type, error_list in param_errors.items():
                errors.extend(error_list)
            
            return errors

# # Singleton accessor function
# def get_tool_registry() -> ToolRegistry:
#     """Get the global tool registry instance"""
#     return ToolRegistry()

# Modify the get_tool_registry function to avoid duplicate registrations
def get_tool_registry():
    """Get the global tool registry instance"""
    registry = ToolRegistry()
    
    # Only register tools if the registry is empty
    # This prevents duplicate registrations when discover_tools is also called
    if not registry._tools:
        logger.info("Registering Robot Framework-based CargoWise tools")
        registry.register_tool(CargoWiseLoginTool)
        registry.register_tool(CargoWiseSearchConsolidationByReferenceNumberTool)
        registry.register_tool(CargoWiseSearchBookingTool)
        registry.register_tool(CargoWiseCreateConsolidationTool)
        registry.register_tool(CargoWiseSearchShipmentByHousebillTool,)
        # Register other existing tools
        registry.register_tool(CargoWiseCreateShipmentTool)
        registry.register_tool(CargoWiseUpdateBookingTool)
        registry.register_tool(CargoWiseGenerateReportTool)
    
    return registry

# Initialize the registry on module import - simplify to avoid double initialization
registry = get_tool_registry()

# Only discover tools if we haven't registered any yet
if len(registry._tools) == 0:
    registry_tools_count = registry.discover_tools()
    logger.info(f"Initialized tool registry with {registry_tools_count} tools")