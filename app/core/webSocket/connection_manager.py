# WebSocket connection manager
from fastapi import WebSocket
from typing import Dict, List, Any, Set
import logging
import asyncio

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Manages WebSocket connections
    
    This class handles WebSocket connections, including connection tracking,
    broadcasting messages, and client data storage.
    """
    
    def __init__(self):
        """Initialize connection manager"""
        # Map of group -> set of connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        # Map of connection -> client data
        self.client_data: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, group: str):
        """
        Connect a WebSocket to a group
        
        Args:
            websocket: The WebSocket connection
            group: The group to connect to
        """
        # Accept the connection
        await websocket.accept()
        
        # Add to group
        if group not in self.active_connections:
            self.active_connections[group] = set()
        self.active_connections[group].add(websocket)
        
        # Initialize client data
        self.client_data[websocket] = {"group": group}
        
        logger.debug(f"WebSocket connected to group {group}")
    
    async def disconnect(self, websocket: WebSocket, group: str):
        """
        Disconnect a WebSocket from a group
        
        Args:
            websocket: The WebSocket connection
            group: The group to disconnect from
        """
        # Remove from group
        if group in self.active_connections:
            self.active_connections[group].discard(websocket)
            if not self.active_connections[group]:
                del self.active_connections[group]
        
        # Remove client data
        if websocket in self.client_data:
            del self.client_data[websocket]
        
        logger.debug(f"WebSocket disconnected from group {group}")
    
    async def broadcast(self, group: str, message: Dict[str, Any]):
        """
        Broadcast a message to all connections in a group
        
        Args:
            group: The group to broadcast to
            message: The message to broadcast
        """
        if group not in self.active_connections:
            return
        
        # Send to all connections in group
        disconnected = set()
        for connection in self.active_connections[group]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {str(e)}")
                disconnected.add(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            await self.disconnect(connection, group)
    
    async def broadcast_filtered(self, message: Dict[str, Any], filter_func=None):
        """
        Broadcast a message to connections that match a filter
        
        Args:
            message: The message to broadcast
            filter_func: Function that takes (connection, client_data) and returns bool
        """
        # Default filter accepts all connections
        if filter_func is None:
            filter_func = lambda conn, data: True
        
        # Send to all connections that match filter
        disconnected = set()
        for connection, data in self.client_data.items():
            if filter_func(connection, data):
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to WebSocket: {str(e)}")
                    disconnected.add(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            group = self.client_data.get(connection, {}).get("group")
            if group:
                await self.disconnect(connection, group)
    
    def set_client_data(self, websocket: WebSocket, key: str, value: Any):
        """
        Set client data for a connection
        
        Args:
            websocket: The WebSocket connection
            key: The data key
            value: The data value
        """
        if websocket in self.client_data:
            self.client_data[websocket][key] = value
    
    def get_client_data(self, websocket: WebSocket, key: str, default=None) -> Any:
        """
        Get client data for a connection
        
        Args:
            websocket: The WebSocket connection
            key: The data key
            default: Default value if key not found
            
        Returns:
            The client data value
        """
        if websocket in self.client_data:
            return self.client_data[websocket].get(key, default)
        return default
    
    def get_connections_in_group(self, group: str) -> Set[WebSocket]:
        """
        Get all connections in a group
        
        Args:
            group: The group name
            
        Returns:
            Set of WebSocket connections
        """
        return self.active_connections.get(group, set())
    
    def get_connection_count(self, group: str = None) -> int:
        """
        Get connection count
        
        Args:
            group: Optional group to count connections for
            
        Returns:
            Number of connections
        """
        if group:
            return len(self.active_connections.get(group, set()))
        else:
            return sum(len(connections) for connections in self.active_connections.values())