from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Setting(BaseSettings):
    # =============================================================================
    # EXISTING SETTINGS (PRESERVE FOR RENDER DEPLOYMENT)
    # =============================================================================
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    ANTHROPIC_API_KEY: str
    AGENT_STORAGE: str
    DATABASE_URL: str
    ALLOWED_ORIGINS: List[str]
    
    # =============================================================================
    # NEW FEATURE FLAGS (DEFAULT VALUES FOR RENDER COMPATIBILITY)
    # =============================================================================
    ENABLE_ENHANCED_VALIDATION: bool = True
    ENABLE_DTO_VALIDATION: bool = True
    ENABLE_ADVANCED_SECURITY: bool = True
    ENABLE_AI_VALIDATION: bool = True
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_REQUEST_LOGGING: bool = True
    
    # =============================================================================
    # VALIDATION LIMITS (RENDER-FRIENDLY DEFAULTS)
    # =============================================================================
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_PROMPT_LENGTH: int = 8000
    MIN_PROMPT_LENGTH: int = 10
    MAX_AGENT_NAME_LENGTH: int = 255
    MAX_DESCRIPTION_LENGTH: int = 1000
    
    # =============================================================================
    # RATE LIMITING (CONSERVATIVE DEFAULTS FOR RENDER)
    # =============================================================================
    DEFAULT_RATE_LIMIT: int = 100  # requests per hour
    BURST_LIMIT: int = 10
    AI_EXECUTION_RATE_LIMIT: int = 20
    
    # =============================================================================
    # PERFORMANCE (RENDER OPTIMIZED)
    # =============================================================================
    CACHE_TTL: int = 300
    CONNECTION_POOL_SIZE: int = 5  # Lower for Render free tier
    
    # =============================================================================
    # LOGGING
    # =============================================================================
    LOG_LEVEL: str = "INFO"
    
    # =============================================================================
    # AI SETTINGS
    # =============================================================================
    AI_MODEL_TIMEOUT: int = 30
    AI_MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def is_enhanced_mode(self) -> bool:
        """Check if any enhanced features are enabled"""
        return any([
            self.ENABLE_ENHANCED_VALIDATION,
            self.ENABLE_DTO_VALIDATION,
            self.ENABLE_ADVANCED_SECURITY,
            self.ENABLE_AI_VALIDATION
        ])

# Global settings instance
settings = Setting()

# Environment detection helpers
def is_development() -> bool:
    return os.getenv("ENVIRONMENT", "development").lower() == "development"

def is_production() -> bool:
    return os.getenv("ENVIRONMENT", "production").lower() == "production"

def is_render_deployment() -> bool:
    return os.getenv("RENDER") is not None
