# Core protocol definitions
# Core protocol definitions
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Marc1ProtocolVersion(str, Enum):
    """MARC-1 Protocol versions"""
    V1 = "1.0"
    V1_1 = "1.1"  # Added NLP support

class Marc1MessageType(str, Enum):
    """Types of MARC-1 messages"""
    COMMAND = "command"
    RESPONSE = "response"
    EVENT = "event"
    QUERY = "query"  # Natural language query
    INTENT = "intent"  # Extracted intent

class Marc1Intent(BaseModel):
    """Representation of an extracted intent from natural language"""
    intent_name: str
    confidence: float = 1.0
    parameters: Dict[str, Any] = Field(default_factory=dict)
    raw_query: str
    extracted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "intent_name": "create_booking",
                "confidence": 0.92,
                "parameters": {
                    "customer": "Acme Inc",
                    "origin": "Shanghai",
                    "destination": "Los Angeles"
                },
                "raw_query": "Create a new booking for Acme Inc from Shanghai to Los Angeles"
            }
        }

class Marc1Command(BaseModel):
    """Command message in MARC-1 protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Marc1MessageType = Marc1MessageType.COMMAND
    tool: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "id": "cmd-123e4567-e89b-12d3-a456-426614174000",
                "type": "command",
                "tool": "browser_navigate",
                "parameters": {"url": "https://example.com"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class Marc1Response(BaseModel):
    """Response message in MARC-1 protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    command_id: str
    type: Marc1MessageType = Marc1MessageType.RESPONSE
    status: str  # SUCCESS, ERROR, etc.
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "id": "resp-123e4567-e89b-12d3-a456-426614174000",
                "command_id": "cmd-123e4567-e89b-12d3-a456-426614174000",
                "type": "response",
                "status": "SUCCESS",
                "outputs": {"title": "Example Domain"},
                "timestamp": "2023-01-01T12:00:01Z"
            }
        }

class Marc1Event(BaseModel):
    """Event message in MARC-1 protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Marc1MessageType = Marc1MessageType.EVENT
    event_type: str  # log, state_change, etc.
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "id": "evt-123e4567-e89b-12d3-a456-426614174000",
                "type": "event",
                "event_type": "log",
                "data": {"level": "info", "message": "Navigation complete"},
                "timestamp": "2023-01-01T12:00:01Z"
            }
        }

class Marc1Query(BaseModel):
    """Natural language query in MARC-1 protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Marc1MessageType = Marc1MessageType.QUERY
    query: str
    context: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "id": "q-123e4567-e89b-12d3-a456-426614174000",
                "type": "query",
                "query": "Create a new booking for Acme Inc from Shanghai to Los Angeles",
                "context": {"user_id": "user123"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }