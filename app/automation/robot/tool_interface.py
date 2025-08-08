from typing import Dict, Any, Optional
import logging
import os
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from .cargowise_automation import CargoWiseAutomation
from datetime import datetime
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

class CargoWiseLoginTool(Marc1Tool):
    """Tool for logging into CargoWise"""
    name = "cargowise_login"
    description = "Log into CargoWise using credentials"
    required_params = {"username": str, "password": str, "environment": str}
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute login tool"""
        try:
            # Extract task_id from context
            task_id = input.context.get("task_id") if input.context else None
            logger.info(f"CargoWiseLoginTool executing with task_id: {task_id}")
            # Store input for use in other methods
            self.input = input
            # Get parameters
            username = input.parameters["username"]
            password = input.parameters["password"]
            environment = input.parameters.get("environment", "desktop").lower()
            
            logger.info(f"CargoWiseLoginTool executing with environment: {environment}")
            
            # Determine which login method to use based on environment
            if environment == "web":
                result = await self._web_login(username, password)
            else:
                result = await self._desktop_login(username, password, task_id)
           
            return result
        except Exception as e:
            logger.exception("Error in CargoWise login tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
    
    async def _desktop_login(self, username: str, password: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute desktop login"""
        try:
            automation = CargoWiseAutomation(task_id=task_id)
            result = await automation.login(
                username=username,
                password=password
            )
            # Handle cancellation case
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "logged_in": False,
                        "username": username,
                        "environment": "desktop",
                        "task_id": task_id,
                        "cancelled": True
                    },
                    "error": result.get("error")
                }
            # **FIX: Check if result has 'success' key before accessing it**
            success = result.get("status") == "SUCCESS"
            return {
                "status": "COMPLETED" if success else "FAILED",
                "outputs": {
                    "logged_in": success,
                    "username": username,
                    "environment": "desktop",
                    "task_id": task_id,
                    "screenshot_dir": str(automation.screenshot_dir) if hasattr(automation, 'screenshot_dir') else None
                },
                "error": result.get("error")
            }
        except Exception as e:
            logger.exception("Error in CargoWise desktop login")
            return {
                "status": "FAILED",
                "outputs": {},
                "error": str(e)
            }
    
    async def _web_login(self, username: str, password: str) -> Dict[str, Any]:
        """Execute web login using browser tools"""
        try:
            # Get task_id from stored input
            task_id = self.input.task_id if hasattr(self, 'input') else None
            logger.info(f"Performing web login for user {username} with task_id {task_id}")
            logger.info(f"Performing web login for user {username}")
            
            # Import browser tools
            from app.ai.tools.browser_tools import BrowserNavigateTool, BrowserClickTool, BrowserSessionManager, BrowserExecuteScriptTool
            
            try:
                # Initialize browser session
                await BrowserSessionManager.initialize(headless=False)
            except Exception as e:  # Catch broader exception
                logger.error(f"Browser initialization failed: {str(e)}", exc_info=True)
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": f"Browser automation failed: {str(e)}"
                }
            
            # Create tool instances
            navigate_tool = BrowserNavigateTool()
            click_tool = BrowserClickTool()
            script_tool = BrowserExecuteScriptTool()
            # Get task_id from input
            # task_id = self.input.task_id if hasattr(self, 'input') and self.input else None
            logger.info(f"Using task_id: {task_id} for browser tools")
            # Navigate to login page
            login_url = os.getenv('CARGOWISE_WEB_LOGIN_URL', 'https://cargowise.com/login')  # Replace with actual URL
            
            navigate_result = await navigate_tool.execute({
                "parameters": {
                    "task_id": task_id,  # Pass task_id here
                    "url": login_url,
                    "retry_count": 3  # Add retry capability
                },
                 "context": self.input.context if hasattr(self, 'input') else {}
            })
            
            if navigate_result.get("status") != "SUCCESS":
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": f"Failed to navigate to login page: {navigate_result.get('error')}"
                }
            
            # Handle cookie consent banner if present
            cookie_banner_script = """
            // Try to find and close cookie consent banner
            const cookieBanner = document.querySelector('div[aria-label="Cookie Consent Banner"]');
            if (cookieBanner) {
                // Try to find accept button with various selectors
                const acceptButton = cookieBanner.querySelector('button[aria-label="Accept"]') || 
                                    cookieBanner.querySelector('.osano-cm-accept-all') ||
                                    cookieBanner.querySelector('.osano-cm-button--type_accept') ||
                                    cookieBanner.querySelector('button.accept-cookies') ||
                                    Array.from(cookieBanner.querySelectorAll('button')).find(el => 
                                        el.textContent.toLowerCase().includes('accept')
                                    );
                
                if (acceptButton) {
                    acceptButton.click();
                    return "Clicked accept button";
                }
                
                // If no accept button, try to hide the banner
                cookieBanner.style.display = 'none';
                return "Hidden cookie banner";
            }
            return "No cookie banner found";
            """
            
            # Execute script to handle cookie banner
            await script_tool.execute({
                "task_id": task_id,  # Pass task_id here
                "parameters": {
                    "script": cookie_banner_script
                },
                
                "context": self.input.context if hasattr(self, 'input') else {}
            })
            
            # Fill username
            username_result = await click_tool.execute({
                "task_id": task_id,  # Pass task_id here
                "parameters": {
                    "selector": "#loginModel_Username",
                    "text": username
                },
                "context": self.input.context if hasattr(self, 'input') else {}
            })
            
            if username_result.get("status") != "SUCCESS":
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": f"Failed to fill username: {username_result.get('error')}"
                }
            
            # Fill password
            password_result = await click_tool.execute({
                "task_id": task_id,  # Pass task_id here
                "parameters": {
                    "selector": "#loginModel_Password",
                    "text": password
                },
                "context": self.input.context if hasattr(self, 'input') else {}
            })
            
            if password_result.get("status") != "SUCCESS":
                # Clean up browser session before returning
                await BrowserSessionManager.cleanup()
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": f"Failed to fill password: {password_result.get('error')}"
                }
            
            # Try to click login button using JavaScript to avoid interception
            login_script = """
            // Find and click the login button
            const loginButton = document.querySelector('button.btn.btn-primary[type="submit"]');
            if (loginButton) {
                loginButton.click();
                return true;
            }
            return false;
            """
            
            login_result = await script_tool.execute({
                "task_id": task_id,  # Pass task_id here
                "parameters": {
                    "script": login_script
                },
                "context": self.input.context if hasattr(self, 'input') else {}
            })
            
            # If JavaScript click fails, try regular click as fallback
            if login_result.get("status") != "SUCCESS" or login_result.get("outputs", {}).get("result") == "false":
                login_result = await click_tool.execute({
                    "task_id": task_id,
                    "parameters": {
                        "selector": "button.btn.btn-primary[type='submit']"
                    },
                    "context": self.input.context if hasattr(self, 'input') else {}
                })
            # Take a final screenshot before closing the browser
            screenshot_base64 = None
            try:
                screenshot_base64 = await BrowserSessionManager.capture_screenshot("login_result", task_id)
            except Exception as screenshot_error:
                logger.warning(f"Failed to capture final screenshot: {str(screenshot_error)}")
            
            # Clean up browser session before returning
            await BrowserSessionManager.cleanup()
            return {
                "status": "COMPLETED" if login_result.get("status") == "SUCCESS" else "FAILED",
                "outputs": {
                    "logged_in": login_result.get("status") == "SUCCESS",
                    "username": username,
                    "environment": "web"
                },
                "error": login_result.get("error") if login_result.get("status") != "SUCCESS" else None
            }
        except Exception as e:
            logger.exception(f"Error during web login: {str(e)}")
            # Ensure browser is cleaned up even if an exception occurs
            try:
                await BrowserSessionManager.cleanup()
            except Exception as cleanup_error:
                logger.warning(f"Error during browser cleanup: {str(cleanup_error)}")
            return {
                "status": "FAILED",
                "outputs": {},
                "error": f"Web login failed: {str(e)}"
            }

