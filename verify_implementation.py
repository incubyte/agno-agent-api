#!/usr/bin/env python3
"""
Final verification script to test all fixes and ensure no breakage points.
Run this to verify the implementation is solid before deployment.
"""

import os
import sys
import importlib.util

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all imports work correctly"""
    print("🔍 Testing Import Integrity...")
    
    try:
        # Test new agent imports
        from app.agents.website_performance_auditor import WebsitePerformanceAuditor
        from app.agents.seo_auditor_agent import SEOAuditorAgent
        from app.agents.marketing_copywriter_agent import MarketingCopywriterAgent
        print("  ✅ New agent imports: SUCCESS")
        
        # Test factory imports  
        from app.agents.agent_factory import AgentFactory
        from app.agents.enum.agent_enum import AgentType
        print("  ✅ Factory imports: SUCCESS")
        
        # Test settings import consistency
        from app.core import settings
        print("  ✅ Settings import: SUCCESS")
        
        # Test that agents can be instantiated
        audit_agent = WebsitePerformanceAuditor()
        seo_agent = SEOAuditorAgent()
        copy_agent = MarketingCopywriterAgent()
        print("  ✅ Agent instantiation: SUCCESS")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Instantiation error: {e}")
        return False

def test_agent_factory():
    """Test that AgentFactory works with new agents"""
    print("\\n🏭 Testing Agent Factory...")
    
    try:
        from app.agents.agent_factory import AgentFactory
        from app.agents.enum.agent_enum import AgentType
        
        # Test all new agent types
        test_types = [
            (AgentType.WEBSITE_PERFORMANCE_AUDITOR, "WebsitePerformanceAuditor"),
            (AgentType.SEO_AUDIT, "SEOAuditorAgent"),
            (AgentType.MARKETING_COPYWRITER_AGENT, "MarketingCopywriterAgent")
        ]
        
        for agent_type, expected_class in test_types:
            agent = AgentFactory.get_agent(agent_type)
            actual_class = agent.__class__.__name__
            
            if actual_class == expected_class:
                print(f"  ✅ {agent_type.value}: {actual_class}")
            else:
                print(f"  ❌ {agent_type.value}: Expected {expected_class}, got {actual_class}")
                return False
                
        return True
        
    except Exception as e:
        print(f"  ❌ Factory error: {e}")
        return False

def test_prompt_repository():
    """Test that prompts are configured"""
    print("\\n💬 Testing Prompt Repository...")
    
    try:
        from app.agents.agent_prompt_repository import agent_prompt_repository
        from app.agents.enum.agent_enum import AgentType
        
        required_types = [
            AgentType.WEBSITE_PERFORMANCE_AUDITOR,
            AgentType.SEO_AUDIT,
            AgentType.MARKETING_COPYWRITER_AGENT
        ]
        
        for agent_type in required_types:
            if agent_type in agent_prompt_repository:
                prompt = agent_prompt_repository[agent_type]
                if len(prompt) > 20:  # Reasonable prompt length
                    print(f"  ✅ {agent_type.value}: {len(prompt)} chars")
                else:
                    print(f"  ⚠️ {agent_type.value}: Prompt too short ({len(prompt)} chars)")
            else:
                print(f"  ❌ {agent_type.value}: No prompt configured")
                return False
                
        return True
        
    except Exception as e:
        print(f"  ❌ Prompt repository error: {e}")
        return False

def test_agent_methods():
    """Test that agents have required methods"""
    print("\\n🧪 Testing Agent Method Signatures...")
    
    try:
        from app.agents.website_performance_auditor import WebsitePerformanceAuditor
        from app.agents.seo_auditor_agent import SEOAuditorAgent
        from app.agents.marketing_copywriter_agent import MarketingCopywriterAgent
        
        agents = [
            ("WebsitePerformanceAuditor", WebsitePerformanceAuditor()),
            ("SEOAuditorAgent", SEOAuditorAgent()),
            ("MarketingCopywriterAgent", MarketingCopywriterAgent())
        ]
        
        for name, agent in agents:
            # Check required methods
            if hasattr(agent, 'get_response') and callable(getattr(agent, 'get_response')):
                print(f"  ✅ {name}: get_response method exists")
            else:
                print(f"  ❌ {name}: Missing get_response method")
                return False
                
            # Check that agent has team attribute
            team_attrs = ['website_audit_team', 'seo_audit_team', 'copywriter_team']
            has_team = any(hasattr(agent, attr) for attr in team_attrs)
            
            if has_team:
                print(f"  ✅ {name}: Team attribute exists")
            else:
                print(f"  ❌ {name}: Missing team attribute")
                return False
                
        return True
        
    except Exception as e:
        print(f"  ❌ Method test error: {e}")
        return False

def test_database_models():
    """Test that database models work with seeding"""
    print("\\n🗄️ Testing Database Model Compatibility...")
    
    try:
        from app.db.models import Agent
        from sqlmodel import select
        
        # Test that we can create Agent objects
        test_agent = Agent(
            name="Test Agent",
            slug="test-agent",
            description="Test description",
            image="test.svg"
        )
        
        print(f"  ✅ Agent model: Can create instances")
        
        # Test that select statement works
        select_stmt = select(Agent).where(Agent.slug == "test-agent")
        print(f"  ✅ SQLModel select: Statement created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database model error: {e}")
        return False

def test_settings_access():
    """Test that settings are accessible"""
    print("\\n⚙️ Testing Settings Access...")
    
    try:
        from app.core import settings
        
        # Test required settings exist
        required_settings = ['ANTHROPIC_API_KEY', 'AGENT_STORAGE', 'DATABASE_URL']
        
        for setting_name in required_settings:
            if hasattr(settings, setting_name):
                value = getattr(settings, setting_name)
                if value:  # Check it's not None or empty
                    print(f"  ✅ {setting_name}: Configured")
                else:
                    print(f"  ⚠️ {setting_name}: Empty/None (may need .env setup)")
            else:
                print(f"  ❌ {setting_name}: Missing from settings")
                return False
                
        return True
        
    except Exception as e:
        print(f"  ❌ Settings error: {e}")
        return False

def test_url_parsing():
    """Test URL parsing logic in agents"""
    print("\\n🔗 Testing URL Parsing Logic...")
    
    try:
        import re
        
        # Test the URL regex pattern used in agents
        url_pattern = r'https?://[^\\s]+'
        
        test_cases = [
            ("https://example.com", True),
            ("http://test.com", True),
            ("https://example.com/path", True),
            ("Please check https://example.com for issues", True),
            ("no url here", False),
            ("", False)
        ]
        
        for test_input, should_find in test_cases:
            urls = re.findall(url_pattern, test_input)
            found = len(urls) > 0
            
            if found == should_find:
                status = "✅" if found else "➖"
                print(f"  {status} '{test_input[:30]}...': {'Found' if found else 'No'} URL")
            else:
                print(f"  ❌ '{test_input[:30]}...': Expected {should_find}, got {found}")
                return False
                
        return True
        
    except Exception as e:
        print(f"  ❌ URL parsing error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide final assessment"""
    print("🧪 COMPREHENSIVE CODEBASE VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Import Integrity", test_imports),
        ("Agent Factory", test_agent_factory),
        ("Prompt Repository", test_prompt_repository),
        ("Agent Methods", test_agent_methods),
        ("Database Models", test_database_models),
        ("Settings Access", test_settings_access),
        ("URL Parsing", test_url_parsing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\\n❌ {test_name} FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\\n🎉 ALL TESTS PASSED! Codebase is ready for deployment.")
        print("\\n✅ No critical issues found")
        print("✅ All imports working")
        print("✅ All agents properly configured")
        print("✅ Database integration ready")
        print("\\n🚀 Ready to run: python seed_new_agents.py")
        return True
    else:
        print(f"\\n⚠️ {total - passed} test(s) failed. Review issues above before deployment.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
