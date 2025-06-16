"""
Agent Service - Business logic layer for agent operations
This service handles the business logic and coordinates between the route layer and repository layer.
"""
from typing import List, Optional
from app.db.models import Agent
from app.db.repository.agent_repository import AgentRepository
from app.agents.agent_factory import AgentFactory
import textwrap
from fastapi import HTTPException




class AgentService:
    """Service layer for managing agents and their operations"""
    
    def __init__(self):
        self.agent_repository = AgentRepository()
    
    def get_all_agents(self) -> List[Agent]:
        """Get all agents from the repository"""
        try:
            agents = self.agent_repository.get_all()
            return agents
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve list of agents: {str(e)}")

    def get_agent_by_id(self, agent_id: int) -> Optional[Agent]:
        """Get a specific agent by ID"""
        try:
            agent = self.agent_repository.get_by_id(agent_id)
            return agent
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve agent with ID {agent_id}: {str(e)}")

    def create_agent(self, agent: Agent) -> Agent:
        """Create a new agent"""
        try:
            # Add any business logic validation here
            if not agent.name or not agent.slug:
                raise ValueError("Agent name and slug are required")
            
            # Check if agent with same slug already exists
            if self.agent_repository.exists_by_slug(agent.slug):
                raise ValueError(f"Agent with slug '{agent.slug}' already exists")
            
            created_agent = self.agent_repository.create(agent)
            return created_agent
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create agent: {str(e)}")

    def run_agent_by_id(self, agent_id: int, prompt: str, user_email: str) -> str:
        """Run an agent by ID with the given prompt"""
        try:
            # Validate inputs
            if not prompt:
                raise ValueError("Prompt must not be empty")
            if not user_email:
                raise ValueError("User email must not be empty")
            
            # Get agent data from repository
            agent_data = self.get_agent_by_id(agent_id)
            if not agent_data:
                raise ValueError(f"Agent with ID {agent_id} not found")
            
            # Get the appropriate agent from factory
            agent = AgentFactory.get_agent(agent_data.slug)
            
            # Generate response
            response = agent.get_response(prompt)
            
            # Clean up response
            clean_response = textwrap.dedent(response).lstrip()
            
            return clean_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to run agent: {str(e)}")

    def update_agent(self, agent_id: int, updated_data: dict) -> Optional[Agent]:
        """Update an existing agent"""
        try:
            agent = self.get_agent_by_id(agent_id)
            if not agent:
                raise ValueError(f"Agent with ID {agent_id} not found")
            
            # Update agent fields
            for key, value in updated_data.items():
                if hasattr(agent, key):
                    setattr(agent, key, value)
            
            # Use the repository update method
            return self.agent_repository.update(agent)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update agent: {str(e)}")

    def delete_agent(self, agent_id: int) -> bool:
        """Delete an agent"""
        try:
            return self.agent_repository.delete(agent_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to delete agent: {str(e)}")

    def get_agent_by_slug(self, slug: str) -> Optional[Agent]:
        """Get an agent by slug"""
        try:
            return self.agent_repository.get_by_slug(slug)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve agent with slug {slug}: {str(e)}")

    def agent_exists_by_slug(self, slug: str) -> bool:
        """Check if an agent exists with the given slug"""
        try:
            return self.agent_repository.exists_by_slug(slug)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to check agent existence: {str(e)}")

    def get_agent_count(self) -> int:
        """Get the total count of agents"""
        try:
            return self.agent_repository.count()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get agent count: {str(e)}")
