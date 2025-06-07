# Logging and monitoring endpoints
# Logging and monitoring endpoints
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.log import LogEntry, LogLevel, LogSource
from app.db.repositories.log_repository import LogRepository
from app.dependencies import get_db
from app.core.auth.permissions import PermissionDependency
from app.models.user import UserRole
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Permission dependency for admin-only endpoints
admin_only = PermissionDependency(required_roles=[UserRole.ADMIN])

@router.get("/", response_model=List[LogEntry])
async def get_logs(
    task_id: Optional[str] = None,
    level: Optional[LogLevel] = None,
    source: Optional[LogSource] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db=Depends(get_db)
):
    """
    Get system logs with optional filtering
    
    This endpoint retrieves logs from the system with various filtering options.
    """
    # Create log repository
    log_repo = LogRepository(db)
    
    # Build query filters
    filters = {}
    if task_id:
        filters["task_id"] = task_id
    if level:
        filters["level"] = level
    if source:
        filters["source"] = source
    if start_time:
        filters["timestamp_gte"] = start_time
    if end_time:
        filters["timestamp_lte"] = end_time
    
    # Get logs
    logs = await log_repo.get_logs(filters, limit, offset)
    
    return logs

@router.get("/task/{task_id}", response_model=List[LogEntry])
async def get_task_logs(
    task_id: str,
    level: Optional[LogLevel] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db=Depends(get_db)
):
    """
    Get logs for a specific task
    
    This endpoint retrieves all logs associated with a specific task ID.
    """
    # Create log repository
    log_repo = LogRepository(db)
    
    # Build query filters
    filters = {"task_id": task_id}
    if level:
        filters["level"] = level
    if start_time:
        filters["timestamp_gte"] = start_time
    if end_time:
        filters["timestamp_lte"] = end_time
    
    # Get logs
    logs = await log_repo.get_logs(filters, limit, offset)
    
    return logs

@router.get("/recent", response_model=List[LogEntry])
async def get_recent_logs(
    hours: int = Query(24, ge=1, le=168),  # Max 1 week
    level: Optional[LogLevel] = None,
    source: Optional[LogSource] = None,
    limit: int = Query(100, ge=1, le=1000),
    db=Depends(get_db)
):
    """
    Get recent system logs
    
    This endpoint retrieves logs from the last specified number of hours.
    """
    # Create log repository
    log_repo = LogRepository(db)
    
    # Calculate start time
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Build query filters
    filters = {"timestamp_gte": start_time}
    if level:
        filters["level"] = level
    if source:
        filters["source"] = source
    
    # Get logs
    logs = await log_repo.get_logs(filters, limit, 0)
    
    return logs

@router.delete("/", dependencies=[Depends(admin_only)])
async def purge_logs(
    days: int = Query(30, ge=7),  # Minimum 7 days retention
    db=Depends(get_db)
):
    """
    Purge old logs from the system
    
    This endpoint deletes logs older than the specified number of days.
    Admin access only.
    """
    # Create log repository
    log_repo = LogRepository(db)
    
    # Calculate cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Delete logs
    deleted_count = await log_repo.delete_logs_before(cutoff_date)
    
    return {"message": f"Deleted {deleted_count} logs older than {days} days"}

@router.get("/stats", dependencies=[Depends(admin_only)])
async def get_log_stats(
    days: int = Query(7, ge=1, le=30),
    db=Depends(get_db)
):
    """
    Get log statistics
    
    This endpoint provides statistics about system logs, such as counts by level,
    source, and time period. Admin access only.
    """
    # Create log repository
    log_repo = LogRepository(db)
    
    # Calculate start time
    start_time = datetime.utcnow() - timedelta(days=days)
    
    # Get statistics
    stats = await log_repo.get_log_stats(start_time)
    
    return stats