from app.db.repositories.base_respository import BaseRepository
from app.models.user import User, Client
from typing import Optional, List, Dict, Any

class UserRepository(BaseRepository[User]):
    """Repository for user operations"""
    
    def __init__(self, db_session):
        super().__init__(db_session, User, "users")
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        doc = await self.collection.find_one({"username": username})
        if not doc:
            return None
        return User(**doc)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        doc = await self.collection.find_one({"email": email})
        if not doc:
            return None
        return User(**doc)
    
    async def count_users(self) -> int:
        """Count total users"""
        return await self.collection.count_documents({})
    
    async def get_active_users(self) -> List[User]:
        """Get all active users"""
        cursor = self.collection.find({"is_active": True})
        results = []
        async for doc in cursor:
            results.append(User(**doc))
        return results

    
    async def get_pending_users(self) -> List[User]:
        """ Get all pending users """
        cursor = self.collection.find({"is_active": False})
        results = []
        async for doc in cursor:
            results.append(User(**doc))
        return results

    async def update_user(self, user_id:str, data: dict) -> bool:
        """Update user information"""
        result = await self.collection.update_one({"id": user_id}, {"$set": data})
        return result.modified_count > 0

    async def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        result = await self.collection.delete_one({"id": user_id})
        return result.deleted_count > 0

    async def get_users_by_client(self, client_id: str) -> List[User]:
        """Get all users for a specific client"""
        cursor = self.collection.find({"client_id": client_id})
        
        results = []
        async for doc in cursor:
            results.append(User(**doc))
        
        return results
    
    async def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        from datetime import datetime
        
        result = await self.collection.update_one(
            {"id": user_id},
            {"$set": {"last_login": datetime.now().isoformat()}}
        )
        
        return result.modified_count > 0
    async def get_client_by_email(self, email: str) -> Optional[Client]:
        """Get client by email"""
        # Access the clients collection
        clients_collection = self.db.get_collection("clients")
        doc = await clients_collection.find_one({"email": email})
        if not doc:
            return None
        return Client(**doc)

   