# Real-time log streaming endpoints
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.dependencies import get_db
from app.db.repositories.task_repository import TaskRepository
from app.core.webSocket.connection_manager import ConnectionManager
from typing import Dict, Any, List
import logging
import json
import asyncio
from app.models.task import TaskStatus

logger = logging.getLogger(__name__)
router = APIRouter()

# WebSocket connection manager
connection_manager = ConnectionManager()

# Dictionary to store active connections for task status updates
active_connections = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    General WebSocket endpoint for client connections
    
    This endpoint provides a basic WebSocket connection for general updates
    and system notifications.
    """
    # Accept the WebSocket connection
    await websocket.accept()
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection_established",
            "message": "Connected to MARC-1 WebSocket server"
        })
        
        # Keep connection open and handle client messages
        while True:
            # Wait for client message
            data = await websocket.receive_text()
            
            # Parse message
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    })
                else:
                    # Echo back the message for now
                    await websocket.send_json({
                        "type": "echo",
                        "data": message
                    })
            except json.JSONDecodeError:
                # Invalid JSON
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON message"
                })
            except Exception as e:
                # Other error
                logger.error(f"Error handling WebSocket message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
    
    except WebSocketDisconnect:
        # Client disconnected
        logger.info("WebSocket client disconnected")
    except Exception as e:
        # Other error
        logger.error(f"WebSocket error: {str(e)}")

@router.websocket("/task/{task_id}")
async def task_stream(websocket: WebSocket, task_id: str, db=Depends(get_db)):
    """
    WebSocket endpoint for real-time task updates
    
    This endpoint provides a WebSocket connection for streaming real-time
    updates about a specific task, including logs, status changes, and
    execution progress.
    """
    # Accept the WebSocket connection
    await connection_manager.connect(websocket, task_id)
    
    try:
        # Create task repository
        task_repo = TaskRepository(db)
        
        # Get initial task state
        task = await task_repo.get_task(task_id)
        if not task:
            await websocket.send_json({
                "type": "error",
                "message": f"Task {task_id} not found"
            })
            await connection_manager.disconnect(websocket, task_id)
            return
        
        # Send initial task state
        await websocket.send_json({
            "type": "task_state",
            "data": task.dict()
        })
        
        # Keep connection open and handle client messages
        while True:
            # Wait for client message
            data = await websocket.receive_text()
            
            # Parse message
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    })
                elif message.get("type") == "get_task":
                    # Get latest task state
                    task = await task_repo.get_task(task_id)
                    await websocket.send_json({
                        "type": "task_state",
                        "data": task.dict()
                    })
                elif message.get("type") == "get_logs":
                    # Get task logs
                    from app.db.repositories.log_repository import LogRepository
                    log_repo = LogRepository(db)
                    
                    # Get parameters
                    limit = message.get("limit", 100)
                    offset = message.get("offset", 0)
                    
                    # Get logs
                    logs = await log_repo.get_logs({"task_id": task_id}, limit, offset)
                    
                    # Send logs
                    await websocket.send_json({
                        "type": "logs",
                        "data": [log.dict() for log in logs]
                    })
                else:
                    # Unknown message type
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message.get('type')}"
                    })
            except json.JSONDecodeError:
                # Invalid JSON
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON message"
                })
            except Exception as e:
                # Other error
                logger.error(f"Error handling WebSocket message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
    
    except WebSocketDisconnect:
        # Client disconnected
        await connection_manager.disconnect(websocket, task_id)
    except Exception as e:
        # Other error
        logger.error(f"WebSocket error: {str(e)}")
        await connection_manager.disconnect(websocket, task_id)

@router.websocket("/task-status/{task_id}")
async def task_status_stream(websocket: WebSocket, task_id: str, db=Depends(get_db)):
    """Stream task status updates via WebSocket"""
    await websocket.accept()
    
    task_repo = TaskRepository(db)
    task = await task_repo.get_task(task_id)
    
    if not task:
        await websocket.send_json({"error": "Task not found"})
        await websocket.close()
        return
    
    # Send initial state
    await websocket.send_json({
        "type": "task_state",
        "data": task.current_state.dict()
    })
    
    # Set up subscription to task updates
    queue = asyncio.Queue()
    
    # Register this connection
    if task_id not in active_connections:
        active_connections[task_id] = []
    active_connections[task_id].append(queue)
    
    try:
        # Keep connection open and stream updates
        while True:
            # Wait for updates
            update = await queue.get()
            
            # Check for completion or failure
            if update.get("status") in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                # Send completion notification with summary
                if update.get("status") == TaskStatus.COMPLETED:
                    summary = update.get("metadata", {}).get("completion_summary", {})
                    message = "Task completed successfully"
                else:
                    summary = update.get("metadata", {}).get("failure_summary", {})
                    message = f"Task failed: {update.get('errors', ['Unknown error'])[0]}"
                
                await websocket.send_json({
                    "type": "task_completion",
                    "data": {
                        "status": update.get("status"),
                        "message": message,
                        "summary": summary,
                        "outputs": update.get("outputs", {}),
                        "errors": update.get("errors", [])
                    }
                })
            
            # Send regular update
            await websocket.send_json({
                "type": "task_state",
                "data": update
            })
            
            # If task is completed or failed, close the connection after sending the update
            if update.get("status") in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                await websocket.close()
                break
    
    except WebSocketDisconnect:
        # Clean up when client disconnects
        if task_id in active_connections and queue in active_connections[task_id]:
            active_connections[task_id].remove(queue)
            if not active_connections[task_id]:
                del active_connections[task_id]

@router.websocket("/logs")
async def logs_stream(websocket: WebSocket, db=Depends(get_db)):
    """
    WebSocket endpoint for real-time log streaming
    
    This endpoint provides a WebSocket connection for streaming real-time
    system logs, with optional filtering.
    """
    # Accept the WebSocket connection
    await connection_manager.connect(websocket, "logs")
    
    try:
        # Keep connection open and handle client messages
        while True:
            # Wait for client message
            data = await websocket.receive_text()
            
            # Parse message
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    })
                elif message.get("type") == "subscribe":
                    # Subscribe to log filters
                    filters = message.get("filters", {})
                    
                    # Store filters in connection manager
                    connection_manager.set_client_data(websocket, "log_filters", filters)
                    
                    # Acknowledge subscription
                    await websocket.send_json({
                        "type": "subscription_ack",
                        "filters": filters
                    })
                else:
                    # Unknown message type
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message.get('type')}"
                    })
            except json.JSONDecodeError:
                # Invalid JSON
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON message"
                })
            except Exception as e:
                # Other error
                logger.error(f"Error handling WebSocket message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
    
    except WebSocketDisconnect:
        # Client disconnected
        await connection_manager.disconnect(websocket, "logs")
    except Exception as e:
        # Other error
        logger.error(f"WebSocket error: {str(e)}")
        await connection_manager.disconnect(websocket, "logs")