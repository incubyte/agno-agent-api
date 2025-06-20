"""
Unified Agent Service
Single service supporting both legacy and enhanced features.
"""

import logging
import time
import textwrap
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from ..models.database import Agent
from ..repositories.agent_repository import AgentRepository
from ..schemas.agent import *
from ..agents.agent_factory import AgentFactory, agent_prompt_repository
from ..agents.enum import AgentType
from ..utils.validation import validation_service
from ..core.config import settings
from ..core.exceptions import NotFoundException, ValidationException, BusinessLogicException

logger = logging.getLogger(__name__)


class AgentService:
    """Unified agent service with configurable features"""
    
    def __init__(self):
        self.repository = AgentRepository()
        self.validation_service = validation_service
    
    # =============================================================================
    # UNIFIED METHODS - Support both legacy and enhanced modes
    # =============================================================================
    
    def get_all_agents(
        self, 
        filters: Optional[AgentFilterRequest] = None,
        return_dto: bool = None
    ) -> Union[List[Dict], AgentListResponse]:
        """
        Get all agents with optional filtering
        
        Args:
            filters: Optional filter parameters
            return_dto: Whether to return DTO format (auto-detected if None)
        
        Returns:
            Either list of dicts (legacy) or AgentListResponse (enhanced)
        """
        try:
            # Auto-detect return format
            if return_dto is None:
                return_dto = (
                    filters is not None or 
                    settings.ENABLE_DTO_VALIDATION or
                    settings.is_enhanced_mode()
                )
            
            # Get agents from repository
            if filters:
                # Use enhanced filtering
                agents = self.repository.search(
                    name_contains=filters.name_contains,
                    has_description=filters.has_description,
                    has_image=filters.has_image,
                    limit=filters.limit,
                    offset=filters.offset
                )
                total = self.repository.count()  # In production, optimize this
            else:
                # Get all agents
                agents = self.repository.get_all()
                total = len(agents)
            
            # Return appropriate format
            if return_dto:
                # Enhanced DTO response
                agent_responses = [create_agent_response(agent) for agent in agents]
                
                if filters:
                    return AgentListResponse.create(
                        items=agent_responses,
                        total=total,
                        page=filters.page,
                        limit=filters.limit
                    )
                else:
                    return AgentListResponse.create(
                        items=agent_responses,
                        total=total,
                        page=1,
                        limit=total
                    )
            else:
                # Legacy dict response
                return [self._agent_to_dict(agent) for agent in agents]
                
        except Exception as e:
            logger.error(f"Failed to get agents: {str(e)}")
            raise
    
    def get_agent_by_id(
        self, 
        agent_id: int,
        return_dto: bool = None,
        include_prompt: bool = True
    ) -> Union[Dict[str, Any], AgentDetailResponse]:
        """
        Get agent by ID
        
        Args:
            agent_id: Agent ID
            return_dto: Whether to return DTO format
            include_prompt: Whether to include agent prompt
        
        Returns:
            Either dict (legacy) or AgentDetailResponse (enhanced)
        """
        try:
            agent = self.repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Auto-detect return format
            if return_dto is None:
                return_dto = settings.ENABLE_DTO_VALIDATION
            
            # Get prompt if requested
            prompt = None
            if include_prompt:
                try:
                    prompt = self.get_prompt(agent.slug)
                except:
                    logger.warning(f"Could not get prompt for agent {agent_id}")
            
            if return_dto:
                # Enhanced DTO response
                return create_agent_detail_response(agent, prompt)
            else:
                # Legacy dict response
                result = self._agent_to_dict(agent)
                if prompt:
                    result["prompt"] = prompt
                return result
                
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {str(e)}")
            raise
    
    def create_agent(
        self, 
        data: Union[CreateAgentRequest, Dict[str, Any]],
        validate_enhanced: bool = None
    ) -> Union[Dict[str, Any], AgentCreatedResponse]:
        """
        Create new agent
        
        Args:
            data: Agent data (DTO or dict)
            validate_enhanced: Whether to use enhanced validation
        
        Returns:
            Either dict (legacy) or AgentCreatedResponse (enhanced)
        """
        try:
            # Determine validation level
            validate_enhanced = validate_enhanced if validate_enhanced is not None else settings.ENABLE_ENHANCED_VALIDATION
            
            # Normalize input data
            if isinstance(data, CreateAgentRequest):
                validated_data = data.model_dump()
                return_dto = True
            else:
                # Legacy dict input
                validated_data = data.copy()
                return_dto = False
                
                # Apply DTO validation if enhanced mode
                if validate_enhanced or settings.ENABLE_DTO_VALIDATION:
                    dto = CreateAgentRequest(**validated_data)
                    validated_data = dto.model_dump()
                    return_dto = True
            
            # Additional validation
            if validate_enhanced:
                self.validation_service.validate_agent_data(validated_data, "create")
            
            # Check uniqueness
            if self.repository.exists_by_slug(validated_data["slug"]):
                raise BusinessLogicException(f"Agent with slug '{validated_data['slug']}' already exists")
            
            # Create agent
            agent = Agent(**validated_data)
            created_agent = self.repository.create(agent)
            
            logger.info(f"Created agent: {created_agent.name} (ID: {created_agent.id})")
            
            # Return appropriate format
            if return_dto:
                return AgentCreatedResponse.model_validate(created_agent)
            else:
                return self._agent_to_dict(created_agent)
                
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise
    
    def update_agent(
        self,
        agent_id: int,
        data: Union[UpdateAgentRequest, Dict[str, Any]]
    ) -> Union[Dict[str, Any], AgentUpdatedResponse]:
        """
        Update existing agent
        
        Args:
            agent_id: Agent ID to update
            data: Update data (DTO or dict)
        
        Returns:
            Either dict (legacy) or AgentUpdatedResponse (enhanced)
        """
        try:
            # Get existing agent
            agent = self.repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Normalize input data
            if isinstance(data, UpdateAgentRequest):
                if not data.has_updates():
                    raise ValidationException("No fields provided for update")
                update_data = {k: v for k, v in data.model_dump().items() if v is not None}
                return_dto = True
            else:
                # Legacy dict input
                update_data = {k: v for k, v in data.items() if v is not None}
                return_dto = settings.ENABLE_DTO_VALIDATION
                
                if not update_data:
                    raise ValidationException("No fields provided for update")
            
            # Track changes
            changes = {}
            
            # Apply updates
            for field, value in update_data.items():
                if hasattr(agent, field):
                    old_value = getattr(agent, field)
                    if old_value != value:
                        changes[field] = {"from": old_value, "to": value}
                        setattr(agent, field, value)
            
            # Check slug uniqueness if changed
            if "slug" in changes:
                if self.repository.exists_by_slug(update_data["slug"], exclude_id=agent_id):
                    raise BusinessLogicException(f"Agent with slug '{update_data['slug']}' already exists")
            
            # Validation
            if settings.ENABLE_ENHANCED_VALIDATION:
                self.validation_service.validate_agent_data(update_data, "update")
            
            # Update in database
            updated_agent = self.repository.update(agent)
            
            logger.info(f"Updated agent {agent_id}: {list(changes.keys())}")
            
            # Return appropriate format
            if return_dto:
                response = AgentUpdatedResponse.model_validate(updated_agent)
                response.changes = changes
                return response
            else:
                result = self._agent_to_dict(updated_agent)
                result["changes"] = changes
                return result
                
        except Exception as e:
            logger.error(f"Failed to update agent {agent_id}: {str(e)}")
            raise
    
    def run_agent(
        self,
        agent_id: int,
        request: Union[RunAgentRequest, Dict[str, Any]]
    ) -> Union[str, AgentExecutionResponse]:
        """
        Execute agent with prompt
        
        Args:
            agent_id: Agent ID to run
            request: Execution request (DTO or dict)
        
        Returns:
            Either string response (legacy) or AgentExecutionResponse (enhanced)
        """
        start_time = time.time()
        
        try:
            # Get agent
            agent = self.repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Normalize request
            if isinstance(request, RunAgentRequest):
                prompt = request.prompt
                user_email = request.user_email
                parameters = request.parameters
                return_dto = True
            else:
                # Legacy dict input
                prompt = request.get("prompt")
                user_email = request.get("user_email")
                parameters = request.get("parameters")
                return_dto = settings.ENABLE_DTO_VALIDATION
            
            # Validation
            validation_data = {
                "prompt": prompt,
                "user_email": user_email
            }
            
            if settings.ENABLE_AI_VALIDATION:
                self.validation_service.validate_agent_data(validation_data, "run")
            
            # Get agent implementation
            try:
                ai_agent = AgentFactory.get_agent(AgentType(agent.slug))
            except ValueError:
                raise BusinessLogicException(f"Agent type '{agent.slug}' is not supported")
            
            # Generate response
            response = ai_agent.get_response(prompt, parameters=parameters or {})
            clean_response = textwrap.dedent(response).strip()
            
            # Calculate metrics
            execution_time_ms = (time.time() - start_time) * 1000
            token_count = len(clean_response.split())  # Rough estimation
            
            logger.info(f"Agent {agent_id} executed in {execution_time_ms:.2f}ms")
            
            # Return appropriate format
            if return_dto:
                return AgentExecutionResponse(
                    agent_id=agent_id,
                    agent_name=agent.name,
                    response=clean_response,
                    execution_time_ms=execution_time_ms,
                    token_count=token_count,
                    executed_at=datetime.utcnow()
                )
            else:
                return clean_response
                
        except Exception as e:
            logger.error(f"Failed to run agent {agent_id}: {str(e)}")
            raise
    
    def delete_agent(self, agent_id: int) -> bool:
        """Delete agent by ID"""
        try:
            success = self.repository.delete(agent_id)
            if success:
                logger.info(f"Deleted agent {agent_id}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete agent {agent_id}: {str(e)}")
            raise
    
    # =============================================================================
    # LEGACY COMPATIBILITY METHODS
    # =============================================================================
    
    def get_agent_by_slug(self, slug: str) -> Optional[Agent]:
        """Get agent by slug (legacy method)"""
        return self.repository.get_by_slug(slug)
    
    def agent_exists_by_slug(self, slug: str) -> bool:
        """Check if agent exists by slug (legacy method)"""
        return self.repository.exists_by_slug(slug)
    
    def get_agent_count(self) -> int:
        """Get total agent count (legacy method)"""
        return self.repository.count()
    
    def get_prompt(self, slug: str) -> str:
        """Get agent prompt by slug (legacy method)"""
        try:
            return agent_prompt_repository.get(AgentType(slug))
        except ValueError:
            raise NotFoundException("Prompt", slug)
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _agent_to_dict(self, agent: Agent) -> Dict[str, Any]:
        """Convert agent model to dict (legacy format)"""
        return {
            "id": agent.id,
            "name": agent.name,
            "slug": agent.slug,
            "description": agent.description,
            "image": agent.image,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "updated_at": agent.updated_at.isoformat() if agent.updated_at else None
        }
    



# Dependency injection
def get_agent_service() -> AgentService:
    """Get agent service instance"""
    return AgentService()
