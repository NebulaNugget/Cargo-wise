# Hybrid logging utilities combining database and file logging
import logging
import logging.handlers
import uuid
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
from app.models.log import LogEntry, LogLevel, LogSource
import functools
import inspect
import traceback
import sys

# Configure log directory
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
TASK_LOG_FILE = os.path.join(LOG_DIR, "tasks.log")
API_LOG_FILE = os.path.join(LOG_DIR, "api.log")

logger = logging.getLogger(__name__)

# Global log repository (will be set during app startup)
_log_repository = None

def set_log_repository(repository):
    """Set the global log repository"""
    global _log_repository
    _log_repository = repository

class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON strings"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add task_id if available
        if hasattr(record, "task_id") and record.task_id:
            log_data["task_id"] = record.task_id
            
        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", 
                          "filename", "funcName", "id", "levelname", "levelno", 
                          "lineno", "module", "msecs", "message", "msg", "name", 
                          "pathname", "process", "processName", "relativeCreated", 
                          "stack_info", "thread", "threadName", "task_id"]:
                log_data[key] = value
                
        return json.dumps(log_data)

def setup_file_logging(level=logging.INFO):
    """Set up file-based logging as backup"""
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handlers
    # 1. Main application log
    app_handler = logging.handlers.RotatingFileHandler(
        APP_LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    app_handler.setLevel(level)
    app_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(app_handler)
    
    # 2. Error log
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(error_handler)
    
    # Task log
    task_logger = logging.getLogger("task")
    task_handler = logging.handlers.RotatingFileHandler(
        TASK_LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    task_handler.setFormatter(JsonFormatter())
    task_logger.addHandler(task_handler)
    
    # API log
    api_logger = logging.getLogger("api")
    api_handler = logging.handlers.RotatingFileHandler(
        API_LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    api_handler.setFormatter(JsonFormatter())
    api_logger.addHandler(api_handler)
    
    return root_logger

# Set up file logging on module import
setup_file_logging()

async def log_to_db(
    message: str,
    level: LogLevel = LogLevel.INFO,
    source: LogSource = LogSource.SYSTEM,
    task_id: Optional[str] = None,
    tool_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> LogEntry:
    """
    Log a message to the database
    
    Args:
        message: Log message
        level: Log level
        source: Log source
        task_id: Associated task ID
        tool_name: Associated tool name
        metadata: Additional metadata
        
    Returns:
        Created log entry
    """
    global _log_repository
    # Also log to file as backup
    log_to_file(message, level, source, task_id, tool_name, metadata)
    if _log_repository is None:
        logger.warning("Log repository not set, skipping database logging")
        return None
    
    # Create log entry
    log_entry = LogEntry(
        id=f"log_{uuid.uuid4().hex}",
        timestamp=datetime.utcnow(),
        level=level,
        source=source,
        message=message,
        task_id=task_id,
        tool_name=tool_name,
        metadata=metadata or {}
    )
    
    # Log to database
    try:
        return await _log_repository.create_log(log_entry)
    except Exception as e:
        logger.error(f"Error logging to database: {str(e)}")
        # Print the full exception traceback for debugging
        import traceback
        logger.error(traceback.format_exc())
        return None

def log_to_file(
    message: str,
    level: LogLevel = LogLevel.INFO,
    source: LogSource = LogSource.SYSTEM,
    task_id: Optional[str] = None,
    tool_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a message to file
    
    Args:
        message: Log message
        level: Log level
        source: Log source
        task_id: Associated task ID
        tool_name: Associated tool name
        metadata: Additional metadata
    """
    # Convert LogLevel to standard logging level
    level_map = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
        LogLevel.CRITICAL: logging.CRITICAL
    }
    log_level = level_map.get(level, logging.INFO)
    
    # Choose appropriate logger based on source
    if source == LogSource.API:
        file_logger = logging.getLogger("api")
    elif source == LogSource.TASK:
        file_logger = logging.getLogger("task")
    else:
        file_logger = logger
    
    # Prepare extra data
    extra = {"source": source.value if isinstance(source, LogSource) else source}
    
    if task_id:
        extra["task_id"] = task_id
    
    if tool_name:
        extra["tool_name"] = tool_name
    
    if metadata:
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                extra[key] = value
    
    # Log to file
    file_logger.log(log_level, message, extra=extra)

def log_api_request(
    request_id: str,
    method: str,
    path: str,
    status_code: Optional[int] = None,
    duration: Optional[float] = None,
    error: Optional[str] = None
):
    """
    Log an API request
    
    Args:
        request_id: Unique request ID
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration: Request duration in seconds
        error: Error message if request failed
    """
        # Determine log level based on status code
    level = LogLevel.INFO
    if status_code:
        if status_code >= 500:
            level = LogLevel.ERROR
        elif status_code >= 400:
            level = LogLevel.WARNING
    elif error:
        level = LogLevel.ERROR
    
    # Create metadata
    metadata = {
        "request_id": request_id,
        "method": method,
        "path": path
    }
    
    if status_code:
        metadata["status_code"] = status_code
    
    if duration:
        metadata["duration_ms"] = round(duration * 1000)
    
    if error:
        metadata["error"] = error
    
    # Create message
    if error:
        message = f"API request failed: {method} {path} - {error}"
    else:
        message = f"API request: {method} {path}"
        if status_code:
            message += f" - {status_code}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.API,
        metadata=metadata
    ))

def log_task_event(
    task_id: str,
    event: str,
    level: LogLevel = LogLevel.INFO,
    tool_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a task event
    
    Args:
        task_id: Task ID
        event: Event description
        level: Log level
        tool_name: Associated tool name
        metadata: Additional metadata
    """
    # Create message
    message = f"Task {task_id}: {event}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.TASK,
        task_id=task_id,
        tool_name=tool_name,
        metadata=metadata
    ))

def log_tool_execution(
    task_id: str,
    tool_name: str,
    action: str,
    level: LogLevel = LogLevel.INFO,
    parameters: Optional[Dict[str, Any]] = None,
    result: Optional[Any] = None,
    error: Optional[str] = None,
    duration: Optional[float] = None
):
    """
    Log a tool execution
    
    Args:
        task_id: Task ID
        tool_name: Tool name
        action: Action description
        level: Log level
        parameters: Tool parameters (sensitive data will be redacted)
        result: Execution result
        error: Error message if execution failed
        duration: Execution duration in seconds
    """
    # Determine log level based on error
    if error:
        level = LogLevel.ERROR
    
    # Create metadata
    metadata = {"action": action}
    
    if parameters:
        # Redact sensitive parameters
        redacted_params = {}
        for key, value in parameters.items():
            if key.lower() in ["password", "token", "secret", "key", "credential"]:
                redacted_params[key] = "********"
            else:
                redacted_params[key] = value
        metadata["parameters"] = redacted_params
    
    if result:
        metadata["result"] = result
    
    if error:
        metadata["error"] = error
    
    if duration:
        metadata["duration_ms"] = round(duration * 1000)
    
    # Create message
    if error:
        message = f"Tool execution failed: {tool_name} - {action} - {error}"
    else:
        message = f"Tool execution: {tool_name} - {action}"
        if duration:
            message += f" ({round(duration * 1000)}ms)"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.TOOL,
        task_id=task_id,
        tool_name=tool_name,
        metadata=metadata
    ))

def log_browser_event(
    task_id: str,
    event: str,
    level: LogLevel = LogLevel.INFO,
    url: Optional[str] = None,
    selector: Optional[str] = None,
    screenshot_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a browser automation event
    
    Args:
        task_id: Task ID
        event: Event description
        level: Log level
        url: Current URL
        selector: Element selector
        screenshot_id: ID of associated screenshot
        metadata: Additional metadata
    """
    # Create metadata
    meta = metadata or {}
    
    if url:
        meta["url"] = url
    
    if selector:
        meta["selector"] = selector
    
    if screenshot_id:
        meta["screenshot_id"] = screenshot_id
    
    # Create message
    message = f"Browser: {event}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.BROWSER,
        task_id=task_id,
        metadata=meta
    ))

def log_desktop_event(
    task_id: str,
    event: str,
    level: LogLevel = LogLevel.INFO,
    window_title: Optional[str] = None,
    screenshot_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a desktop automation event
    
    Args:
        task_id: Task ID
        event: Event description
        level: Log level
        window_title: Current window title
        screenshot_id: ID of associated screenshot
        metadata: Additional metadata
    """
    # Create metadata
    meta = metadata or {}
    
    if window_title:
        meta["window_title"] = window_title
    
    if screenshot_id:
        meta["screenshot_id"] = screenshot_id
    
    # Create message
    message = f"Desktop: {event}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.DESKTOP,
        task_id=task_id,
        metadata=meta
    ))

