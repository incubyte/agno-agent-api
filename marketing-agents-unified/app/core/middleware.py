"""
Unified Middleware System
Configurable middleware based on feature flags.
"""

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
import logging
from typing import Callable

from .config import settings

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ENABLE_REQUEST_LOGGING:
            return await call_next(request)
        
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")
        
        # Log request
        logger.info(
            f"Request {request_id}: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params)
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            f"Response {request_id}: {response.status_code} in {duration:.3f}s",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration": duration
            }
        )
        
        return response


class ValidationMiddleware(BaseHTTPMiddleware):
    """Enhanced validation middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ENABLE_ENHANCED_VALIDATION:
            return await call_next(request)
        
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.MAX_REQUEST_SIZE:
            from .exceptions import ValidationException
            raise ValidationException("Request too large")
        
        return await call_next(request)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware with rate limiting"""
    
    def __init__(self, app, enable_rate_limiting: bool = True):
        super().__init__(app)
        self.enable_rate_limiting = enable_rate_limiting
        self.rate_limit_store = {}  # In production, use Redis
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ENABLE_ADVANCED_SECURITY:
            return await call_next(request)
        
        # Basic rate limiting (simplified)
        if self.enable_rate_limiting and settings.ENABLE_RATE_LIMITING:
            client_ip = request.client.host
            current_time = time.time()
            
            # Clean old entries (simplified)
            self.rate_limit_store = {
                ip: timestamps for ip, timestamps in self.rate_limit_store.items()
                if any(ts > current_time - 3600 for ts in timestamps)  # Keep last hour
            }
            
            # Check rate limit
            if client_ip in self.rate_limit_store:
                recent_requests = [
                    ts for ts in self.rate_limit_store[client_ip]
                    if ts > current_time - 3600  # Last hour
                ]
                
                if len(recent_requests) >= settings.DEFAULT_RATE_LIMIT:
                    from .exceptions import RateLimitException
                    raise RateLimitException()
                
                self.rate_limit_store[client_ip] = recent_requests + [current_time]
            else:
                self.rate_limit_store[client_ip] = [current_time]
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response


def setup_middleware(app: FastAPI):
    """Setup all middleware based on feature flags"""
    
    # Always add request ID middleware
    app.add_middleware(RequestIDMiddleware)
    
    # Conditional middleware
    if settings.ENABLE_REQUEST_LOGGING:
        app.add_middleware(LoggingMiddleware)
    
    if settings.ENABLE_ENHANCED_VALIDATION:
        app.add_middleware(ValidationMiddleware)
    
    if settings.ENABLE_ADVANCED_SECURITY:
        app.add_middleware(
            SecurityMiddleware,
            enable_rate_limiting=settings.ENABLE_RATE_LIMITING
        )
    
    logger.info("✓ Middleware configured")
