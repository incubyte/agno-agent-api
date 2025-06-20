#!/usr/bin/env python3
"""
COMPREHENSIVE CODEBASE ERROR SCANNER
Scans the entire codebase for potential errors, inconsistencies, and issues.
"""

import sys
import os
import ast
import importlib.util
from pathlib import Path
from typing import List, Dict, Any

def scan_python_syntax(file_path: str) -> List[str]:
    """Check Python file for syntax errors"""
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content, filename=file_path)
        
    except SyntaxError as e:
        errors.append(f"Syntax error in {file_path}: {e.msg} at line {e.lineno}")
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
    
    return errors

def check_import_consistency() -> List[str]:
    """Check for import consistency issues"""
    errors = []
    
    # Add app to path
    app_path = Path(__file__).parent / 'app'
    sys.path.insert(0, str(app_path))
    
    # Critical imports to test
    import_tests = [
        # Core imports
        ("app.core.config", "settings"),
        ("app.core.setup", "create_application"),
        ("app.core.exceptions", "BaseAPIException"),
        
        # Model imports
        ("app.models.database", "Agent"),
        
        # Schema imports
        ("app.schemas.agent", "CreateAgentRequest"),
        ("app.schemas.base", "BaseSchema"),
        
        # Service imports
        ("app.services.agent_service", "AgentService"),
        
        # Repository imports
        ("app.repositories.agent_repository", "AgentRepository"),
        
        # Agent system imports
        ("app.agents.enum", "AgentType"),
        ("app.agents.base_agent", "BaseAgent"),
        ("app.agents.agent_factory", "AgentFactory"),
        ("app.agents.marketing_agents", "MarketingAgent"),
        ("app.agents.linkedin_writer_agent", "LinkedInWriterAgent"),
        ("app.agents.tech_blog_writer_agent", "TechBlogWriterAgent"),
        ("app.agents.lifestyle_blog_writer_agent", "LifestyleBlogWriterAgent"),
        
        # Router imports
        ("app.routers.agent_router", "router"),
        ("app.routers.health_router", "router"),
        
        # Utils imports
        ("app.utils.validation", "ValidationService"),
    ]
    
    for module_name, attr_name in import_tests:
        try:
            module = importlib.import_module(module_name)
            if not hasattr(module, attr_name):
                errors.append(f"Module {module_name} missing attribute {attr_name}")
        except ImportError as e:
            errors.append(f"Failed to import {module_name}: {str(e)}")
        except Exception as e:
            errors.append(f"Error testing {module_name}.{attr_name}: {str(e)}")
    
    return errors

def check_enum_consistency() -> List[str]:
    """Check enum and factory consistency"""
    errors = []
    
    try:
        from app.agents.enum import AgentType
        from app.agents.agent_factory import AgentFactory
        
        # Check that all enum values are in factory
        enum_types = set(AgentType)
        factory_types = set(AgentFactory._agents.keys())
        
        missing_in_factory = enum_types - factory_types
        extra_in_factory = factory_types - enum_types
        
        for missing in missing_in_factory:
            errors.append(f"Enum type {missing.name} not found in AgentFactory")
        
        for extra in extra_in_factory:
            errors.append(f"Extra type {extra.name} in AgentFactory not in enum")
        
        # Test that each agent can be created
        for agent_type in AgentType:
            try:
                agent = AgentFactory.get_agent(agent_type)
                if not hasattr(agent, 'get_response'):
                    errors.append(f"Agent {agent_type.name} missing get_response method")
            except Exception as e:
                errors.append(f"Failed to create agent {agent_type.name}: {str(e)}")
        
    except Exception as e:
        errors.append(f"Enum consistency check failed: {str(e)}")
    
    return errors

def check_database_compatibility() -> List[str]:
    """Check database model compatibility"""
    errors = []
    
    try:
        from app.models.database import Agent, create_tables
        from app.core.config import settings
        
        # Check that Agent model has required fields
        required_fields = ['id', 'name', 'slug', 'description', 'image', 'created_at', 'updated_at']
        agent_fields = Agent.model_fields.keys()
        
        for field in required_fields:
            if field not in agent_fields:
                errors.append(f"Agent model missing required field: {field}")
        
        # Test database URL format
        if not settings.DATABASE_URL:
            errors.append("DATABASE_URL not configured")
        elif not (settings.DATABASE_URL.startswith('sqlite://') or 
                  settings.DATABASE_URL.startswith('postgresql://') or
                  settings.DATABASE_URL.startswith('mysql://')):
            errors.append(f"Unsupported DATABASE_URL format: {settings.DATABASE_URL}")
        
    except Exception as e:
        errors.append(f"Database compatibility check failed: {str(e)}")
    
    return errors

def check_application_startup() -> List[str]:
    """Check if application can start without errors"""
    errors = []
    
    try:
        from app.core.setup import create_application
        app = create_application()
        
        # Check that app has required attributes
        if not hasattr(app, 'routes'):
            errors.append("FastAPI app missing routes")
        
        if not hasattr(app, 'middleware'):
            errors.append("FastAPI app missing middleware")
        
    except Exception as e:
        errors.append(f"Application startup failed: {str(e)}")
    
    return errors

