# requirements.txt
robotframework==6.1.1
robotframework-sikulilibrary==2.0.0
Pillow==10.0.0

# =============================================================================
# 1. Simple Robot Framework Driver
# =============================================================================

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RobotSikuliDriver:
    """Simplified driver using Robot Framework + SikuliLibrary"""
    
    def __init__(self, image_dir: str = "images"):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
        
    def execute_robot_script(self, robot_script: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute Robot Framework script with SikuliLibrary"""
        
        # Create temporary robot file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.robot', delete=False) as f:
            f.write(robot_script)
            robot_file = f.name
        
        try:
            # Build command
            cmd = ['robot']
            
            # Add variables
            if variables:
                for key, value in variables.items():
                    cmd.extend(['--variable', f'{key}:{value}'])
            
            # Add output directory
            output_dir = tempfile.mkdtemp()
            cmd.extend(['--outputdir', output_dir])
            
            # Add robot file
            cmd.append(robot_file)
            
            # Execute
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse results
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout,
                "error": result.stderr if not success else None,
                "return_code": result.returncode
            }
            
        except Exception as e:
            logger.error(f"Robot execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "return_code": -1
            }
        finally:
            # Cleanup
            try:
                os.unlink(robot_file)
            except:
                pass

# =============================================================================
# 2. CargoWise Automation (Simplified)
# =============================================================================

class CargoWiseAutomation:
    """Simplified CargoWise automation using Robot Framework"""
    
    def __init__(self, image_dir: str = "cargowise_images"):
        self.driver = RobotSikuliDriver()
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login to CargoWise"""
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${TIMEOUT}      10

*** Test Cases ***
CargoWise Login
    [Documentation]    Login to CargoWise application
    
    # Launch or focus CargoWise
    Click    ${IMAGE_DIR}/cargowise_icon.png
    Sleep    2s
    
    # Wait for login screen
    Wait Until Screen Contain    ${IMAGE_DIR}/login_screen.png    timeout=${TIMEOUT}
    
    # Enter username
    Click    ${IMAGE_DIR}/username_field.png
    Input Text    ${USERNAME}
    
    # Enter password  
    Click    ${IMAGE_DIR}/password_field.png
    Input Text    ${PASSWORD}
    
    # Click login
    Click    ${IMAGE_DIR}/login_button.png
    
    # Verify login success
    Wait Until Screen Contain    ${IMAGE_DIR}/dashboard.png    timeout=30
    
    Log    Login successful
"""
        
        variables = {
            'USERNAME': username,
            'PASSWORD': password
        }
        
        return self.driver.execute_robot_script(robot_script, variables)
    
    def create_booking(self, customer: str, origin: str, destination: str, cargo_details: str) -> Dict[str, Any]:
        """Create new booking"""
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images

*** Test Cases ***
Create New Booking
    [Documentation]    Create a new booking in CargoWise
    
    # Click New Booking
    Click    ${IMAGE_DIR}/new_booking_button.png
    Sleep    2s
    
    # Wait for booking form
    Wait Until Screen Contain    ${IMAGE_DIR}/booking_form.png    timeout=15
    
    # Fill customer
    Click    ${IMAGE_DIR}/customer_field.png
    Input Text    ${CUSTOMER}
    
    # Fill origin
    Click    ${IMAGE_DIR}/origin_field.png  
    Input Text    ${ORIGIN}
    
    # Fill destination
    Click    ${IMAGE_DIR}/destination_field.png
    Input Text    ${DESTINATION}
    
    # Fill cargo details
    Click    ${IMAGE_DIR}/cargo_field.png
    Input Text    ${CARGO_DETAILS}
    
    # Save booking
    Click    ${IMAGE_DIR}/save_button.png
    
    # Verify booking created
    Wait Until Screen Contain    ${IMAGE_DIR}/booking_confirmation.png    timeout=20
    
    Log    Booking created successfully
"""
        
        variables = {
            'CUSTOMER': customer,
            'ORIGIN': origin, 
            'DESTINATION': destination,
            'CARGO_DETAILS': cargo_details
        }
        
        return self.driver.execute_robot_script(robot_script, variables)
    
    def search_booking(self, booking_reference: str) -> Dict[str, Any]:
        """Search for existing booking"""
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Test Cases ***
Search Booking
    [Documentation]    Search for booking by reference
    
    # Click search
    Click    ${IMAGE_DIR}/search_button.png
    Sleep    1s
    
    # Enter booking reference
    Click    ${IMAGE_DIR}/search_field.png
    Input Text    ${BOOKING_REF}
    
    # Press Enter or click search
    Key.enter
    
    # Wait for results
    Wait Until Screen Contain    ${IMAGE_DIR}/search_results.png    timeout=15
    
    Log    Search completed for ${BOOKING_REF}
"""
        
        variables = {'BOOKING_REF': booking_reference}
        return self.driver.execute_robot_script(robot_script, variables)

# =============================================================================
# 3. Simple Tool Interface (if you need it for your existing system)
# =============================================================================

class SimplifiedCargoWiseTool:
    """Simplified tool interface for CargoWise"""
    
    def __init__(self):
        self.automation = CargoWiseAutomation()
    
    def login(self, username: str, password: str, environment: str = "desktop") -> Dict[str, Any]:
        """Login tool"""
        try:
            result = self.automation.login(username, password)
            return {
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "logged_in": result["success"],
                    "username": username,
                    "environment": environment
                },
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
    
    def create_booking(self, customer: str, origin: str, destination: str, cargo_details: str) -> Dict[str, Any]:
        """Create booking tool"""
        try:
            result = self.automation.create_booking(customer, origin, destination, cargo_details)
            return {
                "status": "SUCCESS" if result["success"] else "ERROR", 
                "outputs": {
                    "booking_created": result["success"],
                    "customer": customer,
                    "origin": origin,
                    "destination": destination
                },
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "outputs": {},
                "error": str(e)
            }
    
    def search_booking(self, booking_reference: str) -> Dict[str, Any]:
        """Search booking tool"""
        try:
            result = self.automation.search_booking(booking_reference)
            return {
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "search_completed": result["success"],
                    "booking_reference": booking_reference
                },
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "status": "ERROR", 
                "outputs": {},
                "error": str(e)
            }

# =============================================================================
# 4. Example Usage
# =============================================================================

if __name__ == "__main__":
    # Direct usage
    cargowise = CargoWiseAutomation()
    
    # Login
    login_result = cargowise.login("john.doe", "password123")
    print(f"Login: {login_result}")
    
    # Create booking
    booking_result = cargowise.create_booking(
        customer="ACME Corp",
        origin="New York", 
        destination="Los Angeles",
        cargo_details="Electronics - 5 pallets"
    )
    print(f"Booking: {booking_result}")
    
    # Or use tool interface
    tool = SimplifiedCargoWiseTool()
    result = tool.login("john.doe", "password123")
    print(f"Tool result: {result}")