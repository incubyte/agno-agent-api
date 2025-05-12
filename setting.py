from pydantic_settings import BaseSettings 

class Setting(BaseSettings):

    # Email settings
    # EMAIL_HOST: str = "smtp.example.com"
    # EMAIL_PORT: int = 587
    # SENDER_EMAIL: str = ""
    
    SENDER_EMAIL: str
    SENDER_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Setting()