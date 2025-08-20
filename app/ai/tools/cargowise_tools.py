
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from app.ai.tools.desktop_tools import ClickImageTool, TypeTextTool
from app.ai.tools.browser_tools import BrowserNavigateTool, BrowserClickTool
from typing import Dict, Any, List
import base64
import os
import logging
import asyncio 

logger = logging.getLogger(__name__)
# Add this helper function after the imports
def get_image_base64(image_name, image_dir=None):
    """Load image in base64 format with caching for better performance"""
    if not hasattr(get_image_base64, "cache"):
        get_image_base64.cache = {}
        
    if image_name in get_image_base64.cache:
        return get_image_base64.cache[image_name]
    
    if image_dir is None:
        image_dir = os.path.join(os.getcwd(), "app", "resources", "images", "cargowise")
        
    try:
        with open(os.path.join(image_dir, image_name), "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
            get_image_base64.cache[image_name] = image_data
            return image_data
    except Exception as e:
        logger.error(f"Failed to load image {image_name}: {str(e)}")
        return None

class CargoWiseLoginTool(Marc1Tool):
    name = "cargowise_login"
    description = "Log into CargoWise using credentials"
    required_params = {"username": str, "password": str, "environment": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        # Get parameters safely
        parameters = self._get_parameters(input)
        # Determine if we're using desktop or web version based on environment
        environment = parameters.get("environment", "web").lower()
        
        logger.info(f"Using environment: {environment}")
        if environment == "desktop":
            # return await self._desktop_login(input)
            return await self._web_login(input)
        else:
            return await self._web_login(input)
    
    async def _desktop_login(self, input: ToolNodeInput) -> dict:
        # Get parameters regardless of input type
        if isinstance(input, dict):
            parameters = input.get("parameters", {})
        else:
            parameters = input.parameters
        # Get image paths from configuration
        image_dir = os.path.join(os.getcwd(), "app",  "cargowise_images")
        
        # Load required images using the helper function
        login_button = get_image_base64("login_button.png", image_dir)
        username_field = get_image_base64("username_field.png", image_dir)
        password_field = get_image_base64("password_field.png", image_dir)
        
        
        # Execute login sequence
        click_tool = ClickImageTool()
        type_tool = TypeTextTool()
        
        # Click username field
        username_result = await click_tool.execute({
            "parameters": {
                "image_base64": username_field,
                "timeout": 10
            }
        })
        
        if username_result.get("status") != "SUCCESS":
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Failed to find username field: {username_result.get('error')}"
            }
        
        # Type username
        await type_tool.execute({
            "parameters": {
                "text":parameters["username"]
            }
        })
        
        # Click password field
        password_result = await click_tool.execute({
            "parameters": {
                "image_base64": password_field,
                "timeout": 5
            }
        })
        
        if password_result.get("status") != "SUCCESS":
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Failed to find password field: {password_result.get('error')}"
            }
        
        # Type password
        await type_tool.execute({
            "parameters": {
                "text": input.parameters["password"]
            }
        })
        
        # Click login button
        login_result = await click_tool.execute({
            "parameters": {
                "image_base64": login_button,
                "timeout": 5
            }
        })
        
        return {
            "status": "SUCCESS" if login_result.get("status") == "SUCCESS" else "ERROR",
            "outputs": {
                "logged_in": login_result.get("status") == "SUCCESS"
            },
            "error": login_result.get("error")
        }
    
    async def _web_login(self, input: ToolNodeInput) -> dict:
        """Login to CargoWise web version"""
        # Get parameters regardless of input type
        parameters = self._get_parameters(input)
        
        # Log that we're using web login
        logger.info("Using CargoWise web login")
        
        try:
            # Web version login using browser tools
            from app.ai.tools.browser_tools import BrowserNavigateTool, BrowserClickTool, BrowserSessionManager
            
            # Initialize browser session
            await BrowserSessionManager.initialize()
            
            # Create tool instances
            navigate_tool = BrowserNavigateTool()
            click_tool = BrowserClickTool()
            
            # Navigate to login page
            login_url = "https://cargowise.com/login"  # Replace with actual URL
            
            navigate_result = await navigate_tool.execute({
                "parameters": {
                    "url": login_url
                }
            })
            
            if navigate_result.get("status") != "SUCCESS":
                return {
                    "status": "ERROR",
                    "outputs": {},
                    "error": f"Failed to navigate to login page: {navigate_result.get('error')}"
                }
            
            # Fill username
            username_result = await click_tool.execute({
                "parameters": {
                    "selector": "#username",
                    "text": parameters["username"]
                }
            })
            
            if username_result.get("status") != "SUCCESS":
                return {
                    "status": "ERROR",
                    "outputs": {},
                    "error": f"Failed to fill username: {username_result.get('error')}"
                }
            
            # Fill password
            password_result = await click_tool.execute({
                "parameters": {
                    "selector": "#password",
                    "text": parameters["password"]
                }
            })
            
            if password_result.get("status") != "SUCCESS":
                return {
                    "status": "ERROR",
                    "outputs": {},
                    "error": f"Failed to fill password: {password_result.get('error')}"
                }
            
            # Click login button
            login_result = await click_tool.execute({
                "parameters": {
                    "selector": "button[type='submit']"
                }
            })
            
            return {
                "status": "SUCCESS" if login_result.get("status") == "SUCCESS" else "ERROR",
                "outputs": {
                    "logged_in": login_result.get("status") == "SUCCESS",
                    "username": parameters["username"],
                    "environment": "web"
                },
                "error": login_result.get("error") if login_result.get("status") != "SUCCESS" else None
            }
        except Exception as e:
            logger.error(f"Error during web login: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Web login failed: {str(e)}"
            }

