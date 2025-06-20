"""
Unified Agent Router
Single router supporting multiple API formats with auto-detection.
"""

from fastapi import APIRouter, Depends, Request, Query, Header
from typing import Union, Optional, Dict, Any, List
import logging

from ..services.agent_service import AgentService, get_agent_service
from ..schemas.agent import *
from ..core.config import settings
from ..core.exceptions import ValidationException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agents"])


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def detect_enhanced_request(
    request: Request,
    accept_header: str = Header(default="application/json"),
    explicit_format: Optional[str] = Query(default=None, alias="format")
) -> bool:
    """Detect if client wants enhanced response format"""
    
    # Explicit format parameter
    if explicit_format == "enhanced" or explicit_format == "dto":
        return True
    if explicit_format == "legacy":
        return False
    
    # Accept header detection
    if "application/vnd.api+json" in accept_header:
        return True
    
    # Check for enhanced query parameters
    query_params = dict(request.query_params)
    enhanced_params = ["name_contains", "has_description", "has_image", "page"]
    if any(param in query_params for param in enhanced_params):
        return True
    
    # Large page size requests get enhanced format
    limit = int(query_params.get("limit", 10))
    if limit > settings.MAX_LEGACY_PAGE_SIZE:
        return True
    
    # Default based on settings
    return settings.ENABLE_DTO_VALIDATION


# =============================================================================
# MAIN ENDPOINTS
# =============================================================================

@router.get("/")
async def get_agents(
    request: Request,
    # Legacy pagination parameters
    limit: int = Query(default=10, ge=1, le=100, description="Number of agents to return"),
    offset: int = Query(default=0, ge=0, description="Number of agents to skip"),
    
    # Enhanced filtering parameters (optional)
    name_contains: Optional[str] = Query(default=None, max_length=255, description="Filter by name containing text"),
    has_description: Optional[bool] = Query(default=None, description="Filter agents with/without descriptions"),
    has_image: Optional[bool] = Query(default=None, description="Filter agents with/without images"),
    
    # Response format detection
    accept_header: str = Header(default="application/json"),
    response_format: Optional[str] = Query(default=None, alias="format", description="Response format: legacy, enhanced, dto"),
    
    # Service dependency
    service: AgentService = Depends(get_agent_service)
):
    """
    Get all agents with flexible response format
    
    Supports both legacy and enhanced response formats:
    - Legacy: Simple list of agent objects
    - Enhanced: Paginated response with metadata and computed fields
    
    Format is auto-detected based on:
    - Accept header (application/vnd.api+json for enhanced)
    - Query parameters (enhanced params trigger enhanced response)
    - Explicit format parameter
    - Application settings
    """
    
    # Detect response format
    use_enhanced = detect_enhanced_request(request, accept_header, response_format)
    
    # Build filters if enhanced parameters provided
    filters = None
    if any([name_contains, has_description, has_image]) or use_enhanced:
        page = (offset // limit) + 1 if limit > 0 else 1
        filters = AgentFilterRequest(
            page=page,
            limit=limit,
            name_contains=name_contains,
            has_description=has_description,
            has_image=has_image
        )
    
    # Get agents from service
    result = service.get_all_agents(filters=filters, return_dto=use_enhanced)
    
    logger.info(f"Get agents: format={'enhanced' if use_enhanced else 'legacy'}, filters={filters is not None}")
    
    return result


@router.get("/{agent_id}")
async def get_agent(
    agent_id: int,
    request: Request,
    
    # Response format detection
    accept_header: str = Header(default="application/json"),
    response_format: Optional[str] = Query(default=None, alias="format"),
    include_prompt: bool = Query(default=True, description="Include agent prompt in response"),
    
    # Service dependency
    service: AgentService = Depends(get_agent_service)
):
    """
    Get agent by ID with flexible response format
    
    Returns either:
    - Legacy: Simple agent object with optional prompt
    - Enhanced: Detailed agent response with computed fields and metadata
    """
    
    # Detect response format
    use_enhanced = detect_enhanced_request(request, accept_header, response_format)
    
    # Get agent from service
    result = service.get_agent_by_id(
        agent_id=agent_id,
        return_dto=use_enhanced,
        include_prompt=include_prompt
    )
    
    logger.info(f"Get agent {agent_id}: format={'enhanced' if use_enhanced else 'legacy'}")
    
    return result


@router.post("/", status_code=201)
async def create_agent(
    data: CreateAgentRequest,
    service: AgentService = Depends(get_agent_service)
):
    """
    Create new agent
    
    Accepts CreateAgentRequest DTO with full validation.
    """
    
    # Create agent with DTO validation
    result = service.create_agent(data, validate_enhanced=True)
    
    logger.info(f"Create agent: {data.name}")
    
    return result


@router.put("/{agent_id}")
async def update_agent(
    agent_id: int,
    request: Request,
    data: Union[UpdateAgentRequest, Dict[str, Any]],
    
    # Response format detection
    accept_header: str = Header(default="application/json"),
    response_format: Optional[str] = Query(default=None, alias="format"),
    
    # Service dependency
    service: AgentService = Depends(get_agent_service)
):
    """
    Update existing agent
    
    Accepts both:
    - Enhanced: UpdateAgentRequest DTO with validation
    - Legacy: Simple dict with basic validation
    """
    
    # Auto-detect based on input type
    input_is_dto = isinstance(data, UpdateAgentRequest)
    use_enhanced = input_is_dto or detect_enhanced_request(request, accept_header, response_format)
    
    # Update agent
    result = service.update_agent(agent_id, data)
    
    logger.info(f"Update agent {agent_id}: input={'DTO' if input_is_dto else 'dict'}")
    
    return result


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
):
    """Delete agent by ID"""
    
    success = service.delete_agent(agent_id)
    if not success:
        from ..core.exceptions import NotFoundException
        raise NotFoundException("Agent", agent_id)
    
    logger.info(f"Delete agent {agent_id}")
    
    return None  # 204 No Content


