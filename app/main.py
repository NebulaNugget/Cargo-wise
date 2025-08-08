# FastAPI application entry point
import sys
from pathlib import Path
import asyncio
import logging
import os
from app.utils.logging import set_log_repository
from app.db.repositories.log_repository import LogRepository
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


from app.core.marc1.tool_registry import get_tool_registry
registry = get_tool_registry()



from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, List, Any
import uuid
from datetime import datetime
import time  # Add this import for the time.time() function

# Import API routers
from app.api.v1 import workflow, task, ai, logs, streaming,log_streaming, auth, dashboard
# Import logging utility
from app.utils.logging import logger, log_api_request
from app.db.database import db, get_db_session
from app.db.repositories.task_repository import TaskRepository
from app.models.task import TaskStatus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="MARC-1 Automation Platform", version="1.0.0")

# Task completion metrics
task_metrics = {
    "completed": 0,
    "failed": 0,
    "total_duration": 0,
    "avg_duration": 0
}

# CORS middleware for React frontend
allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    #allow_origins=["*"],
    #allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await db.connect()
    app.state.db = db
    logger.info("Database connected on startup")
    try:
        # Get the database session directly from the context manager
        # This is how other repositories are likely getting their sessions
        async with get_db_session() as db_session:
            # Initialize log repository with the session
            log_repo = LogRepository(db_session)
            set_log_repository(log_repo)
            logger.info("Log repository initialized")
    except Exception as e:
        logger.error(f"Failed to initialize log repository: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.disconnect()
    logger.info("Database disconnected on shutdown")
    # Clean up browser session if it exists
    try:
        from app.ai.tools.browser_tools import cleanup_browser_session
        await cleanup_browser_session()
    except Exception as e:
        logger.error(f"Error cleaning up browser session: {e}")


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response using the utility
        log_api_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=process_time
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        
        # Log error using the utility
        log_api_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            error=str(e),
            duration=process_time
        )
        
        raise

# Task completion tracking middleware
@app.middleware("http")
async def track_task_completion(request: Request, call_next):
    """Middleware to track task completion metrics"""
    response = await call_next(request)
    
    # Check if this is a task completion endpoint
    path = request.url.path
    if path.startswith("/api/v1/tasks/") and path.endswith("/complete"):
        task_id = path.split("/")[-2]
        
        # Get task from database
        async with get_db_session() as db:
            task_repo = TaskRepository(db)
            task = await task_repo.get_task(task_id)
            
            if task and task.current_state:
                # Update metrics
                if task.current_state.status == TaskStatus.COMPLETED:
                    task_metrics["completed"] += 1
                elif task.current_state.status == TaskStatus.FAILED:
                    task_metrics["failed"] += 1
                
                # Update duration metrics
                if "duration_seconds" in task.current_state.metadata.get("completion_summary", {}):
                    duration = task.current_state.metadata["completion_summary"]["duration_seconds"]
                    task_metrics["total_duration"] += duration
                    total_tasks = task_metrics["completed"] + task_metrics["failed"]
                    task_metrics["avg_duration"] = task_metrics["total_duration"] / total_tasks
    
    return response

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])  # Add auth router
app.include_router(workflow.router, prefix="/api/v1/workflow", tags=["workflow"])
app.include_router(task.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(streaming.router, prefix="/api/v1/streaming", tags=["streaming"])
app.include_router(log_streaming.router, prefix="/api/v1/log_streaming", tags=["log_streaming"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the MARC-1 Automation Platform"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "version": "1.0.0",
        "protocol": "MARC-1",
        "timestamp": datetime.now().isoformat()
    }

# Task metrics endpoint
@app.get("/api/v1/metrics/tasks")
async def get_task_metrics():
    """Get task completion metrics"""
    return task_metrics

# Tools listing endpoint
@app.get("/api/v1/tools")
async def list_tools():
    """List all available automation tools"""
    from app.core.marc1.tool_registry import get_tool_registry
    
    registry = get_tool_registry()
    return registry.list_tools()

# Direct task execution endpoint (for testing)
@app.post("/api/v1/execute")
async def execute_direct(task_request: Dict[str, Any]):
    """Direct task execution endpoint"""
    from app.core.marc1.execution_engine import ExecutionEngine
    from app.models.task import Task
    from app.db.database import get_db_session
    
    task_id = task_request.get("task_id", str(uuid.uuid4()))
    
    task = Task(
        id=task_id,
        description=task_request.get("natural_language_input", ""),
        parameters=task_request.get("parameters", {}),
        context=task_request.get("client_context", {})
    )
    
    # Get database session
    db_session = await get_db_session()
    engine = ExecutionEngine(db_session=db_session)
    results = []
    
    try:
        async for state in engine.execute_task(task):
            results.append(state.dict())
        
        return {
            "task_id": task_id,
            "status": "completed",
            "results": results
        }
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # setup_windows_event_loop()
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8000'))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)