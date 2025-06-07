# Task models
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from enum import Enum

class TaskStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"  # Added PENDING for NLP processing
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

class TaskState(BaseModel):
    """Current state of a task"""
    task_id: str
    status: TaskStatus = TaskStatus.CREATED
    step_index: int = 0
    current_tool: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    requires_approval: bool = False  # Add this field
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Make sure metadata field exists
    
    class Config:
        schema_extra = {
            "example": {
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "RUNNING",
                "step_index": 2,
                "current_tool": "browser_navigate",
                "parameters": {"url": "https://example.com"},
                "outputs": {"status": "success"},
                "context": {"session_id": "abc123"},
                "updated_at": "2023-06-01T12:34:56.789Z",
                "requires_approval": False,
                "metadata": {"source": "api"}
            }
        }

class Task(BaseModel):
    """Task model for workflow execution"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_id: Optional[str] = None
    workflow_type: str = "standard"  # Can be "standard", "nlp_query", etc.
    query: Optional[str] = None  # Added for natural language queries
    parameters: Dict[str, Any] = Field(default_factory=dict)
    tools: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    current_state: Optional[TaskState] = None
    history: List[TaskState] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    user_id: Optional[str] = None
    client_id: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "workflow_id": "cargowise_booking",
                "parameters": {"booking_ref": "BK12345"},
                "created_at": "2023-01-01T12:00:00Z"
            }
        }

# Add the missing TaskCreate and TaskUpdate classes
class TaskCreate(BaseModel):
    """Model for creating a new task"""
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_id: Optional[str] = None
    workflow_type: str = "standard"
    tools: List[Dict[str, Any]] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    auto_execute: bool = True
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Process Booking",
                "description": "Process a new CargoWise booking",
                "workflow_id": "cargowise_booking",
                "workflow_type": "standard",
                "tools": [
                    {"name": "browser_navigate", "parameters": {"url": "https://example.com"}},
                    {"name": "form_fill", "parameters": {"field_id": "booking_ref", "value": "BK12345"}}
                ],
                "parameters": {"booking_ref": "BK12345"},
                "auto_execute": True
            }
        }

class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Updated Task Name",
                "parameters": {"booking_ref": "BK67890"}
            }
        }