from typing import Dict, Any
import logging
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from .cargowise_automation import CargoWiseAutomation
from datetime import datetime

logger = logging.getLogger(__name__)

class CargoWiseLoginTool(Marc1Tool):
    """Tool for logging into CargoWise"""
    name = "cargowise_login"
    description = "Log into CargoWise using credentials"
    required_params = {"username": str, "password": str, "environment": str}
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute login tool"""
        try:
            # Get parameters
            username = input.parameters["username"]
            password = input.parameters["password"]
            environment = input.parameters.get("environment", "desktop").lower()
            
            logger.info(f"CargoWiseLoginTool executing with environment: {environment}")
            
            # Determine which login method to use based on environment
            if environment == "web":
                result = await self._web_login(username, password)
            else:
                result = await self._desktop_login(username, password)
           
            return result
        except Exception as e:
            logger.exception("Error in CargoWise login tool")
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
    
    async def _desktop_login(self, username: str, password: str) -> Dict[str, Any]:
        """Execute desktop login"""
        try:
            automation = CargoWiseAutomation()
            result = await automation.login(
                username=username,
                password=password
            )
            
            return {
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "logged_in": result["success"],
                    "username": username,
                    "environment": "desktop"
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
            
            # Navigate to login page
            login_url = "https://cargowise.com/login"  # Replace with actual URL
            
            navigate_result = await navigate_tool.execute({
                "parameters": {
                    "url": login_url,
                    "retry_count": 3  # Add retry capability
                }
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
                "parameters": {
                    "script": cookie_banner_script
                }
            })
            
            # Fill username
            username_result = await click_tool.execute({
                "parameters": {
                    "selector": "#loginModel_Username",
                    "text": username
                }
            })
            
            if username_result.get("status") != "SUCCESS":
                return {
                    "status": "FAILED",
                    "outputs": {},
                    "error": f"Failed to fill username: {username_result.get('error')}"
                }
            
            # Fill password
            password_result = await click_tool.execute({
                "parameters": {
                    "selector": "#loginModel_Password",
                    "text": password
                }
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
                "parameters": {
                    "script": login_script
                }
            })
            
            # If JavaScript click fails, try regular click as fallback
            if login_result.get("status") != "SUCCESS" or login_result.get("outputs", {}).get("result") == "false":
                login_result = await click_tool.execute({
                    "parameters": {
                        "selector": "button.btn.btn-primary[type='submit']"
                    }
                })
            # Take a final screenshot before closing the browser
            screenshot_base64 = None
            try:
                screenshot_base64 = await BrowserSessionManager.capture_screenshot("login_result")
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
class CargoWiseCreateBookingTool(Marc1Tool):
    """Tool for creating a booking in CargoWise"""
    name = "cargowise_create_booking"
    description = "Create a new booking in CargoWise"
    required_params = {
        "customer": str,
        "origin": str,
        "destination": str,
        "cargo_details": str
    }
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        """Execute create booking tool"""
        try:
            automation = CargoWiseAutomation()
            result = await automation.create_booking(
                customer=input.parameters["customer"],
                origin=input.parameters["origin"],
                destination=input.parameters["destination"],
                cargo_details=input.parameters["cargo_details"]
            )
            
            return {
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "booking_created": result["success"],
                    "customer": input.parameters["customer"],
                    "origin": input.parameters["origin"],
                    "destination": input.parameters["destination"]
                },
                "error": result.get("error")
            }
        except Exception as e:
            logger.exception("Error in CargoWise create booking tool")
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
            automation = CargoWiseAutomation()
            result = await automation.search_booking(
                booking_reference=input.parameters["booking_reference"]
            )
            
            return {
                "status": "COMPLETED" if result["success"] else "FAILED",
                "outputs": {
                    "search_completed": result["success"],
                    "booking_reference": input.parameters["booking_reference"]
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