"""
Main application module with enhanced error handling and validation.
Uses the new setup system while preserving existing functionality.
"""

from app.core.setup import create_application
import asyncio
import sys
import signal
import os

# Handle Windows event loop policy for Playwright/Crawl4AI compatibility
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Create the application using the new setup system
app = create_application()

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
    print("Hello from agno-ai-api with enhanced error handling!")


if __name__ == "__main__":
    main()