class CargoWiseCreateShipmentTool(Marc1Tool):
    name = "cargowise_create_shipment"
    description = "Create a new shipment in CargoWise"
    required_params = {
        "weight": str,
        "consignor": str,
        "transport_method": str,
        "description": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        """Execute create shipment using Robot Framework automation"""
        try:
            # Get parameters safely
            parameters = self._get_parameters(input)
            
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for shipment creation")
            
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            
            # Execute shipment creation using Robot Framework
            result = await automation.create_shipment(
                weight=parameters["weight"],
                consignor=parameters["consignor"],
                transport_method=parameters["transport_method"],
                description=parameters["description"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "shipment_created": False,
                        "weight": parameters["weight"],
                        "consignor": parameters["consignor"],
                        "transport_method": parameters["transport_method"],
                        "description": parameters["description"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "shipment_created": result.get("success", False),
                    "weight": parameters["weight"],
                    "consignor": parameters["consignor"],
                    "transport_method": parameters["transport_method"],
                    "description": parameters["description"]
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise create shipment tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseCreateShipment2Tool(Marc1Tool):
    name = "cargowise_create_shipment2"
    description = "Create a new shipment in CargoWise part2"
    required_params = {
        "weight": str,
        "consignor": str,
        "transport_method": str,
        "description": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        """Execute create shipment using Robot Framework automation"""
        try:
            # Get parameters safely
            parameters = self._get_parameters(input)
            
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for shipment creation part2")
            
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            
            # Execute shipment creation using Robot Framework
            result = await automation.create_shipment2(
                weight=parameters["weight"],
                consignor=parameters["consignor"],
                transport_method=parameters["transport_method"],
                description=parameters["description"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "shipment_created": False,
                        "weight": parameters["weight"],
                        "consignor": parameters["consignor"],
                        "transport_method": parameters["transport_method"],
                        "description": parameters["description"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "shipment_created": result.get("success", False),
                    "weight": parameters["weight"],
                    "consignor": parameters["consignor"],
                    "transport_method": parameters["transport_method"],
                    "description": parameters["description"]
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise create shipment tool part2")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseSearchShipmentByHousebillTool(Marc1Tool):
    name = "cargowise_search_shipment_by_housebill"
    description = "Search for a shipment in CargoWise using housebill number"
    required_params = {"housebill": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        try:
            parameters = self._get_parameters(input)
            logger.info("Using CargoWise Robot Framework automation for shipment search by housebill")
            
            # Use the Robot Framework automation
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            result = await automation.search_shipment_by_housebill(
                housebill=parameters["housebill"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "shipment_found": False,
                        "housebill": parameters["housebill"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "shipment_found": result.get("success", False),
                    "housebill": parameters["housebill"],
                    "search_results": result.get("outputs", {}),
                    "shipment_id": f"SHIP-{parameters['housebill']}"
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise search shipment by housebill tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseSearchConsolidationByReferenceNumberTool(Marc1Tool):
    name = "cargowise_search_consolidation_by_referencenumber"
    description = "Search for a consolidation in CargoWise using reference number"
    required_params = {"referencenumber": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        try:
            parameters = self._get_parameters(input)
            logger.info("Using CargoWise Robot Framework automation for consolidation search by reference number")
            
            # Use the Robot Framework automation
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            result = await automation.search_consolidation_by_referencenumber(
                referencenumber=parameters["referencenumber"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "consolidation_found": False,
                        "referencenumber": parameters["referencenumber"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "consolidation_found": result.get("success", False),
                    "referencenumber": parameters["referencenumber"],
                    "search_results": result.get("outputs", {}),
                    "consolidation_id": f"CONS-{parameters['referencenumber']}"
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise search consolidation by reference number tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseCreateConsolidationTool(Marc1Tool):
    name = "cargowise_create_consolidation"
    description = "Create a new consolidation in CargoWise with transport, container mode, load details, voyage info, dates, BOL, and vessel"
    required_params = {
        "transport": str, 
        "container_mode": str,
        "first_load": str,
        "last_load": str,
        "voyage": str,
        "etd": str,
        "eta": str,
        "bol": str,
        "vessel": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        # Get parameters safely
        try:
            parameters = self._get_parameters(input)
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for consolidation creation")
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            # Execute consolidation creation using Robot Framework
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            result = await automation.create_consolidation(
                transport=parameters["transport"],
                container_mode=parameters["container_mode"],
                first_load=parameters["first_load"],
                last_load=parameters["last_load"],
                voyage=parameters["voyage"],
                etd=parameters["etd"],
                eta=parameters["eta"],
                bol=parameters["bol"],
                vessel=parameters["vessel"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "consolidation_created": False,
                        "transport": parameters["transport"],
                        "container_mode": parameters["container_mode"],
                        "first_load": parameters["first_load"],
                        "last_load": parameters["last_load"],
                        "voyage": parameters["voyage"],
                        "etd": parameters["etd"],
                        "eta": parameters["eta"],
                        "bol": parameters["bol"],
                        "vessel": parameters["vessel"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "consolidation_created": result.get("success", False),
                    "transport": parameters["transport"],
                    "container_mode": parameters["container_mode"],
                    "first_load": parameters["first_load"],
                    "last_load": parameters["last_load"],
                    "voyage": parameters["voyage"],
                    "etd": parameters["etd"],
                    "eta": parameters["eta"],
                    "bol": parameters["bol"],
                    "vessel": parameters["vessel"],
                    "consolidation_id": f"CONS-{parameters['voyage']}-{parameters['vessel']}"
                },
                "error": result.get("error")
            }   
        
        
        except Exception as e:
            logger.exception("Error in CargoWise create consolidation tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
class CargoWiseCreateConsolidation2Tool(Marc1Tool):
    name = "cargowise_create_consolidation2"
    description = "Create a new consolidation in CargoWise part 2 with transport, container mode, load details, voyage info, dates, BOL, and vessel"
    required_params = {
        "transport": str, 
        "container_mode": str,
        "first_load": str,
        "last_load": str,
        "voyage": str,
        "etd": str,
        "eta": str,
        "bol": str,
        "vessel": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        # Get parameters safely
        try:
            parameters = self._get_parameters(input)
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for consolidation creation part2")
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            # Execute consolidation creation using Robot Framework
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            result = await automation.create_consolidation2(
                transport=parameters["transport"],
                container_mode=parameters["container_mode"],
                first_load=parameters["first_load"],
                last_load=parameters["last_load"],
                voyage=parameters["voyage"],
                etd=parameters["etd"],
                eta=parameters["eta"],
                bol=parameters["bol"],
                vessel=parameters["vessel"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "consolidation_created": False,
                        "transport": parameters["transport"],
                        "container_mode": parameters["container_mode"],
                        "first_load": parameters["first_load"],
                        "last_load": parameters["last_load"],
                        "voyage": parameters["voyage"],
                        "etd": parameters["etd"],
                        "eta": parameters["eta"],
                        "bol": parameters["bol"],
                        "vessel": parameters["vessel"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "consolidation_created": result.get("success", False),
                    "transport": parameters["transport"],
                    "container_mode": parameters["container_mode"],
                    "first_load": parameters["first_load"],
                    "last_load": parameters["last_load"],
                    "voyage": parameters["voyage"],
                    "etd": parameters["etd"],
                    "eta": parameters["eta"],
                    "bol": parameters["bol"],
                    "vessel": parameters["vessel"],
                    "consolidation_id": f"CONS-{parameters['voyage']}-{parameters['vessel']}"
                },
                "error": result.get("error")
            }   
        
        
        except Exception as e:
            logger.exception("Error in CargoWise create consolidation tool part2")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }


class CargoWiseCreateOrderTool(Marc1Tool):
    name = "cargowise_create_order"
    description = "Navigate to new order creation form in CargoWise"
    required_params = {
        "password":str,
        "buyer": str,
        "supplier": str,
        "container_return_date": str,
        "sanction": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        """Execute create order using Robot Framework automation"""
        try:
            # Get parameters safely
            parameters = self._get_parameters(input)
            
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for order creation")
            
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            
            # Execute order creation using Robot Framework
            result = await automation.create_order_part1(
                password=parameters['password'],
                buyer=parameters["buyer"],
                supplier=parameters["supplier"],
                container_return_date=parameters["container_return_date"],
                sanction=parameters["sanction"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "password":parameters["password"],
                        "order_created": False,
                        "buyer": parameters["buyer"],
                        "supplier": parameters["supplier"],
                        "container_return_date": parameters["container_return_date"],
                        "sanction": parameters["sanction"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "password":parameters["password"],
                    "order_created": result.get("success", False),
                    "buyer": parameters["buyer"],
                    "supplier": parameters["supplier"],
                    "container_return_date": parameters["container_return_date"],
                    "sanction": parameters["sanction"]
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise create order tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseCreateOrder2Tool(Marc1Tool):
    name = "cargowise_create_order2"
    description = "Create a new order in CargoWise"
    required_params = {
        "password":str,
        "buyer": str,
        "supplier": str,
        "container_return_date": str,
        "sanction": str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        """Execute create order using Robot Framework automation"""
        try:
            # Get parameters safely
            parameters = self._get_parameters(input)
            
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for order creation")
            
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            
            # Execute order creation using Robot Framework
            result = await automation.create_order_part2(
                password=parameters['password'],
                buyer=parameters["buyer"],
                supplier=parameters["supplier"],
                container_return_date=parameters["container_return_date"],
                sanction=parameters["sanction"]
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "password":parameters["password"],
                        "order_created": False,
                        "buyer": parameters["buyer"],
                        "supplier": parameters["supplier"],
                        "container_return_date": parameters["container_return_date"],
                        "sanction": parameters["sanction"]
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "password":parameters["password"],
                    "order_created": result.get("success", False),
                    "buyer": parameters["buyer"],
                    "supplier": parameters["supplier"],
                    "container_return_date": parameters["container_return_date"],
                    "sanction": parameters["sanction"]
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise create order tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseLogoutTool(Marc1Tool):
    name = "cargowise_logout"
    description = "Logout from CargoWise"
    required_params = {
        "password":str
    }

    async def _execute(self, input: ToolNodeInput) -> dict:
        """Execute logout using Robot Framework automation"""
        try:
            # Get parameters safely
            parameters = self._get_parameters(input)
            
            # Log that we're using Robot Framework automation
            logger.info("Using CargoWise Robot Framework automation for logout")

            
            # Use the Robot Framework automation instead of desktop image tools
            from app.automation.robot.cargowise_automation import CargoWiseAutomation
            
            # Create automation instance
            automation = CargoWiseAutomation(task_id=input.task_id)
            
            # Execute order creation using Robot Framework
            result = await automation.logout(

                password=parameters['password'],
                
            )
            
            # Check if task was cancelled
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "password":parameters["password"],
                        
                    },
                    "error": "Task was cancelled by user"
                }
            
            # Return result in the expected format
            return {
                "status": "SUCCESS" if result.get("success", False) else "ERROR",
                "outputs": {
                    "password":parameters["password"],
                    "logout_success": result.get("success", False),

                },
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.exception("Error in CargoWise logout tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseSearchBookingTool(Marc1Tool):
    name = "cargowise_search_booking"
    description = "Search for a booking in CargoWise"
    required_params = {"booking_reference": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        # Implementation for searching a booking
        click_tool = ClickImageTool()
        type_tool = TypeTextTool()
        
        # Get image paths
        image_dir = os.path.join(os.getcwd(), "app", "resources", "images", "cargowise")
        
        with open(os.path.join(image_dir, "search_icon.png"), "rb") as f:
            search_icon = base64.b64encode(f.read()).decode('utf-8')
            
        with open(os.path.join(image_dir, "search_field.png"), "rb") as f:
            search_field = base64.b64encode(f.read()).decode('utf-8')
        
        # Click search icon
        await click_tool.execute({
            "parameters": {
                "image_base64": search_icon,
                "timeout": 10
            }
        })
        
        # Click search field
        await click_tool.execute({
            "parameters": {
                "image_base64": search_field,
                "timeout": 5
            }
        })
        
        # Type booking reference
        await type_tool.execute({
            "parameters": {
                "text": input.parameters["booking_reference"]
            }
        })
        
        # Press Enter
        await type_tool.execute({
            "parameters": {
                "text": "\n"
            }
        })
        
        return {
            "status": "SUCCESS",
            "outputs": {
                "booking_reference": input.parameters["booking_reference"],
                "search_completed": True
            }
        }


class CargoWiseUpdateBookingTool(Marc1Tool):
    name = "cargowise_update_booking"
    description = "Update an existing booking in CargoWise"
    required_params = {"booking_reference": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        # First search for the booking
        search_tool = CargoWiseSearchBookingTool()
        search_result = await search_tool.execute({
            "parameters": {
                "booking_reference": input.parameters["booking_reference"]
            }
        })
        
        if search_result.get("status") != "SUCCESS":
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Failed to find booking: {search_result.get('error')}"
            }
        
        # Now update the fields that were provided
        click_tool = ClickImageTool()
        type_tool = TypeTextTool()
        
        # Get image paths
        image_dir = os.path.join(os.getcwd(), "app", "resources", "images", "cargowise")
        
        # Process each field that needs updating
        fields_updated = []
        
        # Update origin if provided
        if "origin" in input.parameters:
            with open(os.path.join(image_dir, "origin_field.png"), "rb") as f:
                origin_field = base64.b64encode(f.read()).decode('utf-8')
            
            await click_tool.execute({
                "parameters": {
                    "image_base64": origin_field,
                    "timeout": 5
                }
            })
            
            await type_tool.execute({
                "parameters": {
                    "text": input.parameters["origin"]
                }
            })
            
            fields_updated.append("origin")
        
        # Update destination if provided
        if "destination" in input.parameters:
            with open(os.path.join(image_dir, "destination_field.png"), "rb") as f:
                destination_field = base64.b64encode(f.read()).decode('utf-8')
            
            await click_tool.execute({
                "parameters": {
                    "image_base64": destination_field,
                    "timeout": 5
                }
            })
            
            await type_tool.execute({
                "parameters": {
                    "text": input.parameters["destination"]
                }
            })
            
            fields_updated.append("destination")
        
        # Save changes if any fields were updated
        if fields_updated:
            with open(os.path.join(image_dir, "save_button.png"), "rb") as f:
                save_button = base64.b64encode(f.read()).decode('utf-8')
            
            save_result = await click_tool.execute({
                "parameters": {
                    "image_base64": save_button,
                    "timeout": 5
                }
            })
            
            return {
                "status": "SUCCESS" if save_result.get("status") == "SUCCESS" else "ERROR",
                "outputs": {
                    "booking_updated": save_result.get("status") == "SUCCESS",
                    "booking_reference": input.parameters["booking_reference"],
                    "fields_updated": fields_updated
                },
                "error": save_result.get("error")
            }
        else:
            return {
                "status": "SUCCESS",
                "outputs": {
                    "booking_reference": input.parameters["booking_reference"],
                    "message": "No fields to update were provided"
                }
            }


class CargoWiseGenerateReportTool(Marc1Tool):
    name = "cargowise_generate_report"
    description = "Generate a report in CargoWise"
    required_params = {"report_type": str, "date_range": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        # Implementation for generating a report
        click_tool = ClickImageTool()
        type_tool = TypeTextTool()
        
        # Get image paths
        image_dir = os.path.join(os.getcwd(), "app", "resources", "images", "cargowise")
        
        with open(os.path.join(image_dir, "reports_menu.png"), "rb") as f:
            reports_menu = base64.b64encode(f.read()).decode('utf-8')
            
        # Click reports menu
        await click_tool.execute({
            "parameters": {
                "image_base64": reports_menu,
                "timeout": 10
            }
        })
        
        # Select report type
        report_type_image = f"{input.parameters['report_type'].lower().replace(' ', '_')}.png"
        with open(os.path.join(image_dir, report_type_image), "rb") as f:
            report_type_img = base64.b64encode(f.read()).decode('utf-8')
        
        await click_tool.execute({
            "parameters": {
                "image_base64": report_type_img,
                "timeout": 5
            }
        })
        
        # Enter date range
        with open(os.path.join(image_dir, "date_range_field.png"), "rb") as f:
            date_range_field = base64.b64encode(f.read()).decode('utf-8')
        
        await click_tool.execute({
            "parameters": {
                "image_base64": date_range_field,
                "timeout": 5
            }
        })
        
        await type_tool.execute({
            "parameters": {
                "text": input.parameters["date_range"]
            }
        })
        
        # Generate report
        with open(os.path.join(image_dir, "generate_button.png"), "rb") as f:
            generate_button = base64.b64encode(f.read()).decode('utf-8')
        
        generate_result = await click_tool.execute({
            "parameters": {
                "image_base64": generate_button,
                "timeout": 5
            }
        })
        
        return {
            "status": "SUCCESS" if generate_result.get("status") == "SUCCESS" else "ERROR",
            "outputs": {
                "report_generated": generate_result.get("status") == "SUCCESS",
                "report_type": input.parameters["report_type"],
                "date_range": input.parameters["date_range"]
            },
            "error": generate_result.get("error")
        }