# Playwright driver for web automation
import asyncio
import base64
import logging
import os
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import uuid

logger = logging.getLogger(__name__)

class PlaywrightDriver:
    """
    Driver for Playwright web automation
    
    This class provides an interface to Playwright for web automation tasks.
    It handles browser control, screenshot capture, and result parsing.
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize Playwright driver
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        
        # Create screenshots directory if it doesn't exist
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
    
    async def start(self):
        """Start browser session"""
        try:
            # Import here to avoid startup delay
            from playwright.async_api import async_playwright
            
            # Start Playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            
            # Create context
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 720},
                accept_downloads=True
            )
            
            # Create page
            self.page = await self.context.new_page()
            
            # Set default timeout
            self.page.set_default_timeout(30000)  # 30 seconds
            
            logger.info("Playwright browser session started")
            return True
            
        except Exception as e:
            logger.error(f"Error starting Playwright: {str(e)}")
            return False
    
    async def stop(self):
        """Stop browser session"""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            
            logger.info("Playwright browser session stopped")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping Playwright: {str(e)}")
            return False
    
    async def navigate(self, url: str, wait_until: str = "load") -> Dict[str, Any]:
        """
        Navigate to a URL
        
        Args:
            url: URL to navigate to
            wait_until: When to consider navigation complete
                        (load, domcontentloaded, networkidle)
            
        Returns:
            Result with success status
        """
        try:
            if not self.page:
                await self.start()
            
            # Navigate to URL
            response = await self.page.goto(url, wait_until=wait_until)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "url": self.page.url,
                "status": response.status if response else None,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error navigating to {url}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def click(self, selector: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Click on an element
        
        Args:
            selector: CSS or XPath selector
            timeout: Timeout in milliseconds
            
        Returns:
            Result with success status
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element to be visible
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Click element
            await self.page.click(selector)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "clicked": True,
                "selector": selector,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error clicking element {selector}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def type_text(self, selector: str, text: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Type text into an element
        
        Args:
            selector: CSS or XPath selector
            text: Text to type
            timeout: Timeout in milliseconds
            
        Returns:
            Result with success status
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element to be visible
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Clear existing text
            await self.page.fill(selector, "")
            
            # Type text
            await self.page.fill(selector, text)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "typed": True,
                "selector": selector,
                "text": text,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error typing text into element {selector}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_text(self, selector: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Get text from an element
        
        Args:
            selector: CSS or XPath selector
            timeout: Timeout in milliseconds
            
        Returns:
            Result with text content
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element to be visible
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Get text
            text = await self.page.text_content(selector)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "text": text,
                "selector": selector,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting text from element {selector}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = 30000) -> Dict[str, Any]:
        """
        Wait for an element to be in a specific state
        
        Args:
            selector: CSS or XPath selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Timeout in milliseconds
            
        Returns:
            Result with success status
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element
            await self.page.wait_for_selector(selector, state=state, timeout=timeout)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "selector": selector,
                "state": state,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error waiting for element {selector}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def execute_script(self, script: str) -> Dict[str, Any]:
        """
        Execute JavaScript in the browser
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Result with script return value
        """
        try:
            if not self.page:
                await self.start()
            
            # Execute script
            result = await self.page.evaluate(script)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "result": result,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error executing script: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _capture_screenshot(self) -> Optional[str]:
        """Capture screenshot of page"""
        try:
            if not self.page:
                return None
            
            # Generate screenshot filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshots_dir, f"screenshot_{timestamp}.png")
            
            # Capture screenshot
            await self.page.screenshot(path=screenshot_path)
            
            # Read screenshot file
            with open(screenshot_path, "rb") as f:
                screenshot_data = f.read()
            
            # Return base64 encoded screenshot
            return base64.b64encode(screenshot_data).decode("utf-8")
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            return None
    
    async def find_element(self, selector: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Find an element on the page
        
        Args:
            selector: CSS or XPath selector
            timeout: Timeout in milliseconds
            
        Returns:
            Result with element properties
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element to be visible
            element = await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            if not element:
                return {
                    "success": False,
                    "found": False,
                    "error": "Element not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Get element properties
            properties = await element.evaluate("""
                element => {
                    const rect = element.getBoundingClientRect();
                    return {
                        tagName: element.tagName,
                        text: element.textContent,
                        value: element.value,
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height,
                        isVisible: element.checkVisibility()
                    };
                }
            """)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "found": True,
                "selector": selector,
                "properties": properties,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error finding element {selector}: {str(e)}")
            return {
                "success": False,
                "found": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def select_option(self, selector: str, value: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Select an option from a dropdown
        
        Args:
            selector: CSS or XPath selector
            value: Option value to select
            timeout: Timeout in milliseconds
            
        Returns:
            Result with success status
        """
        try:
            if not self.page:
                await self.start()
            
            # Wait for element to be visible
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Select option
            await self.page.select_option(selector, value)
            
            # Capture screenshot
            screenshot = await self._capture_screenshot()
            
            return {
                "success": True,
                "selected": True,
                "selector": selector,
                "value": value,
                "screenshot": screenshot,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error selecting option {value} from {selector}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }