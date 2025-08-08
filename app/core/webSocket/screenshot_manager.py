import asyncio
import base64
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, Optional, Any

import aiofiles
from fastapi import WebSocket, WebSocketDisconnect
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

# Dictionary to store active WebSocket connections by user_id and task_id
active_connections: Dict[str, Dict[str, WebSocket]] = {}
# Dictionary to store task_id to user_id mappings
task_user_mappings: Dict[str, str] = {}
# Dictionary to store the last screenshot sent for each task
last_screenshot_sent: Dict[str, str] = {}

class ScreenshotEventHandler(FileSystemEventHandler):
    """Watchdog event handler for screenshot directory"""
    
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Extract task_id from path
            path = Path(event.src_path)
            # The parent directory name should be the task_id
            task_id = path.parent.name
            
            # Check if this is a task screenshot directory
            if task_id and task_id in task_user_mappings:
                logger.info(f"New screenshot detected for task {task_id}: {path.name}")
                # Schedule the broadcast in the event loop
                asyncio.run_coroutine_threadsafe(
                    broadcast_screenshot(task_id, str(path)), 
                    self.loop
                )


class ScreenshotManager:
    """Manager for screenshot directory watching and WebSocket broadcasting"""
    
    _instance = None
    _initialized = False
    _observer = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._screenshot_dir = Path("C:/Users/UK-PC/Desktop/AI driven cargo-wise automation framework/cargowise-ai-backend/screenshots")
        self._screenshot_dir.mkdir(exist_ok=True)
        self._event_handler = ScreenshotEventHandler()
        
    def start_watching(self):
        """Start watching the screenshot directory for changes"""
        if self._observer is None:
            logger.info(f"Starting screenshot directory watcher on {self._screenshot_dir}")
            self._observer = Observer()
            self._observer.schedule(
                self._event_handler, 
                str(self._screenshot_dir), 
                recursive=True
            )
            self._observer.start()
            logger.info("Screenshot directory watcher started")
        
    def stop_watching(self):
        """Stop watching the screenshot directory"""
        if self._observer is not None:
            logger.info("Stopping screenshot directory watcher")
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Screenshot directory watcher stopped")


async def connect_client(websocket: WebSocket, user_id: str, task_id: Optional[str] = None):
    """Connect a client to the WebSocket manager"""
    await websocket.accept()
    
    # Store connection by user_id
    if user_id not in active_connections:
        active_connections[user_id] = {}
    
    # If task_id is provided, associate this connection with the task
    if task_id:
        active_connections[user_id][task_id] = websocket
        task_user_mappings[task_id] = user_id
        logger.info(f"Client connected: user_id={user_id}, task_id={task_id}")
        
        # Send any existing screenshots for this task
        await send_existing_screenshots(websocket, task_id)
    else:
        # This is a user-level connection (not task-specific)
        active_connections[user_id]["_general"] = websocket
        logger.info(f"Client connected: user_id={user_id} (general connection)")


async def disconnect_client(user_id: str, task_id: Optional[str] = None):
    """Disconnect a client from the WebSocket manager"""
    if user_id in active_connections:
        if task_id and task_id in active_connections[user_id]:
            # Remove specific task connection
            del active_connections[user_id][task_id]
            logger.info(f"Client disconnected: user_id={user_id}, task_id={task_id}")
            
            # Remove task mapping if this was the last connection for this task
            if task_id in task_user_mappings and task_user_mappings[task_id] == user_id:
                del task_user_mappings[task_id]
        elif task_id is None and "_general" in active_connections[user_id]:
            # Remove general connection
            del active_connections[user_id]["_general"]
            logger.info(f"Client disconnected: user_id={user_id} (general connection)")
        
        # Clean up empty user entries
        if not active_connections[user_id]:
            del active_connections[user_id]


async def send_existing_screenshots(websocket: WebSocket, task_id: str):
    """Send existing screenshots for a task to a newly connected client"""
    screenshot_dir = Path("C:/Users/UK-PC/Desktop/AI driven cargo-wise automation framework/cargowise-ai-backend/screenshots")
    
    if not screenshot_dir.exists():
        logger.info(f"No screenshot directory found for task {task_id}")
        return
    
    # Get all PNG files in the directory
    png_files = sorted(
        [f for f in screenshot_dir.glob("*.png")],
        key=lambda f: f.stat().st_mtime
    )
    
    if not png_files:
        logger.info(f"No screenshots found for task {task_id}")
        return
    
    # Send the most recent screenshot
    latest_screenshot = png_files[-1]
    logger.info(f"Sending existing screenshot to new client: {latest_screenshot.name}")
    
    try:
        await send_screenshot_to_client(websocket, task_id, str(latest_screenshot))
        # Update last screenshot sent
        last_screenshot_sent[task_id] = str(latest_screenshot)
    except Exception as e:
        logger.error(f"Error sending existing screenshot: {str(e)}")


async def broadcast_screenshot(task_id: str, screenshot_path: str):
    """Broadcast a screenshot to all clients connected to a task"""
    # Check if this screenshot was already sent
    if task_id in last_screenshot_sent and last_screenshot_sent[task_id] == screenshot_path:
        logger.debug(f"Screenshot already sent: {screenshot_path}")
        return
    
    # Update last screenshot sent
    last_screenshot_sent[task_id] = screenshot_path
    
    # Get user_id for this task
    user_id = task_user_mappings.get(task_id)
    if not user_id:
        logger.warning(f"No user mapped for task {task_id}")
        return
    
    # Check if user has active connections
    if user_id not in active_connections:
        logger.warning(f"No active connections for user {user_id}")
        return
    
    # Send to task-specific connection if it exists
    if task_id in active_connections[user_id]:
        websocket = active_connections[user_id][task_id]
        try:
            await send_screenshot_to_client(websocket, task_id, screenshot_path)
            logger.info(f"Screenshot broadcast to task-specific client: {screenshot_path}")
        except Exception as e:
            logger.error(f"Error broadcasting to task-specific client: {str(e)}")
            # Connection might be closed, remove it
            await disconnect_client(user_id, task_id)
    
    # Also send to general connection if it exists
    if "_general" in active_connections[user_id]:
        websocket = active_connections[user_id]["_general"]
        try:
            await send_screenshot_to_client(websocket, task_id, screenshot_path)
            logger.info(f"Screenshot broadcast to general client: {screenshot_path}")
        except Exception as e:
            logger.error(f"Error broadcasting to general client: {str(e)}")
            # Connection might be closed, remove it
            await disconnect_client(user_id)


async def send_screenshot_to_client(websocket: WebSocket, task_id: str, screenshot_path: str):
    """Send a screenshot to a specific client"""
    try:
        # Read the screenshot file
        async with aiofiles.open(screenshot_path, "rb") as f:
            image_data = await f.read()
        
        # Encode as base64
        base64_image = base64.b64encode(image_data).decode("utf-8")
        
        # Create message with metadata
        message = {
            "type": "screenshot",
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "filename": Path(screenshot_path).name,
            "data": base64_image
        }
        
        # Send to client
        await websocket.send_text(json.dumps(message))
        
    except Exception as e:
        logger.error(f"Error sending screenshot to client: {str(e)}")
        raise


def register_task(task_id: str, user_id: str):
    """Register a task with a user for screenshot broadcasting"""
    task_user_mappings[task_id] = user_id
    logger.info(f"Task {task_id} registered for user {user_id}")


# Initialize and start the screenshot watcher
def initialize_screenshot_watcher():
    """Initialize and start the screenshot directory watcher"""
    manager = ScreenshotManager.get_instance()
    manager.start_watching()
    logger.info("Screenshot watcher initialized")
    return manager


