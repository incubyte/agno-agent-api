"""
Agent Schemas
All agent-related DTOs in one organized file.
"""

from pydantic import Field, field_validator, EmailStr, computed_field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from .base import BaseSchema, TimestampMixin, PaginatedResponse


# =============================================================================
# BASE AGENT SCHEMAS
# =============================================================================

class AgentBase(BaseSchema):
    """Base agent schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    slug: str = Field(..., pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", description="Unique agent identifier")
    description: Optional[str] = Field(None, max_length=1000, description="Agent description")
    image: Optional[str] = Field(None, max_length=500, description="Agent image URL")
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format"""
        if not v:
            raise ValueError("Slug cannot be empty")
        return v.lower().strip()
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name"""
        if not v.strip():
            raise ValueError("Agent name cannot be empty")
        return v.strip()


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class CreateAgentRequest(AgentBase):
    """Agent creation request"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Marketing Analysis Agent",
                "slug": "marketing-analysis-agent",
                "description": "AI agent specialized in marketing analysis and strategy",
                "image": "https://example.com/marketing-agent.jpg"
            }
        }


class UpdateAgentRequest(BaseSchema):
    """Agent update request - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
    description: Optional[str] = Field(None, max_length=1000)
    image: Optional[str] = Field(None, max_length=500)
    
    def has_updates(self) -> bool:
        """Check if any fields are being updated"""
        return any(getattr(self, field) is not None for field in ['name', 'slug', 'description', 'image'])


class RunAgentRequest(BaseSchema):
    """Agent execution request"""
    prompt: str = Field(..., min_length=10, max_length=8000, description="Prompt for the AI agent")
    user_email: EmailStr = Field(..., description="User email address")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters")
    generate_pdf: bool = Field(True, description="Generate PDF response")
    send_email: bool = Field(True, description="Send response via email")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Analyze the marketing strategy for a SaaS startup targeting small businesses",
                "user_email": "user@example.com",
                "parameters": {"industry": "SaaS", "target_market": "small businesses"},
                "generate_pdf": True,
                "send_email": True
            }
        }


class AgentFilterRequest(BaseSchema):
    """Agent filtering and pagination request"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    name_contains: Optional[str] = Field(None, max_length=255)
    has_description: Optional[bool] = None
    has_image: Optional[bool] = None
    
    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class AgentResponse(AgentBase, TimestampMixin):
    """Basic agent response"""
    id: int = Field(..., description="Agent unique identifier")
    
    @computed_field
    @property
    def display_name(self) -> str:
        """Formatted display name"""
        return self.name.title()
    
    @computed_field
    @property
    def has_description(self) -> bool:
        """Whether agent has a description"""
        return self.description is not None and len(self.description.strip()) > 0
    
    @computed_field
    @property
    def has_image(self) -> bool:
        """Whether agent has an image"""
        return self.image is not None and len(self.image.strip()) > 0


class AgentDetailResponse(AgentResponse):
    """Detailed agent response with additional information"""
    prompt: Optional[str] = Field(None, description="Agent's system prompt")
    usage_count: Optional[int] = Field(0, description="Number of times used")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    
    @computed_field
    @property
    def is_ready(self) -> bool:
        """Whether agent is ready for execution"""
        return self.prompt is not None


class AgentExecutionResponse(BaseSchema):
    """Agent execution response"""
    agent_id: int
    agent_name: str
    response: str
    execution_time_ms: Optional[float] = None
    token_count: Optional[int] = None
    pdf_generated: bool = False
    pdf_path: Optional[str] = None
    email_sent: bool = False
    warnings: List[str] = Field(default_factory=list)
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    
    @computed_field
    @property
    def response_preview(self) -> str:
        """Preview of the response (first 200 characters)"""
        if len(self.response) <= 200:
            return self.response
        return self.response[:197] + "..."
    
    @computed_field
    @property
    def success_rate(self) -> str:
        """Overall success rate"""
        return "100%" if not self.warnings else "Partial Success"


class AgentListResponse(PaginatedResponse[AgentResponse]):
    """Paginated agent list response"""
    pass


class AgentCreatedResponse(AgentResponse):
    """Agent creation success response"""
    message: str = "Agent created successfully"


class AgentUpdatedResponse(AgentResponse):
    """Agent update success response"""
    message: str = "Agent updated successfully"
    changes: Dict[str, Any] = Field(default_factory=dict)


class AgentDeletedResponse(BaseSchema):
    """Agent deletion response"""
    id: int
    name: str
    message: str = "Agent deleted successfully"
    deleted_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# LEGACY COMPATIBILITY
# =============================================================================

class LegacyAgentRequest(BaseSchema):
    """Legacy agent request for backward compatibility"""
    prompt: str
    user_email: str


class LegacyMarketingAgentRequest(BaseSchema):
    """Legacy marketing agent request"""
    url: str
    user_email: str


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_agent_response(agent) -> AgentResponse:
    """Create agent response from database model"""
    return AgentResponse.model_validate(agent)


def create_agent_detail_response(agent, prompt: Optional[str] = None) -> AgentDetailResponse:
    """Create detailed agent response"""
    data = agent.__dict__.copy()
    data['prompt'] = prompt
    return AgentDetailResponse.model_validate(data)


# Export all schemas
__all__ = [
    # Request schemas
    "CreateAgentRequest",
    "UpdateAgentRequest", 
    "RunAgentRequest",
    "AgentFilterRequest",
    
    # Response schemas
    "AgentResponse",
    "AgentDetailResponse",
    "AgentExecutionResponse", 
    "AgentListResponse",
    "AgentCreatedResponse",
    "AgentUpdatedResponse",
    "AgentDeletedResponse",
    
    # Legacy schemas
    "LegacyAgentRequest",
    "LegacyMarketingAgentRequest",
    
    # Utility functions
    "create_agent_response",
    "create_agent_detail_response"
]
