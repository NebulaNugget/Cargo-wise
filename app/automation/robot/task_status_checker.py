import logging
from typing import Optional
import threading
from pymongo import MongoClient
from app.models.task import TaskStatus
import os

logger = logging.getLogger(__name__)

class TaskStatusChecker:
    def __init__(self, task_id: Optional[str] = None):
        self.task_id = task_id
        self._cancelled = False
        self._lock = threading.Lock()
        # Initialize MongoDB connection for direct access
        self._mongo_client = None
        self._db = None
        self._init_db_connection()
        
    def _init_db_connection(self):
        """Initialize direct MongoDB connection for synchronous access"""
        try:
            # Get MongoDB URL from environment or use default
            mongo_url = os.getenv('MONGODB_URL', 'mongodb+srv://allensteadson:Xl5EDPkL6qSwUprr@cluster0.pzstbpn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
            db_name = os.getenv('DATABASE_NAME', 'cargowise_automation')
            
            self._mongo_client = MongoClient(mongo_url)
            self._db = self._mongo_client[db_name]
            logger.info(f"Initialized direct MongoDB connection for task status checking")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB connection: {str(e)}")
            self._mongo_client = None
            self._db = None
        
    def is_cancelled(self) -> bool:
        """Check if the task has been cancelled (synchronous version)"""
        with self._lock:
            if self._cancelled:
                return True
            
        if not self.task_id:
            return False
            
        # Check database directly without async complications
        return self._check_db_status_sync()
        
    def _check_db_status_sync(self) -> bool:
        """Synchronous database check for task status"""
        # Fix: Use proper None comparison for PyMongo Database objects
        if self._db is None:
            logger.warning("No database connection available for task status check")
            return False
            
        try:
            # Direct MongoDB query
            tasks_collection = self._db['tasks']
            task_doc = tasks_collection.find_one({'id': self.task_id})
            
            if task_doc:
                current_state = task_doc.get('current_state', {})
                status = current_state.get('status')
                
                if status == TaskStatus.CANCELED:
                    with self._lock:
                        self._cancelled = True
                    logger.info(f"Task {self.task_id} has been cancelled")
                    return True
                    
        except Exception as e:
            logger.error(f"Database check error for {self.task_id}: {str(e)}")
            
        return False
        
    def mark_cancelled(self):
        """Manually mark the task as cancelled"""
        with self._lock:
            self._cancelled = True
            
    def cleanup(self):
        """Clean up database connection"""
        if self._mongo_client is not None:
            try:
                self._mongo_client.close()
                logger.info("Closed MongoDB connection for task status checker")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")