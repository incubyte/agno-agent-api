import pytest
from unittest.mock import Mock, patch
from app.agents.seo_auditor_agent import SEOAuditorAgent


class TestSEOAuditorAgent:
    """Test cases for SEO Auditor Agent"""
    
    def test_initialization(self):
        """Test that the agent initializes correctly"""
        agent = SEOAuditorAgent()
        assert agent is not None
        assert agent.seo_audit_team is not None
        assert hasattr(agent, 'AGENT_STORAGE')
    
    def test_create_keyword_intelligence_agent(self):
        """Test creation of keyword intelligence sub-agent"""
        agent = SEOAuditorAgent()
        keyword_agent = agent.create_keyword_intelligence_agent()
        
        assert keyword_agent is not None
        assert keyword_agent.name == "Keyword Intelligence Agent"
        assert "keyword research" in keyword_agent.role.lower()
        assert len(keyword_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    def test_create_seo_implementation_agent(self):
        """Test creation of SEO implementation sub-agent"""
        agent = SEOAuditorAgent()
        seo_agent = agent.create_seo_implementation_agent()
        
        assert seo_agent is not None
        assert seo_agent.name == "SEO Implementation Agent"
        assert "technical seo" in seo_agent.role.lower()
        assert len(seo_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    @patch('app.agents.seo_auditor_agent.pprint_run_response')
    def test_get_response_with_url(self, mock_pprint):
        """Test get_response method with URL input"""
        agent = SEOAuditorAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# SEO Audit Report\nTest SEO audit content"
        agent.seo_audit_team.run = Mock(return_value=[mock_response])
        
        test_url = "https://example.com"
        response = agent.get_response(test_url)
        
        assert response is not None
        assert "SEO Audit Report" in response
        agent.seo_audit_team.run.assert_called_once()
    
    @patch('app.agents.seo_auditor_agent.pprint_run_response')
    def test_get_response_with_keywords(self, mock_pprint):
        """Test get_response method with URL and keywords"""
        agent = SEOAuditorAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# SEO Audit Report\nKeyword analysis included"
        agent.seo_audit_team.run = Mock(return_value=[mock_response])
        
        test_prompt = "https://example.com keywords: web design, digital marketing"
        response = agent.get_response(test_prompt)
        
        assert response is not None
        assert "SEO Audit Report" in response
        agent.seo_audit_team.run.assert_called_once()
    
    @patch('app.agents.seo_auditor_agent.pprint_run_response')
    def test_conduct_seo_audit_error_handling(self, mock_pprint):
        """Test error handling in conduct_seo_audit method"""
        agent = SEOAuditorAgent()
        
        # Mock the agent team to raise an exception
        agent.seo_audit_team.run = Mock(side_effect=Exception("SEO audit error"))
        
        response = agent.conduct_seo_audit("https://example.com")
        
        assert "SEO Audit Error" in response
        assert "SEO audit error" in response
    
    def test_agent_team_configuration(self):
        """Test that the agent team is configured correctly"""
        agent = SEOAuditorAgent()
        team = agent.seo_audit_team
        
        assert team is not None
        assert team.name == "SEO Audit Team"
        assert len(team.team) == 2  # Keyword and Implementation agents
        assert team.model.id == "claude-3-7-sonnet-20250219"
        assert team.model.max_tokens == 10000
        
    def test_keyword_extraction_from_prompt(self):
        """Test keyword extraction from various prompt formats"""
        agent = SEOAuditorAgent()
        
        # Mock the conduct_seo_audit method to capture parameters
        agent.conduct_seo_audit = Mock(return_value="Mocked response")
        
        # Test various keyword prompt formats
        test_cases = [
            ("https://example.com keywords: seo, marketing", "seo, marketing"),
            ("https://example.com target: web design", "web design"),
            ("https://example.com focus keywords digital marketing", "digital marketing"),
            ("https://example.com", "")  # No keywords
        ]
        
        for prompt, expected_keywords in test_cases:
            agent.get_response(prompt)
            # Verify the method was called with extracted keywords
            agent.conduct_seo_audit.assert_called()
            call_args = agent.conduct_seo_audit.call_args
            if expected_keywords:
                assert expected_keywords.strip() in str(call_args)
            agent.conduct_seo_audit.reset_mock()
    
    @patch('app.agents.seo_auditor_agent.pprint_run_response')
    def test_conduct_seo_audit_with_all_parameters(self, mock_pprint):
        """Test conduct_seo_audit method with all parameters"""
        agent = SEOAuditorAgent()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Complete SEO Audit\nWith keywords and context"
        agent.seo_audit_team.run = Mock(return_value=[mock_response])
        
        response = agent.conduct_seo_audit(
            url="https://example.com",
            target_keywords="seo, marketing, web design",
            business_context="E-commerce website for digital services"
        )
        
        assert response is not None
        assert "Complete SEO Audit" in response
        agent.seo_audit_team.run.assert_called_once()
        
        # Verify the prompt includes all parameters
        call_args = agent.seo_audit_team.run.call_args[0][0]
        assert "https://example.com" in call_args
        assert "seo, marketing, web design" in call_args
        assert "E-commerce website" in call_args
