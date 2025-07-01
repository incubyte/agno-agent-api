import pytest
from unittest.mock import Mock, patch
from app.agents.website_performance_auditor import WebsitePerformanceAuditor


class TestWebsitePerformanceAuditor:
    """Test cases for Website Performance Auditor Agent"""
    
    def test_initialization(self):
        """Test that the agent initializes correctly"""
        agent = WebsitePerformanceAuditor()
        assert agent is not None
        assert agent.website_audit_team is not None
        assert hasattr(agent, 'AGENT_STORAGE')
    
    def test_create_technical_analysis_agent(self):
        """Test creation of technical analysis sub-agent"""
        agent = WebsitePerformanceAuditor()
        technical_agent = agent.create_technical_analysis_agent()
        
        assert technical_agent is not None
        assert technical_agent.name == "Technical Analysis Agent"
        assert "technical performance" in technical_agent.role.lower()
        assert len(technical_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    def test_create_business_optimization_agent(self):
        """Test creation of business optimization sub-agent"""
        agent = WebsitePerformanceAuditor()
        business_agent = agent.create_business_optimization_agent()
        
        assert business_agent is not None
        assert business_agent.name == "Business Optimization Agent"
        assert "conversion optimization" in business_agent.role.lower()
        assert len(business_agent.tools) == 2  # GoogleSearchTools and Crawl4aiTools
    
    @patch('app.agents.website_performance_auditor.pprint_run_response')
    def test_get_response_with_url(self, mock_pprint):
        """Test get_response method with URL input"""
        agent = WebsitePerformanceAuditor()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Website Audit Report\nTest audit content"
        agent.website_audit_team.run = Mock(return_value=[mock_response])
        
        test_url = "https://example.com"
        response = agent.get_response(test_url)
        
        assert response is not None
        assert "Website Audit Report" in response
        agent.website_audit_team.run.assert_called_once()
    
    @patch('app.agents.website_performance_auditor.pprint_run_response')
    def test_get_response_with_url_and_context(self, mock_pprint):
        """Test get_response method with URL and additional context"""
        agent = WebsitePerformanceAuditor()
        
        # Mock the agent team run method
        mock_response = Mock()
        mock_response.content = "# Website Audit Report\nTest audit with context"
        agent.website_audit_team.run = Mock(return_value=[mock_response])
        
        test_prompt = "https://example.com Additional business context here"
        response = agent.get_response(test_prompt)
        
        assert response is not None
        assert "Website Audit Report" in response
        agent.website_audit_team.run.assert_called_once()
    
    @patch('app.agents.website_performance_auditor.pprint_run_response')
    def test_audit_website_performance_error_handling(self, mock_pprint):
        """Test error handling in audit_website_performance method"""
        agent = WebsitePerformanceAuditor()
        
        # Mock the agent team to raise an exception
        agent.website_audit_team.run = Mock(side_effect=Exception("Test error"))
        
        response = agent.audit_website_performance("https://example.com")
        
        assert "Website Audit Error" in response
        assert "Test error" in response
    
    def test_agent_team_configuration(self):
        """Test that the agent team is configured correctly"""
        agent = WebsitePerformanceAuditor()
        team = agent.website_audit_team
        
        assert team is not None
        assert team.name == "Website Performance Audit Team"
        assert len(team.team) == 2  # Technical and Business agents
        assert team.model.id == "claude-3-7-sonnet-20250219"
        assert team.model.max_tokens == 10000
        
    def test_prompt_parsing_url_extraction(self):
        """Test URL extraction from various prompt formats"""
        agent = WebsitePerformanceAuditor()
        
        # Mock the audit method to avoid actual execution
        agent.audit_website_performance = Mock(return_value="Mocked response")
        
        # Test various prompt formats
        test_cases = [
            "https://example.com",
            "Please audit https://example.com for performance",
            "https://example.com with additional context",
            "Audit this site: https://example.com business context here"
        ]
        
        for prompt in test_cases:
            agent.get_response(prompt)
            # Verify the method was called (URL extraction worked)
            agent.audit_website_performance.assert_called()
            agent.audit_website_performance.reset_mock()
