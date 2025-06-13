"""
Uvicorn server runner with proper Windows signal handling
"""
import uvicorn
import sys
import signal
import os
import asyncio
import threading
import time


def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}. Shutting down server...")
    
    if sys.platform == "win32":
        # On Windows with ProactorEventLoop, use a more direct approach
        def delayed_exit():
            time.sleep(0.5)  # Allow some cleanup time
            os._exit(0)
        
        shutdown_thread = threading.Thread(target=delayed_exit)
        shutdown_thread.daemon = True
        shutdown_thread.start()
    else:
        sys.exit(0)


def main():
    # Set up Windows event loop policy before anything else
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    if sys.platform == "win32" and hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, signal_handler)  # Ctrl+Break on Windows
    elif hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    print("Starting uvicorn server...")
    print("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
            # Let uvicorn handle the event loop
            loop="auto",
            # Enable graceful shutdown with longer timeout for Windows
            timeout_graceful_shutdown=10 if sys.platform == "win32" else 5,
        )
    except KeyboardInterrupt:
        print("\nShutdown initiated by user")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        print("Server stopped")


if __name__ == "__main__":
    main()
