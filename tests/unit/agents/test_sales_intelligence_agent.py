"""
Test file for Sales Intelligence Agent
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agents.sales_intelligence_agent import SalesIntelligenceAgent
from app.agents.enum.agent_enum import AgentType


class TestSalesIntelligenceAgent:
    
    def setup_method(self):
        """Setup test fixtures"""
        with patch('app.agents.sales_intelligence_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_sales_storage.db"
            self.agent = SalesIntelligenceAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        assert self.agent is not None
        assert hasattr(self.agent, 'sales_intelligence_team')
        assert hasattr(self.agent, 'search_tool')
    
    @patch('app.agents.sales_intelligence_agent.Claude')
    def test_profile_intelligence_agent_creation(self, mock_claude):
        """Test profile intelligence agent is created with correct configuration"""
        profile_agent = self.agent.create_profile_intelligence_agent()
        
        assert profile_agent is not None
        assert profile_agent.name == "Profile Intelligence Agent"
        assert "LinkedIn profiles" in profile_agent.role
        assert profile_agent.model.max_tokens == 6000
    
    @patch('app.agents.sales_intelligence_agent.Claude')
    def test_company_research_agent_creation(self, mock_claude):
        """Test company research agent is created correctly"""
        company_agent = self.agent.create_company_research_agent()
        
        assert company_agent is not None
        assert company_agent.name == "Company Research Agent"
        assert "company analysis" in company_agent.role
        assert company_agent.model.max_tokens == 6000
    
    @patch('app.agents.sales_intelligence_agent.Claude')
    def test_sales_insight_agent_creation(self, mock_claude):
        """Test sales insight agent is created correctly"""
        insight_agent = self.agent.create_sales_insight_agent()
        
        assert insight_agent is not None
        assert insight_agent.name == "Sales Insight Agent"
        assert "actionable sales intelligence" in insight_agent.role
        assert insight_agent.model.max_tokens == 8000
    
    def test_parse_sales_input_linkedin_url(self):
        """Test parsing LinkedIn URL from input"""
        prompt = "Research https://linkedin.com/in/john-doe-cto for our sales team"
        parsed = self.agent._parse_sales_input(prompt)
        
        assert "linkedin.com/in/john-doe-cto" in parsed['linkedin_url']
        assert parsed['research_depth'] == 'standard'
    
    def test_parse_sales_input_email(self):
        """Test parsing email and company from input"""
        prompt = "Research john.doe@techcorp.com for outreach"
        parsed = self.agent._parse_sales_input(prompt)
        
        assert parsed['contact_info'] == "john.doe@techcorp.com"
        assert parsed['company'] == "Techcorp"
    
    def test_parse_sales_input_company_name(self):
        """Test parsing company name from input"""
        prompt = "Research TechCorp Inc for sales intelligence"
        parsed = self.agent._parse_sales_input(prompt)
        
        assert "TechCorp" in parsed['company']
    
    def test_parse_sales_input_prospect_name(self):
        """Test parsing prospect name from input"""
        prompt = "Research John Doe CTO at TechCorp"
        parsed = self.agent._parse_sales_input(prompt)
        
        assert parsed['prospect_name'] == "John Doe"
    
    def test_parse_sales_input_research_depth(self):
        """Test parsing research depth indicators"""
        # Quick research
        prompt_quick = "Quick research on TechCorp"
        parsed_quick = self.agent._parse_sales_input(prompt_quick)
        assert parsed_quick['research_depth'] == 'quick'
        
        # Deep research
        prompt_deep = "Deep dive research on John Doe"
        parsed_deep = self.agent._parse_sales_input(prompt_deep)
        assert parsed_deep['research_depth'] == 'deep'
        
        # Standard research (default)
        prompt_standard = "Research TechCorp"
        parsed_standard = self.agent._parse_sales_input(prompt_standard)
        assert parsed_standard['research_depth'] == 'standard'
    
    def test_extract_business_terms(self):
        """Test extraction of business terms for search"""
        prompt = "Research SaaS CEO at fintech startup"
        terms = self.agent._extract_business_terms(prompt)
        
        assert any(term in terms.lower() for term in ['saas', 'ceo', 'fintech'])
    
    @patch('app.tools.duckduckgo_search.FreeDrugSearchTool')
    def test_enhance_with_search_company(self, mock_search_tool):
        """Test search enhancement for company information"""
        # Mock search tool
        mock_search_instance = Mock()
        mock_search_instance.search_drug_info.return_value = "TechCorp: Leading SaaS company in enterprise solutions..."
        mock_search_tool.return_value = mock_search_instance
        
        # Create fresh agent with mocked search tool
        with patch('app.agents.sales_intelligence_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_storage.db"
            agent = SalesIntelligenceAgent()
            agent.search_tool = mock_search_instance
        
        # Test enhancement
        parsed_input = {'company': 'TechCorp', 'prospect_name': '', 'contact_info': ''}
        result = agent._enhance_with_search("Research TechCorp", parsed_input)
        
        # Should have attempted to search for company
        assert "TechCorp" in result
        mock_search_instance.search_drug_info.assert_called()
    
    @patch('app.tools.duckduckgo_search.FreeDrugSearchTool')
    def test_enhance_with_search_prospect(self, mock_search_tool):
        """Test search enhancement for prospect information"""
        mock_search_instance = Mock()
        mock_search_instance.search_drug_info.return_value = "John Doe: Experienced CTO with background in AI and machine learning..."
        
        with patch('app.agents.sales_intelligence_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_storage.db"
            agent = SalesIntelligenceAgent()
            agent.search_tool = mock_search_instance
        
        parsed_input = {'company': '', 'prospect_name': 'John Doe', 'contact_info': ''}
        result = agent._enhance_with_search("Research John Doe", parsed_input)
        
        assert "John Doe" in result
        mock_search_instance.search_drug_info.assert_called()
    
    def test_enhance_output_with_assets(self):
        """Test enhancement of output with ready-to-use sales assets"""
        content = "# Sales Intelligence Report\n\nProfile analysis complete."
        parsed_input = {
            'prospect_name': 'John Doe',
            'company': 'TechCorp',
            'contact_info': 'john.doe@techcorp.com'
        }
        
        enhanced_content = self.agent._enhance_output_with_assets(content, parsed_input)
        
        # Check for sales assets sections
        assert "Ready-to-Use Sales Assets" in enhanced_content
        assert "Cold Email Template" in enhanced_content
        assert "LinkedIn Connection Message" in enhanced_content
        assert "Meeting Prep Brief" in enhanced_content
        assert "Follow-up Sequence" in enhanced_content
        
        # Check for personalization
        assert "John Doe" in enhanced_content
        assert "TechCorp" in enhanced_content
    
    @patch.object(SalesIntelligenceAgent, '_create_sales_intelligence_team')
    def test_get_response_basic_functionality(self, mock_team):
        """Test basic get_response functionality"""
        # Mock the team response
        mock_response = Mock()
        mock_response.content = """
        # Sales Intelligence Report
        
        ## Executive Summary
        High-value prospect with strong buying signals.
        
        ## Profile Intelligence
        CTO with 10+ years experience in enterprise software.
        
        ## Company Intelligence
        SaaS company, Series B, growing rapidly.
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        # Test with LinkedIn URL
        response = self.agent.get_response("https://linkedin.com/in/john-doe-cto")
        
        # Verify that the team was called
        mock_team.return_value.run.assert_called_once()
        assert "Sales Intelligence Report" in response
        assert "Executive Summary" in response
        assert "Ready-to-Use Sales Assets" in response  # Should be enhanced with assets
    
    @patch.object(SalesIntelligenceAgent, '_create_sales_intelligence_team')
    def test_get_response_with_company_info(self, mock_team):
        """Test response with company information"""
        mock_response = Mock()
        mock_response.content = "# Company Analysis\n\nTechCorp is a leading SaaS provider..."
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("Research TechCorp company")
        
        mock_team.return_value.run.assert_called_once()
        assert "Company Analysis" in response
    
    def test_error_handling_in_get_response(self):
        """Test error handling in get_response method"""
        # Mock the team to raise an exception
        with patch.object(self.agent, 'sales_intelligence_team') as mock_team:
            mock_team.run.side_effect = Exception("Test error")
            
            response = self.agent.get_response("test prompt")
            
            # Should return error message
            assert "Error in Sales Intelligence Analysis" in response
            assert "Test error" in response


