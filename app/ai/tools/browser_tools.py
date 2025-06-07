# Selenium-based browser automation tools
from app.ai.tools.base_tool import Marc1Tool, ToolNodeInput
from typing import Optional, Dict, Any, List
import logging
import base64
import sys
from pathlib import Path
import os
from datetime import datetime
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import Selenium components
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

# Thread pool for running Selenium operations
_thread_pool = ThreadPoolExecutor(max_workers=4)

class BrowserSessionManager:
    """Thread-safe browser session manager for Selenium automation"""
    _driver = None
    _initialized = False
    _lock = asyncio.Lock()

    @classmethod
    async def initialize(cls, headless: bool = False, force_new: bool = False):
        """Initialize browser session with Selenium WebDriver"""
        async with cls._lock:
            # Force new session if requested or if session is invalid
            if force_new and cls._driver:
                await cls.cleanup()
            if cls._initialized and not force_new:
                # Verify the session is still valid
                try:
                    if cls._driver:
                        # Simple operation to check if session is alive
                        await asyncio.get_event_loop().run_in_executor(
                            _thread_pool, lambda: cls._driver.current_url
                        )
                        return
                except Exception as e:
                    logger.warning(f"Existing session is invalid, creating new one: {str(e)}")
                    await cls.cleanup()

            try:
                logger.info(f"Initializing Selenium on {sys.platform}")
                
                # Run browser initialization in a separate thread
                def _init_browser():
                    # Configure Chrome options
                    chrome_options = Options()
                    if headless:
                        chrome_options.add_argument("--headless=new")
                    
                    # Common options for stability
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--disable-gpu")
                    chrome_options.add_argument("--window-size=1280,720")
                    chrome_options.add_argument("--disable-extensions")

                    # Use local ChromeDriver instead of downloading
                    chromedriver_path = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), 
                        "..", "..", "..", "drivers", "chromedriver.exe"
                    )
                    
                    # Create service with local ChromeDriver
                    service = Service(executable_path=chromedriver_path)

                    # # Install and setup ChromeDriver
                    # service = Service(ChromeDriverManager().install())
                    
                    # Create the WebDriver
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    driver.set_page_load_timeout(60)
                    driver.implicitly_wait(10)
                    
                    return driver
                
                # Run browser initialization in thread pool
                cls._driver = await asyncio.get_event_loop().run_in_executor(
                    _thread_pool, _init_browser
                )
                
                cls._initialized = True
                logger.info("Selenium browser session initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize Selenium: {str(e)}", exc_info=True)
                await cls.cleanup()
                raise

    @classmethod
    async def get_driver(cls):
        """Get WebDriver instance"""
        if not cls._initialized:
            await cls.initialize()
        # Verify session is valid before returning
        try:
            if cls._driver:
                # Check if session is still valid
                await asyncio.get_event_loop().run_in_executor(
                    _thread_pool, lambda: cls._driver.current_url
                )
        except Exception as e:
            logger.warning(f"Session validation failed, reinitializing: {str(e)}")
            await cls.initialize(force_new=True)
            
        return cls._driver
        
    @classmethod
    async def cleanup(cls):
        """Clean up browser session"""
        async with cls._lock:
            try:
                if cls._driver:
                    # Run quit in thread pool to avoid blocking
                    try:
                        await asyncio.get_event_loop().run_in_executor(
                            _thread_pool, cls._driver.quit
                        )
                    except Exception as e:
                        logger.warning(f"Error during driver quit: {str(e)}")
                    finally:
                        cls._driver = None
                    
                cls._initialized = False
                logger.info("Selenium browser session cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up Selenium: {str(e)}")
                cls._driver = None
                cls._initialized = False

    @classmethod
    async def capture_screenshot(cls, filename_prefix: str = "screenshot") -> Optional[str]:
        """Capture screenshot of current page"""
        try:
            driver = await cls.get_driver()
            if not driver:
                return None
            
            # Create screenshots directory
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            # Generate filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"{filename_prefix}_{timestamp}.png"
            
            # Capture screenshot (run in thread pool)
            def _take_screenshot():
                driver.save_screenshot(str(screenshot_path))
                
            await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _take_screenshot
            )
            
            # Convert to base64
            if screenshot_path.exists():
                with open(screenshot_path, "rb") as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            
            return None
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            return None


# Enhanced Browser Tools with Selenium
class BrowserNavigateTool(Marc1Tool):
    name = "browser_navigate"
    description = "Navigate to a specific URL in the browser"
    required_params = {"url": str}
    optional_params = {"wait_seconds": int, "retry_count": int}
    
    async def _execute(self, input: ToolNodeInput) -> Dict[str, Any]:
        parameters = self._get_parameters(input)
        url = parameters.get("url")
        wait_seconds = parameters.get("wait_seconds", 3)
        retry_count = parameters.get("retry_count", 2)
        
        if not url:
            return {
                "status": "ERROR",
                "outputs": {},
                "error": "URL parameter is required"
            }
            
        for attempt in range(retry_count + 1):
            try:
                # Initialize browser session with force_new on retries
                await BrowserSessionManager.initialize(force_new=(attempt > 0))
                driver = await BrowserSessionManager.get_driver()
                
                # Navigate to URL (run in thread pool)
                def _navigate():
                    driver.get(url)
                    # Wait for page to load
                    time.sleep(wait_seconds)
                    return {
                        "title": driver.title,
                        "url": driver.current_url
                    }
                
                result = await asyncio.get_event_loop().run_in_executor(
                    _thread_pool, _navigate
                )
                
                # Take screenshot
                screenshot_base64 = await BrowserSessionManager.capture_screenshot("navigate")
                
                return {
                    "status": "SUCCESS",
                    "outputs": {
                        "title": result["title"],
                        "url": result["url"],
                        "screenshot": screenshot_base64
                    }
                }
            except Exception as e:
                logger.error(f"Error navigating to {url} (attempt {attempt+1}/{retry_count+1}): {str(e)}", exc_info=True)
                
                # If this was our last attempt, return error
                if attempt == retry_count:
                    return {
                        "status": "ERROR",
                        "outputs": {},
                        "error": f"Failed to navigate: {str(e)}"
                    }
                
                # Otherwise wait a bit before retrying
                await asyncio.sleep(2)


class BrowserClickTool(Marc1Tool):
    name = "browser_click_element"
    description = "Click a DOM element using CSS selector"
    required_params = {"selector": str}
    optional_params = {"timeout": int, "text": str, "wait_seconds": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        parameters = self._get_parameters(input)
        selector = parameters.get("selector")
        timeout = parameters.get("timeout", 30)
        text = parameters.get("text")
        wait_seconds = parameters.get("wait_seconds", 1)
        
        try:
            # Initialize browser session
            await BrowserSessionManager.initialize()
            driver = await BrowserSessionManager.get_driver()
            
            # Interact with element (run in thread pool)
            def _interact_with_element():
                # Wait for element to be visible
                element = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Fill text if provided
                if text:
                    element.clear()
                    element.send_keys(text)
                    logger.info(f"Filled text '{text}' into {selector}")
                
                # Click the element
                element.click()
                
                # Wait a bit for any dynamic changes
                time.sleep(wait_seconds)
                
                logger.info(f"Clicked element {selector}")
                return True
            
            await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _interact_with_element
            )
            
            # Take screenshot
            screenshot_base64 = await BrowserSessionManager.capture_screenshot("click")
            
            return {
                "status": "SUCCESS",
                "outputs": {
                    "action": "click",
                    "selector": selector,
                    "text_filled": text is not None,
                    "screenshot": screenshot_base64
                }
            }
        except Exception as e:
            logger.error(f"Error interacting with element {selector}: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Element interaction failed: {str(e)}",
                "retryable": True
            }


class BrowserTypeTool(Marc1Tool):
    name = "browser_type_text"
    description = "Type text into an element"
    required_params = {"selector": str, "text": str}
    optional_params = {"timeout": int, "clear_first": bool}

    async def _execute(self, input: ToolNodeInput) -> dict:
        parameters = self._get_parameters(input)
        selector = parameters.get("selector")
        text = parameters.get("text")
        timeout = parameters.get("timeout", 30)
        clear_first = parameters.get("clear_first", True)
        
        try:
            # Initialize browser session
            await BrowserSessionManager.initialize()
            driver = await BrowserSessionManager.get_driver()
            
            # Type text (run in thread pool)
            def _type_text():
                # Wait for element to be visible
                element = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Clear existing text if requested
                if clear_first:
                    element.clear()
                
                # Type text
                element.send_keys(text)
                
                logger.info(f"Typed text into {selector}")
                return True
            
            await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _type_text
            )
            
            # Take screenshot
            screenshot_base64 = await BrowserSessionManager.capture_screenshot("type")
            
            return {
                "status": "SUCCESS",
                "outputs": {
                    "action": "type",
                    "selector": selector,
                    "text": text,
                    "screenshot": screenshot_base64
                }
            }
        except Exception as e:
            logger.error(f"Error typing into element {selector}: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Typing failed: {str(e)}"
            }


