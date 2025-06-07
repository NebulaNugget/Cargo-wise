from fastapi import Depends, HTTPException, status
from typing import List, Optional, Callable, Any
from app.models.user import User, UserRole
from app.models.auth import get_current_active_user

class PermissionDependency:
    """Permission dependency for FastAPI endpoints"""
    
    def __init__(
        self, 
        required_roles: List[UserRole] = None,
        check_client_access: bool = True,
        require_active: bool = True,
        custom_check: Optional[Callable[[User], bool]] = None
    ):
        self.required_roles = required_roles or []
        self.check_client_access = check_client_access
        self.require_active = require_active
        self.custom_check = custom_check
    
    async def __call__(self, user: User = Depends(get_current_active_user)) -> User:
        # Check if user is active (if required)
        if self.require_active and not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        # Check roles (if specified)
        if self.required_roles and user.role not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {user.role} not authorized. Required: {self.required_roles}"
            )
        
        # Run custom check (if provided)
        if self.custom_check and not self.custom_check(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied by custom check"
            )
        
        return user

# Common permission dependencies
require_admin = PermissionDependency(required_roles=[UserRole.ADMIN])
require_operator_or_admin = PermissionDependency(required_roles=[UserRole.ADMIN, UserRole.OPERATOR])
require_any_active_user = PermissionDependency()

# Permission checks for specific actions
def can_execute_workflows(user: User) -> bool:
    return user.can_execute_workflows

def can_approve_tasks(user: User) -> bool:
    return user.can_approve_tasks

def can_modify_workflows(user: User) -> bool:
    return user.can_modify_workflows or user.role == UserRole.ADMIN

def can_access_client(user: User, client_id: str) -> bool:
    """Check if user can access a specific client's data"""
    # Admin can access all clients
    if user.role == UserRole.ADMIN and user.can_view_all_clients:
        return True
    
    # Users can only access their assigned client
    return user.client_id == client_id

# Action-specific dependencies
require_workflow_execution = PermissionDependency(
    custom_check=can_execute_workflows
)

require_task_approval = PermissionDependency(
    custom_check=can_approve_tasks
)

require_workflow_modification = PermissionDependency(
    custom_check=can_modify_workflows
)