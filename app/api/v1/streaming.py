# VNC streaming endpoints
# VNC streaming endpoints
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from app.automation.streaming.stream_manager import get_stream_manager, StreamManager
from pydantic import BaseModel

router = APIRouter()

class StreamCreate(BaseModel):
    stream_id: Optional[str] = None
    vnc_port: Optional[int] = None
    web_port: Optional[int] = None
    display_width: int = 1280
    display_height: int = 720

class StreamResponse(BaseModel):
    id: str
    status: str
    vnc_port: int
    web_port: int
    url: str

@router.post("/streams", response_model=StreamResponse)
async def create_stream(
    stream_data: StreamCreate,
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """Create a new streaming session"""
    # Generate a stream ID if not provided
    stream_id = stream_data.stream_id or f"stream-{len(await stream_manager.list_streams()) + 1}"
    
    result = await stream_manager.create_stream(
        stream_id=stream_id,
        vnc_port=stream_data.vnc_port,
        web_port=stream_data.web_port,
        display_width=stream_data.display_width,
        display_height=stream_data.display_height
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.post("/streams/{stream_id}/start", response_model=StreamResponse)
async def start_stream(
    stream_id: str,
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """Start a streaming session"""
    result = await stream_manager.start_stream(stream_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

@router.post("/streams/{stream_id}/stop", response_model=StreamResponse)
async def stop_stream(
    stream_id: str,
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """Stop a streaming session"""
    result = await stream_manager.stop_stream(stream_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

@router.delete("/streams/{stream_id}")
async def delete_stream(
    stream_id: str,
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """Delete a streaming session"""
    result = await stream_manager.delete_stream(stream_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

@router.get("/streams/{stream_id}", response_model=StreamResponse)
async def get_stream(
    stream_id: str,
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """Get information about a streaming session"""
    result = await stream_manager.get_stream_info(stream_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

@router.get("/streams", response_model=List[StreamResponse])
async def list_streams(
    stream_manager: StreamManager = Depends(get_stream_manager)
):
    """List all streaming sessions"""
    return await stream_manager.list_streams()