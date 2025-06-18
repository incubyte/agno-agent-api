import pytest
from unittest.mock import Mock, patch
from app.agents.linkedin_writer_agent import LinkedInWriterAgent


def test_linkedin_writer_agent_initialization():
    """Test that LinkedInWriterAgent initializes correctly"""
    agent = LinkedInWriterAgent()
    assert agent is not None
    assert agent.linkedin_writer is not None


def test_linkedin_writer_agent_get_response():
    """Test the get_response method with a simple prompt"""
    agent = LinkedInWriterAgent()
    
    # Mock the agent response to avoid actual API calls in tests
    with patch.object(agent, 'generate_linkedin_post') as mock_generate:
        mock_generate.return_value = "Mocked LinkedIn post content"
        
        result = agent.get_response("Create a post about AI in software development")
        
        assert result == "Mocked LinkedIn post content"
        mock_generate.assert_called_once()


def test_linkedin_writer_agent_detects_post_types():
    """Test that the agent correctly detects different post types"""
    agent = LinkedInWriterAgent()
    
    with patch.object(agent, 'generate_linkedin_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test story detection
        agent.get_response("Share a story about my experience with AI")
        args, kwargs = mock_generate.call_args
        assert args[1] == "story"
        
        # Test tip detection
        mock_generate.reset_mock()
        agent.get_response("Give tips for better software development")
        args, kwargs = mock_generate.call_args
        assert args[1] == "tip"
        
        # Test question detection
        mock_generate.reset_mock()
        agent.get_response("Ask about the future of AI")
        args, kwargs = mock_generate.call_args
        assert args[1] == "question"


def test_linkedin_writer_agent_series_detection():
    """Test that the agent correctly detects series requests"""
    agent = LinkedInWriterAgent()
    
    with patch.object(agent, 'create_content_series') as mock_series:
        mock_series.return_value = "Mocked series content"
        
        result = agent.get_response("Create a series about software craftsmanship")
        
        assert result == "Mocked series content"
        mock_series.assert_called_once()


def test_linkedin_writer_agent_optimization_detection():
    """Test that the agent correctly detects optimization requests"""
    agent = LinkedInWriterAgent()
    
    with patch.object(agent, 'optimize_existing_post') as mock_optimize:
        mock_optimize.return_value = "Mocked optimization content"
        
        result = agent.get_response("Optimize this post: Hello world")
        
        assert result == "Mocked optimization content"
        mock_optimize.assert_called_once()


# Integration test class for when you want to test with real API calls
class TestLinkedInWriterAgentIntegration:
    """Integration tests that require actual API calls - run these manually or in CI"""
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_linkedin_post_generation(self):
        """Test actual LinkedIn post generation (requires API key)"""
        agent = LinkedInWriterAgent()
        result = agent.get_response("Create a post about the importance of code quality")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "code quality" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_content_series_generation(self):
        """Test actual content series generation (requires API key)"""
        agent = LinkedInWriterAgent()
        result = agent.create_content_series("AI in software development", 3)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "1/3" in result or "2/3" in result or "3/3" in result
