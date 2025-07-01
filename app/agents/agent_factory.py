from app.agents.base_agent import BaseAgent
from app.agents.marketing_agents import MarketingAgent
from app.agents.ai_agent import AIAgent
from app.agents.linkedin_writer_agent import LinkedInWriterAgent
from app.agents.tech_blog_writer_agent import TechBlogWriterAgent
from app.agents.lifestyle_blog_writer_agent import LifestyleBlogWriterAgent
from app.agents.website_performance_auditor import WebsitePerformanceAuditor
from app.agents.seo_auditor_agent import SEOAuditorAgent
from app.agents.marketing_copywriter_agent import MarketingCopywriterAgent
from app.agents.enum.agent_enum import AgentType


class AgentFactory:
    _agents = {
        AgentType.MARKETING_AGENT: MarketingAgent,
        AgentType.AI_AGENT: AIAgent,
        AgentType.LINKEDIN_WRITER_AGENT: LinkedInWriterAgent,
        AgentType.TECH_BLOG_WRITER_AGENT: TechBlogWriterAgent,
        AgentType.LIFESTYLE_BLOG_WRITER_AGENT: LifestyleBlogWriterAgent,
        AgentType.WEBSITE_PERFORMANCE_AUDITOR: WebsitePerformanceAuditor,
        AgentType.SEO_AUDIT: SEOAuditorAgent,
        AgentType.MARKETING_COPYWRITER_AGENT: MarketingCopywriterAgent,
    }

    @staticmethod
    def get_agent(agent_type: AgentType) -> BaseAgent:
        agent_class = AgentFactory._agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"No agent found for type: {agent_type}")
        return agent_class()
