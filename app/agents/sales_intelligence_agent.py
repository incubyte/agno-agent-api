"""
Sales Intelligence Agent - Complete Implementation
Empower BDRs with precise prospect and company insights for smarter outreach
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


class SalesIntelligenceAgent(BaseAgent):
    """
    Sales Intelligence Agent for BDR prospect and company research
    Optimized for speed with comprehensive search capabilities and ready-to-use sales assets
    """
    
    def __init__(self):
        try:
            self.AGENT_STORAGE = settings.AGENT_STORAGE
        except Exception as e:
            logger.warning(f"Settings error: {e}. Using default storage.")
            self.AGENT_STORAGE = "./default_agent_storage.db"
        
        # Initialize search tool for enhanced research
        try:
            self.search_tool = FreeDrugSearchTool(max_results=5)
        except Exception as e:
            logger.warning(f"Search tool initialization failed: {e}. Search will be disabled.")
            self.search_tool = None
        
        self.sales_intelligence_team = self._create_sales_intelligence_team()
        logger.info("Sales Intelligence Agent initialized successfully")

    def create_profile_intelligence_agent(self):
        return Agent(
            name="Profile Intelligence Agent",
            role="Expert at analyzing LinkedIn profiles and extracting professional insights for sales outreach",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=6000),
            instructions=[
                "Analyze LinkedIn profiles and extract key professional information for sales intelligence",
                "Identify current role, responsibilities, seniority level, and decision-making authority",
                "Extract education background, skills, certifications, and professional experience timeline",
                "Identify recent career changes, promotions, or job transitions as timing signals",
                "Note recent activity, posts, and engagement patterns to understand interests and pain points",
                "Extract contact information when publicly available (email patterns, social handles)",
                "Identify mutual connections and shared experiences for warm introduction opportunities",
                "Generate personality insights and communication style preferences from profile content",
                "Identify potential pain points based on role, industry, and recent professional activities",
                "Create personalization opportunities from interests, achievements, and professional background",
                "Output format: Profile Score (0-100) | Role Details | Background | Pain Points | Personalization Hooks",
                "Focus on information that enables highly personalized, relevant outreach with strong connection potential",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def create_company_research_agent(self):
        return Agent(
            name="Company Research Agent", 
            role="Expert at comprehensive company analysis and business intelligence for strategic sales approach",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=6000),
            instructions=[
                "Research comprehensive company background, size, revenue, and organizational structure",
                "Analyze industry positioning, market dynamics, competitive landscape, and differentiation",
                "Identify recent company news, funding rounds, acquisitions, and growth signals indicating budget/timing",
                "Extract technology stack, tools, infrastructure, and current vendor relationships",
                "Analyze company culture, values, hiring patterns, and expansion signals",
                "Identify potential business challenges, growth opportunities, and transformation initiatives",
                "Research recent press releases, earnings calls, and executive announcements for strategic insights",
                "Detect buying signals: hiring surges, new locations, product launches, competitive losses",
                "Analyze decision-making structure, budget cycles, and procurement processes",
                "Identify strategic initiatives, digital transformation efforts, and technology modernization plans",
                "Generate company intelligence score (0-100) with opportunity assessment and timing indicators",
                "Output format: Company Score | Business Context | Recent Developments | Tech Stack | Buying Signals | Opportunities",
                "Focus on intelligence that reveals immediate sales timing, budget availability, and strategic pain points",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def create_sales_insight_agent(self):
        return Agent(
            name="Sales Insight Agent",
            role="Expert at synthesizing research into actionable sales intelligence with ready-to-use assets",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8000),
            instructions=[
                "Synthesize profile and company data into comprehensive, actionable sales intelligence",
                "Generate overall prospect qualification score (0-100) with detailed scoring rationale",
                "Identify specific pain points, timing signals, and buying intent indicators",
                "Create personalized value propositions tailored to discovered needs and challenges",
                "Generate ready-to-use email templates: cold outreach, LinkedIn connection, follow-up sequences",
                "Develop conversation starters, meeting talking points, and objection handling strategies",
                "Identify optimal outreach timing, communication channels, and message sequencing",
                "Map multi-stakeholder buying committee and influence network",
                "Create competitive intelligence briefs and differentiation strategies",
                "Generate meeting preparation briefs with key topics, questions, and success stories to share",
                "Predict deal size, sales cycle length, and closure probability based on company profile",
                "Suggest follow-up strategies, nurturing campaigns, and relationship building approaches",
                "Create social proof elements: mutual connections, shared experiences, industry credibility",
                "Generate risk assessment: potential objections, competitive threats, decision delays",
                "Output format: Intelligence Summary | Qualification Score | Pain Points | Timing | Assets | Strategy",
                "Focus on immediately actionable intelligence that accelerates deal progression and relationship building",
            ],
            show_tool_calls=True,
            tools=[ReasoningTools()],
            stream=True,
            markdown=True,
        )

    def _create_sales_intelligence_team(self):
        return Agent(
            name="Sales Intelligence Team",
            team=[
                self.create_profile_intelligence_agent(),
                self.create_company_research_agent(),
                self.create_sales_insight_agent()
            ],
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=12000),
            instructions=[
                "You are a specialized sales intelligence team focused on comprehensive prospect and company research.",
                "Work together to transform basic prospect information into actionable sales intelligence.",
                "Follow this optimized workflow:",
                "1. Profile Intelligence: Deep LinkedIn analysis and professional background research",
                "2. Company Research: Comprehensive business intelligence and opportunity assessment", 
                "3. Sales Insight: Synthesis into actionable strategy with ready-to-use assets",
                "",
                "Intelligence Priorities:",
                "- Prospect qualification and scoring with clear rationale",
                "- Timing signals and buying intent indicators",
                "- Personalization opportunities and connection points",
                "- Ready-to-use sales assets: emails, talking points, strategies",
                "- Competitive intelligence and differentiation opportunities",
                "",
                "Output Structure:",
                "1. Executive Summary with prospect score and recommended approach",
                "2. Profile Intelligence with role details and personalization hooks",
                "3. Company Intelligence with business context and buying signals",
                "4. Sales Strategy with value propositions and timing recommendations",
                "5. Ready-to-Use Assets: email templates, talking points, meeting prep",
                "6. Implementation Plan with specific next steps and timeline",
                "7. Risk Assessment and competitive considerations",
                "",
                "Quality Standards:",
                "- Focus on actionable insights over generic information",
                "- Provide specific, personalized recommendations",
                "- Include confidence levels and information sources",
                "- Prioritize insights that directly impact sales success",
            ],
            show_tool_calls=True,
            markdown=True,
            storage=SqliteStorage(table_name="sales_intelligence_team", db_file=self.AGENT_STORAGE),
            stream=True,
        )

    def get_response(self, prompt: str) -> str:
        """
        Main interface method for sales intelligence research
        Supports multiple input formats: LinkedIn URLs, prospect names, company info, mixed inputs
        """
        logger.info(f"Processing sales intelligence request: {prompt[:100]}...")
        
        # Parse and enhance input
        parsed_input = self._parse_sales_input(prompt)
        enhanced_info = self._enhance_with_search(prompt, parsed_input)
        
        # Create comprehensive research prompt
        research_prompt = f"""
        Conduct comprehensive sales intelligence research for BDR outreach optimization.
        
        TARGET PROSPECT INFORMATION:
        {prompt}
        
        PARSED INPUT ANALYSIS:
        - LinkedIn URL: {parsed_input.get('linkedin_url', 'Not provided')}
        - Prospect Name: {parsed_input.get('prospect_name', 'Not provided')}
        - Company: {parsed_input.get('company', 'Not provided')}
        - Email/Contact: {parsed_input.get('contact_info', 'Not provided')}
        - Research Depth: {parsed_input.get('research_depth', 'standard')}
        
        ENHANCED SEARCH INTELLIGENCE:
        {enhanced_info}
        
        RESEARCH OBJECTIVES:
        1. Complete prospect profile with role analysis and background
        2. Comprehensive company intelligence with business context
        3. Sales qualification scoring and opportunity assessment
        4. Personalized outreach strategy with ready-to-use assets
        5. Timing analysis and buying signal identification
        6. Competitive intelligence and differentiation opportunities
        
        DELIVERABLES REQUIRED:
        - Executive Summary with qualification score and approach recommendation
        - Profile Intelligence with personalization opportunities
        - Company Intelligence with buying signals and business context
        - Sales Strategy with value propositions and timing recommendations
        - Ready-to-Use Assets: email templates, LinkedIn messages, talking points
        - Implementation Plan with specific next steps and success metrics
        
        Focus on generating immediately actionable intelligence that enables highly effective, personalized outreach.
        """

        try:
            response_stream: Iterator[RunResponse] = self.sales_intelligence_team.run(research_prompt)
            content = ""
            for response in response_stream:
                content += response.content
            
            # Add ready-to-use assets section
            content = self._enhance_output_with_assets(content, parsed_input)
            
            logger.info("Sales intelligence analysis completed successfully")
            return content
            
        except Exception as e:
            logger.error(f"Error in sales intelligence analysis: {e}")
            return f"# Error in Sales Intelligence Analysis\n\n{str(e)}\n\nPlease try again with prospect information (LinkedIn URL, name, or company)."

    def _parse_sales_input(self, prompt: str) -> Dict[str, str]:
        """Parse input to extract LinkedIn URLs, prospect names, company info, etc."""
        parsed = {
            'linkedin_url': '',
            'prospect_name': '',
            'company': '',
            'contact_info': '',
            'research_depth': 'standard'
        }
        
        # Extract LinkedIn URL
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, prompt)
        if linkedin_match:
            parsed['linkedin_url'] = linkedin_match.group(0)
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, prompt)
        if email_match:
            parsed['contact_info'] = email_match.group(0)
            # Extract company from email domain
            domain = email_match.group(0).split('@')[1]
            parsed['company'] = domain.split('.')[0].title()
        
        # Extract company mentions
        company_patterns = [
            r'(?:company|at|works at|@)[\s:]*([A-Za-z0-9\s&.-]+)(?:\s|,|$)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Inc|Corp|LLC|Ltd|Company)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match and not parsed['company']:
                parsed['company'] = match.group(1).strip()
                break
        
        # Extract prospect name (simple heuristic)
        if not parsed['prospect_name'] and not parsed['linkedin_url']:
            # Look for name patterns: "John Doe" or "John Doe CTO"
            name_pattern = r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b'
            name_match = re.search(name_pattern, prompt)
            if name_match:
                parsed['prospect_name'] = name_match.group(1)
        
        # Determine research depth
        if any(word in prompt.lower() for word in ['quick', 'brief', 'summary']):
            parsed['research_depth'] = 'quick'
        elif any(word in prompt.lower() for word in ['deep', 'comprehensive', 'detailed', 'thorough']):
            parsed['research_depth'] = 'deep'
        
        return parsed

    def _enhance_with_search(self, prompt: str, parsed_input: Dict[str, str]) -> str:
        """Enhance research with additional search intelligence"""
        if self.search_tool is None:
            return "External search enhancement unavailable."
            
        try:
            search_results = []
            
            # Search for company information if available
            if parsed_input.get('company'):
                company = parsed_input['company']
                logger.info(f"Searching for company information: {company}")
                company_info = self.search_tool.search_drug_info(f"{company} company business")
                search_results.append(f"Company Research for '{company}': {company_info[:400]}...")
            
            # Search for prospect if name is available
            if parsed_input.get('prospect_name'):
                prospect = parsed_input['prospect_name']
                logger.info(f"Searching for prospect information: {prospect}")
                prospect_info = self.search_tool.search_drug_info(f"{prospect} professional background")
                search_results.append(f"Prospect Research for '{prospect}': {prospect_info[:400]}...")
            
            # General industry/market search if specific info not available
            if not search_results:
                general_terms = self._extract_business_terms(prompt)
                if general_terms:
                    logger.info(f"Searching for general business intelligence: {general_terms[:50]}")
                    general_info = self.search_tool.search_drug_info(general_terms)
                    search_results.append(f"General Business Intelligence: {general_info[:300]}...")
            
            return "\\n\\n".join(search_results) if search_results else "No additional search performed."
            
        except Exception as e:
            logger.warning(f"Search enhancement failed: {e}")
            return "Search enhancement unavailable due to technical limitations."

    def _extract_business_terms(self, prompt: str) -> str:
        """Extract business-relevant terms for general search"""
        # Common business/industry terms
        business_terms = []
        words = prompt.lower().split()
        
        # Industry terms
        industries = ['saas', 'software', 'technology', 'fintech', 'healthcare', 'manufacturing', 'retail', 'consulting']
        for industry in industries:
            if industry in prompt.lower():
                business_terms.append(industry)
        
        # Role terms  
        roles = ['ceo', 'cto', 'vp', 'director', 'manager', 'engineer', 'developer', 'sales']
        for role in roles:
            if role in prompt.lower():
                business_terms.append(role)
        
        return ' '.join(business_terms[:3])  # Limit to avoid overly broad search

    def _enhance_output_with_assets(self, content: str, parsed_input: Dict[str, str]) -> str:
        """Add ready-to-use sales assets to the output"""
        
        # Extract key info for asset generation
        prospect_name = parsed_input.get('prospect_name', '[Prospect Name]')
        company = parsed_input.get('company', '[Company]')
        
        assets_section = f"""

## 📧 Ready-to-Use Sales Assets

### Cold Email Template
```
Subject: Quick question about {company}'s [relevant challenge]

Hi {prospect_name},

I noticed [specific observation about their company/role]. 

[Personalized insight or mutual connection]

I've helped similar [industry] companies achieve [specific outcome] - thought you might find it interesting.

Worth a brief chat this week?

Best,
[Your Name]
```

### LinkedIn Connection Message
```
Hi {prospect_name}, saw your recent post about [topic]. Would love to connect and share some insights about [relevant area] that might interest you given your work at {company}.
```

### Meeting Prep Brief
- **Opening**: Reference [specific company news/achievement]
- **Pain Point Focus**: [Industry-specific challenges]
- **Value Proposition**: [Tailored solution benefits]
- **Questions to Ask**: [Discovery questions based on research]
- **Success Story**: [Relevant case study to share]

### Follow-up Sequence
- **Day 1**: Initial outreach
- **Day 4**: Value-add follow-up with industry insight
- **Day 10**: Social media engagement + soft follow-up
- **Day 20**: Final attempt with different angle

"""
        
        return content + assets_section
