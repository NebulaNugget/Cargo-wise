from pathlib import Path
from app.utils.task_status_utils import TaskStatusUtils
from typing import Dict, Any, Optional
import logging
import base64
import os
from dotenv import load_dotenv
from datetime import datetime 
from .robot_driver import RobotSikuliDriver
from .task_status_checker import TaskStatusChecker
logger = logging.getLogger(__name__)
# Load environment variables
load_dotenv()

class CargoWiseAutomation:
    """Simplified CargoWise automation using Robot Framework"""
    
    def __init__(self, image_dir: str = "cargowise_images", task_id:Optional[str]=None):

        self.task_id = task_id
        # Add task status checker
        self.task_checker = TaskStatusChecker(task_id)
        screenshot_base_path = os.getenv('SCREENSHOT_BASE_DIR', 'C:/Users/UK-PC/Desktop/AI driven cargo-wise automation framework/cargowise-ai-backend/screenshots')
        self.screenshot_base_dir = Path(screenshot_base_path)
        
        # Create task-specific screenshot directory if task_id is provided
        if self.task_id:
            self.screenshot_dir = self.screenshot_base_dir / self.task_id
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created task-specific screenshot directory: {self.screenshot_dir}")
            print(f"Created task-specific screenshot directory: {self.screenshot_dir}")
        else:
            self.screenshot_dir = self.screenshot_base_dir / "default"
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created default screenshot directory: {self.screenshot_dir}")
            print(f"Created default screenshot directory: {self.screenshot_dir}")
        self.driver = RobotSikuliDriver(

            image_dir=image_dir or os.getenv('IMAGE_DIR', 'cargowise_images'),
            timeout=int(os.getenv('DEFAULT_TIMEOUT', '300')),
            #app_path="C:\Windows\System32\calc.exe"
            app_path=os.getenv('CARGOWISE_APP_PATH'),
            task_id=self.task_id,  # Pass task_id to driver
            screenshot_dir=str(self.screenshot_dir)  # Pass screenshot directory to driver
)


    async def _check_cancellation(self) -> bool:
        """Check if task has been cancelled and raise exception if so"""
        if self.task_checker.is_cancelled():
            logger.info(f"Task {self.task_id} has been cancelled, stopping automation")
            # Clean up any running processes
            await self.driver.cancel_running_tasks()
            raise Exception("Task was cancelled by user")
        return False
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login to CargoWise"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary



*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${TIMEOUT}      30
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}




*** Test Cases ***
Login to cargowise cloud
    [Documentation]    Login to cargowise (for testing)

    Click    ${IMAGE_DIR}/wisecloud_password.png
    Sleep    1s
   
    Input Text    ${IMAGE_DIR}/wisecloud_password.png    ${PASSWORD}
    Sleep    1s
     
 
    Click    ${IMAGE_DIR}/wisecloud-login-btn.png

    Sleep    10s
    Double Click    ${IMAGE_DIR}/org-logo.png
    
    Sleep    60s

    Click    ${IMAGE_DIR}/cargowise-next-password.png
    Input Text    ${IMAGE_DIR}/cargowise-next-password.png    ${PASSWORD}
    Sleep    1s
    Click    ${IMAGE_DIR}/cargowise-next-login.png
  
    Log    Logged into Cargowise successfully
    
    
"""
        
        variables = {
            'USERNAME': username,  # Will be used as contact name
            'PASSWORD': password,   # Will be used as message text
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "login_completed": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def create_order_part1(self, buyer: str, supplier: str, container_return_date: str, sanction: str, password:str) -> Dict[str, Any]:
        """Create new order"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Create New Order
    [Documentation]    Create a new order in CargoWise
   
    Click    ${IMAGE_DIR}/operate-btn.png
    Sleep    3s
    Click    ${IMAGE_DIR}/forwarding-btn.png
    Sleep    3s
    Click    ${IMAGE_DIR}/order.png
    Sleep    7s
    Click    ${IMAGE_DIR}/new-btn.png
    
    Log    Navigated to new order form successfully
