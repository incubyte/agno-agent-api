from app.agents.base_agent import BaseAgent
from app.agents.marketing_agents import MarketingAgent
from app.agents.ai_agent import AIAgent
from app.agents.enum.agent_enum import AgentType


class AgentFactory:
    _agents = {
        AgentType.MARKETING_AGENT: MarketingAgent,
        AgentType.AI_AGENT: AIAgent,
    }

    @staticmethod
    def get_agent(agent_type: AgentType) -> BaseAgent:
        agent_class = AgentFactory._agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"No agent found for type: {agent_type}")
        return agent_class()
