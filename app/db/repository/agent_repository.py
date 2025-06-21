from sqlmodel import select
from app.db.models import Agent
from app.db.engine import session
from typing import List, Optional


class AgentRepository:
    """Repository for agent data access operations"""

    def get_all(self) -> List[Agent]:
        """Get all agents from the database"""
        return session.exec(select(Agent)).all()

    def get_by_id(self, agent_id: int) -> Optional[Agent]:
        """Get an agent by ID"""
        return session.get(Agent, agent_id)

    def get_by_slug(self, slug: str) -> Optional[Agent]:
        """Get an agent by slug"""
        statement = select(Agent).where(Agent.slug == slug)
        return session.exec(statement).first()

    def create(self, agent: Agent) -> Agent:
        """Create a new agent"""
        session.add(agent)
        session.commit()
        session.refresh(agent)
        return agent

    def update(self, agent: Agent) -> Agent:
        """Update an existing agent"""
        session.add(agent)
        session.commit()
        session.refresh(agent)
        return agent

    def delete(self, agent: Agent) -> Agent:
        """Delete an agent by ID"""
        session.delete(agent)
        session.commit()
        return agent

    def exists_by_slug(self, slug: str) -> bool:
        """Check if an agent with the given slug exists"""
        statement = select(Agent).where(Agent.slug == slug)
        result = session.exec(statement).first()
        return result is not None

    def agent_count(self) ->  dict:
        """Count total number of agents"""
        statement = select(Agent)
        return {"count": len(session.exec(statement).all())}
