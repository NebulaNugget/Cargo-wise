from typing import Optional
from pymongo import MongoClient
from app.models.task import TaskStatus
import os
import logging

logger = logging.getLogger(__name__)

class TaskStatusUtils:
    """Utility class for checking task status directly from database"""
    
    _mongo_client = None
    _db = None
    
    @classmethod
    def _get_db_connection(cls):
        """Get database connection (singleton pattern)"""
        if cls._db is None:
            try:
                mongo_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
                db_name = os.getenv('DATABASE_NAME', 'cargowise_ai')
                cls._mongo_client = MongoClient(mongo_url)
                cls._db = cls._mongo_client[db_name]
                logger.info("Database connection established for task status checking")
            except Exception as e:
                logger.error(f"Failed to connect to database: {str(e)}")
                cls._db = None
        return cls._db
    
    @classmethod
    def is_task_cancelled(cls, task_id: str) -> bool:
        """Check if a task is cancelled by querying the database directly"""
        if not task_id:
            return False
            
        db = cls._get_db_connection()
        if db is None:
            logger.warning("No database connection available for task status check")
            return False
            
        try:
            tasks_collection = db['tasks']
            task_doc = tasks_collection.find_one({'id': task_id})
            
            if task_doc:
                current_state = task_doc.get('current_state', {})
                status = current_state.get('status')
                
                if status == TaskStatus.CANCELED:
                    logger.info(f"Task {task_id} is cancelled")
                    return True
                    
        except Exception as e:
            logger.error(f"Database check error for task {task_id}: {str(e)}")
            
        return False
    
    @classmethod
    def get_task_status(cls, task_id: str) -> Optional[TaskStatus]:
        """Get the current status of a task"""
        if not task_id:
            return None
            
        db = cls._get_db_connection()
        if db is None:
            return None
            
        try:
            tasks_collection = db['tasks']
            task_doc = tasks_collection.find_one({'id': task_id})
            
            if task_doc:
                current_state = task_doc.get('current_state', {})
                status = current_state.get('status')
                return TaskStatus(status) if status else None
                
        except Exception as e:
            logger.error(f"Error getting task status for {task_id}: {str(e)}")
            
        return None
    
    @classmethod
    def cleanup_connection(cls):
        """Clean up database connection"""
        if cls._mongo_client is not None:
            try:
                cls._mongo_client.close()
                cls._mongo_client = None
                cls._db = None
                logger.info("Closed MongoDB connection for task status utils")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")