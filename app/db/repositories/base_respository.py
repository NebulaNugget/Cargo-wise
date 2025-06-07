# Base repository for database operations
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Base repository for database operations"""
    
    def __init__(self, db_session, model_class: Type[T], collection_name: str):
        self.db = db_session
        self.model_class = model_class
        self.collection = db_session[collection_name]
    
    async def create(self, model: T) -> T:
        """Create a new document"""
        model_dict = model.dict()
        await self.collection.insert_one(model_dict)
        return model
    
    async def get(self, id: str) -> Optional[T]:
        """Get document by ID"""
        doc = await self.collection.find_one({"id": id})
        if not doc:
            return None
        return self.model_class(**doc)
    
    async def update(self, id: str, update_data: Dict[str, Any]) -> bool:
        """Update document by ID"""
        result = await self.collection.update_one(
            {"id": id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def delete(self, id: str) -> bool:
        """Delete document by ID"""
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
    
    async def list(self, filter_dict: Dict[str, Any] = None, limit: int = 100) -> List[T]:
        """List documents with optional filtering"""
        filter_dict = filter_dict or {}
        cursor = self.collection.find(filter_dict).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self.model_class(**doc))
        
        return results