# The rest of your classes remain the same, but update the status values
class CargoWiseSearchShipmentByHousebillTool(Marc1Tool):
    """Tool for searching a shipment by housebill in CargoWise"""
    name = "cargowise_search_shipment_by_housebill"
    description = "Search for a shipment by housebill in CargoWise"
    required_params = {
        "housebill": str
    }
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """" Execute search_shipment tol"""
        try:
            automation = CargoWiseAutomation()
            result = await automation.search_shipment_by_housebill(
                housebill=input.parameters["housebill"],
            )
            return{
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "shipment_found": result["success"],
                    "housebill": input.parameters["housebill"]
                },
                "error": result.get("error")

            }
    
        except Exception as e:
                logger.exception("Error in CargoWise search shipment by housebill tool")
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": str(e)
                }



class CargoWiseCreateShipmentTool(Marc1Tool):
    """Tool for creating a shipment in CargoWise"""
    name = "cargowise_create_shipment"
    description = "Create a new shipment in CargoWise"
    required_params = {
        "weight": str,
        "consignor": str,
        "transport_method": str,
        "description": str
    }
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute create shipment tool"""
        try:
            automation = CargoWiseAutomation()
            result = await automation.create_shipment(
                weight=input.parameters["weight"],
                consignor=input.parameters["consignor"],
                transport_method=input.parameters["transport_method"],
                description=input.parameters["description"]
            )
            
            return {
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "shipment_created": result["success"],
                    "weight": input.parameters["weight"],
                    "consignor": input.parameters["consignor"],
                    "transport_method": input.parameters["transport_method"],
                    "description": input.parameters["description"]
                },
                "error": result.get("error")
            }
        except Exception as e:
            logger.exception("Error in CargoWise create shipment tool")
            return {
                "status": "FAILED",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseCreateConsolidationTool(Marc1Tool):
    """Tool for creating a consolidation in CargoWise"""
    name = "cargowise_create_consolidation"
    description = "Create a new consolidation in CargoWise"
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
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute create consolidation tool"""
        try:
            # Extract task_id from context
            task_id = input.context.get("task_id") if input.context else None
            automation = CargoWiseAutomation(task_id=task_id)
            result = await automation.create_consolidation(
                transport=input.parameters["transport"],
                container_mode=input.parameters["container_mode"],
                first_load=input.parameters["first_load"],
                last_load=input.parameters["last_load"],
                voyage=input.parameters["voyage"],
                etd=input.parameters["etd"],
                eta=input.parameters["eta"],
                bol=input.parameters["bol"],
                vessel=input.parameters["vessel"]
            )
            
            return {
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "consolidation_created": result["success"],
                    "transport": input.parameters["transport"],
                    "container_mode": input.parameters["container_mode"],
                    "first_load": input.parameters["first_load"],
                    "last_load": input.parameters["last_load"],
                    "voyage": input.parameters["voyage"],
                    "etd": input.parameters["etd"],
                    "eta": input.parameters["eta"],
                    "bol": input.parameters["bol"],
                    "vessel": input.parameters["vessel"]
                },
                "error": result.get("error")
            }
        except Exception as e:
            logger.exception("Error in CargoWise create consolidation tool")
            return {
                "status": "FAILED",
                "outputs": {},
                "error": str(e)
            }

