#!/usr/bin/env python3
"""
Test script for the consolidated Location Specific Agent
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.agents.agent_factory import AgentFactory
from app.agents.enum.agent_enum import AgentType
from app.agents.Location_Specific_Agent import LocationSpecificAgent
import json


def test_location_specific_agent():
    """Test the consolidated Location Specific Agent"""
    print("=== Testing Location Specific Agent ===\n")
    
    try:
        # Test through factory
        print("1. Testing through AgentFactory...")
        agent = AgentFactory.get_agent(AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT)
        print("✓ Agent created successfully through factory")
        
        # Test direct instantiation
        print("\n2. Testing direct instantiation...")
        direct_agent = LocationSpecificAgent()
        print("✓ Agent created successfully through direct instantiation")
        
        # Test simple query
        print("\n3. Testing simple location query...")
        simple_result = agent.get_response("Austin, Texas")
        print("✓ Simple query completed")
        print(f"Result preview: {simple_result[:300]}...\n")
        
        # Test detailed query
        print("4. Testing detailed query with parameters...")
        detailed_query = {
            "location": "Austin, Texas",
            "patient_context": "Elderly patient with diabetes",
            "emergency_level": "urgent",
            "query_type": "comprehensive"
        }
        
        detailed_result = agent.get_response(json.dumps(detailed_query))
        print("✓ Detailed query completed")
        print(f"Result preview: {detailed_result[:300]}...\n")
        
        # Test convenience method
        print("5. Testing convenience method...")
        convenience_result = direct_agent.run_location_intelligence(
            "Denver, Colorado", 
            "Pregnant patient", 
            "routine"
        )
        print("✓ Convenience method completed")
        print(f"Result preview: {convenience_result[:300]}...\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Location Specific Agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sub_agent_functionality():
    """Test that sub-agents are working within the main agent"""
    print("=== Testing Sub-Agent Functionality ===\n")
    
    try:
        agent = LocationSpecificAgent()
        
        # Test geographic sub-agent
        print("1. Testing geographic sub-agent integration...")
        geo_data = agent._run_geographic_analysis("San Francisco, CA", "General population")
        print("✓ Geographic sub-agent working")
        print(f"Geographic data keys: {list(geo_data.keys())}\n")
        
        # Test epidemiological sub-agent
        print("2. Testing epidemiological sub-agent integration...")
        epi_data = agent._run_epidemiological_analysis(geo_data, "comprehensive", "General population")
        print("✓ Epidemiological sub-agent working")
        print(f"Epidemiological data keys: {list(epi_data.keys())}\n")
        
        # Test healthcare resource sub-agent
        print("3. Testing healthcare resource sub-agent integration...")
        resource_data = agent._run_healthcare_resource_analysis(geo_data, "General population", "routine")
        print("✓ Healthcare resource sub-agent working")
        print(f"Resource data keys: {list(resource_data.keys())}\n")
        
        # Test risk assessment sub-agent
        print("4. Testing risk assessment sub-agent integration...")
        risk_data = agent._run_risk_assessment_analysis(geo_data, epi_data, resource_data, "General population")
        print("✓ Risk assessment sub-agent working")
        print(f"Risk data keys: {list(risk_data.keys())}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing sub-agent functionality: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comprehensive_workflow():
    """Test the complete workflow"""
    print("=== Testing Comprehensive Workflow ===\n")
    
    try:
        agent = LocationSpecificAgent()
        
        print("Running comprehensive analysis for Boston, MA...")
        result = agent.analyze_location_health_intelligence(
            location_input="Boston, Massachusetts",
            patient_context="Healthcare worker", 
            emergency_level="routine",
            query_type="comprehensive"
        )
        
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


def main():
    """Run all tests for the consolidated Location Specific Agent"""
    print("Location Specific Agent Test Suite")
    print("=" * 50)
    
    tests = [
        ("Location Specific Agent", test_location_specific_agent),
        ("Sub-Agent Functionality", test_sub_agent_functionality), 
        ("Comprehensive Workflow", test_comprehensive_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Location Specific Agent is ready.")
        print("\n📝 Usage Example:")
        print("```python")
        print("from app.agents.agent_factory import AgentFactory")
        print("from app.agents.enum.agent_enum import AgentType")
        print("")
        print("agent = AgentFactory.get_agent(AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT)")
        print('result = agent.get_response("Your Location Here")')
        print("print(result)")
        print("```")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
