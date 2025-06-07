import os
import subprocess
import socket
import time
import logging
import platform
import signal
from typing import Optional, Dict, Any
import psutil

logger = logging.getLogger(__name__)

class VNCServer:
    """
    Manages a VNC server instance for desktop streaming
    """
    
    def __init__(self, 
                 port: int = 5900, 
                 display_width: int = 1280, 
                 display_height: int = 720,
                 framerate: int = 15):
        self.port = port
        self.display_width = display_width
        self.display_height = display_height
        self.framerate = framerate
        self.process: Optional[subprocess.Popen] = None
        self.display_num = port - 5900  # VNC display number convention
        self.running = False
        
    async def start(self) -> bool:
        """Start the VNC server"""
        if self.running:
            logger.info("VNC server already running")
            return True
            
        try:
            # Check if port is available
            if not self._is_port_available(self.port):
                logger.error(f"Port {self.port} is already in use")
                return False
                
            # Start TightVNC server (Windows) or x11vnc (Linux)
            if platform.system() == "Windows":
                return await self._start_windows_vnc()
            else:
                return await self._start_linux_vnc()
                
        except Exception as e:
            logger.exception(f"Failed to start VNC server: {str(e)}")
            return False
            
    async def _start_windows_vnc(self) -> bool:
        """Start TightVNC server on Windows"""
        try:
            # Path to TightVNC server executable
            tvnserver_path = os.environ.get("TVNSERVER_PATH", r"C:\Program Files\TightVNC\tvnserver.exe")
            
            if not os.path.exists(tvnserver_path):
                logger.error(f"TightVNC server not found at {tvnserver_path}")
                return False
                
            # Start TightVNC with specific settings
            cmd = [
                tvnserver_path,
                "-controlservice",
                "-startservice"
            ]
            
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Configure the server
            config_cmd = [
                tvnserver_path,
                "-controlservice",
                "-configure",
                "-rfbport", str(self.port),
                "-disconnectclients", "1"
            ]
            
            subprocess.run(
                config_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.running = True
            logger.info(f"TightVNC server started on port {self.port}")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to start TightVNC server: {str(e)}")
            return False
            
    async def _start_linux_vnc(self) -> bool:
        """Start x11vnc server on Linux"""
        try:
            # Start x11vnc
            cmd = [
                "x11vnc",
                "-display", f":{self.display_num}",
                "-rfbport", str(self.port),
                "-geometry", f"{self.display_width}x{self.display_height}",
                "-shared",
                "-forever",
                "-bg"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Check if process is running
            if self.process.poll() is not None:
                stderr = self.process.stderr.read().decode('utf-8')
                logger.error(f"x11vnc failed to start: {stderr}")
                return False
                
            self.running = True
            logger.info(f"x11vnc server started on port {self.port}")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to start x11vnc server: {str(e)}")
            return False
    
    async def stop(self) -> bool:
        """Stop the VNC server"""
        if not self.running:
            logger.info("VNC server not running")
            return True
            
        try:
            if platform.system() == "Windows":
                return await self._stop_windows_vnc()
            else:
                return await self._stop_linux_vnc()
                
        except Exception as e:
            logger.exception(f"Failed to stop VNC server: {str(e)}")
            return False
            
    async def _stop_windows_vnc(self) -> bool:
        """Stop TightVNC server on Windows"""
        try:
            # Path to TightVNC server executable
            tvnserver_path = os.environ.get("TVNSERVER_PATH", r"C:\Program Files\TightVNC\tvnserver.exe")
            
            # Stop TightVNC service
            cmd = [
                tvnserver_path,
                "-controlservice",
                "-stopservice"
            ]
            
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.running = False
            logger.info("TightVNC server stopped")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to stop TightVNC server: {str(e)}")
            return False
            
    async def _stop_linux_vnc(self) -> bool:
        """Stop x11vnc server on Linux"""
        try:
            # Find and kill x11vnc processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['name'] == 'x11vnc' and any(f"-rfbport {self.port}" in ' '.join(cmd) for cmd in [proc.info['cmdline']]):
                    os.kill(proc.info['pid'], signal.SIGTERM)
                    
            self.running = False
            logger.info("x11vnc server stopped")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to stop x11vnc server: {str(e)}")
            return False
    
    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0
            
    async def get_status(self) -> Dict[str, Any]:
        """Get the current status of the VNC server"""
        return {
            "running": self.running,
            "port": self.port,
            "display": self.display_num,
            "resolution": f"{self.display_width}x{self.display_height}"
        }