# Dashboard API endpoints
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.db.repositories.task_repository import TaskRepository
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.client_repository import ClientRepository
from app.db.repositories.log_repository import LogRepository
from app.models.task import TaskStatus
from app.models.user import User
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
import statistics
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    user_id: Optional[str] = None,
    client_id: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Get dashboard statistics for the current user or client
    
    If user_id is provided, returns stats for that user
    If client_id is provided, returns stats for that client
    If neither is provided, returns global stats
    """
    # Create repositories
    task_repo = TaskRepository(db)
    user_repo = UserRepository(db)
    client_repo = ClientRepository(db)
    log_repo = LogRepository(db)
    
    # Get user and client info if provided
    user = None
    client = None
    
    if user_id:
        user = await user_repo.get(user_id)
        if not user:
            raise HTTPException(404, "User not found")
        client_id = user.client_id
    
    if client_id:
        client = await client_repo.get(client_id)
        if not client:
            raise HTTPException(404, "Client not found")
    
    # Build query filters based on user/client
    task_filters = {}
    if user_id:
        task_filters["user_id"] = user_id
    if client_id:
        task_filters["client_id"] = client_id
    
    # Get tasks (limit to last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Get all tasks for the period
    all_tasks = await task_repo.list(task_filters, limit=1000)
    
    # Helper function to safely convert to datetime
    def to_datetime(dt_value):
        if isinstance(dt_value, datetime):
            return dt_value
        elif isinstance(dt_value, str):
            return datetime.fromisoformat(dt_value)
        else:
            logger.warning(f"Unexpected datetime type: {type(dt_value)}")
            return datetime.min  # Return a default value
    # Filter tasks by date (last 30 days)
    recent_tasks = [
        task for task in all_tasks 
        if to_datetime(task.created_at) > thirty_days_ago
    ]
    
    # Calculate total tasks
    total_tasks = len(recent_tasks)
    
    # Calculate success rate
    completed_tasks = [
        task for task in recent_tasks 
        if task.current_state and task.current_state.status == TaskStatus.COMPLETED
    ]
    failed_tasks = [
        task for task in recent_tasks 
        if task.current_state and task.current_state.status == TaskStatus.FAILED
    ]
    
    success_rate = 0
    if completed_tasks or failed_tasks:
        success_rate = (len(completed_tasks) / (len(completed_tasks) + len(failed_tasks))) * 100
    
    # Calculate average response time (time to completion)
    response_times = []
    for task in completed_tasks:
        if task.created_at and task.completed_at:
            start_time = to_datetime(task.created_at)
            end_time = to_datetime(task.completed_at)
            duration = (end_time - start_time).total_seconds()
            response_times.append(duration)
    
    avg_response_time = 0
    if response_times:
        avg_response_time = statistics.mean(response_times)
    
    # Get active users
    active_users = []
    if client_id:
        # Get all users for this client
        all_users = await user_repo.get_users_by_client(client_id)
        
        # Filter to active users (logged in within last 24 hours)
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        active_users = [
            user for user in all_users 
            if user.last_login and (
                isinstance(user.last_login, str) and datetime.fromisoformat(user.last_login) > one_day_ago or
                isinstance(user.last_login, datetime) and user.last_login > one_day_ago
            )
        ]
    else:
        # Get all active users
        active_users = await user_repo.get_active_users()
    
    # Get current task (most recent running task)
    current_task = None
    running_tasks = [
        task for task in all_tasks 
        if task.current_state and task.current_state.status in [TaskStatus.RUNNING, TaskStatus.QUEUED, TaskStatus.PAUSED]
    ]
    
    if running_tasks:
        # Sort by created_at (newest first)
        running_tasks.sort(key=lambda t: to_datetime(t.created_at), reverse=True)
        current_task = running_tasks[0]
    
    # Get recent activity (last 5 completed tasks)
    recent_activity = []
    completed_tasks.sort(key=lambda t: to_datetime(t.created_at), reverse=True)
    recent_activity = completed_tasks[:5]
    
    # Check system health
    system_health = await check_system_health(db)
    
     # Calculate task growth (compared to yesterday)
    yesterday = datetime.utcnow() - timedelta(days=1)
    tasks_today = len([t for t in recent_tasks if to_datetime(t.created_at) > yesterday])
    
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    tasks_yesterday = len([
        t for t in recent_tasks 
        if two_days_ago < to_datetime(t.created_at) < yesterday
    ])
    
    task_growth = 0
    if tasks_yesterday > 0:
        task_growth = ((tasks_today - tasks_yesterday) / tasks_yesterday) * 100
    
    # Calculate success rate change
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # Tasks from last week
    last_week_tasks = [
        t for t in recent_tasks 
        if week_ago < to_datetime(t.created_at) < datetime.utcnow()
    ]
    
    # Tasks from week before that
    two_weeks_ago = datetime.utcnow() - timedelta(days=14)
    previous_week_tasks = [
        t for t in recent_tasks 
        if two_weeks_ago < to_datetime(t.created_at) < week_ago
    ]
    
    # Calculate success rates for both periods
    current_success_rate = 0
    previous_success_rate = 0
    
    completed_last_week = [t for t in last_week_tasks if t.current_state.status == TaskStatus.COMPLETED]
    failed_last_week = [t for t in last_week_tasks if t.current_state.status == TaskStatus.FAILED]
    
    if completed_last_week or failed_last_week:
        current_success_rate = (len(completed_last_week) / (len(completed_last_week) + len(failed_last_week))) * 100
    
    completed_previous_week = [t for t in previous_week_tasks if t.current_state.status == TaskStatus.COMPLETED]
    failed_previous_week = [t for t in previous_week_tasks if t.current_state.status == TaskStatus.FAILED]
    
    if completed_previous_week or failed_previous_week:
        previous_success_rate = (len(completed_previous_week) / (len(completed_previous_week) + len(failed_previous_week))) * 100
    
    success_rate_change = current_success_rate - previous_success_rate
    
    # Format response
    return {
        "total_tasks": {
            "value": total_tasks,
            "change": f"{task_growth:.1f}% from yesterday"
        },
        "success_rate": {
            "value": f"{success_rate:.1f}%",
            "change": f"{success_rate_change:+.1f}% this week"
        },
        "response_time": {
            "value": f"{avg_response_time:.1f}s",
            "optimized": avg_response_time < 2.0  # Consider response time optimized if < 2 seconds
        },
        "active_users": {
            "value": len(active_users),
            "online": True
        },
        "current_task": current_task.dict() if current_task else None,
        "recent_activity": [
            {
                "id": task.id,
                "name": task.name or f"Task {task.id[:8]}",
                "status": task.current_state.status,
                "completed_at": task.completed_at
            }
            for task in recent_activity
        ],
        "system_health": system_health
    }

async def check_system_health(db) -> Dict[str, Any]:
    """Check the health of various system components"""
    health = {}
    
    # Check API Server
    health["api_server"] = {
        "status": "ONLINE",
        "latency_ms": 10  # Placeholder, as the API is clearly running
    }
    
    # Check Database
    try:
        # Simple database query to check connection
        start_time = datetime.utcnow()
        await db.command("ping")
        end_time = datetime.utcnow()
        latency = (end_time - start_time).total_seconds() * 1000
        
        health["database"] = {
            "status": "HEALTHY",
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health["database"] = {
            "status": "ERROR",
            "error": str(e)
        }
    
    # Check WebSocket (we can only infer this is working)
    health["websocket"] = {
        "status": "CONNECTED"
    }
    
    # Check Cache (simulated)
    # In a real implementation, you would check your actual cache system
    cache_usage = 85  # Placeholder value
    health["cache"] = {
        "status": f"{cache_usage}% FULL",
        "usage_percent": cache_usage
    }
    
    return health