"""
Enhanced Agent Repository with proper session management and error handling.
"""

from sqlmodel import select, Session
from app.db.models import Agent
from app.db.engine import engine
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class AgentRepository:
    """Enhanced repository for agent data access operations with proper session management"""

    def get_all(self) -> List[Agent]:
        """Get all agents from the database"""
        try:
            with Session(engine) as session:
                statement = select(Agent).order_by(Agent.created_at.desc())
                agents = session.exec(statement).all()
                return list(agents)
        except Exception as e:
            logger.error(f"Failed to get all agents: {str(e)}")
            raise

    def get_by_id(self, agent_id: int) -> Optional[Agent]:
        """Get an agent by ID"""
        try:
            with Session(engine) as session:
                return session.get(Agent, agent_id)
        except Exception as e:
            logger.error(f"Failed to get agent by ID {agent_id}: {str(e)}")
            raise

    def get_by_slug(self, slug: str) -> Optional[Agent]:
        """Get an agent by slug"""
        try:
            with Session(engine) as session:
                statement = select(Agent).where(Agent.slug == slug)
                return session.exec(statement).first()
        except Exception as e:
            logger.error(f"Failed to get agent by slug {slug}: {str(e)}")
            raise

    def create(self, agent: Agent) -> Agent:
        """Create a new agent"""
        try:
            with Session(engine) as session:
                session.add(agent)
                session.commit()
                session.refresh(agent)
                return agent
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise

    def update(self, agent: Agent) -> Agent:
        """Update an existing agent"""
        try:
            with Session(engine) as session:
                session.add(agent)
                session.commit()
                session.refresh(agent)
                return agent
        except Exception as e:
            logger.error(f"Failed to update agent: {str(e)}")
            raise

    def delete(self, agent: Agent) -> Agent:
        """Delete an agent"""
        try:
            with Session(engine) as session:
                # Re-attach the agent to this session
                session.add(agent)
                session.delete(agent)
                session.commit()
                return agent
        except Exception as e:
            logger.error(f"Failed to delete agent: {str(e)}")
            raise

    def exists_by_slug(self, slug: str) -> bool:
        """Check if an agent with the given slug exists"""
        try:
            with Session(engine) as session:
                statement = select(Agent).where(Agent.slug == slug)
                result = session.exec(statement).first()
                return result is not None
        except Exception as e:
            logger.error(f"Failed to check agent existence for slug {slug}: {str(e)}")
            raise

    def agent_count(self) -> dict:
        """Count total number of agents"""
        try:
            with Session(engine) as session:
                statement = select(Agent)
                count = len(list(session.exec(statement).all()))
                return {"count": count}
        except Exception as e:
            logger.error(f"Failed to get agent count: {str(e)}")
            raise

    def search(self, name_contains: Optional[str] = None, 
               has_description: Optional[bool] = None,
               has_image: Optional[bool] = None,
               limit: int = 10, offset: int = 0) -> List[Agent]:
        """Search agents with filters (for future enhancements)"""
        try:
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
        except Exception as e:
            logger.error(f"Failed to search agents: {str(e)}")
            raise
