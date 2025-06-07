from app.db.database import get_db_session

async def get_db():
    """Get database session for dependency injection"""
    async with get_db_session() as db:
        yield db