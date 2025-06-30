"""
Medication Interaction Agent - Complete Implementation
"""

from typing import Iterator, Dict, Any, List, Optional
from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.storage.sqlite import SqliteStorage
from agno.tools.reasoning import ReasoningTools
from app.agents.base_agent import BaseAgent
from app.core import settings
from app.tools.duckduckgo_search import FreeDrugSearchTool
from agno.utils.pprint import pprint_run_response
import json
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicationInteractionAgent(BaseAgent):
    """Medication Interaction Agent with free search capabilities"""
    
    def __init__(self):
        try:
            self.AGENT_STORAGE = settings.AGENT_STORAGE
        except Exception as e:
            logger.warning(f"Settings error: {e}. Using default storage.")
            self.AGENT_STORAGE = "./default_agent_storage.db"
        
        try:
            self.drug_search_tool = FreeDrugSearchTool(max_results=5)
        except Exception as e:
            logger.warning(f"Search tool initialization failed: {e}. Search will be disabled.")
            self.drug_search_tool = None
        
        self.medication_team = self._create_medication_interaction_team()
        logger.info("Medication Interaction Agent initialized successfully")

    def create_drug_parser_agent(self):
        return Agent(
            name="Drug Parser & Standardization Agent",
            role="You are a pharmaceutical data specialist with search capabilities for drug identification",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Parse, standardize, and validate medication inputs",
                "Standardize drug names to generic names when possible",
                "Extract dosage, form, and route information from user input",
                "Handle typos, brand names, and generic name conversion",
                "Use structured JSON output format for drug parsing results",
                "Always indicate confidence level and whether manual review is needed",
                "Flag unknown substances for further investigation",
                "Consider drug synonyms, brand names, and international names",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def create_interaction_detector_agent(self):
        return Agent(
            name="Interaction Detection & Risk Assessment Agent",
            role="You are a clinical pharmacologist specializing in drug interaction analysis",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Analyze drug combinations for potential interactions",
                "Assess interaction severity: contraindicated, major, moderate, minor, or none",
                "Identify interaction mechanisms (pharmacokinetic vs pharmacodynamic)",
                "Consider drug metabolism pathways, especially CYP450 interactions",
                "Determine onset timing and monitoring requirements",
                "Provide clear clinical explanations for each interaction",
                "Include contraindications and special warnings",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def create_patient_context_agent(self):
        return Agent(
            name="Patient Context & Personalization Agent", 
            role="You are a clinical pharmacist specializing in personalized medication therapy",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Apply patient-specific factors to modify drug interaction risks",
                "Consider age, weight, and gender considerations",
                "Adjust interaction severity based on organ function",
                "Consider comorbidities and their impact on drug safety",
                "Apply age-specific considerations (pediatric, geriatric)",
                "Recommend additional monitoring based on patient profile",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def create_alert_generator_agent(self):
        return Agent(
            name="Alert Generation & Recommendation Agent",
            role="You are a clinical communication specialist creating medication safety alerts",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Generate actionable medication safety alerts with appropriate urgency",
                "Suggest specific alternative medications when interactions are problematic",
                "Provide clear timing recommendations for drug administration",
                "Use appropriate alert levels: CRITICAL, WARNING, CAUTION, INFORMATION",
                "Include clear explanations of WHY interactions matter clinically",
                "Provide specific, actionable next steps for each alert level",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def _create_medication_interaction_team(self):
        return Agent(
            name="Medication Interaction Analysis Team",
            team=[
                self.create_drug_parser_agent(),
                self.create_interaction_detector_agent(), 
                self.create_patient_context_agent(),
                self.create_alert_generator_agent()
            ],
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=12000),
            instructions=[
                "You are a comprehensive medication interaction analysis team.",
                "Work together to analyze drug combinations for safety.",
                "Follow this workflow:",
                "1. Drug Parser: Standardize and validate medications",
                "2. Interaction Detector: Analyze drug pairs for interactions",
                "3. Patient Context: Apply patient-specific factors",
                "4. Alert Generator: Create appropriate alerts and recommendations",
                "",
                "Safety Priorities:",
                "- Patient safety is the absolute top priority",
                "- When in doubt, err on the side of caution",
                "- Always recommend professional consultation for complex cases",
                "",
                "Format output as a comprehensive report with:",
                "1. Executive Summary with key findings",
                "2. Drug Analysis with standardized names",
                "3. Interaction Assessment with severity levels", 
                "4. Patient-Specific Considerations",
                "5. Recommendations and Alternatives",
                "6. Monitoring Plan",
                "7. Emergency Guidance when applicable",
            ],
            show_tool_calls=True,
            markdown=True,
            storage=SqliteStorage(table_name="medication_interaction_team", db_file=self.AGENT_STORAGE),
            stream=True,
        )

    def get_response(self, url: str) -> str:
        """Main interface method for medication interaction analysis"""
        # Note: 'url' parameter name kept for BaseAgent compatibility
        # but we treat it as a general prompt for medication analysis
        prompt = url  # Rename for clarity
        logger.info(f"Processing medication request: {prompt[:100]}...")
        
        # Enhance with search results if needed
        enhanced_info = self._enhance_with_search(prompt)
        
        # Create comprehensive prompt
        analysis_prompt = f"""
        Please conduct a comprehensive medication interaction analysis.
        
        USER REQUEST:
        {prompt}
        
        ENHANCED INFORMATION FROM SEARCH:
        {enhanced_info}
        
        Please provide:
        1. Drug identification and standardization
        2. Comprehensive interaction analysis
        3. Risk assessment and severity levels
        4. Patient-specific considerations
        5. Actionable recommendations and alternatives
        6. Monitoring requirements
        7. Emergency guidance if needed
        
        Focus on patient safety and provide clear, actionable guidance.
        """

        try:
            response_stream: Iterator[RunResponse] = self.medication_team.run(analysis_prompt)
            content = ""
            for response in response_stream:
                content += response.content
            
            logger.info("Medication analysis completed successfully")
            return content
        except Exception as e:
            logger.error(f"Error in medication analysis: {e}")
            return f"# Error in Medication Analysis\n\n{str(e)}\n\nPlease try again or consult a healthcare professional."

    def _enhance_with_search(self, prompt: str) -> str:
        """Enhance prompt with search results for unknown drugs"""
        if self.drug_search_tool is None:
            return "Search enhancement unavailable (search tool not initialized)."
            
        try:
            # Extract potential drug names from prompt
            words = prompt.split()
            drug_candidates = [word for word in words if len(word) > 3 and word.isalpha()]
            
            search_results = []
            for drug in drug_candidates[:2]:  # Limit to 2 searches to avoid rate limiting
                if self._might_be_drug(drug):
                    logger.info(f"Searching for drug information: {drug}")
                    result = self.drug_search_tool.search_drug_info(drug)
                    search_results.append(f"Search for '{drug}': {result[:300]}...")
            
            return "\n".join(search_results) if search_results else "No additional search performed."
            
        except Exception as e:
            logger.warning(f"Search enhancement failed: {e}")
            return "Search enhancement unavailable."

    def _might_be_drug(self, word: str) -> bool:
        """Simple heuristic to determine if a word might be a drug name"""
        # Skip common words
        common_words = {'patient', 'taking', 'medication', 'drug', 'interaction', 'check', 'analysis'}
        if word.lower() in common_words:
            return False
        
        # Consider words that might be drug names
        return len(word) > 4 and word.isalpha()
