from pydantic_settings import BaseSettings 

class Setting(BaseSettings):
    
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    ANTHROPIC_API_KEY: str

    class Config:
        env_file = ".env"

settings = Setting()