"""
        
        variables = {
            'PASSWORD':password,
            'BUYER': buyer,
            'SUPPLIER': supplier, 
            'CONTAINER_RETURN_DATE': container_return_date,
            'SANCTION': sanction,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "navigation_completed": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def create_order_part2(self, buyer: str, supplier: str, container_return_date: str, sanction: str, password:str) -> Dict[str, Any]:
        """Create new order"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Fill Order Details
    [Documentation]    Fill in order details and save
    
    Input Text    ${IMAGE_DIR}/order-buyer.png    ${BUYER}
    Sleep    3s
    Input Text    ${IMAGE_DIR}/order-supplier.png    ${SUPPLIER}
    Sleep    3s
    Click    ${IMAGE_DIR}/order-additional-detail.png
    Sleep    2s
    Input Text    ${IMAGE_DIR}/order-empty-return-date.png    ${CONTAINER_RETURN_DATE}
    Sleep    3s
    Input Text    ${IMAGE_DIR}/order-sanction.png    ${SANCTION}
    Sleep    3s
    Click    ${IMAGE_DIR}/save-close-order.png
    Sleep    2s
    Click    ${IMAGE_DIR}/order-no2.png
    Sleep    5s
    
    Click    ${IMAGE_DIR}/exit-cargowise-white2.png
    
    Log    Order created successfully