def log_security_event(
    event: str,
    level: LogLevel = LogLevel.INFO,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a security event
    
    Args:
        event: Event description
        level: Log level
        user_id: User ID
        ip_address: IP address
        metadata: Additional metadata
    """
    # Create metadata
    meta = metadata or {}
    
    if user_id:
        meta["user_id"] = user_id
    
    if ip_address:
        meta["ip_address"] = ip_address
    
    # Create message
    message = f"Security: {event}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=LogSource.SECURITY,
        metadata=meta
    ))

def log_exception(
    exc: Exception,
    task_id: Optional[str] = None,
    tool_name: Optional[str] = None,
    source: LogSource = LogSource.SYSTEM,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log an exception
    
    Args:
        exc: Exception object
        task_id: Task ID
        tool_name: Tool name
        source: Log source
        metadata: Additional metadata
    """
    # Get exception details
    exc_type = type(exc).__name__
    exc_message = str(exc)
    exc_traceback = traceback.format_exception(type(exc), exc, exc.__traceback__)
    
    # Create metadata
    meta = metadata or {}
    meta.update({
        "exception_type": exc_type,
        "traceback": exc_traceback
    })
    
    # Create message
    message = f"Exception: {exc_type} - {exc_message}"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=LogLevel.ERROR,
        source=source,
        task_id=task_id,
        tool_name=tool_name,
        metadata=meta
    ))

