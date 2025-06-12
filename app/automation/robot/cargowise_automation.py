from pathlib import Path
from typing import Dict, Any, Optional
import logging
import base64
import os
from datetime import datetime 
from .robot_driver import RobotSikuliDriver

logger = logging.getLogger(__name__)

class CargoWiseAutomation:
    """Simplified CargoWise automation using Robot Framework"""
    
    def __init__(self, image_dir: str = "cargowise_images"):
        self.driver = RobotSikuliDriver(
    image_dir="cargowise_images",
    timeout=300,
    app_path="C:/Users/UK-PC/AppData/Local/slack/slack.exe"  # Path to CargoWise executable
)
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login to CargoWise"""
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${TIMEOUT}      10

*** Test Cases ***
Send Telegram Message
    [Documentation]    Send a message in Telegram (for testing)
    
    
    # Click on the dm section
    Click    ${IMAGE_DIR}/dm_section.png

    # Click on slack user
    Click    ${IMAGE_DIR}/slack_user.png
   
    # Type a simple message
    Input Text     ${IMAGE_DIR}/message_box.png     Hello, this is a test message from ${USERNAME}
    
    # click send button
    Click    ${IMAGE_DIR}/slack_send_button.png
    
    Log    Test message typed and saved successfully
    
    
"""
        
        variables = {
            'USERNAME': username,  # Will be used as contact name
            'PASSWORD': password   # Will be used as message text
        }
        
        result =  await self.driver.execute_robot_script(robot_script, variables)
        # Process result
        return {
            "success": result["success"],
            "status": "COMPLETED" if result["success"] else "FAILED",  # Change "SUCCESS" to "COMPLETED"
            "error": result.get("error"),
            "completed": result["success"],
            "completed_at": datetime.now().isoformat()
        }
    
    async def create_booking(self, customer: str, origin: str, destination: str, cargo_details: str) -> Dict[str, Any]:
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
        
        result = await self.driver.execute_robot_script(robot_script, variables)
        # Process result - use COMPLETED instead of SUCCESS
        return {
            "success": result["success"],
            "status": "COMPLETED" if result["success"] else "FAILED",
            "completed_at": datetime.now().isoformat(),
            "error": result.get("error")
        }
    
    async def search_booking(self, booking_reference: str) -> Dict[str, Any]:
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
        result = await self.driver.execute_robot_script(robot_script, variables)
        # Process result - use COMPLETED instead of SUCCESS
        return {
            "success": result["success"],
            "status": "COMPLETED" if result["success"] else "FAILED",
            "error": result.get("error")
        }