@router.post("/{agent_id}/run")
async def run_agent(
    agent_id: int,
    request: Request,
    data: Union[RunAgentRequest, LegacyAgentRequest, Dict[str, Any]],
    
    # Response format detection
    accept_header: str = Header(default="application/json"),
    response_format: Optional[str] = Query(default=None, alias="format"),
    
    # Service dependency
    service: AgentService = Depends(get_agent_service)
):
    """
    Run agent with prompt
    
    Accepts multiple input formats:
    - Enhanced: RunAgentRequest with full parameters
    - Legacy: LegacyAgentRequest or simple dict
    
    Returns either string response (legacy) or detailed execution response (enhanced).
    """
    
    # Convert legacy format to standard format
    if isinstance(data, LegacyAgentRequest):
        # Convert legacy format
        run_data = {
            "prompt": data.prompt,
            "user_email": data.user_email,
            "generate_pdf": True,
            "send_email": True
        }
        input_is_dto = False
    elif isinstance(data, RunAgentRequest):
        run_data = data
        input_is_dto = True
    else:
        # Dict input - could be legacy or enhanced
        run_data = data
        input_is_dto = False
    
    # Detect response format
    use_enhanced = input_is_dto or detect_enhanced_request(request, accept_header, response_format)
    
    # Run agent
    result = service.run_agent(agent_id, run_data)
    
    logger.info(f"Run agent {agent_id}: format={'enhanced' if use_enhanced else 'legacy'}")
    
    return result


# =============================================================================
# ADDITIONAL ENDPOINTS
# =============================================================================

@router.get("/slug/{slug}")
async def get_agent_by_slug(
    slug: str,
    service: AgentService = Depends(get_agent_service)
):
    """Get agent by slug (legacy compatibility)"""
    
    agent = service.get_agent_by_slug(slug)
    if not agent:
        from ..core.exceptions import NotFoundException
        raise NotFoundException("Agent", slug)
    
    return service._agent_to_dict(agent)


@router.get("/slug/{slug}/exists")
async def check_agent_exists(
    slug: str,
    service: AgentService = Depends(get_agent_service)
):
    """Check if agent exists by slug"""
    
    exists = service.agent_exists_by_slug(slug)
    return {"exists": exists, "slug": slug}


@router.get("/stats/count")
async def get_agent_count(
    service: AgentService = Depends(get_agent_service)
):
    """Get total agent count"""
    
    count = service.get_agent_count()
    return {"count": count}


# =============================================================================
# BULK OPERATIONS (Enhanced only)
# =============================================================================

@router.post("/bulk/create")
async def bulk_create_agents(
    agents: List[CreateAgentRequest],
    service: AgentService = Depends(get_agent_service)
):
    """Bulk create agents (enhanced feature)"""
    
    if len(agents) > 10:
        raise ValidationException("Maximum 10 agents per bulk operation")
    
    results = []
    for idx, agent_data in enumerate(agents):
        try:
            result = service.create_agent(agent_data)
            results.append({
                "index": idx,
                "success": True,
                "agent": result
            })
        except Exception as e:
            results.append({
                "index": idx,
                "success": False,
                "error": str(e)
            })
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    return {
        "total": len(agents),
        "successful": successful,
        "failed": failed,
        "results": results
    }


# =============================================================================
# LEGACY MARKETING AGENT ENDPOINT
# =============================================================================

@router.post("/marketing/analyze")
async def run_marketing_agent(
    data: LegacyMarketingAgentRequest,
    service: AgentService = Depends(get_agent_service)
):
    """Legacy marketing agent endpoint for backward compatibility"""
    
    # Find marketing agent
    marketing_agent = service.get_agent_by_slug("marketing-agent")
    if not marketing_agent:
        raise ValidationException("Marketing agent not found. Please create it first.")
    
    # Convert URL to prompt
    prompt = f"Analyze the website at {data.url} and provide marketing insights and recommendations."
    
    # Run agent in legacy mode
    result = service.run_agent(
        agent_id=marketing_agent.id,
        request={
            "prompt": prompt,
            "user_email": data.user_email
        }
    )
    
    return {"response": result}
