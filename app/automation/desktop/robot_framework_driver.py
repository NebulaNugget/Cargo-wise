# Desktop automation tools
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from app.automation.desktop.sikulix_driver import SikuliXDriver
from app.automation.desktop.pyautogui_driver import PyAutoGUIDriver
from app.automation.desktop.robot_framework_driver import RobotFrameworkDriver
import base64
import os
import tempfile


class ClickImageTool(Marc1Tool):
    name = "desktop_click_image"
    description = "Click on screen region matching provided image"
    required_params = {"image_base64": str, "timeout": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        sikulix = SikuliXDriver()
        image_bytes = base64.b64decode(input.parameters["image_base64"])
        
        # Fix: Use a temporary file name instead of the base64 string in the script
        script = f"""
        from sikuli import *
        setAutoWaitTimeout({input.parameters["timeout"]})
        click(Pattern("target.png").similar(0.9))
        """
        
        result = await sikulix.execute_script(script, image_bytes)
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "action": "click_image",
                "match_score": 0.9
            },
            "error": result.get("error")
        }

class TypeTextTool(Marc1Tool):
    name = "desktop_type_text"
    description = "Type text into focused desktop application"
    required_params = {"text": str}

    async def _execute(self, input: ToolNodeInput) -> dict:  # Fixed: Changed ToolInput to ToolNodeInput
        sikulix = SikuliXDriver()
        script = f"""
        from sikuli import *
        type("{input.parameters["text"]}")
        """
        
        result = await sikulix.execute_script(script)
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "text_entered": input.parameters["text"],
                "characters": len(input.parameters["text"])
            }
        }

class ClickButtonTool(Marc1Tool):
    name = "click_button"
    description = "Clicks UI button using SikuliX"
    required_params = {"image_path": str, "timeout": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        sikulix = SikuliXDriver()
        
        # Read the image file
        with open(input.parameters["image_path"], "rb") as f:
            image_bytes = f.read()
        
        script = f"""
        from sikuli import *
        setAutoWaitTimeout({input.parameters["timeout"]})
        click(Pattern("target.png").similar(0.9))
        # Take screenshot after clicking for verification
        screenshot = capture(SCREEN)
        screenshot.save("result.png")
        """
        
        result = await sikulix.execute_script(script, image_bytes)
        
        # Get screenshot if available
        screenshot_base64 = ""
        if result["success"] and os.path.exists(os.path.join(result.get("temp_dir", ""), "result.png")):
            with open(os.path.join(result.get("temp_dir", ""), "result.png"), "rb") as f:
                screenshot_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "click_position": result.get("click_position", (0, 0)),
                "screenshot": screenshot_base64
            },
            "error": result.get("error")
        }

# New PyAutoGUI-based tools
class PyAutoGUIClickTool(Marc1Tool):
    name = "pyautogui_click"
    description = "Click at specific coordinates using PyAutoGUI"
    required_params = {"x": int, "y": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        driver = PyAutoGUIDriver()
        result = await driver.click_position(
            input.parameters["x"], 
            input.parameters["y"]
        )
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "position": result.get("position", (0, 0))
            },
            "error": result.get("error")
        }

class PyAutoGUIScreenshotTool(Marc1Tool):
    name = "pyautogui_screenshot"
    description = "Take a screenshot of the screen or region"
    required_params = {}  # Optional parameters handled in _execute

    async def _execute(self, input: ToolNodeInput) -> dict:
        driver = PyAutoGUIDriver()
        
        # Check if region is specified
        region = None
        if all(k in input.parameters for k in ["x", "y", "width", "height"]):
            region = (
                input.parameters["x"],
                input.parameters["y"],
                input.parameters["width"],
                input.parameters["height"]
            )
        
        result = await driver.take_screenshot(region)
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "screenshot": result.get("image_base64", ""),
                "region": result.get("region")
            },
            "error": result.get("error")
        }

# Robot Framework-based tools
class RobotWorkflowTool(Marc1Tool):
    name = "robot_workflow"
    description = "Execute a sequence of desktop actions using Robot Framework"
    required_params = {"steps": list}

    async def _execute(self, input: ToolNodeInput) -> dict:
        driver = RobotFrameworkDriver()
        result = await driver.execute_desktop_workflow(input.parameters["steps"])
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "output": result.get("output", "")
            },
            "error": result.get("error")
        }

class CargoWiseLoginTool(Marc1Tool):
    name = "cargowise_login"
    description = "Log into CargoWise using credentials"
    required_params = {"username": str, "password": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        driver = RobotFrameworkDriver()
        
        # Create a specialized workflow for CargoWise login
        steps = [
            {"action": "Click", "target": "login_button.png", "timeout": 10},
            {"action": "Wait", "target": "username_field.png", "timeout": 5},
            {"action": "Click", "target": "username_field.png"},
            {"action": "Type", "target": input.parameters["username"]},
            {"action": "Click", "target": "password_field.png"},
            {"action": "Type", "target": input.parameters["password"]},
            {"action": "Click", "target": "submit_button.png"},
            {"action": "Wait", "target": "dashboard_loaded.png", "timeout": 20}
        ]
        
        result = await driver.execute_desktop_workflow(steps)
        
        # Take a screenshot for verification
        pyautogui_driver = PyAutoGUIDriver()
        screenshot_result = await pyautogui_driver.take_screenshot()
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "logged_in": result["success"],
                "screenshot": screenshot_result.get("image_base64", "")
            },
            "error": result.get("error")
        }