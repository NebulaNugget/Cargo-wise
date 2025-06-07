# Monitoring utilities
import time
import psutil
import logging
import platform
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SystemMetrics:
    """System resource metrics"""
    
    def __init__(self):
        self.cpu_percent = 0.0
        self.memory_percent = 0.0
        self.disk_percent = 0.0
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "disk_percent": self.disk_percent,
            "timestamp": self.timestamp.isoformat()
        }

class TaskMetrics:
    """Task execution metrics"""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.steps_completed = 0
        self.steps_total = 0
        self.status = "RUNNING"
        self.error: Optional[str] = None
    
    def complete(self, success: bool = True, error: Optional[str] = None):
        """Mark task as complete"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.status = "COMPLETED" if success else "ERROR"
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        result = {
            "task_id": self.task_id,
            "start_time": self.start_time.isoformat(),
            "steps_completed": self.steps_completed,
            "steps_total": self.steps_total,
            "status": self.status
        }
        
        if self.end_time:
            result["end_time"] = self.end_time.isoformat()
            result["duration"] = self.duration
            
        if self.error:
            result["error"] = self.error
            
        return result

class MonitoringService:
    """Service for monitoring system and task metrics"""
    
    def __init__(self, metrics_interval: int = 60):
        self.metrics_interval = metrics_interval  # seconds
        self.system_metrics: List[SystemMetrics] = []
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.collection_thread: Optional[threading.Thread] = None
        self.running = False
        self.max_metrics_history = 1440  # 24 hours at 1 minute intervals
    
    def start(self):
        """Start metrics collection"""
        if self.running:
            return
            
        self.running = True
        self.collection_thread = threading.Thread(target=self._collect_metrics_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        logger.info("Monitoring service started")
    
    def stop(self):
        """Stop metrics collection"""
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        logger.info("Monitoring service stopped")
    
    def _collect_metrics_loop(self):
        """Background thread for collecting metrics"""
        while self.running:
            try:
                self._collect_system_metrics()
                time.sleep(self.metrics_interval)
            except Exception as e:
                logger.error(f"Error collecting metrics: {str(e)}")
                time.sleep(5)  # Short delay before retry
    
    def _collect_system_metrics(self):
        """Collect current system metrics"""
        metrics = SystemMetrics()
        metrics.cpu_percent = psutil.cpu_percent(interval=1)
        metrics.memory_percent = psutil.virtual_memory().percent
        metrics.disk_percent = psutil.disk_usage('/').percent
        
        self.system_metrics.append(metrics)
        
        # Trim history if needed
        if len(self.system_metrics) > self.max_metrics_history:
            self.system_metrics = self.system_metrics[-self.max_metrics_history:]
    
    def start_task_monitoring(self, task_id: str, total_steps: int = 0) -> TaskMetrics:
        """Start monitoring a task"""
        metrics = TaskMetrics(task_id)
        metrics.steps_total = total_steps
        self.task_metrics[task_id] = metrics
        return metrics
    
    def update_task_progress(self, task_id: str, steps_completed: int):
        """Update task progress"""
        if task_id in self.task_metrics:
            self.task_metrics[task_id].steps_completed = steps_completed
    
    def complete_task(self, task_id: str, success: bool = True, error: Optional[str] = None):
        """Mark task as complete"""
        if task_id in self.task_metrics:
            self.task_metrics[task_id].complete(success, error)
    
    def get_system_metrics(self, minutes: int = 60) -> List[Dict[str, Any]]:
        """Get system metrics for the last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [m.to_dict() for m in self.system_metrics if m.timestamp >= cutoff]
    
    def get_task_metrics(self, task_id: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Get metrics for a specific task or all tasks"""
        if task_id:
            if task_id in self.task_metrics:
                return self.task_metrics[task_id].to_dict()
            return {}
        else:
            return [m.to_dict() for m in self.task_metrics.values()]
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        metrics = SystemMetrics()
        metrics.cpu_percent = psutil.cpu_percent(interval=0.5)
        metrics.memory_percent = psutil.virtual_memory().percent
        metrics.disk_percent = psutil.disk_usage('/').percent
        
        return {
            "system": metrics.to_dict(),
            "tasks": {
                "total": len(self.task_metrics),
                "running": sum(1 for m in self.task_metrics.values() if m.status == "RUNNING"),
                "completed": sum(1 for m in self.task_metrics.values() if m.status == "COMPLETED"),
                "error": sum(1 for m in self.task_metrics.values() if m.status == "ERROR")
            },
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "processor": platform.processor()
            }
        }

# Singleton instance
_monitoring_service = None

def get_monitoring_service() -> MonitoringService:
    """Get the monitoring service singleton"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService()
        _monitoring_service.start()
    return _monitoring_service