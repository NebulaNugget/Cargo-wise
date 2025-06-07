from app.db.repositories.base_respository import BaseRepository
from typing import Optional, List
from datetime import datetime
import uuid

class RefreshToken:
    """Refresh token model"""
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        token: str = None,
        expires_at: str = None,
        created_at: str = None,
        revoked: bool = False,
        revoked_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now().isoformat()
        self.revoked = revoked
        self.revoked_at = revoked_at
    
    def dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "revoked": self.revoked,
            "revoked_at": self.revoked_at
        }

class TokenRepository:
    """Repository for token operations"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.collection = db_session["refresh_tokens"]
    
    async def create_refresh_token(self, user_id: str, token: str, expires_at: datetime) -> RefreshToken:
        """Create a new refresh token"""
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at.isoformat()
        )
        
        await self.collection.insert_one(refresh_token.dict())
        return refresh_token
    
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token value"""
        doc = await self.collection.find_one({"token": token})
        if not doc:
            return None
        return RefreshToken(**doc)
    
    async def revoke_token(self, token: str) -> bool:
        """Revoke a refresh token"""
        result = await self.collection.update_one(
            {"token": token},
            {"$set": {
                "revoked": True,
                "revoked_at": datetime.now().isoformat()
            }}
        )
        return result.modified_count > 0
    
    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user"""
        result = await self.collection.update_many(
            {"user_id": user_id, "revoked": False},
            {"$set": {
                "revoked": True,
                "revoked_at": datetime.now().isoformat()
            }}
        )
        return result.modified_count
    
    async def cleanup_expired_tokens(self) -> int:
        """Delete expired tokens"""
        now = datetime.now().isoformat()
        result = await self.collection.delete_many({
            "$or": [
                {"expires_at": {"$lt": now}},
                {"revoked": True}
            ]
        })
        return result.deleted_count