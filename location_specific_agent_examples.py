#!/usr/bin/env python3
"""
Usage examples for the Location Specific Agent
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.agents.agent_factory import AgentFactory
from app.agents.enum.agent_enum import AgentType
from app.agents.Location_Specific_Agent import LocationSpecificAgent
import json


def example_simple_query():
    """Example: Simple location query"""
    print("=== Example 1: Simple Location Query ===\n")
    
    # Get agent through factory
    agent = AgentFactory.get_agent(AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT)
    
    # Simple query
    location = "Austin, Texas"
    print(f"Analyzing health intelligence for: {location}")
    
    result = agent.get_response(location)
    print("\nResult:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def example_detailed_query():
    """Example: Detailed query with parameters"""
    print("\n=== Example 2: Detailed Query with Parameters ===\n")
    
    # Direct instantiation
    agent = LocationSpecificAgent()
    
    # Detailed query with JSON parameters
    query = {
        "location": "San Francisco, California",
        "patient_context": "Elderly patient with diabetes and hypertension",
        "emergency_level": "urgent",
        "query_type": "comprehensive"
    }
    
    print(f"Query parameters:")
    print(json.dumps(query, indent=2))
    print("\nAnalyzing...")
    
    result = agent.get_response(json.dumps(query))
    print("\nResult:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def example_emergency_query():
    """Example: Emergency situation query"""
    print("\n=== Example 3: Emergency Situation Query ===\n")
    
    agent = LocationSpecificAgent()
    
    # Emergency query
    emergency_query = {
        "location": "Miami, Florida", 
        "patient_context": "Pregnant woman experiencing complications",
        "emergency_level": "emergency",
        "query_type": "resource_mapping"
    }
    
    print(f"Emergency query parameters:")
    print(json.dumps(emergency_query, indent=2))
    print("\nAnalyzing emergency situation...")
    
    result = agent.get_response(json.dumps(emergency_query))
    print("\nEmergency Analysis Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def example_travel_advisory():
    """Example: Travel health advisory"""
    print("\n=== Example 4: Travel Health Advisory ===\n")
    
    agent = LocationSpecificAgent()
    
    # Travel advisory query
    travel_query = {
        "location": "Bangkok, Thailand",
        "patient_context": "Business traveler, no chronic conditions",
        "emergency_level": "routine", 
        "query_type": "travel_advisory"
    }
    
    print(f"Travel advisory query:")
    print(json.dumps(travel_query, indent=2))
    print("\nAnalyzing travel health requirements...")
    
    result = agent.get_response(json.dumps(travel_query))
    print("\nTravel Health Advisory:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def example_convenience_method():
    """Example: Using convenience method"""
    print("\n=== Example 5: Using Convenience Method ===\n")
    
    agent = LocationSpecificAgent()
    
    print("Using convenience method for routine analysis...")
    
    result = agent.run_location_intelligence(
        location="Denver, Colorado",
        patient_context="Healthcare worker requiring routine health screening",
        emergency_level="routine"
    )
    
    print("\nConvenience Method Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def main():
    """Run all usage examples"""
    print("Location Specific Agent - Usage Examples")
    print("=" * 60)
    
    examples = [
        example_simple_query,
        example_detailed_query,
        example_emergency_query,
        example_travel_advisory,
        example_convenience_method
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n{'='*20} Running Example {i} {'='*20}")
            example_func()
        except Exception as e:
            print(f"❌ Example {i} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Key Usage Patterns:")
    print("=" * 60)
    print("1. Factory Pattern:   AgentFactory.get_agent(AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT)")
    print("2. Direct Creation:   LocationSpecificAgent()")
    print("3. Simple Query:      agent.get_response('Location')")
    print("4. Detailed Query:    agent.get_response(json.dumps(parameters))")
    print("5. Convenience:       agent.run_location_intelligence(location, context, level)")
    print("\n📋 Query Types: comprehensive, outbreak_monitoring, travel_advisory, resource_mapping")
    print("🚨 Emergency Levels: routine, urgent, emergency")


if __name__ == "__main__":
    main()
