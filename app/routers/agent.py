"""
Enhanced Agent Router with comprehensive error handling and validation.
Preserves existing functionality while adding new features.
"""

from fastapi import APIRouter, Depends, Request, Query, Header
from fastapi_utils.cbv import cbv
from typing import Optional, Union, Dict, Any
import logging

from app.service.agent_service import AgentService
from app.service import PdfService, EmailService
from app.db.models import Agent
from app.core.setting import settings

# Import new schemas and validation
from app.schemas.agent import (
    CreateAgentRequest, UpdateAgentRequest, RunAgentRequest, LegacyAgentRequest,
    AgentResponse, AgentDetailResponse, AgentExecutionResponse,
    create_agent_response, create_agent_detail_response
)

logger = logging.getLogger(__name__)

router = APIRouter()


# =============================================================================
# BACKWARD COMPATIBILITY CLASSES
# =============================================================================

class AgentRequest(LegacyAgentRequest):
    """Legacy agent request for backward compatibility"""
    pass


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
    
    # Default based on settings
    return settings.ENABLE_DTO_VALIDATION


@cbv(router)
class AgentRouter:
    """Enhanced router for agent-related endpoints with comprehensive error handling"""

    agent_service: AgentService = Depends(AgentService)
    pdf_service: PdfService = Depends(PdfService)
    email_service: EmailService = Depends(EmailService)

    @router.get("/agents")
    def get_agents(
        self,
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format")
    ):
        """
        Get all agents with flexible response format
        
        Supports both legacy and enhanced response formats based on:
        - Accept header (application/vnd.api+json for enhanced)
        - Explicit format parameter
        - Application settings
        """
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        # Get agents from service
        agents = self.agent_service.get_all_agents(return_dto=use_enhanced)
        
        # Legacy behavior: raise 404 if no agents (preserve existing behavior)
        if not agents and not use_enhanced:
            from app.core.exceptions import NotFoundException
            raise NotFoundException("Agents")
        
        logger.info(f"Get agents: format={'enhanced' if use_enhanced else 'legacy'}")
        
        return agents

    @router.get("/agents/count")
    def get_agent_count(self):
        """Get the total count of agents"""
        return self.agent_service.get_agent_count()

    @router.get("/agents/{agent_id}")
    def get_agent(
        self, 
        agent_id: int,
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format"),
        include_prompt: bool = Query(default=True, description="Include agent prompt in response")
    ):
        """
        Get a specific agent by ID with flexible response format
        
        Returns either:
        - Legacy: Simple agent object with optional prompt
        - Enhanced: Detailed agent response with computed fields and metadata
        """
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        logger.info(f"Fetching agent with ID: {agent_id}")
        
        # Get agent from service
        agent = self.agent_service.get_agent_by_id(agent_id, return_dto=use_enhanced)
        
        # Get prompt if requested
        prompt = None
        if include_prompt:
            try:
                # For legacy compatibility, pass agent.slug if agent is dict, otherwise agent object
                slug = agent.get("slug") if isinstance(agent, dict) else agent.slug
                prompt = self.agent_service.get_prompt(slug)
            except Exception as e:
                logger.warning(f"Could not get prompt for agent {agent_id}: {str(e)}")
                prompt = "Enter your prompt here"
        
        # Format response
        if use_enhanced:
            # Enhanced response with computed fields
            if isinstance(agent, dict):
                result = agent.copy()
            else:
                result = self.agent_service._agent_to_dict(agent)
            
            if prompt:
                result["prompt"] = prompt
            return result
        else:
            # Legacy format (preserve existing structure)
            logger.info(f"Found agent: {agent}, Prompt: {prompt}")
            result = {"agent": agent, "prompt": prompt}
            return result

    @router.post("/create-agent")
    def create_agent(
        self, 
        agent: Union[Agent, CreateAgentRequest, Dict[str, Any]],
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format")
    ):
        """
        Create a new agent
        
        Accepts:
        - Legacy: Agent model directly
        - Enhanced: CreateAgentRequest DTO with full validation
        - Dict: Raw dictionary data
        """
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        # Create agent with appropriate validation
        created_agent = self.agent_service.create_agent(agent)
        
        logger.info(f"Created agent: {getattr(created_agent, 'name', created_agent.get('name', 'Unknown'))}")
        
        return created_agent

    @router.post("/run-agent/{agent_id}")
    def run_agent_by_id(
        self, 
        agent_id: int, 
        request_data: Union[AgentRequest, RunAgentRequest, Dict[str, Any]],
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format")
    ):
        """
        Run an agent by ID with a given prompt
        
        Accepts multiple input formats:
        - Legacy: AgentRequest with prompt and user_email
        - Enhanced: RunAgentRequest with full parameters
        - Dict: Raw dictionary data
        
        Returns either string response (legacy) or detailed execution response (enhanced).
        """
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        # Normalize request data
        if isinstance(request_data, (AgentRequest, LegacyAgentRequest)):
            prompt = request_data.prompt
            user_email = request_data.user_email
            parameters = None
        elif isinstance(request_data, RunAgentRequest):
            prompt = request_data.prompt
            user_email = request_data.user_email
            parameters = request_data.parameters
        else:
            # Dict input
            prompt = request_data.get("prompt")
            user_email = request_data.get("user_email")
            parameters = request_data.get("parameters")
        
        # Run agent
        response = self.agent_service.run_agent_by_id(
            agent_id=agent_id,
            prompt=prompt,
            user_email=user_email,
            parameters=parameters
        )
        
        logger.info(f"Agent {agent_id} executed successfully")
        
        # Format response based on mode
        if use_enhanced and isinstance(response, dict):
            return response
        elif isinstance(response, str):
            # Legacy format
            return {"response": response}
        else:
            # Enhanced response already formatted
            return response

    @router.put("/agents/{agent_id}")
    def update_agent(
        self, 
        agent_id: int, 
        updated_data: Union[UpdateAgentRequest, Dict[str, Any]],
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format")
    ):
        """
        Update an existing agent
        
        Accepts both:
        - Enhanced: UpdateAgentRequest DTO with validation
        - Legacy: Simple dict with basic validation
        """
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        # Update agent
        updated_agent = self.agent_service.update_agent(agent_id, updated_data)
        
        logger.info(f"Updated agent {agent_id}")
        
        return updated_agent

    @router.delete("/agents/{agent_id}")
    def delete_agent(self, agent_id: int):
        """Delete an agent"""
        success = self.agent_service.delete_agent(agent_id)
        
        logger.info(f"Deleted agent {agent_id}")
        
        return {"message": f"Agent with ID {agent_id} deleted successfully"}

    @router.get("/agents/slug/{slug}")
    def get_agent_by_slug(
        self, 
        slug: str,
        request: Request,
        accept_header: str = Header(default="application/json"),
        response_format: Optional[str] = Query(default=None, alias="format")
    ):
        """Get an agent by slug"""
        
        # Detect response format
        use_enhanced = detect_enhanced_request(request, accept_header, response_format)
        
        agent = self.agent_service.get_agent_by_slug(slug)
        
        logger.info(f"Retrieved agent by slug: {slug}")
        
        return agent
        
    @router.get("/agents/exists/{slug}")
    def check_agent_exists(self, slug: str):
        """Check if an agent exists with the given slug"""
        exists = self.agent_service.agent_exists_by_slug(slug)
        return {"exists": exists, "slug": slug}
