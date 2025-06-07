# SikuliX driver for desktop automation
import subprocess
import tempfile
import os
import base64
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class SikuliXDriver:
    """
    Driver for SikuliX desktop automation
    
    This class provides an interface to SikuliX for desktop automation tasks.
    It handles script execution, screenshot capture, and result parsing.
    """
    
    def __init__(self, sikulix_jar_path: Optional[str] = None):
        """
        Initialize SikuliX driver
        
        Args:
            sikulix_jar_path: Path to SikuliX JAR file. If None, uses default path.
        """
        # Default SikuliX JAR path
        self.sikulix_jar_path = sikulix_jar_path or r"C:\SikuliX\sikulix.jar"
        
        # Create screenshots directory if it doesn't exist
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Validate SikuliX installation
        if not os.path.exists(self.sikulix_jar_path):
            logger.warning(f"SikuliX JAR not found at {self.sikulix_jar_path}")
    
    async def execute_script(self, script: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Execute a SikuliX script
        
        Args:
            script: SikuliX script to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Execution result
        """
        # Create a temporary script file
        with tempfile.NamedTemporaryFile(suffix=".sikuli", delete=False, mode="w") as f:
            script_path = f.name
            f.write(script)
        
        try:
            # Add result handling to script
            script_with_result = self._add_result_handling(script)
            
            # Write updated script
            with open(script_path, "w") as f:
                f.write(script_with_result)
            
            # Execute script
            logger.info(f"Executing SikuliX script: {script_path}")
            
            # Create process
            cmd = ["java", "-jar", self.sikulix_jar_path, "-r", script_path]
            
            # Execute process
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for process to complete with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
                stdout_str = stdout.decode("utf-8", errors="ignore")
                stderr_str = stderr.decode("utf-8", errors="ignore")
                
                # Check for errors
                if process.returncode != 0:
                    logger.error(f"SikuliX script execution failed: {stderr_str}")
                    return {
                        "success": False,
                        "error": stderr_str,
                        "output": stdout_str,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                
                # Parse result
                result = self._parse_result(stdout_str)
                
                # Add screenshot if available
                screenshot_path = self._capture_screenshot()
                if screenshot_path:
                    with open(screenshot_path, "rb") as f:
                        screenshot_data = f.read()
                        result["screenshot"] = base64.b64encode(screenshot_data).decode("utf-8")
                
                return result
                
            except asyncio.TimeoutError:
                # Kill process if it times out
                process.kill()
                logger.error(f"SikuliX script execution timed out after {timeout} seconds")
                return {
                    "success": False,
                    "error": f"Execution timed out after {timeout} seconds",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error executing SikuliX script: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        finally:
            # Clean up temporary script file
            try:
                os.unlink(script_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary script file: {str(e)}")
    
    def _add_result_handling(self, script: str) -> str:
        """Add result handling to script"""
        result_file = os.path.join(tempfile.gettempdir(), f"sikulix_result_{uuid.uuid4()}.json")
        
        # Add imports and result handling
        result_script = f"""
import json
import os
import traceback

# Original script
{script}

# Result handling
try:
    result = {{
        "success": True,
        "output": "Script executed successfully",
        "timestamp": str(java.util.Date())
    }}
except Exception as e:
    result = {{
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc(),
        "timestamp": str(java.util.Date())
    }}

# Write result to file
with open(r"{result_file}", "w") as f:
    f.write(json.dumps(result))
    
print("SIKULIX_RESULT_FILE: " + r"{result_file}")
"""
        return result_script
    
    def _parse_result(self, stdout: str) -> Dict[str, Any]:
        """Parse script execution result"""
        # Look for result file path in output
        for line in stdout.splitlines():
            if "SIKULIX_RESULT_FILE:" in line:
                result_file = line.split("SIKULIX_RESULT_FILE:")[1].strip()
                
                # Read result file
                try:
                    with open(result_file, "r") as f:
                        result = json.load(f)
                    
                    # Clean up result file
                    try:
                        os.unlink(result_file)
                    except:
                        pass
                    
                    return result
                except Exception as e:
                    logger.error(f"Error parsing result file: {str(e)}")
        
        # If no result file found, return default result
        return {
            "success": True if "error" not in stdout.lower() else False,
            "output": stdout,
            "error": "No structured result found" if "error" in stdout.lower() else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _capture_screenshot(self) -> Optional[str]:
        """Capture screenshot of desktop"""
        try:
            # Generate screenshot filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshots_dir, f"screenshot_{timestamp}.png")
            
            # Create SikuliX script for screenshot
            script = f"""
from sikuli import *
import os

# Capture screenshot
screen = Screen()
img = screen.capture(screen.getBounds())
img.save(r"{screenshot_path}")
"""
            
            # Create temporary script file
            with tempfile.NamedTemporaryFile(suffix=".sikuli", delete=False, mode="w") as f:
                script_file = f.name
                f.write(script)
            
            # Execute script
            cmd = ["java", "-jar", self.sikulix_jar_path, "-r", script_file]
            subprocess.run(cmd, capture_output=True, timeout=10)
            
            # Clean up script file
            os.unlink(script_file)
            
            # Check if screenshot was created
            if os.path.exists(screenshot_path):
                return screenshot_path
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
        
        return None
    
    async def find_image(self, image_path: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Find an image on the screen
        
        Args:
            image_path: Path to image file
            timeout: Timeout in seconds
            
        Returns:
            Result with coordinates if found
        """
        script = f"""
from sikuli import *
import time

# Set timeout
Settings.AutoWaitTimeout = {timeout}

# Find image
try:
    start_time = time.time()
    match = find(r"{image_path}")
    end_time = time.time()
    
    # Return result
    result = {{
        "success": True,
        "found": True,
        "x": match.getX(),
        "y": match.getY(),
        "width": match.getW(),
        "height": match.getH(),
        "time_taken": end_time - start_time
    }}
except FindFailed:
    result = {{
        "success": True,
        "found": False,
        "error": "Image not found on screen"
    }}
"""
        return await self.execute_script(script, timeout=timeout+5)
    
    async def click_image(self, image_path: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Click on an image on the screen
        
        Args:
            image_path: Path to image file
            timeout: Timeout in seconds
            
        Returns:
            Result with success status
        """
        script = f"""
from sikuli import *
import time

# Set timeout
Settings.AutoWaitTimeout = {timeout}

# Click image
try:
    start_time = time.time()
    match = click(r"{image_path}")
    end_time = time.time()
    
    # Return result
    result = {{
        "success": True,
        "clicked": True,
        "time_taken": end_time - start_time
    }}
except FindFailed:
    result = {{
        "success": False,
        "clicked": False,
        "error": "Image not found on screen"
    }}
"""
        return await self.execute_script(script, timeout=timeout+5)
    
    async def type_text(self, text: str, target_image: Optional[str] = None) -> Dict[str, Any]:
        """
        Type text, optionally clicking on an image first
        
        Args:
            text: Text to type
            target_image: Optional image to click before typing
            
        Returns:
            Result with success status
        """
        # Escape special characters
        escaped_text = text.replace('"', '\\"')
        
        if target_image:
            script = f"""
from sikuli import *

# Click on target image
try:
    click(r"{target_image}")
    type("{escaped_text}")
    result = {{
        "success": True,
        "typed": True
    }}
except FindFailed:
    result = {{
        "success": False,
        "typed": False,
        "error": "Target image not found on screen"
    }}
"""
        else:
            script = f"""
from sikuli import *

# Type text
type("{escaped_text}")
result = {{
    "success": True,
    "typed": True
}}
"""
        return await self.execute_script(script)