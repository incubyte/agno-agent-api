"""
Agent Repository
Data access layer for agent operations.
"""

from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from ..models.database import Agent, get_session, engine
from ..core.exceptions import NotFoundException


class AgentRepository:
    """Repository for agent data access"""
    
    def __init__(self):
        self.session_factory = get_session
    
    def get_all(self) -> List[Agent]:
        """Get all agents"""
        with Session(engine) as session:
            statement = select(Agent).order_by(Agent.created_at.desc())
            agents = session.exec(statement).all()
            return list(agents)
    
    def get_by_id(self, agent_id: int) -> Optional[Agent]:
        """Get agent by ID"""
        with Session(engine) as session:
            return session.get(Agent, agent_id)
    
    def get_by_slug(self, slug: str) -> Optional[Agent]:
        """Get agent by slug"""
        with Session(engine) as session:
            statement = select(Agent).where(Agent.slug == slug)
            return session.exec(statement).first()
    
    def create(self, agent: Agent) -> Agent:
        """Create new agent"""
        with Session(engine) as session:
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return agent
    
    def update(self, agent: Agent) -> Agent:
        """Update existing agent"""
        agent.updated_at = datetime.utcnow()
        with Session(engine) as session:
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return agent
    
    def delete(self, agent_id: int) -> bool:
        """Delete agent by ID"""
        with Session(engine) as session:
            agent = session.get(Agent, agent_id)
            if not agent:
                return False
            
            session.delete(agent)
            session.commit()
            return True
    
    def exists_by_slug(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if agent exists by slug"""
        with Session(engine) as session:
            statement = select(Agent).where(Agent.slug == slug)
            if exclude_id:
                statement = statement.where(Agent.id != exclude_id)
            
            return session.exec(statement).first() is not None
    
    def count(self) -> int:
        """Get total agent count"""
        with Session(engine) as session:
            statement = select(Agent)
            return len(session.exec(statement).all())
    
    def search(self, name_contains: Optional[str] = None, 
               has_description: Optional[bool] = None,
               has_image: Optional[bool] = None,
               limit: int = 10, offset: int = 0) -> List[Agent]:
        """Search agents with filters"""
        with Session(engine) as session:
            statement = select(Agent)
            
            # Apply filters
            if name_contains:
                statement = statement.where(Agent.name.contains(name_contains))
            
            if has_description is not None:
                if has_description:
                    statement = statement.where(Agent.description.isnot(None))
                else:
                    statement = statement.where(Agent.description.is_(None))
            
            if has_image is not None:
                if has_image:
                    statement = statement.where(Agent.image.isnot(None))
                else:
                    statement = statement.where(Agent.image.is_(None))
            
            # Apply pagination
            statement = statement.offset(offset).limit(limit)
            statement = statement.order_by(Agent.created_at.desc())
            
            return list(session.exec(statement).all())



