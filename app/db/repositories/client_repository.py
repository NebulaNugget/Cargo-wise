from app.db.repositories.base_respository import BaseRepository
from app.models.user import Client
from typing import Optional

class ClientRepository(BaseRepository[Client]):
    """Repository for client operations"""
    
    def __init__(self, db_session):
        super().__init__(db_session, Client, "clients")
    
    async def get_by_name(self, name: str) -> Optional[Client]:
        """Get client by name"""
        doc = await self.collection.find_one({"name": name})
        if not doc:
            return None
        return Client(**doc)

    async def get_by_email(self, email: str) -> Optional[Client]:
        """Get client by name"""
        doc = await self.collection.find_one({"email":email})
        if not doc:
            return None
        return Client(**doc)
    
    async def get_default_client(self) -> Optional[Client]:
        """Get the default client"""
        # Try to find a client with "Default" in the name
        doc = await self.collection.find_one({"name": {"$regex": "Default", "$options": "i"}})
        if doc:
            return Client(**doc)
        
        # If no default client found, return the first client
        cursor = self.collection.find().limit(1)
        async for doc in cursor:
            return Client(**doc)
        
        return None