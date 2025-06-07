# # LangChain tools
# # Import and register all tools
# from app.core.marc1.tool_registry import get_tool_registry
# from app.ai.tools.cargowise_tools import (
#     CargoWiseLoginTool,
#     CargoWiseSearchBookingTool,
#     CargoWiseCreateBookingTool,
#     CargoWiseUpdateBookingTool,
#     CargoWiseGenerateReportTool
# )

# # Register all tools with the registry
# def register_all_tools():
#     registry = get_tool_registry()
    
#     # Register CargoWise tools
#     registry.register_tool(CargoWiseLoginTool)
#     registry.register_tool(CargoWiseSearchBookingTool)
#     registry.register_tool(CargoWiseCreateBookingTool)
#     registry.register_tool(CargoWiseUpdateBookingTool)
#     registry.register_tool(CargoWiseGenerateReportTool)
    
#     return registry