from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import index_router
from app.routers import agent_router
from app.db.engine import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys
import signal
import os

# Handle Windows event loop policy for Playwright/Crawl4AI compatibility
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# Modern lifespan context manager to replace deprecated on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up agno-ai-api...")
    
    # Create database tables
    SQLModel.metadata.create_all(bind=engine)
    
    # Add any other startup code here
    
    yield  # This is where the application runs
    
    # Shutdown code
    print("Shutting down gracefully...")
    # Add any cleanup code here if needed
    # For example: closing database connections, cleaning up resources, etc.


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(index_router)
app.include_router(agent_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Signal handler for graceful shutdown (Windows ProactorEventLoop compatible)
def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}. Shutting down...")
    # For ProactorEventLoop on Windows, we need a more direct approach
    import threading
    import time
    
    def delayed_exit():
        time.sleep(0.1)  # Brief delay to allow cleanup
        os._exit(0)
    
    # Start shutdown in a separate thread
    shutdown_thread = threading.Thread(target=delayed_exit)
    shutdown_thread.daemon = True
    shutdown_thread.start()


# Register signal handlers with Windows-specific handling
if sys.platform == "win32":
    # On Windows with ProactorEventLoop, signal handling is trickier
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, signal_handler)  # Ctrl+Break on Windows
else:
    # Standard signal handling for other platforms
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal


def main():
    print("Hello from agno-ai-api!")


if __name__ == "__main__":
    main()
