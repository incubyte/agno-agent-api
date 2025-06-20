"""
Agent Factory Implementation
Factory class for creating agent instances and managing agent types.
"""

from typing import List
from .enum import AgentType
from .base_agent import BaseAgent
from .marketing_agents import MarketingAgent
from .linkedin_writer_agent import LinkedInWriterAgent
from .tech_blog_writer_agent import TechBlogWriterAgent
from .lifestyle_blog_writer_agent import LifestyleBlogWriterAgent


class AgentFactory:
    """Factory class for creating agent instances"""
    
    _agents = {
        AgentType.MARKETING_AGENT: MarketingAgent,
        AgentType.TECH_BLOG_WRITER: TechBlogWriterAgent,
        AgentType.LINKEDIN_WRITER: LinkedInWriterAgent,
        AgentType.LIFESTYLE_BLOG_WRITER: LifestyleBlogWriterAgent
    }
    
    @classmethod
    def get_agent(cls, agent_type: AgentType) -> BaseAgent:
        """Get agent instance by type"""
        if agent_type not in cls._agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return cls._agents[agent_type]()
    
    @classmethod
    def get_available_types(cls) -> List[AgentType]:
        """Get list of available agent types"""
        return list(cls._agents.keys())
    
    @classmethod
    def get_agent_prompt(cls, agent_type: AgentType) -> str:
        """Get the system prompt for an agent type"""
        agent = cls.get_agent(agent_type)
        return agent.get_prompt_template()


# Agent prompt repository for backward compatibility
class AgentPromptRepository:
    """Repository for agent prompts"""
    
    @staticmethod
    def get(agent_type: AgentType) -> str:
        """Get prompt for agent type"""
        return AgentFactory.get_agent_prompt(agent_type)


# Global instance for backward compatibility
agent_prompt_repository = AgentPromptRepository()
