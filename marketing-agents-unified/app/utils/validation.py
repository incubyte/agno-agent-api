"""
Unified Validation System
Configurable validation with feature flags.
"""

import re
import logging
from typing import Optional, Dict, Any
from ..core.config import settings
from ..core.exceptions import ValidationException

logger = logging.getLogger(__name__)


class ValidationService:
    """Unified validation service with configurable features"""
    
    def __init__(self, enable_enhanced: bool = None, enable_ai_checks: bool = None):
        self.enable_enhanced = enable_enhanced if enable_enhanced is not None else settings.ENABLE_ENHANCED_VALIDATION
        self.enable_ai_checks = enable_ai_checks if enable_ai_checks is not None else settings.ENABLE_AI_VALIDATION
    
    def validate_agent_data(self, data: Dict[str, Any], context: str = "create") -> Dict[str, Any]:
        """Unified agent data validation"""
        
        # Always do basic validation
        self._basic_validation(data, context)
        
        # Enhanced validation if enabled
        if self.enable_enhanced:
            self._enhanced_validation(data, context)
        
        # AI-specific validation for execution
        if self.enable_ai_checks and context == "run":
            self._ai_validation(data)
        
        return data
    
    def _basic_validation(self, data: Dict[str, Any], context: str):
        """Basic validation that always runs"""
        errors = []
        
        if context in ["create", "update"]:
            # Name validation
            if "name" in data:
                name = data.get("name", "").strip()
                if not name:
                    errors.append({"field": "name", "message": "Name cannot be empty"})
                elif len(name) > settings.MAX_AGENT_NAME_LENGTH:
                    errors.append({"field": "name", "message": f"Name too long (max {settings.MAX_AGENT_NAME_LENGTH} chars)"})
            
            # Slug validation
            if "slug" in data:
                slug = data.get("slug", "").strip().lower()
                if not slug:
                    errors.append({"field": "slug", "message": "Slug cannot be empty"})
                elif not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", slug):
                    errors.append({"field": "slug", "message": "Slug must contain only lowercase letters, numbers, and hyphens"})
        
        elif context == "run":
            # Prompt validation
            if "prompt" in data:
                prompt = data.get("prompt", "").strip()
                if not prompt:
                    errors.append({"field": "prompt", "message": "Prompt cannot be empty"})
                elif len(prompt) < settings.MIN_PROMPT_LENGTH:
                    errors.append({"field": "prompt", "message": f"Prompt too short (min {settings.MIN_PROMPT_LENGTH} chars)"})
                elif len(prompt) > settings.MAX_PROMPT_LENGTH:
                    errors.append({"field": "prompt", "message": f"Prompt too long (max {settings.MAX_PROMPT_LENGTH} chars)"})
            
            # Email validation
            if "user_email" in data:
                email = data.get("user_email", "").strip()
                if not email:
                    errors.append({"field": "user_email", "message": "Email cannot be empty"})
                elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
                    errors.append({"field": "user_email", "message": "Invalid email format"})
        
        if errors:
            raise ValidationException("Validation failed", errors)
    
    def _enhanced_validation(self, data: Dict[str, Any], context: str):
        """Enhanced validation when feature is enabled"""
        errors = []
        
        # Enhanced name validation
        if "name" in data:
            name = data.get("name", "")
            if self._contains_suspicious_patterns(name):
                errors.append({"field": "name", "message": "Name contains potentially harmful content"})
        
        # Enhanced description validation  
        if "description" in data and data["description"]:
            description = data["description"]
            if len(description) > settings.MAX_DESCRIPTION_LENGTH:
                errors.append({"field": "description", "message": f"Description too long (max {settings.MAX_DESCRIPTION_LENGTH} chars)"})
            elif self._contains_suspicious_patterns(description):
                errors.append({"field": "description", "message": "Description contains potentially harmful content"})
        
        # URL validation for image
        if "image" in data and data["image"]:
            image_url = data["image"]
            if not self._is_valid_image_url(image_url):
                errors.append({"field": "image", "message": "Invalid image URL format"})
        
        if errors:
            raise ValidationException("Enhanced validation failed", errors)
    
    def _ai_validation(self, data: Dict[str, Any]):
        """AI-specific validation for prompts and execution"""
        errors = []
        
        if "prompt" in data:
            prompt = data["prompt"]
            
            # Check for prompt injection patterns
            injection_patterns = [
                r"(?i)ignore\s+previous\s+instructions",
                r"(?i)forget\s+everything",
                r"(?i)system\s*:\s*you\s+are",
                r"(?i)act\s+as\s+if",
                r"(?i)pretend\s+to\s+be"
            ]
            
            for pattern in injection_patterns:
                if re.search(pattern, prompt):
                    errors.append({
                        "field": "prompt", 
                        "message": "Potential prompt injection detected. Please revise your input."
                    })
                    logger.warning(f"Prompt injection attempt detected: {pattern}")
                    break
            
            # Check for harmful content
            if self._contains_harmful_content(prompt):
                errors.append({
                    "field": "prompt",
                    "message": "Prompt contains potentially harmful content"
                })
        
        if errors:
            raise ValidationException("AI validation failed", errors)
    
    def _contains_suspicious_patterns(self, text: str) -> bool:
        """Check for suspicious patterns in text"""
        suspicious_patterns = [
            r"<script.*?>",
            r"javascript:",
            r"vbscript:",
            r"on\w+\s*=",
            r"eval\s*\(",
            r"exec\s*\("
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _contains_harmful_content(self, text: str) -> bool:
        """Check for harmful content in prompts"""
        harmful_patterns = [
            r"(?i)\b(hack|crack|exploit|malware|virus)\b",
            r"(?i)\b(illegal|criminal|fraud|scam)\b",
            r"(?i)\b(violence|harm|attack|threat)\b"
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _is_valid_image_url(self, url: str) -> bool:
        """Validate image URL format"""
        if not url.startswith(("http://", "https://")):
            return False
        
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        return any(url.lower().endswith(ext) for ext in image_extensions)


# Global validation service instance
validation_service = ValidationService()
