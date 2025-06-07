# HITL (Human-In-The-Loop) models
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class HITLConfig(BaseModel):
    """Configuration for Human-In-The-Loop settings"""
    confidence_threshold: float = Field(
        default=0.7, 
        description="Minimum confidence level required to proceed without human approval"
    )
    critical_operations: List[str] = Field(
        default_factory=list,
        description="List of operations that always require human approval regardless of confidence"
    )
    auto_approve_tools: List[str] = Field(
        default_factory=list,
        description="List of tools that can be auto-approved regardless of confidence"
    )
    max_auto_retries: int = Field(
        default=3,
        description="Maximum number of automatic retries before requiring human intervention"
    )
    approval_timeout_seconds: int = Field(
        default=3600,  # 1 hour
        description="Time in seconds before a paused task is flagged for attention"
    )
    default_reviewers: List[str] = Field(
        default_factory=list,
        description="Default reviewers for tasks requiring approval"
    )
    escalation_timeout: int = Field(
        default=7200,  # 2 hours
        description="Time in seconds before escalating to additional reviewers"
    )

class HITLApproval(BaseModel):
    """Human approval data for a paused task"""
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Updated context values for the task"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes from the human operator"
    )
    override_confidence: Optional[float] = Field(
        default=None,
        description="Optional confidence override for future similar operations"
    )
    modified_parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Modified parameters for the task execution"
    )
    modified_tools: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Modified tool configurations if needed"
    )
    reviewer_id: Optional[str] = Field(
        default=None,
        description="ID of the reviewer who approved the task"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp of the approval"
    )

class HITLRejection(BaseModel):
    """Human rejection data for a paused task"""
    reason: str = Field(
        description="Reason for rejecting the task"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes from the human operator"
    )
    trigger_alternative: bool = Field(
        default=False,
        description="Whether to trigger an alternative flow"
    )
    alternative_flow: Optional[str] = Field(
        default=None,
        description="Name of alternative flow to trigger if applicable"
    )
    reviewer_id: Optional[str] = Field(
        default=None,
        description="ID of the reviewer who rejected the task"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp of the rejection"
    )

class HITLFeedback(BaseModel):
    """Feedback on a completed task for continuous improvement"""
    task_id: str = Field(
        description="ID of the task this feedback relates to"
    )
    rating: int = Field(
        ..., 
        ge=1, 
        le=5,
        description="Rating from 1-5 where 5 is best"
    )
    feedback: Optional[str] = Field(
        default=None,
        description="Detailed feedback text"
    )
    success: bool = Field(
        default=True,
        description="Whether the task was ultimately successful"
    )
    issues: Optional[List[str]] = Field(
        default=None,
        description="List of specific issues encountered"
    )
    suggestions: Optional[str] = Field(
        default=None,
        description="Suggestions for improvement"
    )
    reviewer_id: Optional[str] = Field(
        default=None,
        description="ID of the person providing feedback"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp of the feedback submission"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "rating": 4,
                "feedback": "Task completed successfully but took longer than expected",
                "success": True,
                "issues": ["Slow response time"],
                "suggestions": "Optimize the login process",
                "reviewer_id": "user123"
            }
        }