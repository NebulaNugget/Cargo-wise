import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import asyncio
import traceback
import concurrent.futures
import glob
import re
import signal
import psutil
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class RobotSikuliDriver:
    """Improved driver using Robot Framework + SikuliLibrary with timeout handling"""
    
    def __init__(self, image_dir: str = "images", app_path: str="C:/Users/UK-PC/AppData/Local/slack/slack.exe", timeout: int = 60):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
        self.timeout = timeout  # Reduced default timeout
        self.app_path = app_path  # CargoWise application path
        # Create a thread pool executor for running subprocesses
        # Create a thread pool executor for running subprocesses
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)  # Reduced workers
        # Track running processes
        self._running_processes = set()
        # Verify environment on initialization
        self._verify_environment()
    
    def _verify_environment(self):
        """Verify that Robot Framework and SikuliLibrary are properly installed"""
        try:
            # Check if robot is available
            robot_version = subprocess.run(
                ['robot', '--version'], 
                capture_output=True, 
                text=True, 
                check=False,
                timeout=10  # Quick timeout for version check
            )
            if robot_version.returncode != 0:
                logger.error(f"Robot Framework not found. Please install with: pip install robotframework")
                logger.error(f"Error: {robot_version.stderr}")
                return False
            else:
                logger.info(f"Robot Framework version: {robot_version.stdout.strip()}")
            
            # Check if Java is available
            java_version = subprocess.run(
                ['java', '-version'], 
                capture_output=True, 
                text=True, 
                check=False,
                timeout=10
            )
            if java_version.returncode != 0:
                logger.error(f"Java not found. Please install Java 8 or later.")
                logger.error(f"Error: {java_version.stderr}")
                return False
            else:
                logger.info(f"Java available")
            
            # Quick dry-run test instead of full SikuliLibrary test
            test_script = """*** Settings ***
Library    Collections

*** Test Cases ***
Quick Test
    Log    Quick verification test
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.robot', delete=False) as f:
                f.write(test_script)
                test_file = f.name
            
            try:
                output_dir = tempfile.mkdtemp()
                test_result = subprocess.run(
                    ['robot', '--outputdir', output_dir, '--dryrun', test_file],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=15  # Quick timeout
                )
                
                if test_result.returncode != 0:
                    logger.warning(f"Basic Robot test failed: {test_result.stderr}")
                    return False
                else:
                    logger.info("Basic Robot Framework verification passed")
                    return True
                    
            finally:
                try:
                    os.unlink(test_file)
                    import shutil
                    if os.path.exists(output_dir):
                        shutil.rmtree(output_dir, ignore_errors=True)
                except Exception as cleanup_error:
                    logger.warning(f"Cleanup error: {cleanup_error}")
                
        except Exception as e:
            logger.error(f"Error verifying environment: {str(e)}")
            return False
    
    @contextmanager
    def _process_timeout_handler(self, process):
        """Context manager to handle process timeouts and cleanup"""
        try:
            self._running_processes.add(process.pid)
            yield process
        finally:
            self._running_processes.discard(process.pid)
            # Kill process tree if still running
            try:
                if process.poll() is None:  # Process still running
                    self._kill_process_tree(process.pid)
            except Exception as e:
                logger.warning(f"Error during process cleanup: {e}")
    
    def _kill_process_tree(self, pid):
        """Kill process and all its children"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Kill children first
            for child in children:
                try:
                    child.kill()
                except psutil.NoSuchProcess:
                    pass
            
            # Kill parent
            try:
                parent.kill()
            except psutil.NoSuchProcess:
                pass
                
            # Wait for processes to die
            psutil.wait_procs(children + [parent], timeout=3)
            
        except psutil.NoSuchProcess:
            pass  # Process already dead
        except Exception as e:
            logger.warning(f"Error killing process tree {pid}: {e}")
    
    def _run_robot_command_with_timeout(self, cmd, timeout):
        """Run robot command with proper timeout handling"""
        try:
            logger.info(f"Running robot command: {' '.join(cmd)}")
            
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Create process group on Unix
            )
            
            with self._process_timeout_handler(process):
                try:
                    stdout, stderr = process.communicate(timeout=timeout)
                    
                    # Log results
                    if process.returncode != 0:
                        logger.error(f"Robot command failed with return code {process.returncode}")
                        logger.error(f"STDOUT: {stdout}")
                        logger.error(f"STDERR: {stderr}")
                    else:
                        logger.info(f"Robot command completed successfully")
                        logger.debug(f"STDOUT: {stdout}")
                        
                    return {
                        "success": process.returncode == 0,
                        "output": stdout,
                        "error": stderr if process.returncode != 0 else None,
                        "return_code": process.returncode
                    }
                    
                except subprocess.TimeoutExpired:
                    logger.error(f"Robot command timed out after {timeout} seconds")
                    
                    # Force kill the process
                    self._kill_process_tree(process.pid)
                    
                    # Try to get partial output
                    try:
                        stdout, stderr = process.communicate(timeout=1)
                        if stdout:
                            last_lines = '\n'.join(stdout.split('\n')[-20:]) if stdout else ""
                            logger.error(f"Last output before timeout:\n{last_lines}")
                    except:
                        stdout, stderr = "", "Process killed due to timeout"
                    
                    return {
                        "success": False,
                        "error": f"Command timed out after {timeout} seconds",
                        "output": stdout,
                        "return_code": -2,
                        "timeout_occurred": True
                    }
                    
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"Robot command execution failed: {str(e)}\n{error_traceback}")
            return {
                "success": False,
                "error": str(e),
                "traceback": error_traceback,
                "output": "",
                "return_code": -1
            }
    
    def _create_lightweight_robot_script(self, robot_script: str, variables: Dict[str, Any] = None) -> str:
        """Create a lightweight Robot script that initializes Sikuli properly"""
        
        # Normalize the script first
        robot_script = self._normalize_robot_script(robot_script)
        
        # Add app path variable if provided
        app_path_var = f"${{APP_PATH}}    {self.app_path}" if self.app_path else ""
        
        # Create a minimal script with simplified SikuliLibrary initialization
        minimal_script = f'''*** Settings ***
Library    SikuliLibrary    WITH NAME    Sikuli
Library    OperatingSystem
Library    Process
Library    Collections
Library    DateTime

*** Variables ***
${{IMAGE_DIR}}    {str(self.image_dir.absolute())}
${{SIKULI_TIMEOUT}}    {min(self.timeout // 2, 20)}
${{TIMEOUT}}  {self.timeout}
{app_path_var}

*** Test Cases ***
Execute Sikuli Task
    [Documentation]    Execute Sikuli automation task
    [Timeout]    {self.timeout + 30}s
    [Setup]    Initialize Sikuli Environment
    [Teardown]    Cleanup Sikuli Environment
    Run Keyword And Continue On Failure    Execute Task With Progress Logging

*** Keywords ***
Initialize Sikuli Environment
    [Documentation]    Initialize Sikuli with minimal settings
    Log    Initializing Sikuli environment
    Set Library Search Order    Sikuli
    Log To Console    Starting Sikuli Process...
    Sikuli.Start Sikuli Process
    Log To Console    Adding image path: ${{IMAGE_DIR}}
    Sikuli.Add Image Path    ${{IMAGE_DIR}}
    Sikuli.Set Move Mouse Delay    0.5
    # Set shorter timeouts for Sikuli operations
    Sikuli.Set Min Similarity    0.7
    # Launch CargoWise if app path is provided
    Run Keyword If    '${{APP_PATH}}' != '${{EMPTY}}'    Launch CargoWise Application
    Log    Sikuli environment initialized

Launch CargoWise Application
    [Documentation]    Launch the CargoWise application
    Log    Launching application from: ${{APP_PATH}}
    Log To Console    Launching application: ${{APP_PATH}}
    Run Keyword If    '${{APP_PATH}}' != '${{EMPTY}}'    Run Process    ${{APP_PATH}}    shell=True
    ${{timestamp}}=    Get Current Date
    Log To Console    Application launch initiated at ${{timestamp}}
    Sleep    5s    # Wait for application to start
    Log To Console    Application should be started now

Cleanup Sikuli Environment
    [Documentation]    Clean up Sikuli resources
    Log    Cleaning up Sikuli environment
    Log To Console    Stopping Sikuli Process...
    Run Keyword And Ignore Error    Sikuli.Stop Sikuli Process
    Log    Sikuli environment cleaned up

Execute Task With Progress Logging
    [Documentation]    Execute the task with progress logging
    ${{start_time}}=    Get Current Date
    Log To Console    Task execution started at ${{start_time}}
    
    # Set a timeout for the task execution
    ${{status}}=    Run Keyword And Return Status    
    ...    Run Keyword With Timeout    Run Sikuli Task    {self.timeout - 5}s
    
    ${{end_time}}=    Get Current Date
    ${{duration}}=    Subtract Date From Date    ${{end_time}}    ${{start_time}}
    Log To Console    Task execution ended at ${{end_time}} (Duration: ${{duration}}s)
    
    Run Keyword If    not ${{status}}    Log To Console    WARNING: Task execution timed out or failed
    Run Keyword If    not ${{status}}    Log    WARNING: Task execution timed out or failed    WARN
    
    RETURN    ${{status}}

Run Keyword With Timeout
    [Arguments]    ${{keyword}}    ${{timeout}}    @{{args}}
    [Documentation]    Run a keyword with a timeout
    Log To Console    Running keyword with timeout: ${{keyword}} (${{timeout}})
    ${{result}}=    Run Keyword And Return Status    Wait Until Keyword Succeeds    ${{timeout}}    1s    ${{keyword}}    @{{args}}
    Return    ${{result}}

Run Sikuli Task
    [Documentation]    Execute the actual Sikuli task
    Log    Starting Sikuli task execution
    Log To Console    Executing Sikuli task...
    
    # Add progress logging to the task content
    ${{task_start}}=    Get Current Date
    Log To Console    Task started at ${{task_start}}
    
    # Execute the task content with progress logging
    {self._extract_task_content_with_logging(robot_script)}
    
    ${{task_end}}=    Get Current Date
    Log To Console    Task completed at ${{task_end}}
    Log    Sikuli task execution completed
'''
        return minimal_script
    def _extract_task_content_with_logging(self, robot_script: str) -> str:
        """Extract task content from the original robot script and add progress logging"""
        lines = robot_script.split('\n')
        task_lines = []
        in_task = False
        step_count = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Skip section headers and empty lines
            if stripped.startswith('***') or not stripped:
                continue
                
            # Check if this is a task/test case name
            if not line.startswith(' ') and stripped:
                in_task = True
                continue
                
            # If we're in a task and this is content
            if in_task and line.startswith(' '):
                # Skip setup/teardown and documentation
                if not any(keyword in stripped.lower() for keyword in ['[setup]', '[teardown]', '[documentation]', '[timeout]']):
                    # Add step count and logging for significant operations
                    if any(keyword in stripped.lower() for keyword in ['click', 'input text', 'wait until', 'type', 'press']):
                        step_count += 1
                        # Add logging before the step
                        task_lines.append(f'    Log To Console    Step {step_count}: {stripped}')
                        task_lines.append(f'    ${{step{step_count}_start}}=    Get Current Date')
                        # Add the actual step
                        task_lines.append('    ' + stripped)
                        # Add logging after the step
                        task_lines.append(f'    ${{step{step_count}_end}}=    Get Current Date')
                        task_lines.append(f'    ${{step{step_count}_duration}}=    Subtract Date From Date    ${{step{step_count}_end}}    ${{step{step_count}_start}}')
                        task_lines.append(f'    Log To Console    Step {step_count} completed in ${{step{step_count}_duration}}s')
                    else:
                        # Just add the step without additional logging
                        task_lines.append('    ' + stripped)
        
        if not task_lines:
            # Default content if no task content found
            task_lines = [
                '    Log    No specific task content provided',
                '    Log To Console    No specific task content provided',
                '    Log    Sikuli is ready for image-based automation'
            ]
        
        return '\n'.join(task_lines)
    
    def _normalize_robot_script(self, robot_script: str) -> str:
        """Normalize Robot Framework script format"""
        lines = robot_script.split('\n')
        normalized_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                normalized_lines.append(line.rstrip())
        
        return '\n'.join(normalized_lines)
    
    async def execute_robot_script(self, robot_script: str, variables: Dict[str, Any] = None, 
                                 timeout: Optional[int] = None, app_path: Optional[str] = None) -> Dict[str, Any]:
        """Execute Robot Framework script with SikuliLibrary asynchronously"""
        
        if timeout is None:
            timeout = self.timeout
            
        # Add some buffer to the timeout to allow for proper cleanup
        execution_timeout = timeout + 10  # Add 10 seconds buffer for cleanup

        # Use provided app_path or fall back to the one set during initialization
        current_app_path = app_path if app_path is not None else self.app_path
            
        # Create lightweight script
        processed_script = self._create_lightweight_robot_script(robot_script, variables)
        
        # Create temporary robot file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.robot', delete=False, encoding='utf-8') as f:
            f.write(processed_script)
            robot_file = f.name
        
        output_dir = None
        try:
            # Log the script being executed for debugging
            logger.info(f"Executing Robot script with timeout {timeout}s")
            logger.debug(f"Script content:\n{processed_script}")
            # Build command with optimizations
            cmd = ['robot']
            
            # Add variables
            if not variables:
                variables = {}
                
            # Add essential variables
            variables.update({
                'IMAGE_DIR': str(self.image_dir.absolute()),
                'SIKULI_TIMEOUT': str(min(timeout // 2, 30))  # Half timeout or max 30s
            })
            # Add APP_PATH if available
            if current_app_path:
                variables['APP_PATH'] = current_app_path
                
            for key, value in variables.items():
                cmd.extend(['--variable', f'{key}:{value}'])
            
            # Add Java options to help with SikuliLibrary initialization
            java_opts = "-Dfile.encoding=UTF-8 -Dsikuli.Debug=0"
            os.environ["JAVA_TOOL_OPTIONS"] = java_opts
            
            # Add output directory
            output_dir = tempfile.mkdtemp()
            cmd.extend(['--outputdir', output_dir])
            
            # Add optimized options
            cmd.extend([
                '--log', 'log.html',
                '--report', 'NONE',  # Skip report generation to save time
                '--output', 'output.xml',
                '--loglevel',
                'DEBUG:INFO',
                '--pythonpath', '.',
                '--consolecolors', 'on',
                '--consolemarkers', 'on'
               
            ])
            
            # Add robot file
            cmd.append(robot_file)
            
            logger.debug(f"Generated Robot script:\n{processed_script}")
            logger.debug(f"Executing Robot command with timeout {timeout}s: {' '.join(cmd[:5])}...")
            
            # Execute in a thread pool with timeout
            result = await asyncio.get_event_loop().run_in_executor(
                self._executor, 
                self._run_robot_command_with_timeout,
                cmd,
                timeout
            )
            # Try to parse output.xml if it exists
            try:
                output_xml = os.path.join(output_dir, 'output.xml')
                if os.path.exists(output_xml):
                    logger.info(f"Robot output.xml exists at {output_xml}")
                    # You could parse this file for more detailed error information
            except Exception as xml_error:
                logger.warning(f"Error checking output.xml: {xml_error}")
            
            # Add additional info to result
            result.update({
                "output_dir": output_dir,
                "robot_script": processed_script,
                "timeout_used": timeout
            })
            
            if not result["success"]:
                logger.error(f"Robot execution failed: {result.get('error', 'Unknown error')}")
                # Check if there's a log.html file we can reference
                log_html = os.path.join(output_dir, 'log.html')
                if os.path.exists(log_html):
                    logger.info(f"Robot log.html exists at {log_html} - check for detailed error information")
            
            return result
            
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"Robot execution failed: {str(e)}\n{error_traceback}")
            
            return {
                "success": False,
                "error": str(e),
                "traceback": error_traceback,
                "output": "",
                "return_code": -1,
                "output_dir": output_dir,
                "robot_script": processed_script if 'processed_script' in locals() else None,
                "timeout_used": timeout
            }
        finally:
            # Cleanup robot file
            try:
                if robot_file and os.path.exists(robot_file):
                    os.unlink(robot_file)
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up temporary robot file: {str(cleanup_error)}")
    
    def kill_all_processes(self):
        """Kill all running Robot/Sikuli processes"""
        for pid in list(self._running_processes):
            try:
                self._kill_process_tree(pid)
            except Exception as e:
                logger.warning(f"Error killing process {pid}: {e}")
        self._running_processes.clear()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Kill any running processes
            self.kill_all_processes()
            
            # Shutdown executor
            self._executor.shutdown(wait=False)
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except:
            pass

# Example usage and testing
async def test_robot_sikuli_driver():
    """Test function for the improved RobotSikuliDriver"""
    driver = RobotSikuliDriver(timeout=30)  # 30 second timeout
    
    # Simple test script
    test_script = """
*** Test Cases ***
Simple Sikuli Test
    Log    Starting Sikuli test
    Log    Testing image directory access
    Log    Test completed successfully
"""
    
    try:
        result = await driver.execute_robot_script(test_script)
        print(f"Test result: {result['success']}")
        if not result['success']:
            print(f"Error: {result.get('error', 'Unknown error')}")
        return result
    finally:
        driver.cleanup()

if __name__ == "__main__":
    # Run test
    asyncio.run(test_robot_sikuli_driver())