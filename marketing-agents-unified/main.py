"""
Unified Marketing Agents API
Single, clean main application file with feature flags.
"""

from app.core.setup import create_application

# Create the unified application
app = create_application()

# Export for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
