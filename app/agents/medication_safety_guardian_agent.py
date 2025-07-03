from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.storage.sqlite import SqliteStorage
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.reasoning import ReasoningTools
from app.agents.base_agent import BaseAgent
from app.core import settings
from agno.utils.pprint import pprint_run_response
# from agno.models.google import Gemini
import os


class MedicationSafetyGuardianAgent(BaseAgent):
    def __init__(self):
        self.AGENT_STORAGE = settings.AGENT_STORAGE
        print(self.AGENT_STORAGE)
        self.medication_safety_team = self._create_medication_safety_team()

    # Factory methods for creating individual agents
    def create_recall_monitor_agent(self):
        return Agent(
            name="FDA Recall Monitor Agent",
            role="You are an expert FDA drug recall monitoring specialist focused on patient safety",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "Monitor and analyze FDA drug recalls with clinical precision",
                "Identify recall severity levels and patient impact immediately",
                "Cross-reference recalled products with patient medication lists",
                "Prioritize recalls by urgency: Class I (life-threatening), Class II (moderate risk), Class III (low risk)",
                "Extract critical recall information: NDC codes, lot numbers, expiration dates",
                "Determine geographic distribution and affected patient populations",
                "Calculate timeline urgency for patient notifications",
                "Provide clear risk assessment for healthcare providers",
                "Generate immediate action items for recalled medications",
                "Use structured clinical communication for urgent alerts",
                "Search current FDA databases for recall information",
                "Format all output in markdown with urgency indicators",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
            stream=True,
            markdown=True,
        )

    def create_drug_interaction_agent(self):
        return Agent(
            name="Drug Interaction Analyzer Agent",
            role="You are a clinical pharmacology expert specializing in drug-drug interactions",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "Analyze drug interactions with clinical precision and evidence-based assessment",
                "Classify interactions by severity: Major (contraindicated), Moderate (caution), Minor (awareness)",
                "Identify mechanism of interactions: pharmacokinetic vs pharmacodynamic",
                "Consider patient-specific factors: age, kidney function, liver function",
                "Provide specific clinical management strategies for each interaction",
                "Include monitoring parameters and timeline recommendations",
                "Flag interactions requiring immediate intervention vs routine monitoring",
                "Consider drug-food and drug-disease interactions",
                "Provide alternative medication suggestions when interactions are problematic",
                "Use clinical severity indicators: CRITICAL, CAUTION, MONITOR",
                "Search for latest interaction data and clinical guidelines",
                "Format all output in markdown with clear action items",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
            stream=True,
            markdown=True,
        )

    def create_therapeutic_alternative_agent(self):
        return Agent(
            name="Therapeutic Alternative Specialist Agent",
            role="You are a clinical pharmacist expert in therapeutic alternatives and medication substitutions",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "Identify safe and effective therapeutic alternatives for problematic medications",
                "Consider bioequivalent, therapeutically equivalent, and pharmacologically similar options",
                "Evaluate alternatives based on efficacy, safety, and patient-specific factors",
                "Provide evidence-based recommendations with clinical rationale",
                "Consider formulary status, cost, and insurance coverage implications",
                "Account for patient allergies, contraindications, and comorbidities",
                "Suggest appropriate dosing conversions and equivalencies",
                "Include monitoring requirements for new medications",
                "Provide transition protocols and timing recommendations",
                "Prioritize alternatives by safety profile and clinical appropriateness",
                "Search for current clinical guidelines and therapeutic options",
                "Format all output in markdown with prioritized recommendations",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
            stream=True,
            markdown=True,
        )

    def create_clinical_safety_agent(self):
        return Agent(
            name="Clinical Safety Analyst Agent",
            role="You are a clinical safety expert specializing in comprehensive medication risk assessment",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "Perform comprehensive clinical safety assessments for medication regimens",
                "Evaluate patient-specific risk factors: age, organ function, comorbidities",
                "Assess medication appropriateness for patient population",
                "Identify contraindications, precautions, and special considerations",
                "Evaluate dosing appropriateness and adjustment needs",
                "Consider polypharmacy risks and medication burden",
                "Assess adherence challenges and practical considerations",
                "Provide risk stratification and priority ranking",
                "Generate actionable safety recommendations with timelines",
                "Include monitoring protocols and safety benchmarks",
                "Search for evidence-based safety guidelines and standards",
                "Format all output in markdown with risk assessments",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
            stream=True,
            markdown=True,
        )

    def create_patient_monitoring_agent(self):
        return Agent(
            name="Patient Monitoring Specialist Agent",
            role="You are a clinical monitoring expert specializing in patient safety during medication changes",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "Design comprehensive monitoring protocols for medication transitions",
                "Establish safety benchmarks and warning indicators",
                "Create follow-up schedules based on medication risk profiles",
                "Monitor therapeutic effectiveness and safety outcomes",
                "Identify red flag symptoms requiring immediate intervention",
                "Track adherence and patient-reported outcomes",
                "Coordinate monitoring between healthcare team members",
                "Generate progress reports and safety updates",
                "Recommend monitoring frequency and duration",
                "Provide patient education on monitoring expectations",
                "Search for monitoring best practices and protocols",
                "Format all output in markdown with monitoring schedules",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
            stream=True,
            markdown=True,
        )

    def _create_medication_safety_team(self):
        return Agent(
            name="Medication Safety Guardian Team",
            team=[
                self.create_recall_monitor_agent(),
                self.create_drug_interaction_agent(),
                self.create_therapeutic_alternative_agent(),
                self.create_clinical_safety_agent(),
                self.create_patient_monitoring_agent()
            ],
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                "You are a team of medication safety experts who work together to ensure patient safety and optimal therapeutic outcomes.",
                "Given patient information and medication details, conduct a comprehensive safety review.",
                "Each team member has specific expertise aligned with core medication safety domains:",
                "1. FDA Recall Monitor - Reviews current recalls and safety alerts",
                "2. Drug Interaction Analyzer - Evaluates all drug interactions",
                "3. Therapeutic Alternative Specialist - Identifies safe medication alternatives",
                "4. Clinical Safety Analyst - Performs overall safety risk assessment",
                "5. Patient Monitoring Specialist - Designs monitoring and follow-up protocols",
                "Provide a comprehensive medication safety report with specific recommendations",
                "Include urgency indicators: CRITICAL, CAUTION, ROUTINE",
                "Format all output in markdown with clear sections and action items",
                "Always prioritize patient safety while maintaining therapeutic effectiveness",
                "Create specific timelines for implementation and monitoring",
                "Provide clear communication templates for healthcare providers and patients",
                "Ensure recommendations are evidence-based and clinically practical",
                "Include regulatory compliance considerations when applicable",
            ],
            show_tool_calls=True,
            markdown=True,
            storage=SqliteStorage(table_name="medication_safety_team", db_file=self.AGENT_STORAGE),
            stream=True,
        )


    def review_medication_safety(self, patient_case):
        """
        Main method to conduct comprehensive medication safety review (like review_marketing_website)
        """
        print(f"Starting medication safety review for patient case")
        
        prompt = f"""
        Please conduct a complete medication safety review and analysis for this patient case.
        The goal is to ensure patient safety and optimal therapeutic outcomes through comprehensive assessment.
        
        PATIENT CASE:
        {patient_case}
        
        Follow this comprehensive process:
        1. FDA Recall Monitor: Check all medications against current FDA recalls and safety alerts
        2. Drug Interaction Analyzer: Evaluate all potential drug-drug, drug-food, and drug-disease interactions
        3. Therapeutic Alternative Specialist: Identify any problematic medications and suggest alternatives
        4. Clinical Safety Analyst: Perform overall patient safety risk assessment
        5. Patient Monitoring Specialist: Design monitoring protocols and follow-up plans
        
        For each area, provide:
        - Current safety status assessment
        - Specific safety concerns identified
        - Evidence-based recommendations with urgency levels
        - Monitoring requirements and timelines
        - Patient and provider communication guidance
        
        Create a comprehensive medication safety report with:
        - Executive summary with key safety alerts
        - Detailed analysis from each specialist
        - Prioritized action items with timelines
        - Monitoring and follow-up protocols
        - Patient education recommendations
        - Provider notification requirements
        
        Use urgency indicators throughout:
        CRITICAL - Immediate action required (within 2 hours)
        CAUTION - Action needed within 24 hours
        ROUTINE - Include in routine care and monitoring
        
        Provide a comprehensive safety assessment with all findings and actionable recommendations.
        """

        try:
            print(f"Running medication safety team for patient case")
            
            print(self.medication_safety_team)
            response_stream: Iterator[RunResponse] = self.medication_safety_team.run(prompt)
            content = ""
            for response in response_stream:
                content += response.content
            pprint_run_response(response, markdown=True)
            print("Medication safety team review completed successfully.")
            return content
        except Exception as e:
            print(f"Error running medication safety team: {e}")
            return f"# Error: {e}"

    def run_medication_safety_agent(self, patient_case: str) -> str:
        """
        Wrapper method (like run_marketing_agent)
        """
        return self.review_medication_safety(patient_case)
    
    def get_response(self, patient_case: str) -> str:
        """
        Main interface method following the marketing agent pattern exactly
        """
        response = self.run_medication_safety_agent(patient_case)
        return response
