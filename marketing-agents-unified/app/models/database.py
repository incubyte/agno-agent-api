"""
Database Models
Unified database models using SQLModel.
"""

from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from datetime import datetime

from ..core.config import settings


class Agent(SQLModel, table=True):
    """Agent database model"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    slug: str = Field(max_length=255, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    image: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __repr__(self):
        return f"Agent(id={self.id}, name='{self.name}', slug='{self.slug}')"


# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False  # Set to True for SQL logging
)


def create_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