class CargoWiseSearchBookingTool(Marc1Tool):
    """Tool for searching bookings in CargoWise"""
    name = "cargowise_search_booking"
    description = "Search for a booking in CargoWise"
    required_params = {"booking_reference": str}
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute search booking tool"""
        try:
            # Extract task_id from context
            task_id = input.context.get("task_id") if input.context else None
            automation = CargoWiseAutomation(task_id=task_id)
            result = await automation.search_booking(
                booking_reference=input.parameters["booking_reference"]
            )
            
            # Handle cancellation case
            if result.get("status") == "CANCELED":
                return {
                    "status": "CANCELED",
                    "outputs": {
                        "search_completed": False,
                        "booking_reference": input.parameters["booking_reference"],
                        "task_id": task_id,
                        "cancelled": True
                    },
                    "error": result.get("error")
                }
            
            # **FIX: Use result.get() to safely access 'success' key**
            success = result.get("success", False)
            return {
                "status": "COMPLETED" if success else "FAILED",
                "outputs": {
                    "search_completed": success,
                    "booking_reference": input.parameters["booking_reference"],
                    "task_id": task_id
                },
                "error": result.get("error")
            }
        except Exception as e:
            logger.exception("Error in CargoWise search booking tool")
            return {
                "status": "FAILED",
                "outputs": {},
                "error": str(e)
            }