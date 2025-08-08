# Register Robot Framework-based tools with the tool registry
from app.core.marc1.tool_registry import get_tool_registry
from app.automation.robot import (
    CargoWiseLoginTool,
    
    CargoWiseSearchBookingTool
)
import logging

logger = logging.getLogger(__name__)

def register_robot_tools():
    """
    Register Robot Framework-based tools with the global tool registry
    
    This function registers the simplified Robot Framework-based tools
    that replace the more complex desktop automation tools.
    """
    registry = get_tool_registry()
    
    # Register CargoWise tools based on Robot Framework
    logger.info("Registering Robot Framework-based CargoWise tools")
    registry.register_tool(CargoWiseLoginTool)
  
    registry.register_tool(CargoWiseSearchBookingTool)
    
    return registry