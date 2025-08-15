# Intent parser for natural language queries
from typing import Dict, Any, Tuple, List, Optional
import re
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
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
        self.default_confidence_threshold = float(os.getenv('INTENT_CONFIDENCE_THRESHOLD', '0.9'))
        
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize regex patterns for intent matching"""
        low_confidence = float(os.getenv('LOW_CONFIDENCE_THRESHOLD', '0.5'))
        medium_confidence = float(os.getenv('MEDIUM_CONFIDENCE_THRESHOLD', '0.7'))
        high_confidence = float(os.getenv('HIGH_CONFIDENCE_THRESHOLD', '0.75'))
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
                "confidence": low_confidence
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
                "confidence": medium_confidence
            },
             "create_shipment": {
                "patterns": [
                    r"(?i)create\s+(?:a\s+)?(?:new\s+)?shipment",
                    r"(?i)make\s+(?:a\s+)?(?:new\s+)?shipment",
                    r"(?i)add\s+(?:a\s+)?(?:new\s+)?shipment",
                    r"(?i)new\s+shipment"
                ],
                "param_patterns": {
                    "weight": r"(?i)(?:weight|wt)[:\s]+([^,]+?)(?:,|\s+kg|\s+lbs|\s+tons|\s+and|\s+with|\s*$)",
                    "consignor": r"(?i)(?:consignor|sender|from)[:\s]+([^,]+?)(?:,|\s+to|\s+with|\s+and|\s*$)",
                    "transport_method": r"(?i)(?:transport|method|via|by)[:\s]+([^,]+?)(?:,|\s+with|\s+and|\s*$)",
                    "description": r"(?i)(?:description|desc|details)[:\s]+([^,]+?)(?:,|\s+and|\s*$)",
                    "login_password": r"(?i)(?:password|pass)[:\s]+([^\s,]+)"
                },
                "confidence": high_confidence
            },
            "search_shipment_by_housebill": {
                "patterns": [
                    r"(?i)search\s+(?:for\s+)?(?:a\s+)?shipment\s+(?:by\s+)?housebill",
                    r"(?i)find\s+(?:a\s+)?shipment\s+(?:by\s+)?housebill",
                    r"(?i)look\s+(?:up|for)\s+(?:a\s+)?shipment\s+(?:by\s+)?housebill",
                    r"(?i)search\s+housebill",
                    r"(?i)find\s+housebill"
                ],
                "param_patterns": {
                    "housebill": r"(?i)(?:housebill|house\s+bill|hbl)[:\s]+([^\s,]+)",
                    "login_password": r"(?i)(?:password|pass)[:\s]+([^\s,]+)"
                },
                "confidence": high_confidence
            },
            "search_consolidation_by_referencenumber": {
                "patterns": [
                    r"(?i)search\s+(?:for\s+)?(?:a\s+)?consolidation\s+(?:by\s+)?referencenumber",
                    r"(?i)find\s+(?:a\s+)?consolidation\s+(?:by\s+)?referencenumber",
                    r"(?i)look\s+(?:up|for)\s+(?:a\s+)?consolidation\s+(?:by\s+)?referencenumber",
                    r"(?i)search\s+referencenumber",
                    r"(?i)find\s+referencenumber"
                ],
                "param_patterns": {
                    "referencenumber": r"(?i)(?:referencenumber|reference\s+number|rfn)[:\s]+([^\s,]+)",
                    "login_password": r"(?i)(?:password|pass)[:\s]+([^\s,]+)"
                },
                "confidence": high_confidence
            },
            "create_consolidation": {
                "patterns": [
                    r"(?i)create\s+(?:a\s+)?(?:new\s+)?consolidation",
                    r"(?i)make\s+(?:a\s+)?(?:new\s+)?consolidation",
                    r"(?i)add\s+(?:a\s+)?(?:new\s+)?consolidation",
                    r"(?i)new\s+consolidation",
                    r"(?i)consolidate\s+(?:shipments?|cargo)"
                ],
                "param_patterns": {
                    "transport": r"(?i)(?:transport|method|via|by)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "container_mode": r"(?i)(?:container\s+mode|mode)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "first_load": r"(?i)(?:first\s+load|first)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "last_load": r"(?i)(?:last\s+load|last)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "voyage": r"(?i)voyage[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "etd": r"(?i)(?:etd|departure)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "eta": r"(?i)(?:eta|arrival)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "bol": r"(?i)(?:bol|bill\s+of\s+lading)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "vessel": r"(?i)vessel[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "login_password": r"(?i)(?:password|pass)[:\s]+([^\s,]+)"
                },
                "confidence": high_confidence
            }
            ,
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
            },
            "create_order": {
                "patterns": [
                    r"(?i)create\s+(?:a\s+)?(?:new\s+)?order",
                    r"(?i)make\s+(?:a\s+)?(?:new\s+)?order",
                    r"(?i)add\s+(?:a\s+)?(?:new\s+)?order",
                    r"(?i)new\s+order"
                ],
                "param_patterns": {
                    "buyer": r"(?i)(?:buyer|customer)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "supplier": r"(?i)(?:supplier|vendor)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "container_return_date": r"(?i)(?:container\s+return\s+date|return\s+date)[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "sanction": r"(?i)sanction[:\s]+([^,]+?)(?:,|\s+and|\s+with|\s*$)",
                    "login_password": r"(?i)(?:password|pass)[:\s]+([^\s,]+)"
                },
                "confidence": high_confidence
            },
            
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
                        best_confidence = min(confidence, 0.85)  # Cap at 0.95
                        best_params = params
                    
                    break  # No need to check other patterns for this intent
        
        # If no intent matched, use a fallback
        if not best_intent:
            best_intent = "unknown"
            best_confidence = 0.3
            best_params = {}
            
            # Try to extract some basic parameters anyway
            if "shipment" in query.lower():
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
            "create_order": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": intent.parameters.get("login_password", "${password}"),
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_order",
                    "description": "Create a new order in CargoWise",
                    "parameters": {
                        "buyer": intent.parameters.get("buyer", "${buyer}"),
                        "supplier": intent.parameters.get("supplier", "${supplier}"),
                        "container_return_date": intent.parameters.get("container_return_date", "${container_return_date}"),
                        "sanction": intent.parameters.get("sanction", "${sanction}")
                    }
                }
            ],
            "create_shipment": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": intent.parameters.get("login_password", "${password}"),
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_shipment",
                    "description": "Create a new shipment in CargoWise",
                    "parameters": {
                        "weight": intent.parameters.get("weight", "${weight}"),
                        "consignor": intent.parameters.get("consignor", "${consignor}"),
                        "transport_method": intent.parameters.get("transport_method", "${transport_method}"),
                        "description": intent.parameters.get("description", "${description}")
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
            ],

            "search_shipment_by_housebill":[
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": intent.parameters.get("login_password", "${password}"),
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_shipment_by_housebill",
                    "description": "Search for a shipment by housebill in CargoWise",
                    "parameters": {
                        "housebill": intent.parameters.get("housebill", "${housebill}")
                    }
                }
            ],

            "search_consolidation_by_referencenumber":[
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": intent.parameters.get("login_password", "${password}"),
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_search_consolidation_by_referencenumber",
                    "description": "Search for a consolidation in CargoWise",
                    "parameters": {
                        "housebill": intent.parameters.get("referencenumber", "${housebill}")
                    }
                }
            ],

            "create_consolidation": [
                {
                    "name": "cargowise_login",
                    "description": "Log into CargoWise",
                    "parameters": {
                        "username": "${username}",
                        "password": intent.parameters.get("login_password", "${password}"),
                        "environment": "desktop"
                    }
                },
                {
                    "name": "cargowise_create_consolidation",
                    "description": "Create a new consolidation in CargoWise",
                    "parameters": {
                        "transport": intent.parameters.get("transport", "${transport}"),
                        "container_mode": intent.parameters.get("container_mode", "${container_mode}"),
                        "first_load": intent.parameters.get("first_load", "${first_load}"),
                        "last_load": intent.parameters.get("last_load", "${last_load}"),
                        "voyage": intent.parameters.get("voyage", "${voyage}"),
                        "etd": intent.parameters.get("etd", "${etd}"),
                        "eta": intent.parameters.get("eta", "${eta}"),
                        "bol": intent.parameters.get("bol", "${bol}"),
                        "vessel": intent.parameters.get("vessel", "${vessel}")
                    }
                }
            ],
        }
        
        return intent_to_tools.get(intent.intent_name, [])