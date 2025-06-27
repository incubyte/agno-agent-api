"""
Enhanced Agent Service - Business logic layer with comprehensive error handling
This service handles the business logic and coordinates between the route layer and repository layer.
"""
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import textwrap
import time
import logging

from app.db.models import Agent
from app.db.repository.agent_repository import AgentRepository
from app.agents.agent_factory import AgentFactory
from app.agents.agent_prompt_repository import agent_prompt_repository
from app.agents.enum.agent_enum import AgentType

# Import new error handling and validation
from app.core.exceptions import NotFoundException, ValidationException, BusinessLogicException
from app.core.setting import settings
from app.utils.validation import validation_service
from app.schemas.agent import (
    CreateAgentRequest, UpdateAgentRequest, RunAgentRequest, LegacyAgentRequest,
    AgentResponse, AgentDetailResponse, AgentExecutionResponse, AgentCreatedResponse,
    AgentUpdatedResponse, create_agent_response, create_agent_detail_response
)

logger = logging.getLogger(__name__)


class AgentService:
    """Enhanced service layer for managing agents and their operations"""
    
    def __init__(self):
        self.agent_repository = AgentRepository()
        self.validation_service = validation_service
    
    # =============================================================================
    # ENHANCED METHODS WITH COMPREHENSIVE ERROR HANDLING
    # =============================================================================
    
    def get_all_agents(self, return_dto: bool = None) -> Union[List[Agent], List[Dict[str, Any]]]:
        """Get all agents from the repository with optional DTO format"""
        try:
            agents = self.agent_repository.get_all()
            
            # Auto-detect return format based on settings
            if return_dto is None:
                return_dto = settings.ENABLE_DTO_VALIDATION
            
            if return_dto:
                return [self._agent_to_dict(agent) for agent in agents]
            
            return agents
        except Exception as e:
            logger.error(f"Failed to retrieve agents: {str(e)}")
            raise BusinessLogicException(f"Failed to retrieve list of agents: {str(e)}")

    def get_agent_by_id(self, agent_id: int, return_dto: bool = None) -> Union[Agent, Dict[str, Any]]:
        """Get a specific agent by ID with enhanced error handling"""
        try:
            agent = self.agent_repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Auto-detect return format based on settings
            if return_dto is None:
                return_dto = settings.ENABLE_DTO_VALIDATION
            
            if return_dto:
                return self._agent_to_dict(agent)
            
            return agent
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {str(e)}")
            raise BusinessLogicException(f"Failed to retrieve agent: {str(e)}")
    
    def get_prompt(self, slug: str) -> str:
        """Get the prompt for a specific agent by slug with error handling"""
        try:
            agent_type = AgentType(slug)
            prompt = agent_prompt_repository.get(agent_type)
            if not prompt:
                logger.warning(f"No prompt found for agent slug: {slug}")
                return "Enter your prompt here"
            return prompt
        except ValueError as e:
            logger.warning(f"Invalid agent type: {slug}")
            raise NotFoundException("Agent type", slug)
        except Exception as e:
            logger.error(f"Failed to get prompt for {slug}: {str(e)}")
            return "Enter your prompt here"

    def create_agent(self, agent_data: Union[Agent, CreateAgentRequest, Dict[str, Any]]) -> Union[Agent, Dict[str, Any]]:
        """Create a new agent with comprehensive validation"""
        try:
            # Normalize input data
            if isinstance(agent_data, Agent):
                # Direct Agent model
                validated_data = {
                    "name": agent_data.name,
                    "slug": agent_data.slug,
                    "description": agent_data.description,
                    "image": agent_data.image
                }
                return_dto = False
            elif isinstance(agent_data, CreateAgentRequest):
                # DTO input
                validated_data = agent_data.model_dump()
                return_dto = True
            else:
                # Dict input - apply validation if enhanced mode
                validated_data = agent_data.copy()
                return_dto = settings.ENABLE_DTO_VALIDATION
                
                if settings.ENABLE_DTO_VALIDATION:
                    # Convert to DTO for validation
                    dto = CreateAgentRequest(**validated_data)
                    validated_data = dto.model_dump()
            
            # Additional validation
            if settings.ENABLE_ENHANCED_VALIDATION:
                self.validation_service.validate_agent_data(validated_data, "create")
            
            # Business logic validation
            if not validated_data.get("name") or not validated_data.get("slug"):
                raise ValidationException("Agent name and slug are required")
            
            # Check uniqueness
            if self.agent_repository.exists_by_slug(validated_data["slug"]):
                raise BusinessLogicException(f"Agent with slug '{validated_data['slug']}' already exists")

            # Create agent
            agent = Agent(**validated_data)
            created_agent = self.agent_repository.create(agent)
            
            logger.info(f"Created agent: {created_agent.name} (ID: {created_agent.id})")
            
            if return_dto:
                return self._agent_to_dict(created_agent)
            
            return created_agent
            
        except (ValidationException, BusinessLogicException):
            raise
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise BusinessLogicException(f"Failed to create agent: {str(e)}")

    def run_agent_by_id(self, agent_id: int, prompt: str, user_email: Optional[str] = None, 
                       parameters: Optional[Dict[str, Any]] = None) -> Union[str, AgentExecutionResponse]:
        """Run an agent by ID with enhanced validation and error handling"""
        start_time = time.time()
        
        try:
            # Prepare validation data
            validation_data = {
                "prompt": prompt,
                "user_email": user_email
            }
            
            # Validate inputs
            if settings.ENABLE_AI_VALIDATION:
                self.validation_service.validate_agent_data(validation_data, "run")
            elif not prompt:
                raise ValidationException("Prompt must not be empty")
            
            # Get agent data from repository
            agent = self.agent_repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Get agent implementation
            try:
                ai_agent = AgentFactory.get_agent(AgentType(agent.slug))
            except ValueError:
                raise BusinessLogicException(f"Agent type '{agent.slug}' is not supported")
            
            # Generate response
            response = ai_agent.get_response(prompt)
            clean_response = textwrap.dedent(response).lstrip()
            
            # Calculate metrics
            execution_time_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Agent {agent_id} executed successfully in {execution_time_ms:.2f}ms")
            
            # Return format based on settings
            if settings.ENABLE_DTO_VALIDATION:
                return AgentExecutionResponse(
                    agent_id=agent_id,
                    agent_name=agent.name,
                    response=clean_response,
                    execution_time_ms=execution_time_ms,
                    executed_at=datetime.utcnow()
                ).model_dump()
            
            return clean_response
            
        except (ValidationException, NotFoundException, BusinessLogicException):
            raise
        except Exception as e:
            logger.error(f"Failed to run agent {agent_id}: {str(e)}")
            raise BusinessLogicException(f"Failed to execute agent: {str(e)}")

    def update_agent(self, agent_id: int, updated_data: Union[UpdateAgentRequest, Dict[str, Any]]) -> Union[Agent, Dict[str, Any]]:
        """Update an existing agent with validation"""
        try:
            # Get existing agent
            agent = self.agent_repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            # Normalize update data
            if isinstance(updated_data, UpdateAgentRequest):
                if not updated_data.has_updates():
                    raise ValidationException("No fields provided for update")
                update_data = {k: v for k, v in updated_data.model_dump().items() if v is not None}
                return_dto = True
            else:
                update_data = {k: v for k, v in updated_data.items() if v is not None}
                return_dto = settings.ENABLE_DTO_VALIDATION
                
                if not update_data:
                    raise ValidationException("No fields provided for update")
            
            # Validation
            if settings.ENABLE_ENHANCED_VALIDATION:
                self.validation_service.validate_agent_data(update_data, "update")
            
            # Check slug uniqueness if changed
            if "slug" in update_data and update_data["slug"] != agent.slug:
                if self.agent_repository.exists_by_slug(update_data["slug"]):
                    raise BusinessLogicException(f"Agent with slug '{update_data['slug']}' already exists")
            
            # Update agent fields
            for key, value in update_data.items():
                if hasattr(agent, key):
                    setattr(agent, key, value)
            
            # Update timestamp
            agent.updated_at = datetime.utcnow()
            
            # Save to database
            updated_agent = self.agent_repository.update(agent)
            
            logger.info(f"Updated agent {agent_id}: {list(update_data.keys())}")
            
            if return_dto:
                return self._agent_to_dict(updated_agent)
            
            return updated_agent
            
        except (ValidationException, NotFoundException, BusinessLogicException):
            raise
        except Exception as e:
            logger.error(f"Failed to update agent {agent_id}: {str(e)}")
            raise BusinessLogicException(f"Failed to update agent: {str(e)}")

    def delete_agent(self, agent_id: int) -> bool:
        """Delete an agent with error handling"""
        try:
            agent = self.agent_repository.get_by_id(agent_id)
            if not agent:
                raise NotFoundException("Agent", agent_id)
            
            self.agent_repository.delete(agent)
            logger.info(f"Deleted agent {agent_id}")
            return True
            
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete agent {agent_id}: {str(e)}")
            raise BusinessLogicException(f"Failed to delete agent: {str(e)}")

    def get_agent_by_slug(self, slug: str) -> Union[Agent, Dict[str, Any]]:
        """Get an agent by slug with error handling"""
        try:
            agent = self.agent_repository.get_by_slug(slug)
            if not agent:
                raise NotFoundException("Agent", slug)
            
            if settings.ENABLE_DTO_VALIDATION:
                return self._agent_to_dict(agent)
            
            return agent
            
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to get agent by slug {slug}: {str(e)}")
            raise BusinessLogicException(f"Failed to retrieve agent: {str(e)}")

    def agent_exists_by_slug(self, slug: str) -> bool:
        """Check if an agent exists with the given slug"""
        try:
            return self.agent_repository.exists_by_slug(slug)
        except Exception as e:
            logger.error(f"Failed to check agent existence for {slug}: {str(e)}")
            raise BusinessLogicException(f"Failed to check agent existence: {str(e)}")

    def get_agent_count(self) -> Dict[str, int]:
        """Get the total count of agents"""
        try:
            return self.agent_repository.agent_count()
        except Exception as e:
            logger.error(f"Failed to get agent count: {str(e)}")
            raise BusinessLogicException(f"Failed to get agent count: {str(e)}")
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _agent_to_dict(self, agent: Agent) -> Dict[str, Any]:
        """Convert agent model to dict (enhanced format)"""
        return {
            "id": agent.id,
            "name": agent.name,
            "slug": agent.slug,
            "description": agent.description,
            "image": agent.image,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "updated_at": agent.updated_at.isoformat() if agent.updated_at else None
        }
