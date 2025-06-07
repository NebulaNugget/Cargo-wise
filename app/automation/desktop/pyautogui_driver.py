import pyautogui
import base64
import tempfile
import os
from io import BytesIO
from PIL import Image
from typing import Tuple, Optional, Dict, Any

class PyAutoGUIDriver:
    """Driver for PyAutoGUI-based desktop automation"""
    
    def __init__(self):
        # Configure PyAutoGUI settings
        pyautogui.PAUSE = 0.5  # Default pause between actions
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    
    async def click_position(self, x: int, y: int) -> Dict[str, Any]:
        """Click at specific coordinates"""
        try:
            pyautogui.click(x, y)
            return {
                "success": True,
                "action": "click",
                "position": (x, y)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def click_image(self, image_bytes: bytes, confidence: float = 0.9, timeout: int = 10) -> Dict[str, Any]:
        """Click on an image on screen"""
        try:
            # Save image to temp file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_file.write(image_bytes)
                temp_path = temp_file.name
            
            # Find and click the image
            try:
                location = pyautogui.locateCenterOnScreen(temp_path, confidence=confidence, timeout=timeout)
                if location:
                    pyautogui.click(location)
                    return {
                        "success": True,
                        "action": "click_image",
                        "position": location,
                        "confidence": confidence
                    }
                else:
                    return {
                        "success": False,
                        "error": "Image not found on screen"
                    }
            finally:
                # Clean up temp file
                os.unlink(temp_path)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def type_text(self, text: str) -> Dict[str, Any]:
        """Type text at current cursor position"""
        try:
            pyautogui.write(text)
            return {
                "success": True,
                "action": "type",
                "text": text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def press_key(self, key: str) -> Dict[str, Any]:
        """Press a specific key"""
        try:
            pyautogui.press(key)
            return {
                "success": True,
                "action": "keypress",
                "key": key
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """Take screenshot of entire screen or region"""
        try:
            screenshot = pyautogui.screenshot(region=region)
            
            # Convert to base64
            buffered = BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                "success": True,
                "action": "screenshot",
                "image_base64": img_str,
                "region": region
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }