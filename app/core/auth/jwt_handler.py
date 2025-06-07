from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwt, JWTError
import os
import logging
import uuid
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY_HERE")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenPayload(BaseModel):
    """JWT token payload structure"""
    sub: str  # Subject (username)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at
    jti: str  # JWT ID (unique identifier)
    type: str  # Token type (access or refresh)
    user_id: str  # User ID
    role: str  # User role

class JWTHandler:
    """JWT token handler for authentication"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        """Create a new access token"""
        to_encode = data.copy()
        
        # Set expiration time
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Add token metadata
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4()),
            "type": "access"
        })
        
        # Encode the JWT
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create a new refresh token"""
        to_encode = data.copy()
        
        # Set expiration time (longer than access token)
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Add token metadata
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4()),
            "type": "refresh"
        })
        
        # Encode the JWT
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            return None
    
    @staticmethod
    def is_token_valid(token: str) -> bool:
        """Check if a token is valid"""
        payload = JWTHandler.decode_token(token)
        if not payload:
            return False
            
        # Check if token is expired
        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp) < datetime.utcnow():
            return False
            
        return True
    
    @staticmethod
    def is_refresh_token(token: str) -> bool:
        """Check if a token is a refresh token"""
        payload = JWTHandler.decode_token(token)
        if not payload:
            return False
            
        return payload.get("type") == "refresh"