def log_function_call(
    func_name: str,
    args: tuple,
    kwargs: Dict[str, Any],
    result: Any = None,
    error: Optional[Exception] = None,
    duration: Optional[float] = None,
    task_id: Optional[str] = None,
    source: LogSource = LogSource.SYSTEM
):
    """
    Log a function call
    
    Args:
        func_name: Function name
        args: Function arguments
        kwargs: Function keyword arguments
        result: Function result
        error: Exception if function failed
        duration: Execution duration in seconds
        task_id: Task ID
        source: Log source
    """
    # Determine log level based on error
    level = LogLevel.INFO if not error else LogLevel.ERROR
    
    # Create metadata
    metadata = {
        "function": func_name,
        "args": str(args),
        "kwargs": str(kwargs)
    }
    
    if result is not None:
        metadata["result"] = str(result)
    
    if error:
        metadata["error"] = str(error)
        metadata["error_type"] = type(error).__name__
    
    if duration:
        metadata["duration_ms"] = round(duration * 1000)
    
    # Create message
    if error:
        message = f"Function call failed: {func_name} - {error}"
    else:
        message = f"Function call: {func_name}"
        if duration:
            message += f" ({round(duration * 1000)}ms)"
    
    # Log to database asynchronously
    asyncio.create_task(log_to_db(
        message=message,
        level=level,
        source=source,
        task_id=task_id,
        metadata=metadata
    ))

def log_function(source: LogSource = LogSource.SYSTEM, task_id_arg: Optional[str] = None):
    """
    Decorator to log function calls
    
    Args:
        source: Log source
        task_id_arg: Name of argument containing task ID
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Get function name
            func_name = f"{func.__module__}.{func.__qualname__}"
            
            # Get task ID
            task_id = None
            if task_id_arg and task_id_arg in kwargs:
                task_id = kwargs[task_id_arg]
            elif task_id_arg and len(args) > 0:
                # Check if task_id_arg is in positional arguments
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if task_id_arg in params:
                    idx = params.index(task_id_arg)
                    if idx < len(args):
                        task_id = args[idx]
            
            # Record start time
            start_time = datetime.now()
            
            try:
                # Call function
                result = func(*args, **kwargs)
                
                # Calculate duration
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log function call
                log_function_call(
                    func_name=func_name,
                    args=args,
                    kwargs=kwargs,
                    result=result,
                    duration=duration,
                    task_id=task_id,
                    source=source
                )
                
                return result
            except Exception as e:
                # Calculate duration
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log function call with error
                log_function_call(
                    func_name=func_name,
                    args=args,
                    kwargs=kwargs,
                    error=e,
                    duration=duration,
                    task_id=task_id,
                    source=source
                )
                
                # Re-raise exception
                raise
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Get function name
            func_name = f"{func.__module__}.{func.__qualname__}"
            
            # Get task ID
            task_id = None
            if task_id_arg and task_id_arg in kwargs:
                task_id = kwargs[task_id_arg]
            elif task_id_arg and len(args) > 0:
                # Check if task_id_arg is in positional arguments
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if task_id_arg in params:
                    idx = params.index(task_id_arg)
                    if idx < len(args):
                        task_id = args[idx]
            
            # Record start time
            start_time = datetime.now()
            
            try:
                # Call function
                result = await func(*args, **kwargs)
                
                # Calculate duration
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log function call
                log_function_call(
                    func_name=func_name,
                    args=args,
                    kwargs=kwargs,
                    result=result,
                    duration=duration,
                    task_id=task_id,
                    source=source
                )
                
                return result
            except Exception as e:
                # Calculate duration
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log function call with error
                log_function_call(
                    func_name=func_name,
                    args=args,
                    kwargs=kwargs,
                    error=e,
                    duration=duration,
                    task_id=task_id,
                    source=source
                )
                
                # Re-raise exception
                raise
        
        # Use appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
    