def check_file_structure() -> List[str]:
    """Check that all required files exist and have correct structure"""
    errors = []
    
    required_files = [
        'main.py',
        'requirements.txt',
        '.env.example',
        'app/__init__.py',
        'app/core/__init__.py',
        'app/core/config.py',
        'app/core/setup.py',
        'app/core/exceptions.py',
        'app/core/middleware.py',
        'app/models/__init__.py',
        'app/models/database.py',
        'app/schemas/__init__.py',
        'app/schemas/base.py',
        'app/schemas/agent.py',
        'app/services/__init__.py',
        'app/services/agent_service.py',
        'app/repositories/__init__.py',
        'app/repositories/agent_repository.py',
        'app/routers/__init__.py',
        'app/routers/agent_router.py',
        'app/routers/health_router.py',
        'app/agents/__init__.py',
        'app/agents/base_agent.py',
        'app/agents/agent_factory.py',
        'app/agents/enum/__init__.py',
        'app/agents/enum/agent_enum.py',
        'app/agents/marketing_agents.py',
        'app/agents/linkedin_writer_agent.py',
        'app/agents/tech_blog_writer_agent.py',
        'app/agents/lifestyle_blog_writer_agent.py',
        'app/utils/__init__.py',
        'app/utils/validation.py'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Missing required file: {file_path}")
    
    # Check for leftover files that shouldn't exist
    problematic_files = [
        'app/agents/agent_system.py'  # Should be .backup only
    ]
    
    for file_path in problematic_files:
        if Path(file_path).exists():
            errors.append(f"Found problematic file that should be removed: {file_path}")
    
    return errors

def scan_all_python_files() -> List[str]:
    """Scan all Python files for syntax errors"""
    errors = []
    
    for py_file in Path('.').rglob('*.py'):
        # Skip backup files and virtual environments
        if '.backup' in str(py_file) or 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        file_errors = scan_python_syntax(str(py_file))
        errors.extend(file_errors)
    
    return errors

def check_configuration_consistency() -> List[str]:
    """Check configuration consistency"""
    errors = []
    
    try:
        from app.core.config import settings
        
        # Check that critical settings are properly configured
        if settings.MAX_PROMPT_LENGTH < settings.MIN_PROMPT_LENGTH:
            errors.append("MAX_PROMPT_LENGTH is less than MIN_PROMPT_LENGTH")
        
        if settings.DEFAULT_RATE_LIMIT <= 0:
            errors.append("DEFAULT_RATE_LIMIT must be positive")
        
        if settings.MAX_REQUEST_SIZE <= 0:
            errors.append("MAX_REQUEST_SIZE must be positive")
        
        # Check CORS origins format
        for origin in settings.ALLOWED_ORIGINS:
            if not (origin.startswith('http://') or origin.startswith('https://') or origin == '*'):
                errors.append(f"Invalid CORS origin format: {origin}")
        
    except Exception as e:
        errors.append(f"Configuration check failed: {str(e)}")
    
    return errors

def main():
    """Run comprehensive error scan"""
    print("🔍 COMPREHENSIVE CODEBASE ERROR SCANNER")
    print("=" * 70)
    
    all_errors = []
    
    # Run all checks
    print("📁 Checking file structure...")
    all_errors.extend(check_file_structure())
    
    print("🐍 Scanning Python syntax...")
    all_errors.extend(scan_all_python_files())
    
    print("📦 Checking import consistency...")
    all_errors.extend(check_import_consistency())
    
    print("🔧 Checking enum consistency...")
    all_errors.extend(check_enum_consistency())
    
    print("🗄️ Checking database compatibility...")
    all_errors.extend(check_database_compatibility())
    
    print("⚙️ Checking configuration consistency...")
    all_errors.extend(check_configuration_consistency())
    
    print("🚀 Testing application startup...")
    all_errors.extend(check_application_startup())
    
    print("=" * 70)
    print("📊 SCAN RESULTS")
    
    if all_errors:
        print(f"❌ FOUND {len(all_errors)} ERRORS/ISSUES:")
        print()
        for i, error in enumerate(all_errors, 1):
            print(f"   {i:2d}. {error}")
        print()
        print("🔧 Please fix these issues before deploying to production.")
        return 1
    else:
        print("🎉 NO ERRORS FOUND!")
        print("✅ The codebase is clean and ready for production.")
        print()
        print("📋 Scan Summary:")
        print("   • File structure: ✅ Complete")
        print("   • Python syntax: ✅ Valid")
        print("   • Import consistency: ✅ Working")
        print("   • Enum/Factory mapping: ✅ Consistent")
        print("   • Database compatibility: ✅ Ready")
        print("   • Configuration: ✅ Valid")
        print("   • Application startup: ✅ Successful")
        print()
        print("🚀 Ready to run: python main.py")
        return 0

if __name__ == "__main__":
    exit(main())
