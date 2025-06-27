"""
Base Schema Classes
Foundation for all DTOs with common functionality.
"""

from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Optional, List, Any, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        validate_assignment=True,
        from_attributes=True
    )


class TimestampMixin(BaseSchema):
    """Mixin for timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginationParams(BaseSchema):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    
    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, limit: int):
        """Create paginated response"""
        pages = (total + limit - 1) // limit
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class SuccessResponse(BaseSchema):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorDetail(BaseSchema):
    """Error detail for validation errors"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None
