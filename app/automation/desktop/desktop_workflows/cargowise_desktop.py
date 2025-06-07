from app.automation.desktop.desktop_workflow.base_workflow import DesktopWorkflow
from typing import Dict, Any, List

class CargoWiseLoginWorkflow(DesktopWorkflow):
    """Workflow for logging into CargoWise desktop application"""
    
    def __init__(self):
        super().__init__(
            name="cargowise_login",
            description="Log into CargoWise desktop application"
        )
    
    def _initialize_steps(self) -> None:
        self.steps = [
            {
                "description": "Launch CargoWise application",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${cargowise_icon}",
                    "timeout": 10
                },
                "output_key": "launch_result",
                "abort_on_failure": True
            },
            {
                "description": "Wait for login screen",
                "tool": "desktop_wait_image",
                "parameters": {
                    "image_base64": "${login_screen}",
                    "timeout": 20
                },
                "abort_on_failure": True
            },
            {
                "description": "Click username field",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${username_field}",
                    "timeout": 5
                }
            },
            {
                "description": "Enter username",
                "tool": "desktop_type_text",
                "parameters": {
                    "text": "${username}"
                }
            },
            {
                "description": "Click password field",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${password_field}",
                    "timeout": 5
                }
            },
            {
                "description": "Enter password",
                "tool": "desktop_type_text",
                "parameters": {
                    "text": "${password}"
                }
            },
            {
                "description": "Click login button",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${login_button}",
                    "timeout": 5
                }
            },
            {
                "description": "Verify successful login",
                "tool": "desktop_wait_image",
                "parameters": {
                    "image_base64": "${dashboard_screen}",
                    "timeout": 30
                },
                "output_key": "login_verification"
            }
        ]

class CargoWiseCreateBookingWorkflow(DesktopWorkflow):
    """Workflow for creating a new booking in CargoWise"""
    
    def __init__(self):
        super().__init__(
            name="cargowise_create_booking",
            description="Create a new booking in CargoWise"
        )
    
    def _initialize_steps(self) -> None:
        self.steps = [
            {
                "description": "Click 'New Booking' button",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${new_booking_button}",
                    "timeout": 10
                },
                "abort_on_failure": True
            },
            {
                "description": "Wait for booking form",
                "tool": "desktop_wait_image",
                "parameters": {
                    "image_base64": "${booking_form}",
                    "timeout": 15
                }
            },
            {
                "description": "Enter customer reference",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${customer_ref_field}",
                    "timeout": 5
                }
            },
            {
                "description": "Type customer reference",
                "tool": "desktop_type_text",
                "parameters": {
                    "text": "${customer_reference}"
                }
            },
            {
                "description": "Select origin",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${origin_field}",
                    "timeout": 5
                }
            },
            {
                "description": "Type origin",
                "tool": "desktop_type_text",
                "parameters": {
                    "text": "${origin}"
                }
            },
            {
                "description": "Select destination",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${destination_field}",
                    "timeout": 5
                }
            },
            {
                "description": "Type destination",
                "tool": "desktop_type_text",
                "parameters": {
                    "text": "${destination}"
                }
            },
            {
                "description": "Click save button",
                "tool": "desktop_click_image",
                "parameters": {
                    "image_base64": "${save_button}",
                    "timeout": 5
                }
            },
            {
                "description": "Verify booking created",
                "tool": "desktop_wait_image",
                "parameters": {
                    "image_base64": "${booking_confirmation}",
                    "timeout": 20
                },
                "output_key": "booking_result"
            }
        ]