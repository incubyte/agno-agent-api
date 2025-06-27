"""
Application Setup and Configuration
Unified application creation with all features.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import sys
import asyncio

from .setting import settings, is_render_deployment
from .exceptions import setup_exception_handlers
from .middleware import setup_middleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Handle Windows event loop policy for Playwright/Crawl4AI compatibility
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    logger.info("Starting up agno-ai-api with enhanced error handling...")
    
    # Create database tables
    from ..db.engine import engine
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    
    # Log feature flags status
    logger.info(f"Enhanced validation: {settings.ENABLE_ENHANCED_VALIDATION}")
    logger.info(f"DTO validation: {settings.ENABLE_DTO_VALIDATION}")
    logger.info(f"Advanced security: {settings.ENABLE_ADVANCED_SECURITY}")
    logger.info(f"AI validation: {settings.ENABLE_AI_VALIDATION}")
    logger.info(f"Rate limiting: {settings.ENABLE_RATE_LIMITING}")
    logger.info(f"Request logging: {settings.ENABLE_REQUEST_LOGGING}")
    
    if is_render_deployment():
        logger.info("Running in Render deployment mode")
    
    yield  # Application runs here
    
    logger.info("Shutting down gracefully...")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title="Agno AI API",
        description="Marketing Agents API with Enhanced Error Handling",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Setup error handling
    setup_exception_handlers(app)
    
    # Setup middleware
    setup_middleware(app)
    
    # Add CORS middleware (preserve existing functionality)
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    from ..routers.index import router as index_router
    from ..routers.agent import router as agent_router
    
    app.include_router(index_router)
    app.include_router(agent_router)
    
    logger.info("✓ Application configured successfully")
    
    return app
