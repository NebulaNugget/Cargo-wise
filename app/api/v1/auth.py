# Authentication endpoints 
from fastapi import APIRouter, Depends, HTTPException, status, Body, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any, Optional
from datetime import timedelta, datetime
from pydantic import BaseModel, EmailStr, validator

from app.models.auth import (
    authenticate_user, 
    get_password_hash,
)
from app.models.user import User, UserRole, Client
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.client_repository import ClientRepository
from app.db.repositories.token_repository import TokenRepository  # Added missing import
from app.dependencies import get_db
from app.core.auth.permissions import require_admin, require_any_active_user
from app.core.auth.jwt_handler import JWTHandler
from app.core.auth.validator import AuthValidator

router = APIRouter()

class UserResponse(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str 
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    client_id: str
    client_email: str
    client_name: str
    client_description: str
    is_active: bool
    created_at: str
    updated_at: str
    preferences: Dict[str, Any]
    can_execute_workflows: bool
    can_approve_tasks: bool
    can_modify_workflows: bool
    can_view_all_clients: bool
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str
    role: str

class TokenRefresh(BaseModel):
    refresh_token: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    full_name: Optional[str] = None
    role: UserRole = UserRole.OPERATOR
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str]= None
    client_description:Optional[str]=None


    @validator('password')
    def validate_password(cls, v):
        validation = AuthValidator.validate_password(v)
        if not validation["valid"]:
            raise ValueError(f"Password validation failed: {', '.join(validation['errors'])}")
        return v
    
    @validator('email')
    def validate_email(cls, v):
        validation = AuthValidator.validate_email(str(v))
        if not validation["valid"]:
            raise ValueError(f"Email validation failed: {', '.join(validation['errors'])}")
        return v
    
    @validator('username')
    def validate_username(cls, v):
        validation = AuthValidator.validate_username(v)
        if not validation["valid"]:
            raise ValueError(f"Username validation failed: {', '.join(validation['errors'])}")
        return v

class ClientCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rag_enabled: bool = True

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    login_data: LoginRequest,
    db = Depends(get_db)
):
    """Login endpoint to get access token (JSON)"""
    user = await authenticate_user(login_data.username, login_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not active. Please contact your administrator for approval or if your account has been suspended.",
        )
    # Update last login timestamp
    user_repo = UserRepository(db)
    await user_repo.update_last_login(user.id)
    
    # Create token data
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role
    }
    
    # Create access token
    access_token = JWTHandler.create_access_token(token_data)
    
    # Create refresh token
    refresh_token = JWTHandler.create_refresh_token(token_data)
    
    # Store refresh token in database
    token_repo = TokenRepository(db)
    expires_at = datetime.utcnow() + timedelta(days=7)
    await token_repo.create_refresh_token(user.id, refresh_token, expires_at)
    
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        secure=True,  # Only send over HTTPS
        samesite="lax"  # Protect against CSRF
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }

@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,  # Added missing Response parameter
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db)
):
    """Login endpoint to get access token"""
    user = await authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not active. Please contact your administrator for approval or if your account has been suspended.",
        )
    
    # Update last login timestamp
    user_repo = UserRepository(db)
    await user_repo.update_last_login(user.id)
    
    # Create token data
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role
    }
    
    # Create access token
    access_token = JWTHandler.create_access_token(token_data)
    
    # Create refresh token
    refresh_token = JWTHandler.create_refresh_token(token_data)
    
    # Store refresh token in database
    token_repo = TokenRepository(db)
    expires_at = datetime.utcnow() + timedelta(days=7)
    await token_repo.create_refresh_token(user.id, refresh_token, expires_at)
    
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        secure=True,  # Only send over HTTPS
        samesite="lax"  # Protect against CSRF
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    response: Response,
    refresh_data: TokenRefresh = Body(...),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
    db = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Use token from body or cookie
    refresh_token = refresh_data.refresh_token or refresh_token_cookie
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required"
        )
    
    # Validate refresh token
    if not JWTHandler.is_token_valid(refresh_token) or not JWTHandler.is_refresh_token(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Check if token exists in database and is not revoked
    token_repo = TokenRepository(db)
    token_record = await token_repo.get_by_token(refresh_token)
    
    if not token_record or token_record.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )
    
    # Decode token to get user info
    payload = JWTHandler.decode_token(refresh_token)
    user_id = payload.get("user_id")
    username = payload.get("sub")
    role = payload.get("role")
    
    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify user still exists
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    
    if not user or not user.is_active:
        # Revoke token if user doesn't exist or is inactive
        await token_repo.revoke_token(refresh_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    token_data = {
        "sub": username,
        "user_id": user_id,
        "role": role
    }
    
    new_access_token = JWTHandler.create_access_token(token_data)
    new_refresh_token = JWTHandler.create_refresh_token(token_data)
    
    # Revoke old refresh token
    await token_repo.revoke_token(refresh_token)
    
    # Store new refresh token
    expires_at = datetime.utcnow() + timedelta(days=7)
    await token_repo.create_refresh_token(user_id, new_refresh_token, expires_at)
    
    # Set new refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        secure=True,
        samesite="lax"
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username,
        "role": role
    }

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db = Depends(get_db)
):
    """Register a new user"""
    user_repo = UserRepository(db)
    client_repo = ClientRepository(db)
    
    # Check if username already exists
    existing_user = await user_repo.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await user_repo.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Extract role from user_data
    role = user_data.role
    # set is_active based on role
    is_active = True if role == UserRole.ADMIN else False
    client_id = user_data.client_id

    # For admin users registering a new client/tenant
    if role == UserRole.ADMIN:
        if not user_data.client_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client name is required for admin registration"
            ) 
        # Create new client if admin is registering
        import uuid
        rag_collection_name = f"rag_{uuid.uuid4().hex[:8]}"  # Generate a unique RAG collection name
        new_client = Client(
            name=user_data.client_name,
            description=user_data.client_description or "",
            email=user_data.client_email,
            rag_collection_name=rag_collection_name,
            rag_enabled=True
        )
        created_client = await client_repo.create(new_client)
        client_id = created_client.id
    # For non-admin users (operators, viewers)
    else:
        if not user_data.client_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client email is required for non-admin registration"
            )

        # Verify client email exists in the system
        client = await user_repo.get_client_by_email(user_data.client_email)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client email does not exist"
            )
        client_id = client.id
        # Populate client name and description from the found client
        user_data.client_name = client.name
        user_data.client_description = client.description

    # Create new user - moved outside of the if/else blocks
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        full_name=user_data.first_name + " " + user_data.last_name,
        role=role,
        is_active=is_active,
        client_id=client_id,
        client_email=user_data.client_email,
        client_name=user_data.client_name,
        client_description=user_data.client_description,
        # Set permissions based on role
        can_execute_workflows=role != UserRole.VIEWER,
        can_approve_tasks=role != UserRole.VIEWER,
        can_modify_workflows=role == UserRole.ADMIN,
        can_view_all_clients=role == UserRole.ADMIN
    )
    
    created_user = await user_repo.create(new_user)
    
    # Convert to UserResponse (excluding hashed_password)
    return UserResponse(
        id=created_user.id,
        username=created_user.username,
        email=created_user.email,
        full_name=created_user.full_name,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        role=created_user.role,
        client_id=created_user.client_id,
        client_name=created_user.client_name or "",
        client_email=created_user.client_email or "",
        client_description=created_user.client_description or "",  # Add default empty string
        is_active=created_user.is_active,
        created_at=str(created_user.created_at),
        updated_at=str(created_user.updated_at),
        preferences=created_user.preferences or {},
        can_execute_workflows=created_user.can_execute_workflows,
        can_approve_tasks=created_user.can_approve_tasks,
        can_modify_workflows=created_user.can_modify_workflows,
        can_view_all_clients=created_user.can_view_all_clients
    )

@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    db = Depends(get_db)
):
    """Logout user by revoking refresh token"""
    if refresh_token:
        token_repo = TokenRepository(db)
        await token_repo.revoke_token(refresh_token)
    
    # Clear refresh token cookie
    response.delete_cookie(key="refresh_token")
    
    return {"message": "Successfully logged out"}

@router.post("/clients", response_model=Client)
async def create_client(
    client_data: ClientCreate,
    user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """Create a new client (admin only)"""
    client_repo = ClientRepository(db)
    
    # Create a unique RAG collection name
    import uuid
    rag_collection_name = f"rag_{uuid.uuid4().hex[:8]}"
    
    new_client = Client(
        name=client_data.name,
        description=client_data.description,
        rag_collection_name=rag_collection_name,
        rag_enabled=client_data.rag_enabled
    )
    
    return await client_repo.create(new_client)

@router.get("/me", response_model=UserResponse)  # Changed from User to UserResponse
async def get_current_user_info(
    current_user: User = Depends(require_any_active_user)
):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        first_name=current_user.first_name,  # Add this line
        last_name=current_user.last_name, 
        full_name=current_user.first_name + current_user.last_name,
        role=current_user.role,
        client_id=current_user.client_id,
        client_name=current_user.client_name,
        client_email=current_user.client_email,
        client_description=current_user.client_description,
        is_active=current_user.is_active,
        created_at=str(current_user.created_at),
        updated_at=str(current_user.updated_at),
        preferences=current_user.preferences or {},
        can_execute_workflows=current_user.can_execute_workflows,
        can_approve_tasks=current_user.can_approve_tasks,
        can_modify_workflows=current_user.can_modify_workflows,
        can_view_all_clients=current_user.can_view_all_clients
    )

# ... existing code ...

@router.get("/users", response_model=list[UserResponse])
async def get_client_users(
    current_user: User = Depends(require_any_active_user),
    db = Depends(get_db)
):
    """Get all users for the current client"""
    user_repo = UserRepository(db)
    
    # Admin with view_all_clients permission can see all users
    if current_user.role == UserRole.ADMIN and current_user.can_view_all_clients:
        users = await user_repo.get_users_by_client(current_user.client_id)
    else:
        # Regular users can only see users from their client
        users = await user_repo.get_users_by_client(current_user.client_id)
    
    # Convert to UserResponse objects
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            role=user.role,
            client_id=user.client_id,
            client_name=user.client_name or "",
            client_email=user.client_email or "",
            client_description=user.client_description or "",
            is_active=user.is_active,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
            preferences=user.preferences or {},
            can_execute_workflows=user.can_execute_workflows,
            can_approve_tasks=user.can_approve_tasks,
            can_modify_workflows=user.can_modify_workflows,
            can_view_all_clients=user.can_view_all_clients
        ) for user in users
    ]

@router.patch("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: str,
    status_data: dict,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """Update user active status (admin only)"""
    user_repo = UserRepository(db)
    
    # Get the user to update
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update the user's active status
    is_active = status_data.get("is_active", user.is_active)
    
    # Update user in database
    update_data = {
        "is_active": is_active,
        "updated_at": datetime.now().isoformat()
    }
    
    success = await user_repo.update_user(user_id, update_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status"
        )
    
    # Get updated user
    updated_user = await user_repo.get(user_id)
    
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        full_name=updated_user.full_name,
        role=updated_user.role,
        client_id=updated_user.client_id,
        client_name=updated_user.client_name or "",
        client_email=updated_user.client_email or "",
        client_description=updated_user.client_description or "",
        is_active=updated_user.is_active,
        created_at=str(updated_user.created_at),
        updated_at=str(updated_user.updated_at),
        preferences=updated_user.preferences or {},
        can_execute_workflows=updated_user.can_execute_workflows,
        can_approve_tasks=updated_user.can_approve_tasks,
        can_modify_workflows=updated_user.can_modify_workflows,
        can_view_all_clients=updated_user.can_view_all_clients
    )

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """Delete a user (admin only)"""
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user_repo = UserRepository(db)
    
    # Check if user exists
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete the user
    success = await user_repo.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    
    return None  # 204 No Content response
@router.get("/clients", response_model=list[Client])
async def list_clients(
    user: User = Depends(require_any_active_user),
    db = Depends(get_db)
):
    """List clients (filtered by user permissions)"""
    client_repo = ClientRepository(db)
    
    # Admin with view_all_clients permission can see all clients
    if user.role == UserRole.ADMIN and user.can_view_all_clients:
        return await client_repo.list()
    
    # Other users can only see their assigned client
    client = await client_repo.get(user.client_id)
    return [client] if client else []