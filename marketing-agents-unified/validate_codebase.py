#!/usr/bin/env python3
"""
Quick validation script to check for import and syntax issues
Run this to verify the unified codebase is complete and functional.
"""

import sys
import os
import importlib.util

def test_imports():
    """Test critical imports to catch issues early"""
    
    # Add the app directory to path
    app_path = os.path.join(os.path.dirname(__file__), 'app')
    sys.path.insert(0, app_path)
    
    errors = []
    
    try:
        print("Testing core imports...")
        from app.core.config import settings
        from app.core.setup import create_application
        from app.core.exceptions import setup_exception_handlers
        print("✓ Core imports successful")
    except Exception as e:
        errors.append(f"Core imports failed: {e}")
        print(f"❌ Core imports failed: {e}")
    
    try:
        print("Testing schema imports...")
        from app.schemas.agent import CreateAgentRequest, AgentResponse
        from app.schemas.base import BaseSchema
        print("✓ Schema imports successful")
    except Exception as e:
        errors.append(f"Schema imports failed: {e}")
        print(f"❌ Schema imports failed: {e}")
    
    try:
        print("Testing service imports...")
        from app.services.agent_service import AgentService
        print("✓ Service imports successful")
    except Exception as e:
        errors.append(f"Service imports failed: {e}")
        print(f"❌ Service imports failed: {e}")
    
    try:
        print("Testing router imports...")
        from app.routers.agent_router import router
        from app.routers.health_router import router as health_router
        print("✓ Router imports successful")
    except Exception as e:
        errors.append(f"Router imports failed: {e}")
        print(f"❌ Router imports failed: {e}")
    
    try:
        print("Testing agent system imports...")
        from app.agents.agent_factory import AgentFactory, agent_prompt_repository
        from app.agents.enum import AgentType
        from app.agents import MarketingAgent, LinkedInWriterAgent, TechBlogWriterAgent, LifestyleBlogWriterAgent
        print("✓ Agent system imports successful")
    except Exception as e:
        errors.append(f"Agent system imports failed: {e}")
        print(f"❌ Agent system imports failed: {e}")
    
    try:
        print("Testing main application creation...")
        from app.core.setup import create_application
        app = create_application()
        print("✓ Application creation successful")
    except Exception as e:
        errors.append(f"Application creation failed: {e}")
        print(f"❌ Application creation failed: {e}")
    
    return errors

def check_file_structure():
    """Check that all required files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'app/__init__.py',
        'app/core/config.py',
        'app/core/setup.py',
        'app/core/exceptions.py',
        'app/core/middleware.py',
        'app/models/database.py',
        'app/schemas/agent.py',
        'app/schemas/base.py',
        'app/services/agent_service.py',
        'app/routers/agent_router.py',
        'app/routers/health_router.py',
        'app/repositories/agent_repository.py',
        'app/agents/base_agent.py',
        'app/agents/agent_factory.py',
        'app/agents/enum/__init__.py',
        'app/agents/enum/agent_enum.py',
        'app/agents/marketing_agents.py',
        'app/agents/linkedin_writer_agent.py',
        'app/agents/tech_blog_writer_agent.py',
        'app/agents/lifestyle_blog_writer_agent.py',
        'app/utils/validation.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return missing_files
    else:
        print("✓ All required files present")
        return []

if __name__ == "__main__":
    print("🔍 Validating unified codebase...")
    print("="*50)
    
    # Check file structure
    missing_files = check_file_structure()
    
    # Test imports
    import_errors = test_imports()
    
    print("="*50)
    if missing_files or import_errors:
        print("❌ VALIDATION FAILED")
        if missing_files:
            print(f"Missing files: {missing_files}")
        if import_errors:
            print(f"Import errors: {import_errors}")
        sys.exit(1)
    else:
        print("✅ ALL VALIDATIONS PASSED")
        print("🚀 The unified codebase is ready to run!")
        print("\nTo start the application:")
        print("  python main.py")
        print("  # or")
        print("  uvicorn main:app --reload")
