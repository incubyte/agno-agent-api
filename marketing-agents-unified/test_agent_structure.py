#!/usr/bin/env python3
"""
Test script to verify the new agent structure works correctly.
Run this to test all agents and their functionality.
"""

import sys
import os

# Add the app directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_enum_imports():
    """Test that enum imports work correctly"""
    print("🔧 Testing enum imports...")
    try:
        from app.agents.enum import AgentType
        print(f"✅ AgentType imported successfully")
        print(f"   Available types: {[agent.value for agent in AgentType]}")
        return True
    except Exception as e:
        print(f"❌ Enum import failed: {e}")
        return False

def test_agent_imports():
    """Test that individual agent imports work"""
    print("\n🤖 Testing agent imports...")
    success_count = 0
    
    agents_to_test = [
        ("MarketingAgent", "app.agents.marketing_agents"),
        ("LinkedInWriterAgent", "app.agents.linkedin_writer_agent"), 
        ("TechBlogWriterAgent", "app.agents.tech_blog_writer_agent"),
        ("LifestyleBlogWriterAgent", "app.agents.lifestyle_blog_writer_agent")
    ]
    
    for agent_name, module_path in agents_to_test:
        try:
            module = __import__(module_path, fromlist=[agent_name])
            agent_class = getattr(module, agent_name)
            agent_instance = agent_class()
            print(f"✅ {agent_name}: {agent_instance.name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {agent_name} failed: {e}")
    
    return success_count == len(agents_to_test)

def test_factory_pattern():
    """Test the agent factory"""
    print("\n🏭 Testing agent factory...")
    try:
        from app.agents.agent_factory import AgentFactory
        from app.agents.enum import AgentType
        
        # Test getting an agent
        marketing_agent = AgentFactory.get_agent(AgentType.MARKETING_AGENT)
        print(f"✅ Factory created: {marketing_agent.name}")
        
        # Test getting available types
        available_types = AgentFactory.get_available_types()
        print(f"✅ Available agent types: {len(available_types)}")
        
        return True
    except Exception as e:
        print(f"❌ Factory test failed: {e}")
        return False

def test_agent_responses():
    """Test that agents can generate responses"""
    print("\n💬 Testing agent responses...")
    try:
        from app.agents import MarketingAgent, LifestyleBlogWriterAgent
        
        # Test marketing agent
        marketing_agent = MarketingAgent()
        marketing_response = marketing_agent.get_response("Analyze social media strategy for a tech startup")
        print(f"✅ Marketing agent response: {len(marketing_response)} characters")
        
        # Test lifestyle agent  
        lifestyle_agent = LifestyleBlogWriterAgent()
        lifestyle_response = lifestyle_agent.get_response("morning routine for better productivity")
        print(f"✅ Lifestyle agent response: {len(lifestyle_response)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Response test failed: {e}")
        return False

def test_package_imports():
    """Test importing from the main agents package"""
    print("\n📦 Testing package-level imports...")
    try:
        from app.agents import (
            MarketingAgent, 
            LinkedInWriterAgent, 
            TechBlogWriterAgent, 
            LifestyleBlogWriterAgent
        )
        print("✅ All agents imported from package successfully")
        return True
    except Exception as e:
        print(f"❌ Package import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing New Agent Structure")
    print("=" * 50)
    
    tests = [
        test_enum_imports,
        test_agent_imports,
        test_factory_pattern,
        test_agent_responses,
        test_package_imports
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The new agent structure is working perfectly.")
        print("\n🚀 You can now:")
        print("   • Add new agents easily by creating new files")
        print("   • Import specific agents: from app.agents import MarketingAgent")
        print("   • Use the factory: AgentFactory.get_agent(AgentType.MARKETING_AGENT)")
        print("   • Maintain each agent independently")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
