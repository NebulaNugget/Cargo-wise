import logging
import asyncio
from typing import Dict, Any, Optional, List
from app.automation.streaming.vnc_server import VNCServer
from app.automation.streaming.novnc_integration import NoVNCProxy

logger = logging.getLogger(__name__)

class StreamManager:
    """
    Manages desktop streaming sessions for automation monitoring
    """
    
    def __init__(self):
        self.streams: Dict[str, Dict[str, Any]] = {}
        self.default_vnc_port = 5900
        self.default_web_port = 6080
        
    async def create_stream(self, 
                           stream_id: str, 
                           vnc_port: Optional[int] = None,
                           web_port: Optional[int] = None,
                           display_width: int = 1280,
                           display_height: int = 720) -> Dict[str, Any]:
        """Create a new streaming session"""
        if stream_id in self.streams:
            logger.warning(f"Stream {stream_id} already exists")
            return await self.get_stream_info(stream_id)
            
        # Find available ports if not specified
        if vnc_port is None:
            vnc_port = await self._find_available_vnc_port()
            
        if web_port is None:
            web_port = await self._find_available_web_port()
            
        # Create VNC server
        vnc_server = VNCServer(
            port=vnc_port,
            display_width=display_width,
            display_height=display_height
        )
        
        # Create noVNC proxy
        novnc_proxy = NoVNCProxy(
            vnc_port=vnc_port,
            web_port=web_port
        )
        
        # Store stream components
        self.streams[stream_id] = {
            "id": stream_id,
            "vnc_server": vnc_server,
            "novnc_proxy": novnc_proxy,
            "vnc_port": vnc_port,
            "web_port": web_port,
            "status": "created"
        }
        
        logger.info(f"Stream {stream_id} created with VNC port {vnc_port} and web port {web_port}")
        return await self.get_stream_info(stream_id)
        
    async def start_stream(self, stream_id: str) -> Dict[str, Any]:
        """Start a streaming session"""
        if stream_id not in self.streams:
            logger.error(f"Stream {stream_id} not found")
            return {"error": f"Stream {stream_id} not found"}
            
        stream = self.streams[stream_id]
        
        # Start VNC server
        vnc_success = await stream["vnc_server"].start()
        if not vnc_success:
            logger.error(f"Failed to start VNC server for stream {stream_id}")
            stream["status"] = "error"
            return await self.get_stream_info(stream_id)
            
        # Start noVNC proxy
        novnc_success = await stream["novnc_proxy"].start()
        if not novnc_success:
            logger.error(f"Failed to start noVNC proxy for stream {stream_id}")
            await stream["vnc_server"].stop()
            stream["status"] = "error"
            return await self.get_stream_info(stream_id)
            
        # Update status
        stream["status"] = "running"
        logger.info(f"Stream {stream_id} started successfully")
        return await self.get_stream_info(stream_id)
        
    async def stop_stream(self, stream_id: str) -> Dict[str, Any]:
        """Stop a streaming session"""
        if stream_id not in self.streams:
            logger.error(f"Stream {stream_id} not found")
            return {"error": f"Stream {stream_id} not found"}
            
        stream = self.streams[stream_id]
        
        # Stop noVNC proxy
        await stream["novnc_proxy"].stop()
        
        # Stop VNC server
        await stream["vnc_server"].stop()
        
        # Update status
        stream["status"] = "stopped"
        logger.info(f"Stream {stream_id} stopped")
        return await self.get_stream_info(stream_id)
        
    async def delete_stream(self, stream_id: str) -> Dict[str, Any]:
        """Delete a streaming session"""
        if stream_id not in self.streams:
            logger.error(f"Stream {stream_id} not found")
            return {"error": f"Stream {stream_id} not found"}
            
        # Stop the stream if it's running
        if self.streams[stream_id]["status"] == "running":
            await self.stop_stream(stream_id)
            
        # Get info before deletion
        info = await self.get_stream_info(stream_id)
        
        # Delete the stream
        del self.streams[stream_id]
        logger.info(f"Stream {stream_id} deleted")
        
        return {**info, "deleted": True}
        
    async def get_stream_info(self, stream_id: str) -> Dict[str, Any]:
        """Get information about a streaming session"""
        if stream_id not in self.streams:
            logger.error(f"Stream {stream_id} not found")
            return {"error": f"Stream {stream_id} not found"}
            
        stream = self.streams[stream_id]
        
        # Get status from components
        vnc_status = await stream["vnc_server"].get_status()
        novnc_status = await stream["novnc_proxy"].get_status()
        
        return {
            "id": stream_id,
            "status": stream["status"],
            "vnc_port": stream["vnc_port"],
            "web_port": stream["web_port"],
            "vnc_server": vnc_status,
            "novnc_proxy": novnc_status,
            "url": f"http://localhost:{stream['web_port']}/vnc.html?host=localhost&port={stream['web_port']}"
        }
        
    async def list_streams(self) -> List[Dict[str, Any]]:
        """List all streaming sessions"""
        result = []
        for stream_id in self.streams:
            info = await self.get_stream_info(stream_id)
            result.append(info)
        return result
        
    async def _find_available_vnc_port(self) -> int:
        """Find an available VNC port"""
        # Start from default port and increment until an available port is found
        port = self.default_vnc_port
        while any(stream["vnc_port"] == port for stream in self.streams.values()):
            port += 1
        return port
        
    async def _find_available_web_port(self) -> int:
        """Find an available web port"""
        # Start from default port and increment until an available port is found
        port = self.default_web_port
        while any(stream["web_port"] == port for stream in self.streams.values()):
            port += 1
        return port

# Singleton instance
_stream_manager = None

def get_stream_manager() -> StreamManager:
    """Get the stream manager singleton"""
    global _stream_manager
    if _stream_manager is None:
        _stream_manager = StreamManager()
    return _stream_manager