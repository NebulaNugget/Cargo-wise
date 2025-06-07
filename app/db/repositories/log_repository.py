# Log repository for database operations
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import uuid
from app.models.log import LogEntry, LogLevel, LogSource, LogStats
from app.db.repositories.base_respository import BaseRepository

logger = logging.getLogger(__name__)

class LogRepository(BaseRepository[LogEntry]):
    """Repository for log operations"""
    
    def __init__(self, db_session):
        """Initialize with database session"""
        super().__init__(db_session, LogEntry, "logs")
    
    async def create_log(self, log_entry: LogEntry) -> LogEntry:
        """
        Create a new log entry
        
        Args:
            log_entry: The log entry to create
            
        Returns:
            The created log entry
        """
        # Generate ID if not provided
        if not log_entry.id:
            log_entry.id = f"log_{uuid.uuid4().hex}"
        
        # Set timestamp if not provided
        if not log_entry.timestamp:
            log_entry.timestamp = datetime.utcnow()
        
        # Insert into database using base repository method
        return await self.create(log_entry)
    
    async def get_logs(
        self, 
        filters: Dict[str, Any], 
        limit: int = 100, 
        offset: int = 0
    ) -> List[LogEntry]:
        """
        Get logs with optional filtering
        
        Args:
            filters: Dictionary of filter conditions
            limit: Maximum number of logs to return
            offset: Offset for pagination
            
        Returns:
            List of log entries
        """
        # Convert Enum values to strings if present
        processed_filters = {}
        for key, value in filters.items():
            if key == "level" and isinstance(value, LogLevel):
                processed_filters[key] = value.value
            elif key == "source" and isinstance(value, LogSource):
                processed_filters[key] = value.value
            elif key == "timestamp_gte":
                processed_filters["timestamp"] = {"$gte": value}
            elif key == "timestamp_lte":
                if "timestamp" not in processed_filters:
                    processed_filters["timestamp"] = {}
                processed_filters["timestamp"]["$lte"] = value
            else:
                processed_filters[key] = value
        
        # Use base repository list method with skip for offset
        cursor = self.collection.find(processed_filters).limit(limit).skip(offset).sort("timestamp", -1)
        
        logs = []
        async for doc in cursor:
            logs.append(LogEntry(**doc))
        
        return logs
    
    async def delete_logs_before(self, cutoff_date: datetime) -> int:
        """
        Delete logs older than a specified date
        
        Args:
            cutoff_date: Delete logs before this date
            
        Returns:
            Number of logs deleted
        """
        result = await self.collection.delete_many({"timestamp": {"$lt": cutoff_date}})
        return result.deleted_count
    
    async def get_log_stats(self, start_time: datetime) -> LogStats:
        """
        Get log statistics
        
        Args:
            start_time: Start time for statistics calculation
            
        Returns:
            Log statistics
        """
        # Get total count
        total_count = await self.collection.count_documents({"timestamp": {"$gte": start_time}})
        
        # Get counts by level
        level_pipeline = [
            {"$match": {"timestamp": {"$gte": start_time}}},
            {"$group": {"_id": "$level", "count": {"$sum": 1}}}
        ]
        level_cursor = self.collection.aggregate(level_pipeline)
        level_counts = {}
        async for doc in level_cursor:
            level_counts[doc["_id"]] = doc["count"]
        
        # Get counts by source
        source_pipeline = [
            {"$match": {"timestamp": {"$gte": start_time}}},
            {"$group": {"_id": "$source", "count": {"$sum": 1}}}
        ]
        source_cursor = self.collection.aggregate(source_pipeline)
        source_counts = {}
        async for doc in source_cursor:
            source_counts[doc["_id"]] = doc["count"]
        
        # Get hourly counts (simplified for MongoDB)
        hourly_counts = []
        
        # Get top tasks
        task_pipeline = [
            {"$match": {"timestamp": {"$gte": start_time}, "task_id": {"$ne": None}}},
            {"$group": {"_id": "$task_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        task_cursor = self.collection.aggregate(task_pipeline)
        top_tasks = []
        async for doc in task_cursor:
            top_tasks.append({"task_id": doc["_id"], "count": doc["count"]})
        
        # Get top errors
        error_pipeline = [
            {"$match": {"timestamp": {"$gte": start_time}, "level": {"$in": ["ERROR", "CRITICAL"]}}},
            {"$group": {"_id": "$message", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        error_cursor = self.collection.aggregate(error_pipeline)
        top_errors = []
        async for doc in error_cursor:
            top_errors.append({"message": doc["_id"], "count": doc["count"]})
        
        # Create stats object
        stats = LogStats(
            total_count=total_count,
            level_counts=level_counts,
            source_counts=source_counts,
            hourly_counts=hourly_counts,
            top_tasks=top_tasks,
            top_errors=top_errors
        )
        
        return stats