# Desktop automation tools
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from app.automation.desktop.sikulix_driver import SikuliXDriver
import base64
import os
import tempfile
from typing import Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

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
        # Calculate confidence based on text complexity
        confidence = self._assess_text_confidence(input.parameters["text"])
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "text_entered": input.parameters["text"],
                "characters": len(input.parameters["text"])
            },
            "confidence": confidence
        }
    def _assess_text_confidence(self, text: str) -> float:
        """Assess confidence based on text characteristics"""
        # Lower confidence for very long text (more prone to errors)
        if len(text) > 100:
            return 0.85
        
        # Lower confidence for text with special characters
        if re.search(r'[^\w\s]', text):
            return 0.9
        
        # High confidence for simple text
        return 0.98

class DesktopWaitImageTool(Marc1Tool):
    name = "desktop_wait_image"
    description = "Wait for an image to appear on screen"
    required_params = {"image_base64": str, "timeout": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        sikulix = SikuliXDriver()
        image_bytes = base64.b64decode(input.parameters["image_base64"])
        
        script = f"""
        from sikuli import *
        setAutoWaitTimeout({input.parameters["timeout"]})
        wait(Pattern("target.png").similar(0.9), {input.parameters["timeout"]})
        """
        
        result = await sikulix.execute_script(script, image_bytes)
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "action": "wait_image",
                "timeout": input.parameters["timeout"],
                "found": result["success"]
            },
            "error": result.get("error")
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

class ClickElementTool(Marc1Tool):
    name = "desktop_click_element"
    description = "Click on a UI element identified by image or coordinates"
    required_params = {"target": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        from app.automation.desktop.sikulix_driver import SikuliXDriver
        
        sikulix = SikuliXDriver()
        target = input.parameters["target"]
        
        # Check if target is coordinates or image path
        if isinstance(target, str) and "," in target:
            # Coordinates
            x, y = map(int, target.split(","))
            script = f"""
            from sikuli import *
            click({x}, {y})
            """
            confidence = 0.95  # High confidence for exact coordinates
        else:
            # Image path
            script = f"""
            from sikuli import *
            click("{target}")
            """
            confidence = 0.75  # Lower confidence for image recognition
        
        result = await sikulix.execute_script(script)
        
        # If SikuliX returns a match score, use that for confidence
        if "match_score" in result:
            confidence = result["match_score"]
        
        return {
            "status": "SUCCESS" if result["success"] else "ERROR",
            "outputs": {
                "target": target,
                "match_found": result.get("success", False)
            },
            "confidence": confidence,
            "error": result.get("error")
        }