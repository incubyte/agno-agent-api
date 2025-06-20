"""
Schemas Package
Centralized exports for all DTOs and schemas.
"""

from .base import *
from .agent import *

# Export commonly used schemas for easy imports
__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampMixin", 
    "PaginationParams",
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorDetail",
    
    # Agent schemas
    "CreateAgentRequest",
    "UpdateAgentRequest",
    "RunAgentRequest", 
    "AgentFilterRequest",
    "AgentResponse",
    "AgentDetailResponse",
    "AgentExecutionResponse",
    "AgentListResponse",
    "AgentCreatedResponse", 
    "AgentUpdatedResponse",
    "AgentDeletedResponse",
    
    # Legacy compatibility
    "LegacyAgentRequest",
    "LegacyMarketingAgentRequest",
    
    # Utility functions
    "create_agent_response",
    "create_agent_detail_response"
]
