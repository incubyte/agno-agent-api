from pydantic_settings import BaseSettings 
from typing import Optional

class Setting(BaseSettings):
    
    SENDER_EMAIL: Optional[str] = None
    SENDER_PASSWORD: Optional[str] = None
    ANTHROPIC_API_KEY: str  # This is required
    AGENT_STORAGE: str = "./default_agent_storage.db"  # Default value
    DATABASE_URL: str = "sqlite:///./agents.db"  # Default value
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]  # Default value

    class Config:
        env_file = ".env"

settings = Setting()