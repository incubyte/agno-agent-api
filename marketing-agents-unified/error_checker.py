#!/usr/bin/env python3
"""
Comprehensive Error Checker for Agent System
Checks for import errors, enum mismatches, and other potential issues.
"""

import sys
import os
from pathlib import Path

# Add the app directory to path for testing
app_path = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_path))

def check_import_errors():
    """Check for any import errors in the new structure"""
    print("🔍 Checking for import errors...")
    errors = []
    
    try:
        # Test enum imports
        from app.agents.enum import AgentType
        print("✅ AgentType enum imported successfully")
        print(f"   Available types: {[t.value for t in AgentType]}")
    except Exception as e:
        errors.append(f"Enum import failed: {e}")
        print(f"❌ Enum import failed: {e}")
    
    try:
        # Test base agent import
        from app.agents.base_agent import BaseAgent
        print("✅ BaseAgent imported successfully")
    except Exception as e:
        errors.append(f"BaseAgent import failed: {e}")
        print(f"❌ BaseAgent import failed: {e}")
    
    try:
        # Test factory import
        from app.agents.agent_factory import AgentFactory, agent_prompt_repository
        print("✅ AgentFactory imported successfully")
    except Exception as e:
        errors.append(f"AgentFactory import failed: {e}")
        print(f"❌ AgentFactory import failed: {e}")
    
    # Test individual agent imports
    agent_imports = [
        ("MarketingAgent", "app.agents.marketing_agents"),
        ("LinkedInWriterAgent", "app.agents.linkedin_writer_agent"),
        ("TechBlogWriterAgent", "app.agents.tech_blog_writer_agent"),
        ("LifestyleBlogWriterAgent", "app.agents.lifestyle_blog_writer_agent")
    ]
    
    for agent_name, module_path in agent_imports:
        try:
            module = __import__(module_path, fromlist=[agent_name])
            agent_class = getattr(module, agent_name)
            print(f"✅ {agent_name} imported successfully")
        except Exception as e:
            errors.append(f"{agent_name} import failed: {e}")
            print(f"❌ {agent_name} import failed: {e}")
    
    try:
        # Test package-level import
        from app.agents import MarketingAgent, LinkedInWriterAgent, TechBlogWriterAgent, LifestyleBlogWriterAgent
        print("✅ Package-level imports successful")
    except Exception as e:
        errors.append(f"Package import failed: {e}")
        print(f"❌ Package import failed: {e}")
    
    return errors

def check_enum_factory_mapping():
    """Check that all enum values are mapped in the factory"""
    print("\n🔧 Checking enum-factory mapping...")
    errors = []
    
    try:
        from app.agents.enum import AgentType
        from app.agents.agent_factory import AgentFactory
        
        enum_types = set(AgentType)
        factory_types = set(AgentFactory._agents.keys())
        
        missing_in_factory = enum_types - factory_types
        extra_in_factory = factory_types - enum_types
        
        if missing_in_factory:
            error_msg = f"Enum types missing in factory: {[t.value for t in missing_in_factory]}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        if extra_in_factory:
            error_msg = f"Extra types in factory: {[t.value for t in extra_in_factory]}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        if not missing_in_factory and not extra_in_factory:
            print("✅ All enum types properly mapped in factory")
            
        # Test that factory can create each agent
        for agent_type in AgentType:
            try:
                agent = AgentFactory.get_agent(agent_type)
                print(f"✅ Factory can create {agent_type.value}: {agent.name}")
            except Exception as e:
                error_msg = f"Factory failed to create {agent_type.value}: {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                
    except Exception as e:
        errors.append(f"Enum-factory mapping check failed: {e}")
        print(f"❌ Enum-factory mapping check failed: {e}")
    
    return errors

def check_agent_inheritance():
    """Check that all agents properly inherit from BaseAgent"""
    print("\n🏗️ Checking agent inheritance...")
    errors = []
    
    try:
        from app.agents.base_agent import BaseAgent
        from app.agents import MarketingAgent, LinkedInWriterAgent, TechBlogWriterAgent, LifestyleBlogWriterAgent
        
        agents = [MarketingAgent, LinkedInWriterAgent, TechBlogWriterAgent, LifestyleBlogWriterAgent]
        
        for agent_class in agents:
            try:
                # Check inheritance
                if not issubclass(agent_class, BaseAgent):
                    error_msg = f"{agent_class.__name__} does not inherit from BaseAgent"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue
                
                # Check that agent can be instantiated
                agent_instance = agent_class()
                
                # Check required methods exist
                if not hasattr(agent_instance, 'get_response'):
                    error_msg = f"{agent_class.__name__} missing get_response method"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue
                
                # Test that get_response works
                response = agent_instance.get_response("test prompt")
                if not isinstance(response, str):
                    error_msg = f"{agent_class.__name__}.get_response() should return string"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue
                
                print(f"✅ {agent_class.__name__} properly inherits and implements BaseAgent")
                
            except Exception as e:
                error_msg = f"{agent_class.__name__} inheritance check failed: {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                
    except Exception as e:
        errors.append(f"Inheritance check failed: {e}")
        print(f"❌ Inheritance check failed: {e}")
    
    return errors

def check_service_integration():
    """Check that the service layer can work with new agent structure"""
    print("\n🔗 Checking service integration...")
    errors = []
    
    try:
        from app.agents.enum import AgentType
        from app.agents.agent_factory import AgentFactory
        
        # Test the key integration point - can service create agent by enum value?
        for agent_type in AgentType:
            try:
                # This simulates what the service does
                agent = AgentFactory.get_agent(agent_type)
                prompt_template = agent.get_prompt_template()
                
                print(f"✅ Service can create {agent_type.value}")
                
            except Exception as e:
                error_msg = f"Service integration failed for {agent_type.value}: {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                
    except Exception as e:
        errors.append(f"Service integration check failed: {e}")
        print(f"❌ Service integration check failed: {e}")
    
    return errors

def check_file_structure():
    """Check that all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'app/agents/enum/__init__.py',
        'app/agents/enum/agent_enum.py',
        'app/agents/__init__.py',
        'app/agents/base_agent.py',
        'app/agents/agent_factory.py',
        'app/agents/marketing_agents.py',
        'app/agents/linkedin_writer_agent.py',
        'app/agents/tech_blog_writer_agent.py',
        'app/agents/lifestyle_blog_writer_agent.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    return missing_files

def main():
    """Run all error checks"""
    print("🔍 COMPREHENSIVE ERROR CHECKER")
    print("=" * 60)
    
    all_errors = []
    
    # Run all checks
    all_errors.extend(check_file_structure())
    all_errors.extend(check_import_errors())
    all_errors.extend(check_enum_factory_mapping())
    all_errors.extend(check_agent_inheritance())
    all_errors.extend(check_service_integration())
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    
    if all_errors:
        print(f"❌ FOUND {len(all_errors)} ERRORS:")
        for i, error in enumerate(all_errors, 1):
            print(f"   {i}. {error}")
        print("\n🔧 Please fix these errors before proceeding.")
        return 1
    else:
        print("🎉 NO ERRORS FOUND!")
        print("✅ All systems are working correctly.")
        print("\n🚀 The agent system reorganization is successful!")
        print("\n💡 You can now:")
        print("   • Delete the agent_system.py.backup file safely")
        print("   • Start using the new modular structure")
        print("   • Add new agents following the established pattern")
        return 0

if __name__ == "__main__":
    exit(main())
