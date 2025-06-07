#log models
# Log data models
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

class LogLevel(str, Enum):
    """Log severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogSource(str, Enum):
    """Log source types"""
    API = "API"
    TASK = "TASK"
    TOOL = "TOOL"
    BROWSER = "BROWSER"
    DESKTOP = "DESKTOP"
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"

class LogEntry(BaseModel):
    """Log entry model"""
    id: str = Field(..., description="Unique log entry ID")
    timestamp: datetime = Field(..., description="Log timestamp")
    level: LogLevel = Field(..., description="Log severity level")
    source: LogSource = Field(..., description="Log source")
    message: str = Field(..., description="Log message")
    task_id: Optional[str] = Field(None, description="Associated task ID")
    tool_name: Optional[str] = Field(None, description="Associated tool name")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "log_123456789",
                "timestamp": "2023-06-01T12:34:56.789Z",
                "level": "INFO",
                "source": "TASK",
                "message": "Task execution started",
                "task_id": "task_123456789",
                "tool_name": "cargowise_login",
                "metadata": {
                    "user_id": "user_123",
                    "client_ip": "192.168.1.1",
                    "execution_time_ms": 123
                }
            }
        }

class LogStats(BaseModel):
    """Log statistics model"""
    total_count: int = Field(..., description="Total number of logs")
    level_counts: Dict[str, int] = Field(..., description="Counts by log level")
    source_counts: Dict[str, int] = Field(..., description="Counts by log source")
    hourly_counts: List[Dict[str, Any]] = Field(..., description="Counts by hour")
    top_tasks: List[Dict[str, Any]] = Field(..., description="Most logged tasks")
    top_errors: List[Dict[str, Any]] = Field(..., description="Most common errors")