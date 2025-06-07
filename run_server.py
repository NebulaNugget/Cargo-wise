import sys
import asyncio
import uvicorn

if __name__ == "__main__":
    # Set the event loop policy for Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("Set WindowsProactorEventLoopPolicy for Playwright compatibility")
    
    # Run with the correct loop policy
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        loop="asyncio"
    )