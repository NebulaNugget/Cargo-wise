import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RemoteConnectionManager:
    def __init__(self):
        # Simple list of remote connection processes to terminate
        self.remote_processes = [
            "remoteApp.exe", 
            "mstsc.exe",  # Remote Desktop Connection
            "rdpclip.exe",  # RDP Clipboard
            "TeamViewer.exe",  # TeamViewer
            "anydesk.exe",
            "remoteApp.exe"  # AnyDesk

        ]
    
    def disconnect_all_remote_connections(self) -> Dict[str, Any]:
        """
        Simple function to terminate remote connection processes.
        Works like ending tasks in Task Manager.
        """
        logger.info("Terminating remote connection processes...")
        
        terminated_count = 0
        failed_count = 0
        
        try:
            # Find and terminate remote processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    process_name = proc.info['name']
                    
                    if process_name in self.remote_processes:
                        logger.info(f"Terminating {process_name} (PID: {proc.info['pid']})")
                        proc.terminate()  # Graceful termination
                        terminated_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Process already gone or no permission - skip
                    continue
                except Exception as e:
                    logger.error(f"Error terminating process: {e}")
                    failed_count += 1
            
            if terminated_count == 0:
                logger.info("No remote connection processes found")
                return {
                    'success': True,
                    'message': 'No remote connections found',
                    'terminated': 0
                }
            else:
                logger.info(f"Successfully terminated {terminated_count} remote connection process(es)")
                return {
                    'success': True,
                    'message': f'Terminated {terminated_count} remote connection process(es)',
                    'terminated': terminated_count,
                    'failed': failed_count
                }
                
        except Exception as e:
            logger.error(f"Error during remote connection cleanup: {e}")
            return {
                'success': False,
                'message': f'Error during cleanup: {str(e)}',
                'terminated': terminated_count,
                'failed': failed_count
            }


# Convenience function for direct usage
def disconnect_remote_connections() -> Dict[str, Any]:
    """
    Simple convenience function to disconnect remote connections.
    """
    manager = RemoteConnectionManager()
    return manager.disconnect_all_remote_connections()


if __name__ == "__main__":
    # Test the function
    result = disconnect_remote_connections()
    print(f"Result: {result}")