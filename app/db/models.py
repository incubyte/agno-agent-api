from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

from pydantic import model_serializer


class Agent(SQLModel, table=True):
    __tablename__ = "agents"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255, nullable=False, unique=True)
    description: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name})>"
    
    @model_serializer()
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "image": self.image,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
class UserAgentRun(SQLModel, table=True):
    __tablename__ = "user_agent_runs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, nullable=False)
    agent_id: int = Field(default=None, foreign_key="agents.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<UserAgentRun(id={self.id}, email={self.email}, agent_id={self.agent_id})>"

    @model_serializer()
    def serialize(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "agent_id": self.agent_id,
        }
