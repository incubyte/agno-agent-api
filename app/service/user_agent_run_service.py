"""
Agent Service - Business logic layer for agent operations
This service handles the business logic and coordinates between the route layer and repository layer.
"""
from typing import  Optional
from app.db.models import  UserAgentRun
from app.db.repository.user_agent_run_repository import UserAgentRunRepository
from fastapi import HTTPException




class UserAgentRunService:
    """Service layer for managing user agent runs"""

    def __init__(self):
        self.user_agent_run_repository = UserAgentRunRepository()

    
    def get_by_email(self, email: str) -> Optional[UserAgentRun]:
        """Get a specific user agent run by email"""
        user_agent_run = self.user_agent_run_repository.get_by_email(email)
        if not user_agent_run:
            raise HTTPException(status_code=404, detail=f"User agent run with email {email} not found")
        return user_agent_run
     


    def create(self, email: str, agent_id: int  ) -> UserAgentRun:
        """Create a new user agent run"""
        return self.user_agent_run_repository.create(email, agent_id)

