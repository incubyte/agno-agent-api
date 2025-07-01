import pytest
from unittest.mock import Mock, patch
from app.agents.marketing_copywriter_agent import MarketingCopywriterAgent


class TestMarketingCopywriterAgent:
    """Test cases for Marketing Copywriter Agent"""
    
    def test_initialization(self):
        """Test that the agent initializes correctly"""
        agent = MarketingCopywriterAgent()
        assert agent is not None
        assert agent.copywriter_team is not None
        assert hasattr(agent, 'AGENT_STORAGE')
    
    def test_create_audience_strategy_agent(self):
        """Test creation of audience strategy sub-agent"""
        agent = MarketingCopywriterAgent()
        audience_agent = agent.create_audience_strategy_agent()
        
        assert audience_agent is not None
        assert audience_agent.name == "Audience Strategy Agent"
        assert "audience analysis" in audience_agent.role.lower()
        assert len(audience_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    def test_create_copy_creation_agent(self):
        """Test creation of copy creation sub-agent"""
        agent = MarketingCopywriterAgent()
        copy_agent = agent.create_copy_creation_agent()
        
        assert copy_agent is not None
        assert copy_agent.name == "Copy Creation Agent"
        assert "marketing copy" in copy_agent.role.lower()
        assert len(copy_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
        assert copy_agent.model.max_tokens == 8000  # Higher token limit for copy
    
    def test_create_conversion_optimizer_agent(self):
        """Test creation of conversion optimizer sub-agent"""
        agent = MarketingCopywriterAgent()
        conversion_agent = agent.create_conversion_optimizer_agent()
        
        assert conversion_agent is not None
        assert conversion_agent.name == "Conversion Optimizer Agent"
        assert "conversion rate optimization" in conversion_agent.role.lower()
        assert len(conversion_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    @patch('app.agents.marketing_copywriter_agent.pprint_run_response')
    def test_get_response_with_url(self, mock_pprint):
        """Test get_response method with URL input"""
        agent = MarketingCopywriterAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Marketing Copy Strategy\nTest copywriting content"
        agent.copywriter_team.run = Mock(return_value=[mock_response])
        
        test_url = "https://example.com"
        response = agent.get_response(test_url)
        
        assert response is not None
        assert "Marketing Copy Strategy" in response
        agent.copywriter_team.run.assert_called_once()
    
    @patch('app.agents.marketing_copywriter_agent.pprint_run_response')
    def test_get_response_with_audience_info(self, mock_pprint):
        """Test get_response method with URL and audience information"""
        agent = MarketingCopywriterAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Targeted Copy Strategy\nAudience-specific content"
        agent.copywriter_team.run = Mock(return_value=[mock_response])
        
        test_prompt = "https://example.com audience: tech startups, SaaS companies"
        response = agent.get_response(test_prompt)
        
        assert response is not None
        assert "Targeted Copy Strategy" in response
        agent.copywriter_team.run.assert_called_once()
    
    @patch('app.agents.marketing_copywriter_agent.pprint_run_response')
    def test_create_marketing_copy_error_handling(self, mock_pprint):
        """Test error handling in create_marketing_copy method"""
        agent = MarketingCopywriterAgent()
        
        # Mock the agent team to raise an exception
        agent.copywriter_team.run = Mock(side_effect=Exception("Copy creation error"))
        
        response = agent.create_marketing_copy("https://example.com")
        
        assert "Marketing Copy Creation Error" in response
        assert "Copy creation error" in response
    
    def test_agent_team_configuration(self):
        """Test that the agent team is configured correctly"""
        agent = MarketingCopywriterAgent()
        team = agent.copywriter_team
        
        assert team is not None
        assert team.name == "Marketing Copywriter Team"
        assert len(team.team) == 3  # Audience, Copy, Conversion agents
        assert team.model.id == "claude-3-7-sonnet-20250219"
        assert team.model.max_tokens == 12000
        
    def test_audience_and_goals_extraction_from_prompt(self):
        """Test audience and goals extraction from various prompt formats"""
        agent = MarketingCopywriterAgent()
        
        # Mock the create_marketing_copy method to capture parameters
        agent.create_marketing_copy = Mock(return_value="Mocked response")
        
        # Test various prompt formats
        test_cases = [
            ("https://example.com audience: tech startups goals: increase conversions", "tech startups", "increase conversions"),
            ("https://example.com target: small businesses", "small businesses", ""),
            ("https://example.com goals: lead generation", "", "lead generation"),
            ("https://example.com", "", "")  # No audience or goals
        ]
        
        for prompt, expected_audience, expected_goals in test_cases:
            agent.get_response(prompt)
            # Verify the method was called with extracted parameters
            agent.create_marketing_copy.assert_called()
            call_args = agent.create_marketing_copy.call_args
            if expected_audience:
                assert expected_audience in str(call_args)
            if expected_goals:
                assert expected_goals in str(call_args)
            agent.create_marketing_copy.reset_mock()
    
    @patch('app.agents.marketing_copywriter_agent.pprint_run_response')
    def test_create_marketing_copy_with_all_parameters(self, mock_pprint):
        """Test create_marketing_copy method with all parameters"""
        agent = MarketingCopywriterAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Complete Copy Strategy\nWith audience and goals"
        agent.copywriter_team.run = Mock(return_value=[mock_response])
        
        response = agent.create_marketing_copy(
            url="https://example.com",
            target_audience="B2B SaaS companies, 50-500 employees",
            business_context="Lead generation focused software company",
            copy_goals="Increase demo requests by 25%"
        )
        
        assert response is not None
        assert "Complete Copy Strategy" in response
        agent.copywriter_team.run.assert_called_once()
        
        # Verify the prompt includes all parameters
        call_args = agent.copywriter_team.run.call_args[0][0]
        assert "https://example.com" in call_args
        assert "B2B SaaS companies" in call_args
        assert "Lead generation focused" in call_args
        assert "Increase demo requests" in call_args
    
    @patch('app.agents.marketing_copywriter_agent.pprint_run_response')
    def test_get_response_complex_prompt_parsing(self, mock_pprint):
        """Test complex prompt parsing with multiple parameters"""
        agent = MarketingCopywriterAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Complex Copy Analysis\nMulti-parameter strategy"
        agent.copywriter_team.run = Mock(return_value=[mock_response])
        
        complex_prompt = """
        https://example.com 
        audience: tech startups, early-stage companies
        goals: improve conversion rates, generate leads
        Additional context about the business model and target market
        """
        
        response = agent.get_response(complex_prompt)
        
        assert response is not None
        assert "Complex Copy Analysis" in response
        agent.copywriter_team.run.assert_called_once()
