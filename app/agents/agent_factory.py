from app.agents.base_agent import BaseAgent
from app.agents.marketing_agents import MarketingAgent
from app.agents.ai_agent import AIAgent


class AgentFactory:
    _agents = {
        "marketing-agent": MarketingAgent,
        "ai-agent": AIAgent,
    }

    @staticmethod
    def get_agent(slug: str) -> BaseAgent:
        agent_class = AgentFactory._agents.get(slug)
        if not agent_class:
            raise ValueError(f"No agent found for slug: {slug}")
        return agent_class()
