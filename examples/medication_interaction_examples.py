#!/usr/bin/env python3
"""
Example usage of the Medication Interaction Agent
Demonstrates different ways to use the agent for drug interaction analysis
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import required modules
from app.agents.medication_interaction_agent import MedicationInteractionAgent

def example_basic_interaction_check():
    """Example: Basic medication interaction check"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Medication Interaction Check")
    print("=" * 60)
    
    agent = MedicationInteractionAgent()
    
    prompt = "Check interaction between aspirin and warfarin for a 65-year-old patient"
    
    print(f"Query: {prompt}")
    print("\nAnalysis:")
    print("-" * 40)
    
    try:
        result = agent.get_response(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")


def example_multiple_medication_analysis():
    """Example: Analysis of multiple medications"""
    print("=" * 60)
    print("EXAMPLE 2: Multiple Medication Analysis")
    print("=" * 60)
    
    agent = MedicationInteractionAgent()
    
    prompt = """
    Analyze these medications for a 68-year-old patient with diabetes and hypertension:
    1. Warfarin 5mg daily
    2. Aspirin 81mg daily
    3. Metformin 500mg twice daily
    4. Lisinopril 10mg daily
    5. Atorvastatin 20mg daily
    """
    
    print(f"Query: {prompt.strip()}")
    print("\nAnalysis:")
    print("-" * 40)
    
    try:
        result = agent.get_response(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")


def example_medication_safety_review():
    """Example: Comprehensive medication safety review"""
    print("=" * 60)
    print("EXAMPLE 3: Medication Safety Review")
    print("=" * 60)
    
    agent = MedicationInteractionAgent()
    
    prompt = """
    Safety review for patient taking:
    - Warfarin 5mg daily
    - Aspirin 81mg daily  
    - Metformin 500mg twice daily
    - Omeprazole 20mg daily
    
    Patient is 72 years old with recent GI bleeding episode.
    """
    
    print(f"Query: {prompt.strip()}")
    print("\nAnalysis:")
    print("-" * 40)
    
    try:
        result = agent.get_response(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")


def example_with_search_enhancement():
    """Example: Using search enhancement for unknown drugs"""
    print("=" * 60)
    print("EXAMPLE 4: Search Enhancement for Unknown Drugs")
    print("=" * 60)
    
    agent = MedicationInteractionAgent()
    
    prompt = "Check interaction between semaglutide and metformin"
    
    print(f"Query: {prompt}")
    print("Note: This will use DuckDuckGo search to find information about less common drugs")
    print("\nAnalysis:")
    print("-" * 40)
    
    try:
        result = agent.get_response(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")


def example_patient_specific_analysis():
    """Example: Patient-specific risk assessment"""
    print("=" * 60)
    print("EXAMPLE 5: Patient-Specific Risk Assessment")
    print("=" * 60)
    
    agent = MedicationInteractionAgent()
    
    prompt = """
    Patient: 85-year-old female, 120 lbs, with kidney disease and heart failure
    Medications: digoxin, furosemide, lisinopril
    Allergic to penicillin
    
    Please assess interaction risks and provide personalized recommendations.
    """
    
    print(f"Query: {prompt.strip()}")
    print("\nAnalysis:")
    print("-" * 40)
    
    try:
        result = agent.get_response(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")


def test_search_tool():
    """Test the DuckDuckGo search tool separately"""
    print("=" * 60)
    print("TESTING: DuckDuckGo Search Tool")
    print("=" * 60)
    
    try:
        from app.tools.duckduckgo_search import FreeDrugSearchTool
        
        search_tool = FreeDrugSearchTool()
        
        print("Testing drug information search...")
        result = search_tool.search_drug_info("aspirin")
        print(f"Search result length: {len(result)} characters")
        print(f"First 200 characters: {result[:200]}...")
        
        print("\nTesting drug interaction search...")
        result = search_tool.search_drug_interactions("aspirin", "warfarin")
        print(f"Interaction search result length: {len(result)} characters")
        print(f"First 200 characters: {result[:200]}...")
        
    except Exception as e:
        print(f"Search tool test failed: {e}")
    
    print("\n")


def main():
    """Run all examples"""
    print("🧪 Medication Interaction Agent - Example Usage")
    print("=" * 80)
    print()
    
    # Check if we have the required environment variables
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  Warning: ANTHROPIC_API_KEY not found in environment")
        print("Some examples may not work without this API key.")
        print("Please set it in your .env file or environment.")
        print()
    
    try:
        # Test search tool first
        test_search_tool()
        
        # Run examples
        example_basic_interaction_check()
        example_multiple_medication_analysis()
        example_medication_safety_review()
        example_with_search_enhancement()
        example_patient_specific_analysis()
        
        print("=" * 80)
        print("✅ All examples completed!")
        print()
        print("💡 Tips for using the Medication Interaction Agent:")
        print("- Be specific about dosages and patient information")
        print("- Include patient age, weight, and medical conditions when relevant")
        print("- Mention allergies and organ function if known")
        print("- The agent will search for unknown drugs automatically")
        print("- Always consult healthcare professionals for medical decisions")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
