#!/usr/bin/env python3
"""
Test script for Location Health Intelligence Agent system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.agents.location_health_intelligence_agent import LocationHealthIntelligenceAgent
from app.agents.agent_factory import AgentFactory
from app.agents.enum.agent_enum import AgentType
import json


def test_individual_agents():
    """Test individual specialized agents"""
    print("=== Testing Individual Agents ===\n")
    
    try:
        # Test Geographic Context Agent
        print("1. Testing Geographic Context Agent...")
        geo_agent = AgentFactory.get_agent(AgentType.GEOGRAPHIC_CONTEXT_AGENT)
        geo_result = geo_agent.get_response("Austin, Texas")
        print("✓ Geographic Context Agent working")
        print(f"Sample result: {geo_result[:200]}...\n")
        
        # Test Epidemiological Intelligence Agent  
        print("2. Testing Epidemiological Intelligence Agent...")
        epi_agent = AgentFactory.get_agent(AgentType.EPIDEMIOLOGICAL_INTELLIGENCE_AGENT)
        epi_result = epi_agent.get_response("Austin, Texas")
        print("✓ Epidemiological Intelligence Agent working")
        print(f"Sample result: {epi_result[:200]}...\n")
        
        # Test Healthcare Resource Mapping Agent
        print("3. Testing Healthcare Resource Mapping Agent...")
        resource_agent = AgentFactory.get_agent(AgentType.HEALTHCARE_RESOURCE_MAPPING_AGENT)
        resource_result = resource_agent.get_response("Austin, Texas")
        print("✓ Healthcare Resource Mapping Agent working")
        print(f"Sample result: {resource_result[:200]}...\n")
        
        # Test Risk Assessment Agent
        print("4. Testing Risk Assessment Alert Agent...")
        risk_agent = AgentFactory.get_agent(AgentType.RISK_ASSESSMENT_ALERT_AGENT)
        risk_result = risk_agent.get_response("Austin, Texas")
        print("✓ Risk Assessment Alert Agent working")
        print(f"Sample result: {risk_result[:200]}...\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing individual agents: {e}")
        return False


def test_master_agent():
    """Test the master Location Health Intelligence Agent"""
    print("=== Testing Master Location Health Intelligence Agent ===\n")
    
    try:
        # Test master agent
        print("Testing Master Location Health Intelligence Agent...")
        master_agent = AgentFactory.get_agent(AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT)
        
        # Test with simple location
        result = master_agent.get_response("Austin, Texas")
        print("✓ Master Location Health Intelligence Agent working")
        print("Sample result preview:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing master agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comprehensive_workflow():
    """Test the comprehensive workflow with detailed parameters"""
    print("\n=== Testing Comprehensive Workflow ===\n")
    
    try:
        # Initialize master agent
        master_agent = LocationHealthIntelligenceAgent()
        
        # Test with detailed parameters
        test_query = {
            "location": "Austin, Texas",
            "patient_context": "Elderly patient with diabetes",
            "emergency_level": "urgent",
            "query_type": "comprehensive"
        }
        
        print("Running comprehensive analysis with parameters:")
        print(json.dumps(test_query, indent=2))
        print("\nExecuting analysis...")
        
        result = master_agent.get_response(json.dumps(test_query))
        
        print("\n✓ Comprehensive workflow completed successfully")
        print("\nFull Analysis Result:")
        print("=" * 80)
        print(result)
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in comprehensive workflow: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_enum_completeness():
    """Test that all agent types are properly registered"""
    print("\n=== Testing Agent Enum Completeness ===\n")
    
    try:
        from app.agents.enum.agent_enum import AgentType
        
        location_intelligence_agents = [
            AgentType.GEOGRAPHIC_CONTEXT_AGENT,
            AgentType.EPIDEMIOLOGICAL_INTELLIGENCE_AGENT,
            AgentType.HEALTHCARE_RESOURCE_MAPPING_AGENT,
            AgentType.RISK_ASSESSMENT_ALERT_AGENT,
            AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT
        ]
        
        print("Checking agent type registrations:")
        for agent_type in location_intelligence_agents:
            try:
                agent = AgentFactory.get_agent(agent_type)
                print(f"✓ {agent_type.value} - registered and accessible")
            except Exception as e:
                print(f"❌ {agent_type.value} - error: {e}")
                return False
        
        print("\n✓ All location intelligence agents properly registered")
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent enum: {e}")
        return False


def main():
    """Run all tests"""
    print("Location Health Intelligence Agent System Test")
    print("=" * 60)
    
    tests = [
        ("Agent Enum Completeness", test_agent_enum_completeness),
        ("Individual Agents", test_individual_agents),
        ("Master Agent", test_master_agent),
        ("Comprehensive Workflow", test_comprehensive_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:30} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Location Health Intelligence Agent system is ready.")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
