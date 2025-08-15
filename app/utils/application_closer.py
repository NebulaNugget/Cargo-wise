import psutil
import subprocess
import os
import time
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import logging
load_dotenv()
logger = logging.getLogger(__name__)

class ApplicationCloser:
    def __init__(self, app_path: str = None):
        """
        Initialize the ApplicationCloser with the CargoWise application path.
        
        Args:
            app_path (str): Path to the CargoWise application executable
        """
        self.app_path= app_path or os.getenv('CARGOWISE_APP_PATH' ,r"C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe")
        #self.app_path = app_path or r"C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe"
        # Expanded list of process names to catch all CargoWise/WiseCloud processes
        self.process_names = [
            "WiseCloudClient.exe", 
            "CargoWise.exe", 
            "WiseCloud.exe",
            "WiseTech.exe",
            "wisecloud.exe",
            "cargowise.exe",
            "wisetech.exe"
        ]
        # Also check for processes containing these keywords
        self.process_keywords = ["wise", "cargo", "wisetech", "wisecloud"]
    
    def is_application_running(self) -> Dict[str, Any]:
        """
        Check if CargoWise application is currently running.
        
        Returns:
            Dict containing status and process information
        """
        running_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    process_info = proc.info
                    process_name = process_info['name'].lower()
                    
                    # Check exact matches
                    if process_info['name'] in self.process_names:
                        running_processes.append({
                            'pid': process_info['pid'],
                            'name': process_info['name'],
                            'exe': process_info['exe']
                        })
                    # Check keyword matches
                    elif any(keyword in process_name for keyword in self.process_keywords):
                        running_processes.append({
                            'pid': process_info['pid'],
                            'name': process_info['name'],
                            'exe': process_info['exe']
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return {
                'is_running': len(running_processes) > 0,
                'processes': running_processes,
                'count': len(running_processes)
            }
        
        except Exception as e:
            logger.error(f"Error checking if application is running: {e}")
            return {
                'is_running': False,
                'processes': [],
                'count': 0,
                'error': str(e)
            }
    
    def force_close_application(self, process_info: Dict) -> bool:
        """
        Force close the application using multiple methods.
        
        Args:
            process_info (Dict): Process information containing PID
            
        Returns:
            bool: True if successfully closed, False otherwise
        """
        try:
            pid = process_info['pid']
            process_name = process_info['name']
            
            # Method 1: Try psutil force kill
            try:
                process = psutil.Process(pid)
                process.kill()  # Force kill immediately
                process.wait(timeout=5)  # Wait for confirmation
                logger.info(f"Force killed {process_name} (PID: {pid}) using psutil")
                return True
            except psutil.TimeoutExpired:
                logger.warning(f"Process {process_name} (PID: {pid}) didn't die after kill signal")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                logger.info(f"Process {process_name} (PID: {pid}) already gone or no access")
                return True
            
            # Method 2: Use taskkill with force
            try:
                result = subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F", "/T"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    logger.info(f"Force killed {process_name} (PID: {pid}) using taskkill")
                    return True
                else:
                    logger.error(f"Taskkill failed for {process_name}: {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.error(f"Taskkill timeout for {process_name}")
            
            # Method 3: Try taskkill by name as last resort
            try:
                result = subprocess.run(
                    ["taskkill", "/IM", process_name, "/F", "/T"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    logger.info(f"Force killed {process_name} using taskkill by name")
                    return True
            except subprocess.TimeoutExpired:
                logger.error(f"Taskkill by name timeout for {process_name}")
                
            return False
                    
        except Exception as e:
            logger.error(f"Error force closing {process_info['name']}: {e}")
            return False
    
    def close_cargowise_application(self) -> Dict[str, Any]:
        """
        Main method to close CargoWise application if it's running.
        Uses aggressive force-close methods.
        
        Returns:
            Dict containing the operation result
        """
        logger.info("Checking if CargoWise/WiseCloud application is running...")
        
        # Check if application is running
        status = self.is_application_running()
        
        if not status['is_running']:
            logger.info("CargoWise/WiseCloud application is not running")
            return {
                'success': True,
                'message': 'CargoWise/WiseCloud application is not running',
                'was_running': False,
                'processes_closed': 0
            }
        
        logger.info(f"Found {status['count']} CargoWise/WiseCloud process(es) running")
        
        closed_processes = []
        failed_processes = []
        
        # Force close each running process
        for process_info in status['processes']:
            logger.info(f"Force closing {process_info['name']} (PID: {process_info['pid']})")
            
            if self.force_close_application(process_info):
                closed_processes.append(process_info)
            else:
                failed_processes.append(process_info)
        
        # Wait and verify closure
        time.sleep(3)
        final_status = self.is_application_running()
        
        success = not final_status['is_running']
        
        result = {
            'success': success,
            'was_running': True,
            'processes_found': status['count'],
            'processes_closed': len(closed_processes),
            'processes_failed': len(failed_processes),
            'closed_processes': closed_processes,
            'failed_processes': failed_processes,
            'still_running': final_status['processes'] if not success else []
        }
        
        if success:
            result['message'] = f"Successfully force-closed {len(closed_processes)} CargoWise/WiseCloud process(es)"
            logger.info(result['message'])
        else:
            result['message'] = f"Failed to close {len(failed_processes)} process(es). {final_status['count']} still running"
            logger.error(result['message'])
            # Log what's still running
            for proc in final_status['processes']:
                logger.error(f"Still running: {proc['name']} (PID: {proc['pid']})")
        
        return result


# Convenience function for direct usage
def close_cargowise() -> Dict[str, Any]:
    """
    Convenience function to force close CargoWise application.
    
    Returns:
        Dict containing the operation result
    """
    closer = ApplicationCloser()
    return closer.close_cargowise_application()


if __name__ == "__main__":
    # Example usage
    result = close_cargowise()
    print(f"Result: {result}")