"""
        
        variables = {
            'PASSWORD':password,
            'BUYER': buyer,
            'SUPPLIER': supplier, 
            'CONTAINER_RETURN_DATE': container_return_date,
            'SANCTION': sanction,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "order_created": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def logout(self, password: str) -> Dict[str, Any]:
        """Logout from CargoWise"""
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Logout from CargoWise
    [Documentation]    Exit CargoWise application
    
    
    Click    ${IMAGE_DIR}/exit-cargowise-btn.png
    Sleep    5s
    Click    ${IMAGE_DIR}/close-wisetech.png
    Sleep    2s
    Click    ${IMAGE_DIR}/close-wisetech.png
    
    Log    Logged out successfully
"""
        
        variables = {
            'PASSWORD': password,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "logged_out": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def search_shipment_by_housebill(self, housebill: str) -> Dict[str, Any]:
        """Search for shipment by housebill number"""
        # Check for cancellation before starting
        await self._check_cancellation()
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Search Shipment By Housebill
    [Documentation]    Search for shipment by housebill number in CargoWise
    
    
    # Enter housebill number
    Input Text    ${IMAGE_DIR}/search-shipment.png    ${HOUSEBILL}
    Sleep    3s
    Click    ${IMAGE_DIR}/housebill2.png
    Sleep    20s
    Click    ${IMAGE_DIR}/additional-detail.png
    Sleep    5s
    Click    ${IMAGE_DIR}/close.png
    Sleep    3s
    Click    ${IMAGE_DIR}/close-cargowise2.png
    Sleep    3s

    Click    ${IMAGE_DIR}/wisecloud-logo.png
    Sleep    2s
    Click    ${IMAGE_DIR}/close-wisetech-white.png
    Sleep    2s
    Click    ${IMAGE_DIR}/close-wisetech.png
    
    
    
    Log    Search completed for housebill: ${HOUSEBILL}
"""
        
        variables = {
            'HOUSEBILL': housebill,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "shipment_found": result["success"],
                    "housebill": housebill,
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def search_consolidation_by_referencenumber(self, referencenumber: str) -> Dict[str, Any]:
        """Search for consolidation by reference number"""
        # Check for cancellation before starting
        await self._check_cancellation()
        
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Search Consolidation By Reference Number
    [Documentation]    Search for consolidation by reference number in CargoWise
    
    # Enter reference number
    Input Text    ${IMAGE_DIR}/search_consolidation2.png    ${REFERENCENUMBER}
    Sleep    5s
    Click    ${IMAGE_DIR}/select_consolidation.png
    Sleep    20s
    Click    ${IMAGE_DIR}/consolidation_route.png
    Sleep    5s
    Click    ${IMAGE_DIR}/consolidation_container.png
    Sleep    5s
    Click    ${IMAGE_DIR}/close.png
    Sleep    3s
    Click    ${IMAGE_DIR}/close-cargowise2.png
    Sleep    3s

    Click    ${IMAGE_DIR}/wisecloud-logo.png
    Sleep    2s
    Click    ${IMAGE_DIR}/close-wisetech-white.png
    Sleep    2s
    Click    ${IMAGE_DIR}/close-wisetech.png
    
    Log    Search completed for reference number: ${REFERENCENUMBER}
"""
        
        variables = {
            'REFERENCENUMBER': referencenumber,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "consolidation_found": result["success"],
                    "referencenumber": referencenumber,
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def create_shipment(self, weight: str, consignor: str, transport_method: str, description: str) -> Dict[str, Any]:
        """Create new shipment"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Create New Shipment
    [Documentation]    Create a new shipment in CargoWise
    
    # Click New Shipment
    Click    ${IMAGE_DIR}/operate-btn.png
    Sleep    3s
    
    Click    ${IMAGE_DIR}/forwarding-btn.png
    Sleep    3s
    
    Click    ${IMAGE_DIR}/shipment-btn.png
    Sleep    6s

    Click    ${IMAGE_DIR}/new-btn.png
    Sleep    10s

    Input Text    ${IMAGE_DIR}/transport-btn.png    ${TRANSPORT_METHOD}
    
    
    Log    Shipment created successfully
"""
        
        variables = {
            'WEIGHT': weight,
            'CONSIGNOR': consignor, 
            'TRANSPORT_METHOD': transport_method,
            'DESCRIPTION': description,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],  # Add this line
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,  # Add this line,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    async def create_shipment2(self, weight: str, consignor: str, transport_method: str, description: str) -> Dict[str, Any]:
        """Create new shipment part2"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Create New Shipment
    [Documentation]    Create a new shipment in CargoWise
   

    Input Text    ${IMAGE_DIR}/consignor-btn.png    ${CONSIGNOR}
    Sleep    3s

    Input Text    ${IMAGE_DIR}/weight-btn.png    ${WEIGHT}
    Sleep    3s
  
    Input Text    ${IMAGE_DIR}/description-btn.png    ${DESCRIPTION}
    Sleep    3s
    
    Click    ${IMAGE_DIR}/save-close-btn.png
    Sleep    15s

    Double Click    ${IMAGE_DIR}/minimise-shipment.png
    Sleep    4s

    Click    ${IMAGE_DIR}/exit-cargowise-white2.png
  
    
    Log    Shipment created successfully
"""
        
        variables = {
            'WEIGHT': weight,
            'CONSIGNOR': consignor, 
            'TRANSPORT_METHOD': transport_method,
            'DESCRIPTION': description,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],  # Add this line
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "shipment_created": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,  # Add this line,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

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
    Sleep    1s

    
    # Fill origin
    Click    ${IMAGE_DIR}/origin_field.png  
    Input Text    ${ORIGIN}
    Sleep    1s
    
    # Fill destination
    Click    ${IMAGE_DIR}/destination_field.png
    Input Text    ${DESTINATION}
    Sleep    1s
    
    # Fill cargo details
    Click    ${IMAGE_DIR}/cargo_field.png
    Input Text    ${CARGO_DETAILS}
    Sleep    1s
    
    # Save booking
    Click    ${IMAGE_DIR}/save_button.png
    Sleep    7s


    Click    ${IMAGE_DIR}/exit-cargowise-btn.png
    Sleep    3s

    Click    ${IMAGE_DIR}/exit-wisetech-btn.png
    Sleep    3s
    
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
    
    async def create_consolidation(self, transport: str, container_mode: str, first_load: str, last_load: str, voyage: str, etd: str, eta: str, bol: str, vessel: str) -> Dict[str, Any]:
        """Create new consolidation"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Create New Consolidation
    [Documentation]    Create a new consolidation in CargoWise
    
    # Click New Consolidation
    Click    ${IMAGE_DIR}/operate-btn.png
    Sleep    3s
    
    Click    ${IMAGE_DIR}/forwarding-btn.png
    Sleep    3s
    
    Click    ${IMAGE_DIR}/consolidation-btn.png
    Sleep    10s

    Click    ${IMAGE_DIR}/new-btn.png
    Sleep    15s

    Input Text    ${IMAGE_DIR}/consolidation-transport.png    ${TRANSPORT}
    Sleep    3s
    
    Input Text    ${IMAGE_DIR}/container-mode.png    ${CONTAINER_MODE}
    Sleep    3s
    
    Input Text    ${IMAGE_DIR}/voyage2.png    ${VOYAGE}
    Sleep    3s
    
    Log    Consolidation created successfully
"""
        
        variables = {
            'TRANSPORT': transport,
            'CONTAINER_MODE': container_mode,
            'FIRST_LOAD': first_load,
            'LAST_LOAD': last_load,
            'VOYAGE': voyage,
            'ETD': etd,
            'ETA': eta,
            'BOL': bol,
            'VESSEL': vessel,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    # Replace the _check_cancellation method:
    async def _check_cancellation(self) -> bool:
        """Check if task has been cancelled using direct database query"""
        if not self.task_id:
            return False
            
        if TaskStatusUtils.is_task_cancelled(self.task_id):
            logger.info(f"Task {self.task_id} has been cancelled, stopping automation")
            # Clean up any running processes
            await self.driver.cancel_running_tasks()
            raise Exception("Task was cancelled by user")
        return False
   
    async def create_consolidation2(self, transport: str, container_mode: str, first_load: str, last_load: str, voyage: str, etd: str, eta: str, bol: str, vessel: str) -> Dict[str, Any]:
        """Create new consolidation part2"""
        # Check for cancellation before starting
        await self._check_cancellation()
        robot_script = """
*** Settings ***
Library    SikuliLibrary

*** Variables ***
${IMAGE_DIR}    ${CURDIR}/cargowise_images
${SCREENSHOT_DIR}    ${SCREENSHOT_DIR}

*** Test Cases ***
Create New Consolidation
    [Documentation]    Create a new consolidation in CargoWise
    
    # Click New Consolidation
    
    

    
    Input Text    ${IMAGE_DIR}/etd2.png    ${ETD}
    Sleep    3s

    Input Text    ${IMAGE_DIR}/eta.png    ${ETA}
    Sleep    3s

    Input Text    ${IMAGE_DIR}/last-load.png    ${LAST_LOAD}
    Sleep    3s
    Input Text    ${IMAGE_DIR}/first-load.png    ${FIRST_LOAD}
    Sleep    3s

    Input Text    ${IMAGE_DIR}/bol.png    ${BOL}
    Sleep    3s
    
    Click    ${IMAGE_DIR}/unlink-vessel.png
    Sleep    3s
    
   
    Click    ${IMAGE_DIR}/save-close-consolidation3.png
    Sleep    15s
    
    Click    ${IMAGE_DIR}/exit-cargowise-white2.png

    Log    Consolidation created successfully
"""
        
        variables = {
            'TRANSPORT': transport,
            'CONTAINER_MODE': container_mode,
            'FIRST_LOAD': first_load,
            'LAST_LOAD': last_load,
            'VOYAGE': voyage,
            'ETD': etd,
            'ETA': eta,
            'BOL': bol,
            'VESSEL': vessel,
            'SCREENSHOT_DIR': str(self.screenshot_dir)
        }
        
        try:
            result = await self.driver.execute_robot_script(
                robot_script, 
                variables=variables,
                task_id=self.task_id
            )
            
            # Check for cancellation after execution
            await self._check_cancellation()
            
            return {
                "success": result["success"],
                "status": "SUCCESS" if result["success"] else "ERROR",
                "outputs": {
                    "consolidation_created": result["success"],
                    "robot_output": result.get("output", ""),
                    "screenshot_dir": str(self.screenshot_dir)
                },
                "error": result.get("error")
            }
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                return {
                    "status": "CANCELED",
                    "success": False,
                    "outputs": {},
                    "error": "Task was cancelled by user"
                }
            raise

    # Replace the _check_cancellation method:
    async def _check_cancellation(self) -> bool:
        """Check if task has been cancelled using direct database query"""
        if not self.task_id:
            return False
            
        if TaskStatusUtils.is_task_cancelled(self.task_id):
            logger.info(f"Task {self.task_id} has been cancelled, stopping automation")
            # Clean up any running processes
            await self.driver.cancel_running_tasks()
            raise Exception("Task was cancelled by user")
        return False

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

 