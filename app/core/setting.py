from pydantic_settings import BaseSettings 
from typing import Optional

class Setting(BaseSettings):
    
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    ANTHROPIC_API_KEY: str
    AGENT_STORAGE: str
    DATABASE_URL: str
    ALLOWED_ORIGINS: list[str] 
    GOOGLE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Setting()