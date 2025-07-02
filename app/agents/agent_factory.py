from app.agents.base_agent import BaseAgent
from app.agents.ai_agent import AIAgent
from app.agents.linkedin_writer_agent import LinkedInWriterAgent
from app.agents.medication_safety_guardian_agent import MedicationSafetyGuardianAgent
from app.agents.tech_blog_writer_agent import TechBlogWriterAgent
from app.agents.lifestyle_blog_writer_agent import LifestyleBlogWriterAgent
from app.agents.Location_Specific_Agent import LocationSpecificAgent
from app.agents.clinical_decision_agents import ClinicalDecisionAgent
from app.agents.enum.agent_enum import AgentType


class AgentFactory:
    _agents = {
        AgentType.AI_AGENT: AIAgent,
        AgentType.LINKEDIN_WRITER_AGENT: LinkedInWriterAgent,
        AgentType.TECH_BLOG_WRITER_AGENT: TechBlogWriterAgent,
        AgentType.LIFESTYLE_BLOG_WRITER_AGENT: LifestyleBlogWriterAgent,
        AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT: LocationSpecificAgent,
        AgentType.MEDICATION_SAFETY_GUARDIAN: MedicationSafetyGuardianAgent,
        AgentType.CLINICAL_DECISION_AGENT: ClinicalDecisionAgent,
    }

    @staticmethod
    def get_agent(agent_type: AgentType) -> BaseAgent:
        agent_class = AgentFactory._agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"No agent found for type: {agent_type}")
        return agent_class()