class TestSalesIntelligenceAgentIntegration:
    """Integration tests for sales intelligence agent"""
    
    def test_agent_type_enum_exists(self):
        """Test that the agent type is properly defined"""
        assert hasattr(AgentType, 'SALES_INTELLIGENCE_AGENT')
        assert AgentType.SALES_INTELLIGENCE_AGENT.value == "lead-enrichment"
    
    def test_agent_factory_integration(self):
        """Test that the agent can be created through factory"""
        from app.agents.agent_factory import AgentFactory
        
        # This should not raise an exception
        agent = AgentFactory.get_agent(AgentType.SALES_INTELLIGENCE_AGENT)
        assert isinstance(agent, SalesIntelligenceAgent)
    
    def test_agent_prompt_repository_integration(self):
        """Test that the agent prompt is defined"""
        from app.agents.agent_prompt_repository import agent_prompt_repository
        
        prompt = agent_prompt_repository.get(AgentType.SALES_INTELLIGENCE_AGENT)
        assert prompt is not None
        assert "sales intelligence" in prompt.lower()
        assert "prospect" in prompt.lower()


# Example usage tests
class TestSalesIntelligenceAgentUsage:
    """Test real usage scenarios"""
    
    def setup_method(self):
        with patch('app.agents.sales_intelligence_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_sales_storage.db"
            self.agent = SalesIntelligenceAgent()
    
    @patch.object(SalesIntelligenceAgent, '_create_sales_intelligence_team')
    def test_linkedin_profile_research(self, mock_team):
        """Test LinkedIn profile research scenario"""
        mock_response = Mock()
        mock_response.content = """
        # Sales Intelligence Report
        
        ## Executive Summary
        - Prospect Score: 85/100
        - Timing Signals: High
        - Recommended Approach: Technical
        
        ## Profile Intelligence
        John Doe, CTO at TechCorp
        - 10+ years in enterprise software
        - Recently promoted to CTO (timing signal)
        - Active on LinkedIn discussing cloud migration
        
        ## Company Intelligence
        TechCorp - Series B SaaS company
        - Recently raised $50M Series B
        - Expanding engineering team (hiring signals)
        - Current tech stack: AWS, React, Node.js
        
        ## Sales Strategy
        - Lead with cloud optimization value prop
        - Reference recent funding for budget context
        - Mention mutual connection at previous company
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("https://linkedin.com/in/john-doe-cto")
        
        assert "Sales Intelligence Report" in response
        assert "Prospect Score: 85/100" in response
        assert "Technical" in response
        assert "Ready-to-Use Sales Assets" in response
    
    @patch.object(SalesIntelligenceAgent, '_create_sales_intelligence_team')
    def test_company_research_scenario(self, mock_team):
        """Test company research scenario"""
        mock_response = Mock()
        mock_response.content = """
        # Company Intelligence Brief
        
        ## Company Overview
        TechCorp - Enterprise SaaS Platform
        - 500+ employees, $50M ARR
        - Series B funded, growing 40% YoY
        
        ## Buying Signals
        - Recent CTO hire (new decision maker)
        - Engineering team expansion (30 new hires)
        - Cloud migration initiative announced
        
        ## Technology Stack
        - Current: Legacy on-premise infrastructure
        - Migrating to: AWS cloud platform
        - Development: React, Node.js, PostgreSQL
        
        ## Competitive Landscape
        - Current vendors: Salesforce, HubSpot
        - Recent churn: Zendesk (support ticket)
        - Evaluating: Slack alternatives
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("Deep company research on TechCorp")
        
        assert "Company Intelligence" in response
        assert "Buying Signals" in response
        assert "Technology Stack" in response
    
    @patch.object(SalesIntelligenceAgent, '_create_sales_intelligence_team')
    def test_mixed_input_scenario(self, mock_team):
        """Test mixed input with prospect and company info"""
        mock_response = Mock()
        mock_response.content = """
        # Comprehensive Sales Intelligence
        
        ## Target: Sarah Johnson, VP Engineering at DataFlow Inc
        
        ## Executive Summary
        - Prospect Score: 92/100 (Excellent fit)
        - Timing: Optimal (Q4 budget available)
        - Approach: Engineering efficiency focus
        
        ## Profile Insights
        - 12 years experience, recently joined DataFlow
        - Previously at Google, led platform team
        - Pain points: Legacy system scalability
        
        ## Company Context
        - DataFlow: Data analytics platform
        - 200 employees, post-Series A
        - Tech stack modernization underway
        
        ## Opportunity Assessment
        - Budget: $500K-1M estimated
        - Timeline: Q1 implementation target
        - Decision makers: Sarah (technical), CEO (budget)
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("Research Sarah Johnson VP Engineering at DataFlow Inc for Q4 outreach")
        
        assert "Comprehensive Sales Intelligence" in response
        assert "Prospect Score: 92/100" in response
        assert "Opportunity Assessment" in response


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
