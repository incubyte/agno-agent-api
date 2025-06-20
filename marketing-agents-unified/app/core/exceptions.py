"""
Unified Exception Handling System
Comprehensive error handling with structured responses.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTION CLASSES
# =============================================================================

class BaseAPIException(Exception):
    """Base exception for all API errors"""
    def __init__(self, detail: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(detail)


class ValidationException(BaseAPIException):
    """Validation error exception"""
    def __init__(self, detail: str, errors: List[Dict[str, Any]] = None):
        super().__init__(detail, 400, "VALIDATION_ERROR")
        self.errors = errors or []


class NotFoundException(BaseAPIException):
    """Resource not found exception"""
    def __init__(self, resource: str, identifier: Any = None):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} with ID '{identifier}' not found"
        super().__init__(detail, 404, "NOT_FOUND")


class BusinessLogicException(BaseAPIException):
    """Business logic violation exception"""
    def __init__(self, detail: str):
        super().__init__(detail, 400, "BUSINESS_LOGIC_ERROR")


class RateLimitException(BaseAPIException):
    """Rate limit exceeded exception"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(detail, 429, "RATE_LIMIT_EXCEEDED")


# =============================================================================
# ERROR RESPONSE FORMAT
# =============================================================================

def create_error_response(
    error_code: str,
    detail: str,
    errors: List[Dict[str, Any]] = None,
    path: str = None
) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error_id": str(uuid.uuid4()),
        "error_code": error_code,
        "detail": detail,
        "errors": errors,
        "timestamp": datetime.utcnow().isoformat(),
        "path": path
    }


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

def setup_exception_handlers(app: FastAPI):
    """Setup all exception handlers"""
    
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(request: Request, exc: BaseAPIException):
        """Handle custom API exceptions"""
        logger.warning(f"API Exception: {exc.error_code} - {exc.detail}")
        
        response_data = create_error_response(
            error_code=exc.error_code,
            detail=exc.detail,
            path=str(request.url.path)
        )
        
        if isinstance(exc, ValidationException):
            response_data["errors"] = exc.errors
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_data
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors"""
        logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
        
        errors = []
        for error in exc.errors():
            field_path = ".".join(str(loc) for loc in error.get("loc", []))
            errors.append({
                "field": field_path,
                "message": error.get("msg", "Invalid value"),
                "code": error.get("type", "validation_error")
            })
        
        return JSONResponse(
            status_code=422,
            content=create_error_response(
                error_code="VALIDATION_ERROR",
                detail="Request validation failed",
                errors=errors,
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions"""
        error_code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_ERROR",
            503: "SERVICE_UNAVAILABLE"
        }
        
        error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")
        
        return JSONResponse(
            status_code=exc.status_code,
            content=create_error_response(
                error_code=error_code,
                detail=exc.detail,
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content=create_error_response(
                error_code="INTERNAL_ERROR",
                detail="An internal server error occurred",
                path=str(request.url.path)
            )
        )
    
    logger.info("✓ Exception handlers configured")
