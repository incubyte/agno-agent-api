#!/usr/bin/env python3
"""
Validation script to test the enhanced error handling and validation system.
This script performs basic tests to ensure the implementation is working correctly.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir.parent))

# Set up minimal environment variables for testing
os.environ.setdefault("SENDER_EMAIL", "test@example.com")
os.environ.setdefault("SENDER_PASSWORD", "test_password")
os.environ.setdefault("ANTHROPIC_API_KEY", "test_api_key")
os.environ.setdefault("AGENT_STORAGE", "./test_agents_storage.db")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_agents.db")
os.environ.setdefault("ALLOWED_ORIGINS", '["http://localhost:3000", "http://localhost:8000"]')

def test_imports():
    """Test that all new modules can be imported successfully"""
    print("Testing imports...")
    
    try:
        # Test core modules
        from app.core.setting import settings, is_development, is_production, is_render_deployment
        from app.core.exceptions import (
            BaseAPIException, ValidationException, NotFoundException, 
            BusinessLogicException, RateLimitException, setup_exception_handlers
        )
        from app.core.middleware import setup_middleware
        from app.core.setup import create_application
        
        # Test schemas
        from app.schemas.base import BaseSchema, TimestampMixin, PaginationParams
        from app.schemas.agent import (
            CreateAgentRequest, UpdateAgentRequest, RunAgentRequest,
            AgentResponse, AgentDetailResponse, AgentExecutionResponse
        )
        
        # Test utils
        from app.utils.validation import ValidationService, validation_service
        
        print("✓ All imports successful")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during imports: {e}")
        return False

def test_settings():
    """Test that settings are loaded correctly"""
    print("Testing settings...")
    
    try:
        from app.core.setting import settings
        
        # Test that all required new settings exist
        required_settings = [
            'ENABLE_ENHANCED_VALIDATION',
            'ENABLE_DTO_VALIDATION',
            'ENABLE_ADVANCED_SECURITY',
            'ENABLE_AI_VALIDATION',
            'MAX_PROMPT_LENGTH',
            'MIN_PROMPT_LENGTH'
        ]
        
        for setting_name in required_settings:
            if not hasattr(settings, setting_name):
                print(f"✗ Missing setting: {setting_name}")
                return False
        
        # Test original settings are still accessible (with test values)
        original_settings = [
            'SENDER_EMAIL',
            'SENDER_PASSWORD',
            'ANTHROPIC_API_KEY',
            'AGENT_STORAGE',
            'DATABASE_URL',
            'ALLOWED_ORIGINS'
        ]
        
        for setting_name in original_settings:
            if not hasattr(settings, setting_name):
                print(f"✗ Missing original setting: {setting_name}")
                return False
        
        print(f"✓ Settings loaded successfully")
        print(f"  - Enhanced validation: {settings.ENABLE_ENHANCED_VALIDATION}")
        print(f"  - DTO validation: {settings.ENABLE_DTO_VALIDATION}")
        print(f"  - Advanced security: {settings.ENABLE_ADVANCED_SECURITY}")
        print(f"  - AI validation: {settings.ENABLE_AI_VALIDATION}")
        print(f"  - Database URL: {settings.DATABASE_URL}")
        
        return True
        
    except Exception as e:
        print(f"✗ Settings error: {e}")
        return False

def test_validation_service():
    """Test that the validation service works correctly"""
    print("Testing validation service...")
    
    try:
        from app.utils.validation import validation_service
        
        # Test basic validation
        test_data = {
            "name": "Test Agent",
            "slug": "test-agent",
            "description": "A test agent for validation"
        }
        
        # This should not raise any exceptions
        validation_service.validate_agent_data(test_data, "create")
        
        # Test invalid data
        try:
            invalid_data = {"name": "", "slug": ""}
            validation_service.validate_agent_data(invalid_data, "create")
            print("✗ Validation should have failed for empty data")
            return False
        except Exception:
            # This is expected
            pass
        
        print("✓ Validation service working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Validation service error: {e}")
        return False

def test_schemas():
    """Test that schemas work correctly"""
    print("Testing schemas...")
    
    try:
        from app.schemas.agent import CreateAgentRequest, RunAgentRequest
        
        # Test valid agent creation request
        valid_agent = CreateAgentRequest(
            name="Test Agent",
            slug="test-agent",
            description="A test agent"
        )
        
        # Test valid run request
        valid_run = RunAgentRequest(
            prompt="This is a test prompt for the agent",
            user_email="test@example.com"
        )
        
        print("✓ Schemas working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Schema error: {e}")
        return False

def test_application_creation():
    """Test that the application can be created successfully"""
    print("Testing application creation...")
    
    try:
        from app.core.setup import create_application
        
        # This should create the FastAPI app without errors
        app = create_application()
        
        if app is None:
            print("✗ Application creation returned None")
            return False
        
        print("✓ Application created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Application creation error: {e}")
        return False

def test_exception_handling():
    """Test that exception classes work correctly"""
    print("Testing exception handling...")
    
    try:
        from app.core.exceptions import (
            BaseAPIException, ValidationException, NotFoundException,
            BusinessLogicException, RateLimitException
        )
        
        # Test creating exceptions
        validation_exc = ValidationException("Test validation error")
        not_found_exc = NotFoundException("TestResource", "test-id")
        business_exc = BusinessLogicException("Test business logic error")
        
        # Test exception properties
        if validation_exc.status_code != 400:
            print("✗ ValidationException has wrong status code")
            return False
        
        if not_found_exc.status_code != 404:
            print("✗ NotFoundException has wrong status code")
            return False
        
        print("✓ Exception handling working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Exception handling error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("ENHANCED ERROR HANDLING VALIDATION SCRIPT")
    print("=" * 60)
    print("Note: Using test environment variables for validation")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_settings,
        test_validation_service,
        test_schemas,
        test_application_creation,
        test_exception_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with unexpected error: {e}")
            print()
    
    print("=" * 60)
    print(f"VALIDATION RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced error handling system is ready.")
        print("\nNext steps:")
        print("1. Install new dependencies: pip install email-validator python-multipart")
        print("2. Set up your .env file with actual values for:")
        print("   - SENDER_EMAIL")
        print("   - SENDER_PASSWORD") 
        print("   - ANTHROPIC_API_KEY")
        print("   - AGENT_STORAGE")
        print("   - DATABASE_URL")
        print("   - ALLOWED_ORIGINS")
        print("3. Test the application: python run_server.py")
        print("4. Deploy to Render with confidence!")
        print("\nRender deployment notes:")
        print("- All existing environment variables will work unchanged")
        print("- New feature flags have sensible defaults")
        print("- No additional configuration required")
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
