import os
import subprocess
import logging
import platform
import signal
import time
import psutil
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class NoVNCProxy:
    """
    Manages a noVNC websocket proxy for browser-based VNC access
    """
    
    def __init__(self, 
                 vnc_host: str = "localhost", 
                 vnc_port: int = 5900,
                 web_port: int = 6080,
                 novnc_path: Optional[str] = None):
        self.vnc_host = vnc_host
        self.vnc_port = vnc_port
        self.web_port = web_port
        self.process: Optional[subprocess.Popen] = None
        self.running = False
        
        # Set default noVNC path if not provided
        if novnc_path is None:
            if platform.system() == "Windows":
                self.novnc_path = os.environ.get(
                    "NOVNC_PATH", 
                    os.path.join(os.getcwd(), "app", "resources", "novnc")
                )
            else:
                self.novnc_path = os.environ.get(
                    "NOVNC_PATH", 
                    "/usr/share/novnc"
                )
        else:
            self.novnc_path = novnc_path
            
    async def start(self) -> bool:
        """Start the noVNC websocket proxy"""
        if self.running:
            logger.info("noVNC proxy already running")
            return True
            
        try:
            # Check if noVNC is installed
            websockify_path = self._get_websockify_path()
            if not websockify_path:
                logger.error("websockify not found")
                return False
                
            # Start websockify
            cmd = [
                websockify_path,
                "--web", os.path.join(self.novnc_path, ""),
                f"{self.web_port}",
                f"{self.vnc_host}:{self.vnc_port}"
            ]
            
            if platform.system() == "Windows":
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
            # Wait for proxy to start
            time.sleep(2)
            
            # Check if process is running
            if self.process.poll() is not None:
                stderr = self.process.stderr.read().decode('utf-8')
                logger.error(f"noVNC proxy failed to start: {stderr}")
                return False
                
            self.running = True
            logger.info(f"noVNC proxy started on port {self.web_port}")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to start noVNC proxy: {str(e)}")
            return False
            
    def _get_websockify_path(self) -> Optional[str]:
        """Get the path to the websockify executable"""
        if platform.system() == "Windows":
            # Check for Python script
            websockify_path = os.path.join(self.novnc_path, "utils", "websockify", "run")
            if os.path.exists(websockify_path):
                return f"python {websockify_path}"
                
            # Check for executable
            websockify_exe = os.path.join(self.novnc_path, "utils", "websockify", "websockify.exe")
            if os.path.exists(websockify_exe):
                return websockify_exe
                
            # Try to find in PATH
            try:
                subprocess.run(["where", "websockify"], check=True, capture_output=True)
                return "websockify"
            except subprocess.CalledProcessError:
                return None
        else:
            # Check for Python script
            websockify_path = os.path.join(self.novnc_path, "utils", "websockify", "run")
            if os.path.exists(websockify_path):
                return websockify_path
                
            # Try to find in PATH
            try:
                subprocess.run(["which", "websockify"], check=True, capture_output=True)
                return "websockify"
            except subprocess.CalledProcessError:
                return None
    
    async def stop(self) -> bool:
        """Stop the noVNC websocket proxy"""
        if not self.running:
            logger.info("noVNC proxy not running")
            return True
            
        try:
            if platform.system() == "Windows":
                # On Windows, terminate the process
                if self.process:
                    self.process.terminate()
                    self.process.wait(timeout=5)
            else:
                # On Linux, find and kill websockify processes
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    if (proc.info['name'] == 'websockify' or 
                        (proc.info['name'] == 'python' and 
                         any('websockify' in cmd for cmd in proc.info['cmdline']))):
                        if any(str(self.web_port) in cmd for cmd in proc.info['cmdline']):
                            os.kill(proc.info['pid'], signal.SIGTERM)
                            
            self.running = False
            logger.info("noVNC proxy stopped")
            return True
            
        except Exception as e:
            logger.exception(f"Failed to stop noVNC proxy: {str(e)}")
            return False
            
    async def get_status(self) -> Dict[str, Any]:
        """Get the current status of the noVNC proxy"""
        return {
            "running": self.running,
            "vnc_host": self.vnc_host,
            "vnc_port": self.vnc_port,
            "web_port": self.web_port,
            "url": f"http://localhost:{self.web_port}/vnc.html?host=localhost&port={self.web_port}"
        }