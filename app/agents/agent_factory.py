from app.agents.base_agent import BaseAgent
from app.agents.marketing_agents import MarketingAgent
from app.agents.ai_agent import AIAgent
from app.agents.linkedin_writer_agent import LinkedInWriterAgent
from app.agents.tech_blog_writer_agent import TechBlogWriterAgent
from app.agents.lifestyle_blog_writer_agent import LifestyleBlogWriterAgent


class AgentFactory:
    _agents = {
        "marketing-agent": MarketingAgent,
        "ai-agent": AIAgent,
        "linkedin-writer-agent": LinkedInWriterAgent,
        "tech-blog-writer-agent": TechBlogWriterAgent,
        "lifestyle-blog-writer-agent": LifestyleBlogWriterAgent,
    }

    @staticmethod
    def get_agent(agent_slug: str) -> BaseAgent:
        agent_class = AgentFactory._agents.get(agent_slug)
        if not agent_class:
            # Default to AIAgent for unknown types
            return AIAgent()
        return agent_class()
