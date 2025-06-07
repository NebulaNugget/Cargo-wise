# Intent parser for natural language queries
from typing import Dict, Any, Tuple, List, Optional
import re
import logging
from app.core.marc1.protocol import Marc1Intent

logger = logging.getLogger(__name__)

class IntentParser:
    """
    Parses natural language queries to extract intents and parameters
    
    In Phase 1, this uses simple rule-based matching.
    In Phase 3, this will be replaced with LLM-based processing.
    """
    
    def __init__(self):
        self.intent_patterns = self._initialize_patterns()
        
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize regex patterns for intent matching"""
        return {
            "cargowise_login": {
                "patterns": [
                    r"(?i)log\s*in\s+to\s+cargowise",
                    r"(?i)login\s+to\s+cargowise",
                    r"(?i)access\s+cargowise",
                    r"(?i)open\s+cargowise"
                ],
                "param_patterns": {
                    "username": r"(?i)username[:\s]+([^\s]+)",
                    "password": r"(?i)password[:\s]+([^\s]+)",
                    "environment": r"(?i)environment[:\s]+([^\s]+)"
                },
                "confidence": 0.8
            },
            "create_booking": {
                "patterns": [
                    r"(?i)create\s+(?:a\s+)?(?:new\s+)?booking",
                    r"(?i)make\s+(?:a\s+)?(?:new\s+)?booking",
                    r"(?i)add\s+(?:a\s+)?(?:new\s+)?booking"
                ],
                "param_patterns": {
                    "customer": r"(?i)(?:for|customer)[:\s]+([^,]+?)(?:,|\s+from|\s+to|\s+with|\s+and|\s+at|\s*$)",
                    "origin": r"(?i)(?:from|origin)[:\s]+([^,]+?)(?:,|\s+to|\s+with|\s+and|\s+at|\s*$)",
                    "destination": r"(?i)(?:to|destination)[:\s]+([^,]+?)(?:,|\s+with|\s+and|\s+at|\s*$)",
                    "cargo_details": r"(?i)(?:with|cargo)[:\s]+([^,]+?)(?:,|\s+and|\s+at|\s*$)"
                },
                "confidence": 0.75
            },
            "search_booking": {
                "patterns": [
                    r"(?i)search\s+(?:for\s+)?(?:a\s+)?booking",
                    r"(?i)find\s+(?:a\s+)?booking",
                    r"(?i)look\s+(?:up|for)\s+(?:a\s+)?booking"
                ],
                "param_patterns": {
                    "booking_reference": r"(?i)(?:reference|ref|number)[:\s]+([^\s,]+)",
                    "customer": r"(?i)(?:for|customer)[:\s]+([^,]+?)(?:,|\s+with|\s+and|\s+at|\s*$)"
                },
                "confidence": 0.7
            },
            "track_shipment": {
                "patterns": [
                    r"(?i)track\s+(?:a\s+)?shipment",
                    r"(?i)check\s+(?:the\s+)?status\s+of\s+(?:a\s+)?shipment",
                    r"(?i)where\s+is\s+(?:my|the)\s+shipment"
                ],
                "param_patterns": {
                    "tracking_number": r"(?i)(?:tracking|number|reference|ref)[:\s]+([^\s,]+)",
                    "container_number": r"(?i)container[:\s]+([^\s,]+)"
                },
                "confidence": 0.7
            }
        }
    
    def parse_query(self, query: str) -> Tuple[Marc1Intent, List[Dict[str, Any]]]:
        """
        Parse a natural language query to extract intent and parameters
        
        Args:
            query: The natural language query
            
        Returns:
            A tuple of (Marc1Intent, suggested_tools)
        """
        best_intent = None
        best_confidence = 0.0
        best_params = {}
        # Add debug logging for the query
        logger.info(f"Parsing query: {query}")
        
        # Try to match against known patterns
        for intent_name, intent_config in self.intent_patterns.items():
            # Check if any pattern matches
            for pattern in intent_config["patterns"]:
                if re.search(pattern, query):
                    confidence = intent_config["confidence"]
                    
                    # Extract parameters
                    params = {}
                    for param_name, param_pattern in intent_config["param_patterns"].items():
                        match = re.search(param_pattern, query)
                        if match:
                            params[param_name] = match.group(1).strip()
                            # Boost confidence if we found parameters
                            confidence += 0.05
                            # Add debug logging
                            logger.debug(f"Extracted parameter {param_name}: {params[param_name]} using pattern {param_pattern}")
                        else:
                            logger.debug(f"Failed to extract parameter {param_name} using pattern {param_pattern}")
                    
                    # If this is the best match so far, update
                    if confidence > best_confidence:
                        best_intent = intent_name
                        best_confidence = min(confidence, 0.95)  # Cap at 0.95
                        best_params = params
                    
                    break  # No need to check other patterns for this intent
        
        # If no intent matched, use a fallback
        if not best_intent:
            best_intent = "unknown"
            best_confidence = 0.3
            best_params = {}
            
            # Try to extract some basic parameters anyway
            if "booking" in query.lower():
                if "create" in query.lower() or "new" in query.lower() or "make" in query.lower():
                    best_intent = "create_booking"
                    best_confidence = 0.4
                elif "search" in query.lower() or "find" in query.lower() or "look" in query.lower():
                    best_intent = "search_booking"
                    best_confidence = 0.4
        
        # Create Marc1Intent object
        intent = Marc1Intent(
            intent_name=best_intent,
            confidence=best_confidence,
            parameters=best_params,
            raw_query=query
        )
        
        # Determine suggested tools based on intent
        suggested_tools = self._get_suggested_tools(intent)
        
        return intent, suggested_tools
    
    def _get_suggested_tools(self, intent: Marc1Intent) -> List[Dict[str, Any]]:
        """
        Get suggested tools based on the extracted intent
        
        Args:
            intent: The extracted intent
            
        Returns:
            A list of tool configurations
        """
        # Map intents to tool configurations
        intent_to_tools = {
            "cargowise_login": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": intent.parameters.get("username", "${username}"),
                        "password": intent.parameters.get("password", "${password}"),
                        "environment": intent.parameters.get("environment", "web")
                    }
                }
            ],
            "create_booking": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_booking",
                    "description": "Create a new booking in CargoWise",
                    "parameters": {
                        "customer": intent.parameters.get("customer", "${customer}"),
                        "origin": intent.parameters.get("origin", "${origin}"),
                        "destination": intent.parameters.get("destination", "${destination}"),
                        "cargo_details": intent.parameters.get("cargo_details", "${cargo_details}")
                    }
                }
            ],
            "search_booking": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_booking",
                    "description": "Search for a booking in CargoWise",
                    "parameters": {
                        "booking_reference": intent.parameters.get("booking_reference", "${booking_reference}")
                    }
                }
            ],
            "track_shipment": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": "${password}",
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_track_shipment",
                    "description": "Track a shipment in CargoWise",
                    "parameters": {
                        "tracking_number": intent.parameters.get("tracking_number", "${tracking_number}"),
                        "container_number": intent.parameters.get("container_number", "${container_number}")
                    }
                }
            ]
        }
        
        return intent_to_tools.get(intent.intent_name, [])