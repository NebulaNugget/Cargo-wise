# User models
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import uuid
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"

class User(BaseModel):
    """User model for authentication and authorization"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole = UserRole.OPERATOR
    # Multi-tenant fields
    client_id: Optional[str] = None  # For multi-tenant isolation
    client_name: Optional[str] = None  # Name of the client/tenant
    client_email: Optional[str] = None  # Email of the client/tenant
    client_description: Optional[str] = None  # Description of the client/tenant
    is_active: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_login: Optional[datetime] = None
    
    
    # User preferences and settings
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    # Permissions
    can_execute_workflows: bool = True
    can_approve_tasks: bool = False
    can_modify_workflows: bool = False
    can_view_all_clients: bool = False  # Admin-only permission
    
    class Config:
        orm_mode = True

class Client(BaseModel):
    """Client model for multi-tenant isolation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    email: Optional[str]= None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Client-specific settings
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    # RAG configuration
    rag_collection_name: str  # Unique collection name for this client
    rag_enabled: bool = True
    
    class Config:
        orm_mode = True