from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, AsyncGenerator
from pydantic import BaseModel
import os
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseSettings(BaseModel):
    """Database connection settings"""
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb+srv://allensteadson:Xl5EDPkL6qSwUprr@cluster0.pzstbpn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    database_name: str = os.getenv("DATABASE_NAME", "cargowise_automation")

class Database:
    client: Optional[AsyncIOMotorClient] = None
    settings: DatabaseSettings = DatabaseSettings()
    
    def __init__(self, settings: Optional[DatabaseSettings] = None):
        if settings:
            self.settings = settings
    
    async def connect(self):
        """Connect to MongoDB"""
        if self.client is None:
            try:
                self.client = AsyncIOMotorClient(self.settings.mongo_uri)
                logger.info(f"Connected to MongoDB at {self.settings.mongo_uri}")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Disconnected from MongoDB")
    
    @property
    def db(self):
        """Get database instance"""
        if not self.client:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.client[self.settings.database_name]

# Create a global database instance
db = Database()

@asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    """Context manager for database sessions"""
    # We don't need to connect here since we're connecting on app startup
    # This just ensures we have a valid connection
    if db.client is None:
        await db.connect()
    try:
        yield db.db
    finally:
        # We don't disconnect here since we're managing connection in app lifecycle
        pass