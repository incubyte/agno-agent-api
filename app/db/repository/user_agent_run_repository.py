from sqlmodel import select
from app.db.models import  UserAgentRun
from app.db.engine import session
from typing import  Optional


class UserAgentRunRepository:

    def create(self, email: str, agent_id: int) -> UserAgentRun:
        """Create a new user agent run"""
        user_agent_run = UserAgentRun(email=email, agent_id=agent_id)
        session.add(user_agent_run)
        session.commit()
        session.refresh(user_agent_run)
        return user_agent_run

    def get_by_email(self, email: str) -> Optional[UserAgentRun]:
        """Get a user agent run by email"""
        statement = select(UserAgentRun).where(UserAgentRun.email == email)
        return session.exec(statement).first()

 
    