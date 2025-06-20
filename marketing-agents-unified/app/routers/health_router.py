"""
Health Check Router
System health and status endpoints.
"""

from fastapi import APIRouter, Depends
from datetime import datetime
import logging

from ..services.agent_service import AgentService, get_agent_service
from ..core.config import settings
from ..agents.agent_factory import AgentFactory

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check(
    service: AgentService = Depends(get_agent_service)
):
    """Detailed health check with dependency status"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "marketing-agents-unified",
        "dependencies": {},
        "features": {
            "enhanced_validation": settings.ENABLE_ENHANCED_VALIDATION,
            "dto_validation": settings.ENABLE_DTO_VALIDATION,
            "advanced_security": settings.ENABLE_ADVANCED_SECURITY,
            "ai_validation": settings.ENABLE_AI_VALIDATION,
            "rate_limiting": settings.ENABLE_RATE_LIMITING,
            "caching": settings.ENABLE_CACHING
        },
        "configuration": {
            "default_api_version": settings.DEFAULT_API_VERSION,
            "support_legacy_format": settings.SUPPORT_LEGACY_FORMAT,
            "max_request_size": settings.MAX_REQUEST_SIZE,
            "max_prompt_length": settings.MAX_PROMPT_LENGTH
        }
    }
    
    # Check database health
    try:
        agent_count = service.get_agent_count()
        health_status["dependencies"]["database"] = {
            "status": "healthy",
            "agent_count": agent_count
        }
    except Exception as e:
        health_status["dependencies"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check AI agent system
    try:
        available_types = AgentFactory.get_available_types()
        health_status["dependencies"]["ai_agents"] = {
            "status": "healthy",
            "available_types": [t.value for t in available_types],
            "count": len(available_types)
        }
    except Exception as e:
        health_status["dependencies"]["ai_agents"] = {
            "status": "unhealthy", 
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Overall status check
    unhealthy_deps = [
        dep for dep, info in health_status["dependencies"].items()
        if info["status"] != "healthy"
    ]
    
    if unhealthy_deps:
        health_status["status"] = "degraded"
        health_status["unhealthy_dependencies"] = unhealthy_deps
    
    return health_status


@router.get("/features")
async def feature_status():
    """Get current feature flag status"""
    return {
        "feature_flags": {
            "enhanced_validation": settings.ENABLE_ENHANCED_VALIDATION,
            "dto_validation": settings.ENABLE_DTO_VALIDATION,
            "advanced_security": settings.ENABLE_ADVANCED_SECURITY,
            "ai_validation": settings.ENABLE_AI_VALIDATION,
            "rate_limiting": settings.ENABLE_RATE_LIMITING,
            "caching": settings.ENABLE_CACHING,
            "request_logging": settings.ENABLE_REQUEST_LOGGING
        },
        "api_configuration": {
            "default_version": settings.DEFAULT_API_VERSION,
            "legacy_support": settings.SUPPORT_LEGACY_FORMAT,
            "auto_enhance_large_requests": settings.AUTO_ENHANCE_LARGE_REQUESTS,
            "max_legacy_page_size": settings.MAX_LEGACY_PAGE_SIZE
        },
        "limits": {
            "max_request_size": settings.MAX_REQUEST_SIZE,
            "max_prompt_length": settings.MAX_PROMPT_LENGTH,
            "min_prompt_length": settings.MIN_PROMPT_LENGTH,
            "max_agent_name_length": settings.MAX_AGENT_NAME_LENGTH,
            "max_description_length": settings.MAX_DESCRIPTION_LENGTH,
            "default_rate_limit": settings.DEFAULT_RATE_LIMIT,
            "burst_limit": settings.BURST_LIMIT
        }
    }


@router.get("/agents")
async def agent_system_status(
    service: AgentService = Depends(get_agent_service)
):
    """Get agent system status"""
    
    try:
        # Get agent statistics
        agent_count = service.get_agent_count()
        
        # Get available agent types
        available_types = AgentFactory.get_available_types()
        
        # Get sample of existing agents
        all_agents = service.get_all_agents(return_dto=False)
        agent_slugs = [agent.get("slug") for agent in all_agents[:10]]  # First 10
        
        return {
            "status": "healthy",
            "agent_count": agent_count,
            "available_types": [t.value for t in available_types],
            "sample_agents": agent_slugs,
            "factory_status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Agent system health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "agent_count": 0,
            "available_types": [],
            "sample_agents": [],
            "factory_status": "error"
        }
