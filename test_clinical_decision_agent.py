"""
Test script for Clinical Decision Agent
This demonstrates how to use the Clinical Decision Agent with the example case
"""

import json
from app.agents.clinical_decision_agents import ClinicalDecisionAgent

def test_clinical_decision_agent():
    # Example patient case from the document
    patient_case = {
        "demographics": {
            "age": 45,
            "gender": "female",
            "weight": "140 lbs",
            "ethnicity": "Hispanic"
        },
        "primary_diagnosis": "Major Depressive Disorder, moderate severity (PHQ-9 score: 16)",
        "comorbidities": [
            "Migraine headaches",
            "Obesity (BMI 32)",
            "Pre-diabetes"
        ],
        "current_medications": [
            "Sumatriptan 50mg PRN",
            "Metformin 500mg daily"
        ],
        "previous_treatments": [
            {
                "medication": "Sertraline 50mg",
                "outcome": "discontinued due to weight gain and sexual side effects"
            }
        ],
        "social_history": "Works full-time, has teenage children, concerned about cognitive effects",
        "lab_values": {
            "fasting_glucose": 118,
            "TSH": "normal",
            "CBC": "normal"
        },
        "allergies": ["Penicillin (rash)"],
        "clinical_question": "What antidepressant should be initiated given previous SSRI intolerance and patient's concerns about weight/cognitive effects?"
    }
    
    # Initialize the Clinical Decision Agent
    agent = ClinicalDecisionAgent()
    
    # Get clinical decision analysis
    print("Starting Clinical Decision Analysis...")
    print("=" * 50)
    
    response = agent.get_response(patient_case)
    
    print("Clinical Decision Analysis Complete:")
    print("=" * 50)
    print(response)

if __name__ == "__main__":
    test_clinical_decision_agent()
