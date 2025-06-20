"""
Centralized Application Setup
Handles all initialization logic for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from .config import settings
from .exceptions import setup_exception_handlers
from .middleware import setup_middleware
from ..models.database import create_tables


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting Marketing Agents API (Unified)")
    
    # Initialize database
    create_tables()
    logger.info("✓ Database initialized")
    
    # Log feature flags
    if settings.is_enhanced_mode():
        logger.info("✓ Enhanced features enabled")
        if settings.ENABLE_DTO_VALIDATION:
            logger.info("  - DTO validation enabled")
        if settings.ENABLE_ADVANCED_SECURITY:
            logger.info("  - Advanced security enabled")
        if settings.ENABLE_AI_VALIDATION:
            logger.info("  - AI validation enabled")
    else:
        logger.info("✓ Running in legacy compatibility mode")
    
    yield  # Application runs here
    
    logger.info("🛑 Shutting down gracefully")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create FastAPI instance
    app = FastAPI(
        title="Marketing Agents API",
        description="Unified AI Agent Management API with feature flags",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Setup components
    setup_exception_handlers(app)
    setup_middleware(app)
    setup_cors(app)
    setup_routers(app)
    
    return app


def setup_cors(app: FastAPI):
    """Setup CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_routers(app: FastAPI):
    """Setup all routers"""
    from ..routers.agent_router import router as agent_router
    from ..routers.health_router import router as health_router
    
    # Include routers
    app.include_router(agent_router)
    app.include_router(health_router)
    
    logger.info("✓ Routers configured")



