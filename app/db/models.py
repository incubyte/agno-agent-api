from datetime import datetime
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

        