class BrowserGetTextTool(Marc1Tool):
    name = "browser_get_text"
    description = "Get text content from an element"  
    required_params = {"selector": str}
    optional_params = {"timeout": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        parameters = self._get_parameters(input)
        selector = parameters.get("selector")
        timeout = parameters.get("timeout", 30)
        
        try:
            # Initialize browser session
            await BrowserSessionManager.initialize()
            driver = await BrowserSessionManager.get_driver()
            
            # Get text content (run in thread pool)
            def _get_text():
                # Wait for element to be visible
                element = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Get text content
                text = element.text
                
                logger.info(f"Retrieved text from {selector}")
                return text
            
            text = await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _get_text
            )
            
            # Take screenshot
            screenshot_base64 = await BrowserSessionManager.capture_screenshot("get_text")
            
            return {
                "status": "SUCCESS",
                "outputs": {
                    "action": "get_text",
                    "selector": selector,
                    "text": text,
                    "screenshot": screenshot_base64
                }
            }
        except Exception as e:
            logger.error(f"Error getting text from element {selector}: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Getting text failed: {str(e)}"
            }


class BrowserWaitTool(Marc1Tool):
    name = "browser_wait_for_element"
    description = "Wait for an element to be in a specific state"
    required_params = {"selector": str}
    optional_params = {"state": str, "timeout": int}

    async def _execute(self, input: ToolNodeInput) -> dict:
        parameters = self._get_parameters(input)
        selector = parameters.get("selector")
        state = parameters.get("state", "visible")
        timeout = parameters.get("timeout", 30)
        
        try:
            # Initialize browser session
            await BrowserSessionManager.initialize()
            driver = await BrowserSessionManager.get_driver()
            
            # Wait for element (run in thread pool)
            def _wait_for_element():
                if state == "visible":
                    WebDriverWait(driver, timeout).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                elif state == "clickable":
                    WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                elif state == "present":
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                elif state == "invisible":
                    WebDriverWait(driver, timeout).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                
                logger.info(f"Element {selector} is now {state}")
                return True
            
            await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _wait_for_element
            )
            
            # Take screenshot
            screenshot_base64 = await BrowserSessionManager.capture_screenshot("wait")
            
            return {
                "status": "SUCCESS",
                "outputs": {
                    "action": "wait",
                    "selector": selector,
                    "state": state,
                    "screenshot": screenshot_base64
                }
            }
        except Exception as e:
            logger.error(f"Error waiting for element {selector}: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Wait failed: {str(e)}"
            }


class BrowserExecuteScriptTool(Marc1Tool):
    name = "browser_execute_script"
    description = "Execute JavaScript in the browser"
    required_params = {"script": str}

    async def _execute(self, input: ToolNodeInput) -> dict:
        parameters = self._get_parameters(input)
        script = parameters.get("script")
        
        try:
            # Initialize browser session
            await BrowserSessionManager.initialize()
            driver = await BrowserSessionManager.get_driver()
            
            # Execute script (run in thread pool)
            def _execute_script():
                result = driver.execute_script(script)
                logger.info("Executed JavaScript script")
                return result
            
            result = await asyncio.get_event_loop().run_in_executor(
                _thread_pool, _execute_script
            )
            
            # Take screenshot
            screenshot_base64 = await BrowserSessionManager.capture_screenshot("script")
            
            return {
                "status": "SUCCESS",
                "outputs": {
                    "action": "execute_script",
                    "result": str(result),
                    "screenshot": screenshot_base64
                }
            }
        except Exception as e:
            logger.error(f"Error executing script: {str(e)}", exc_info=True)
            return {
                "status": "ERROR",
                "outputs": {},
                "error": f"Script execution failed: {str(e)}"
            }


# Cleanup function for FastAPI shutdown
async def cleanup_browser_session():
    """Call this during FastAPI shutdown"""
    await BrowserSessionManager.cleanup()