from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
# from agno.models.google import Gemini
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.crawl4ai import Crawl4aiTools
from agno.storage.sqlite import SqliteStorage
from app.agents.base_agent import BaseAgent
from app.agents.agent_prompt_repository import agent_prompt_repository
from app.agents.enum.agent_enum import AgentType
from app.core.setting import settings
from app.tools.geo_intelligence_tools import FreeGeoIntelligenceTools, FreeHealthDataSources
import json
from datetime import datetime
from typing import Dict, List, Any, Iterator
from agno.utils.pprint import pprint_run_response


class LocationSpecificAgent(BaseAgent):
    """
    Location Specific Intelligence Medical Agent
    
    A comprehensive AI agent that provides real-time, location-specific medical intelligence
    with four specialized sub-agent capabilities:
    1. Geographic Context Analysis
    2. Epidemiological Intelligence Monitoring  
    3. Healthcare Resource Mapping
    4. Risk Assessment & Alert Generation
    """
    
    def __init__(self):
        self.AGENT_STORAGE = settings.AGENT_STORAGE
        
        # Initialize geo intelligence tools
        self.geo_tools = FreeGeoIntelligenceTools()
        self.health_sources = FreeHealthDataSources()
        
        # Create the main agent with sub-agent capabilities
        self.main_agent = self._create_main_agent()
        
        # Create specialized sub-agents
        self.geographic_sub_agent = self._create_geographic_sub_agent()
        self.epidemiological_sub_agent = self._create_epidemiological_sub_agent()
        self.healthcare_resource_sub_agent = self._create_healthcare_resource_sub_agent()
        self.risk_assessment_sub_agent = self._create_risk_assessment_sub_agent()
    
    def _create_main_agent(self):
        """Create the main location intelligence agent"""
        return Agent(
            name="Location Specific Intelligence Medical Agent",
            role="Master location intelligence coordinator with comprehensive health analysis capabilities",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                agent_prompt_repository[AgentType.LOCATION_HEALTH_INTELLIGENCE_AGENT],
                "You are the master Location Specific Intelligence Medical Agent",
                "Coordinate geographic, epidemiological, healthcare resource, and risk assessment analysis",
                "Provide comprehensive location-based health intelligence reports",
                "Use search tools to gather real-time health data and outbreak information",
                "Generate actionable recommendations for healthcare providers and patients",
                "Ensure all recommendations are evidence-based and location-specific",
                "Include emergency preparedness and response protocols",
                "Synthesize data from all sub-agent analyses into cohesive intelligence"
            ],
            tools=[
                GoogleSearchTools(fixed_max_results=10),
                Crawl4aiTools(max_length=8000)
            ],
            show_tool_calls=True,
            markdown=True,
            storage=SqliteStorage(table_name="location_specific_agent", db_file=self.AGENT_STORAGE),
            stream=True
        )
    
    def _create_geographic_sub_agent(self):
        """Create geographic context sub-agent"""
        return Agent(
            name="Geographic Context Sub-Agent",
            role="Geographic health intelligence specialist with real-time search capabilities",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                agent_prompt_repository[AgentType.GEOGRAPHIC_CONTEXT_AGENT],
                "Process location inputs and provide geographic health context",
                "Search for health jurisdiction information and administrative boundaries",
                "Validate coordinates and standardize location data",
                "Research demographic and population health data",
                "Provide structured geographic context for health analysis"
            ],
            tools=[
                GoogleSearchTools(fixed_max_results=5),
                Crawl4aiTools(max_length=5000)
            ],
            show_tool_calls=True,
            markdown=False,
            stream=False
        )
    
    def _create_epidemiological_sub_agent(self):
        """Create epidemiological intelligence sub-agent"""
        return Agent(
            name="Epidemiological Intelligence Sub-Agent", 
            role="Epidemiological intelligence analyst with real-time monitoring capabilities",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                agent_prompt_repository[AgentType.EPIDEMIOLOGICAL_INTELLIGENCE_AGENT],
                "Monitor disease patterns, outbreaks, and epidemiological trends by location",
                "Search CDC, WHO, and local health department outbreak reports",
                "Track antimicrobial resistance patterns and travel advisories", 
                "Analyze seasonal disease patterns and emerging threats",
                "Provide structured epidemiological intelligence data"
            ],
            tools=[
                GoogleSearchTools(fixed_max_results=10),
                Crawl4aiTools(max_length=8000)
            ],
            show_tool_calls=True,
            markdown=False,
            stream=False
        )
    
    def _create_healthcare_resource_sub_agent(self):
        """Create healthcare resource mapping sub-agent"""
        return Agent(
            name="Healthcare Resource Mapping Sub-Agent",
            role="Healthcare resource specialist with real-time facility monitoring capabilities",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                agent_prompt_repository[AgentType.HEALTHCARE_RESOURCE_MAPPING_AGENT],
                "Map healthcare resources, capacity, and accessibility by location",
                "Search for hospital capacity, emergency services, and specialist availability",
                "Research insurance acceptance and transportation options",
                "Assess facility quality ratings and current availability status",
                "Provide structured healthcare resource mapping data"
            ],
            tools=[
                GoogleSearchTools(fixed_max_results=12),
                Crawl4aiTools(max_length=6000)
            ],
            show_tool_calls=True,
            markdown=False,
            stream=False
        )
    
    def _create_risk_assessment_sub_agent(self):
        """Create risk assessment and alert sub-agent"""
        return Agent(
            name="Risk Assessment & Alert Sub-Agent",
            role="Public health risk assessment specialist with real-time advisory monitoring capabilities",
            model=Claude(
                id="claude-3-5-sonnet-latest",
                api_key=settings.ANTHROPIC_API_KEY,
            ),
            instructions=[
                agent_prompt_repository[AgentType.RISK_ASSESSMENT_ALERT_AGENT],
                "Synthesize location intelligence into actionable health alerts and recommendations",
                "Generate risk assessments based on geographic, epidemiological, and resource data",
                "Search for current health advisories and prevention guidelines",
                "Create emergency preparedness and response protocols",
                "Provide structured risk assessment and alert data"
            ],
            tools=[
                GoogleSearchTools(fixed_max_results=8),
                Crawl4aiTools(max_length=6000)
            ],
            show_tool_calls=True,
            markdown=False,
            stream=False
        )
    
    def analyze_location_health_intelligence(self, 
                                           location_input: str,
                                           patient_context: str = None,
                                           emergency_level: str = "routine",
                                           query_type: str = "comprehensive") -> str:
        """
        Comprehensive location health intelligence analysis using sub-agents
        
        Args:
            location_input: Location to analyze (address, coordinates, or region)
            patient_context: Optional patient demographics or medical context
            emergency_level: routine/urgent/emergency
            query_type: comprehensive/outbreak_monitoring/travel_advisory/resource_mapping
            
        Returns:
            Comprehensive health intelligence report
        """
        try:
            print(f"Starting Location Specific Intelligence Analysis for: {location_input}")
            print(f"Emergency level: {emergency_level}, Query type: {query_type}")
            
            # Step 1: Geographic Context Analysis (Sub-Agent)
            print("\n=== STEP 1: Geographic Context Analysis (Sub-Agent) ===")
            geographic_data = self._run_geographic_analysis(location_input, patient_context)
            print("Geographic analysis completed")
            
            # Step 2: Epidemiological Intelligence Monitoring (Sub-Agent)
            print("\n=== STEP 2: Epidemiological Intelligence Monitoring (Sub-Agent) ===")
            epidemiological_data = self._run_epidemiological_analysis(
                geographic_data, query_type, patient_context
            )
            print("Epidemiological monitoring completed")
            
            # Step 3: Healthcare Resource Mapping (Sub-Agent)
            print("\n=== STEP 3: Healthcare Resource Mapping (Sub-Agent) ===")
            healthcare_resources = self._run_healthcare_resource_analysis(
                geographic_data, patient_context, emergency_level
            )
            print("Healthcare resource mapping completed")
            
            # Step 4: Risk Assessment and Alert Generation (Sub-Agent)
            print("\n=== STEP 4: Risk Assessment and Alert Generation (Sub-Agent) ===")
            risk_assessment = self._run_risk_assessment_analysis(
                geographic_data, epidemiological_data, healthcare_resources, patient_context
            )
            print("Risk assessment completed")
            
            # Step 5: Master Synthesis and Final Report Generation (Main Agent)
            print("\n=== STEP 5: Master Synthesis and Report Generation (Main Agent) ===")
            final_report = self._generate_comprehensive_report(
                location_input, patient_context, emergency_level, query_type,
                geographic_data, epidemiological_data, healthcare_resources, risk_assessment
            )
            
            print("Location Specific Intelligence Analysis completed successfully.")
            return final_report
            
        except Exception as e:
            print(f"Error in location intelligence analysis: {e}")
            return self._create_error_report(location_input, str(e))
    
    def _run_geographic_analysis(self, location_input: str, patient_context: str) -> Dict[str, Any]:
        """Run geographic context analysis using sub-agent and tools"""
        try:
            # First, use geo tools for basic location processing
            basic_geo_data = self.geo_tools.geocode_location(location_input)
            
            # Enhanced analysis using geographic sub-agent
            geo_prompt = f"""
            Enhance the following basic geographic data with comprehensive health context:
            
            Location Input: {location_input}
            Patient Context: {patient_context or "General population"}
            
            Basic Geographic Data:
            {json.dumps(basic_geo_data, indent=2)}
            
            Please provide enhanced geographic health context including:
            1. Health jurisdiction information and contacts
            2. Administrative boundaries and health authorities
            3. Demographic and population health data
            4. Any special health administrative considerations
            
            Format response as structured data for further analysis.
            """
            
            response: RunResponse = self.geographic_sub_agent.run(geo_prompt)
            
            # Combine basic geo data with enhanced analysis
            enhanced_geo_data = {
                **basic_geo_data,
                'enhanced_analysis': response.content,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return enhanced_geo_data
            
        except Exception as e:
            print(f"Error in geographic analysis: {e}")
            return {'error': str(e), 'basic_data': basic_geo_data if 'basic_geo_data' in locals() else {}}
    
    def _run_epidemiological_analysis(self, geographic_data: Dict, query_type: str, 
                                     patient_context: str) -> Dict[str, Any]:
        """Run epidemiological intelligence analysis using sub-agent and tools"""
        try:
            # Get basic outbreak data from tools
            basic_outbreak_data = self.health_sources.get_cdc_outbreak_data(geographic_data)
            basic_who_alerts = self.health_sources.get_who_health_alerts(geographic_data)
            
            # Enhanced analysis using epidemiological sub-agent
            epi_prompt = f"""
            Conduct comprehensive epidemiological intelligence analysis:
            
            Geographic Context: {json.dumps(geographic_data.get('administrative_levels', {}), indent=2)}
            Query Type: {query_type}
            Patient Context: {patient_context or "General population"}
            
            Basic Data Available:
            - CDC Outbreak Data: {len(basic_outbreak_data)} items
            - WHO Health Alerts: {len(basic_who_alerts)} items
            
            Provide comprehensive epidemiological intelligence including:
            1. Current outbreak monitoring and assessment
            2. Endemic disease risks and seasonal patterns
            3. Travel health advisories and requirements
            4. Antimicrobial resistance patterns
            5. Surveillance data and trends
            
            Format response as structured intelligence data.
            """
            
            response: RunResponse = self.epidemiological_sub_agent.run(epi_prompt)
            
            # Combine basic data with enhanced analysis
            enhanced_epi_data = {
                'basic_outbreak_data': basic_outbreak_data,
                'basic_who_alerts': basic_who_alerts,
                'enhanced_analysis': response.content,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return enhanced_epi_data
            
        except Exception as e:
            print(f"Error in epidemiological analysis: {e}")
            return {'error': str(e), 'basic_data': {'outbreaks': basic_outbreak_data if 'basic_outbreak_data' in locals() else []}}
    
    def _run_healthcare_resource_analysis(self, geographic_data: Dict, patient_context: str,
                                         emergency_level: str) -> Dict[str, Any]:
        """Run healthcare resource mapping analysis using sub-agent"""
        try:
            resource_prompt = f"""
            Map comprehensive healthcare resources for the location:
            
            Geographic Context: {json.dumps(geographic_data.get('administrative_levels', {}), indent=2)}
            Patient Context: {patient_context or "General care needs"}
            Emergency Level: {emergency_level}
            
            Provide comprehensive healthcare resource mapping including:
            1. Emergency services and hospital capacity
            2. Primary care and specialist availability
            3. Urgent care and walk-in clinic options
            4. Insurance coverage and payment options
            5. Transportation and accessibility factors
            6. Quality ratings and facility recommendations
            
            Prioritize based on emergency level and patient needs.
            Format response as structured resource data.
            """
            
            response: RunResponse = self.healthcare_resource_sub_agent.run(resource_prompt)
            
            # Calculate distances if coordinates available
            coordinates = geographic_data.get('coordinates', {})
            if coordinates and coordinates.get('latitude') and coordinates.get('longitude'):
                center_point = (coordinates['latitude'], coordinates['longitude'])
                # Add distance calculation context
                resource_data = {
                    'resource_analysis': response.content,
                    'center_coordinates': center_point,
                    'distance_calculation_available': True,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            else:
                resource_data = {
                    'resource_analysis': response.content,
                    'distance_calculation_available': False,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            
            return resource_data
            
        except Exception as e:
            print(f"Error in healthcare resource analysis: {e}")
            return {'error': str(e)}
    
    def _run_risk_assessment_analysis(self, geographic_data: Dict, epidemiological_data: Dict,
                                    healthcare_resources: Dict, patient_context: str) -> Dict[str, Any]:
        """Run risk assessment and alert generation using sub-agent"""
        try:
            # Safely extract data for risk assessment
            admin_levels = geographic_data.get('administrative_levels', {})
            outbreak_count = len(epidemiological_data.get('basic_outbreak_data', []))
            who_alert_count = len(epidemiological_data.get('basic_who_alerts', []))
            epi_analysis = epidemiological_data.get('enhanced_analysis', 'No detailed analysis')
            resource_analysis = healthcare_resources.get('resource_analysis', 'Limited resource data')
            
            risk_prompt = f"""
            Generate comprehensive risk assessment and health alerts:
            
            GEOGRAPHIC CONTEXT:
            {json.dumps(admin_levels, indent=2)}
            
            EPIDEMIOLOGICAL INTELLIGENCE:
            Basic Outbreaks: {outbreak_count}
            WHO Alerts: {who_alert_count}
            Analysis: {epi_analysis[:500]}...
            
            HEALTHCARE RESOURCES:
            {resource_analysis[:500]}...
            
            PATIENT CONTEXT: {patient_context or "General population"}
            
            Provide comprehensive risk assessment including:
            1. Overall risk level assessment (low/moderate/high/critical)
            2. Primary health risks and threats identification
            3. Immediate and long-term recommendations
            4. Preventive measures and interventions
            5. Emergency preparedness and contact information
            6. Monitoring alerts and escalation protocols
            
            Base assessment on current data and provide actionable recommendations.
            Format response as structured risk assessment data.
            """
            
            response: RunResponse = self.risk_assessment_sub_agent.run(risk_prompt)
            
            risk_data = {
                'risk_assessment': response.content,
                'assessment_timestamp': datetime.now().isoformat(),
                'data_sources': ['geographic', 'epidemiological', 'healthcare_resources']
            }
            
            return risk_data
            
        except Exception as e:
            print(f"Error in risk assessment analysis: {e}")
            return {'error': str(e)}
    
    def _generate_comprehensive_report(self, location_input: str, patient_context: str,
                                     emergency_level: str, query_type: str,
                                     geographic_data: Dict, epidemiological_data: Dict,
                                     healthcare_resources: Dict, risk_assessment: Dict) -> str:
        """Generate final comprehensive report using main agent"""
        try:
            synthesis_prompt = f"""
            Generate a comprehensive Location Specific Intelligence Medical Report:
            
            QUERY CONTEXT:
            Location: {location_input}
            Patient Context: {patient_context or "General population"}
            Emergency Level: {emergency_level}
            Query Type: {query_type}
            Analysis Timestamp: {datetime.now().isoformat()}
            
            SUB-AGENT ANALYSIS RESULTS:
            
            1. GEOGRAPHIC INTELLIGENCE:
            {json.dumps(geographic_data, indent=2)}
            
            2. EPIDEMIOLOGICAL INTELLIGENCE:
            {json.dumps(epidemiological_data, indent=2)}
            
            3. HEALTHCARE RESOURCE MAPPING:
            {json.dumps(healthcare_resources, indent=2)}
            
            4. RISK ASSESSMENT:
            {json.dumps(risk_assessment, indent=2)}
            
            Generate a comprehensive, actionable health intelligence report with:
            
            # Location Specific Intelligence Medical Report
            
            ## Executive Summary
            - Overall situation assessment
            - Key findings and immediate actions
            - Critical contact information
            
            ## Geographic Health Context
            - Location details and jurisdiction
            - Demographics and population factors
            - Administrative health contacts
            
            ## Current Health Situation
            - Disease surveillance and outbreaks
            - Health alerts and advisories
            - Seasonal and endemic risks
            
            ## Healthcare Resources
            - Emergency and urgent care availability
            - Specialist and primary care options
            - Capacity, quality, and accessibility
            
            ## Risk Assessment & Recommendations
            - Detailed risk analysis and levels
            - Immediate and preventive actions
            - Monitoring and escalation protocols
            
            ## Emergency Preparedness
            - Emergency contacts and procedures
            - Facility recommendations by urgency
            - Transportation and backup plans
            
            ## Data Quality & Next Steps
            - Analysis confidence and limitations
            - Recommended follow-up actions
            - Update schedule and monitoring
            
            FORMATTING: Use clear markdown, highlight critical info, provide specific actionable steps.
            """
            
            # Generate comprehensive report using main agent
            response_stream: Iterator[RunResponse] = self.main_agent.run(synthesis_prompt)
            
            # Collect the streaming response
            final_content = ""
            final_response = None
            for response in response_stream:
                final_content += response.content
                final_response = response
            
            # Print the final response for debugging
            if final_response:
                pprint_run_response(final_response, markdown=True)
            
            return final_content
            
        except Exception as e:
            return self._create_error_report(location_input, f"Report generation error: {str(e)}")
    
    def _create_error_report(self, location_input: str, error_msg: str) -> str:
        """Create error report when analysis fails"""
        return f"""
        # Location Specific Intelligence Medical Report - Error
        
        **Location:** {location_input}
        **Analysis Time:** {datetime.now().isoformat()}
        **Status:** Error
        
        ## Error Summary
        
        An error occurred during the location intelligence analysis:
        
        ```
        {error_msg}
        ```
        
        ## Recommended Actions
        
        1. **Immediate:** Contact local health authorities directly
        2. **Emergency Services:** Call 911 for any health emergencies
        3. **Health Information:** Contact local health department
        4. **Poison Control:** 1-800-222-1222
        
        ## Manual Resources
        
        - Local health department website
        - CDC website (cdc.gov)
        - WHO website (who.int)
        - State health department resources
        
        Please retry the analysis or consult healthcare providers directly for urgent needs.
        """
    
    def get_response(self, query: str) -> str:
        """
        BaseAgent interface implementation
        
        Args:
            query: Can be simple location string or JSON with detailed parameters
            
        Returns:
            Comprehensive location health intelligence report
        """
        try:
            # Try to parse as JSON for detailed parameters
            if query.strip().startswith('{'):
                query_data = json.loads(query)
                location_input = query_data.get('location', '')
                patient_context = query_data.get('patient_context')
                emergency_level = query_data.get('emergency_level', 'routine')
                query_type = query_data.get('query_type', 'comprehensive')
            else:
                # Treat as simple location string
                location_input = query
                patient_context = None
                emergency_level = 'routine'
                query_type = 'comprehensive'
            
            if not location_input:
                return "Error: No location provided for analysis"
            
            return self.analyze_location_health_intelligence(
                location_input, patient_context, emergency_level, query_type
            )
            
        except Exception as e:
            return self._create_error_report(query, str(e))
    
    def run_location_intelligence(self, location: str, patient_context: str = None,
                                emergency_level: str = "routine") -> str:
        """
        Convenience method for running location intelligence analysis
        
        Args:
            location: Location to analyze
            patient_context: Optional patient information
            emergency_level: routine/urgent/emergency
            
        Returns:
            Comprehensive health intelligence report
        """
        return self.analyze_location_health_intelligence(
            location, patient_context, emergency_level, "comprehensive"
        )
