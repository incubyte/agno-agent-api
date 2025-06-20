"""
Unified Configuration System
Single source of truth for all application settings with feature flags.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Unified application settings with feature flags"""
    
    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    DATABASE_URL: str = "sqlite:///./agents.db"
    
    # =============================================================================
    # FEATURE FLAGS - Control application behavior
    # =============================================================================
    ENABLE_ENHANCED_VALIDATION: bool = True
    ENABLE_DTO_VALIDATION: bool = True
    ENABLE_ADVANCED_SECURITY: bool = True
    ENABLE_AI_VALIDATION: bool = True
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_CACHING: bool = True
    
    # =============================================================================
    # API BEHAVIOR
    # =============================================================================
    DEFAULT_API_VERSION: str = "v1"
    SUPPORT_LEGACY_FORMAT: bool = True
    AUTO_ENHANCE_LARGE_REQUESTS: bool = True
    MAX_LEGACY_PAGE_SIZE: int = 50
    
    # =============================================================================
    # VALIDATION LIMITS
    # =============================================================================
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_PROMPT_LENGTH: int = 8000
    MIN_PROMPT_LENGTH: int = 10
    MAX_AGENT_NAME_LENGTH: int = 255
    MAX_DESCRIPTION_LENGTH: int = 1000
    
    # =============================================================================
    # RATE LIMITING
    # =============================================================================
    DEFAULT_RATE_LIMIT: int = 100  # requests per hour
    BURST_LIMIT: int = 10  # requests per minute
    AI_EXECUTION_RATE_LIMIT: int = 20  # AI executions per hour
    
    # =============================================================================
    # SECURITY
    # =============================================================================
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # =============================================================================
    # PERFORMANCE
    # =============================================================================
    CACHE_TTL: int = 300  # seconds
    CONNECTION_POOL_SIZE: int = 10
    
    # =============================================================================
    # LOGGING
    # =============================================================================
    LOG_LEVEL: str = "INFO"
    ENABLE_REQUEST_LOGGING: bool = True
    
    # =============================================================================
    # AI SETTINGS
    # =============================================================================
    AI_MODEL_TIMEOUT: int = 30  # seconds
    AI_MAX_RETRIES: int = 3
    
    # =============================================================================
    # AGENT STORAGE
    # =============================================================================
    AGENT_STORAGE: str = "./agents_storage.db"
    
    # =============================================================================
    # ANTHROPIC API
    # =============================================================================
    ANTHROPIC_API_KEY: Optional[str] = None
    
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
settings = Settings()


# Environment detection helpers
def is_development() -> bool:
    """Check if running in development mode"""
    return os.getenv("ENVIRONMENT", "development").lower() == "development"


def is_production() -> bool:
    """Check if running in production mode"""
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def is_testing() -> bool:
    """Check if running in test mode"""
    return os.getenv("ENVIRONMENT", "development").lower() == "testing"


# Export commonly used settings
__all__ = ["settings", "Settings", "is_development", "is_production", "is_testing"]
