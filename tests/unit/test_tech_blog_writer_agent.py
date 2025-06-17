import pytest
from unittest.mock import Mock, patch
from app.agents.tech_blog_writer_agent import TechBlogWriterAgent


def test_tech_blog_writer_agent_initialization():
    """Test that TechBlogWriterAgent initializes correctly"""
    agent = TechBlogWriterAgent()
    assert agent is not None
    assert agent.tech_blog_writer is not None


def test_tech_blog_writer_agent_get_response():
    """Test the get_response method with a simple prompt"""
    agent = TechBlogWriterAgent()
    
    # Mock the agent response to avoid actual API calls in tests
    with patch.object(agent, 'generate_tech_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked technical blog post content"
        
        result = agent.get_response("Create a blog post about Python async programming")
        
        assert result == "Mocked technical blog post content"
        mock_generate.assert_called_once()


def test_tech_blog_writer_agent_detects_complexity_levels():
    """Test that the agent correctly detects complexity levels"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'generate_tech_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test beginner detection
        agent.get_response("Create a beginner guide to Python")
        args, kwargs = mock_generate.call_args
        assert args[1] == "beginner"  # complexity parameter
        
        # Test advanced detection
        mock_generate.reset_mock()
        agent.get_response("Write an advanced tutorial on machine learning")
        args, kwargs = mock_generate.call_args
        assert args[1] == "advanced"
        
        # Test intermediate (default)
        mock_generate.reset_mock()
        agent.get_response("Explain Docker containers")
        args, kwargs = mock_generate.call_args
        assert args[1] == "intermediate"


def test_tech_blog_writer_agent_detects_length():
    """Test that the agent correctly detects post length"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'generate_tech_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test short detection
        agent.get_response("Write a short post about Git")
        args, kwargs = mock_generate.call_args
        assert args[2] == "short"  # length parameter
        
        # Test long detection
        mock_generate.reset_mock()
        agent.get_response("Create a comprehensive guide to Kubernetes")
        args, kwargs = mock_generate.call_args
        assert args[2] == "long"


def test_tech_blog_writer_agent_detects_post_types():
    """Test that the agent correctly detects different post types"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'generate_tech_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test tutorial detection
        agent.get_response("How to set up a React application")
        args, kwargs = mock_generate.call_args
        assert args[3] == "tutorial"  # post_type parameter
        
        # Test explainer detection
        mock_generate.reset_mock()
        agent.get_response("Explain what is GraphQL")
        args, kwargs = mock_generate.call_args
        assert args[3] == "explainer"
        
        # Test guide detection
        mock_generate.reset_mock()
        agent.get_response("Complete guide to microservices")
        args, kwargs = mock_generate.call_args
        assert args[3] == "guide"


def test_tech_blog_writer_agent_series_detection():
    """Test that the agent correctly detects series requests"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'create_blog_series') as mock_series:
        mock_series.return_value = "Mocked series content"
        
        result = agent.get_response("Create a series about web development")
        
        assert result == "Mocked series content"
        mock_series.assert_called_once()


def test_tech_blog_writer_agent_review_detection():
    """Test that the agent correctly detects review requests"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'review_technology') as mock_review:
        mock_review.return_value = "Mocked review content"
        
        result = agent.get_response("Review the latest version of Django")
        
        assert result == "Mocked review content"
        mock_review.assert_called_once()


def test_tech_blog_writer_agent_comparison_detection():
    """Test that the agent correctly detects comparison requests"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'create_technical_comparison') as mock_comparison:
        mock_comparison.return_value = "Mocked comparison content"
        
        result = agent.get_response("Compare React vs Vue.js")
        
        assert result == "Mocked comparison content"
        mock_comparison.assert_called_once()


def test_tech_blog_writer_agent_series_length_detection():
    """Test that the agent correctly detects series length"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'create_blog_series') as mock_series:
        mock_series.return_value = "Mocked series content"
        
        # Test specific number detection
        agent.get_response("Create a 7-part series about machine learning")
        args, kwargs = mock_series.call_args
        assert args[1] == 7  # series_length parameter
        
        # Test default length
        mock_series.reset_mock()
        agent.get_response("Create a series about Python")
        args, kwargs = mock_series.call_args
        assert args[1] == 5  # default series_length


def test_tech_blog_writer_agent_parameter_combinations():
    """Test complex parameter combinations"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent, 'generate_tech_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test multiple parameters
        agent.get_response("Create a long advanced tutorial about machine learning algorithms")
        args, kwargs = mock_generate.call_args
        
        # Check all parameters are correctly detected
        assert args[1] == "advanced"  # complexity
        assert args[2] == "long"      # length
        assert args[3] == "tutorial"  # post_type


def test_tech_blog_writer_agent_error_handling():
    """Test error handling in the agent"""
    agent = TechBlogWriterAgent()
    
    with patch.object(agent.tech_blog_writer, 'run') as mock_run:
        # Simulate an exception
        mock_run.side_effect = Exception("API Error")
        
        result = agent.get_response("Create a blog post about Python")
        
        assert "Error generating technical blog post" in result
        assert "API Error" in result


def test_tech_blog_writer_agent_method_specific_tests():
    """Test individual methods of the agent"""
    agent = TechBlogWriterAgent()
    
    # Test generate_tech_blog_post with specific parameters
    with patch.object(agent.tech_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Test content")])
        
        result = agent.generate_tech_blog_post(
            topic="Python Testing",
            complexity="beginner",
            length="short",
            post_type="tutorial"
        )
        
        assert result == "Test content"
        mock_run.assert_called_once()
    
    # Test create_blog_series
    with patch.object(agent.tech_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Series content")])
        
        result = agent.create_blog_series("Web Development", 3, "intermediate")
        
        assert result == "Series content"
        mock_run.assert_called_once()
    
    # Test review_technology
    with patch.object(agent.tech_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Review content")])
        
        result = agent.review_technology("Django", ["features", "performance"])
        
        assert result == "Review content"
        mock_run.assert_called_once()
    
    # Test create_technical_comparison
    with patch.object(agent.tech_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Comparison content")])
        
        result = agent.create_technical_comparison(["React", "Angular"], ["performance", "ease_of_use"])
        
        assert result == "Comparison content"
        mock_run.assert_called_once()


# Integration test class for when you want to test with real API calls
class TestTechBlogWriterAgentIntegration:
    """Integration tests that require actual API calls - run these manually or in CI"""
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_blog_post_generation(self):
        """Test actual blog post generation (requires API key)"""
        agent = TechBlogWriterAgent()
        result = agent.get_response("Create a blog post about Python decorators")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "decorator" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_blog_series_generation(self):
        """Test actual blog series generation (requires API key)"""
        agent = TechBlogWriterAgent()
        result = agent.create_blog_series("Web Development Fundamentals", 4)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "web development" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_technology_review(self):
        """Test actual technology review (requires API key)"""
        agent = TechBlogWriterAgent()
        result = agent.review_technology("FastAPI")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "fastapi" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_technology_comparison(self):
        """Test actual technology comparison (requires API key)"""
        agent = TechBlogWriterAgent()
        result = agent.create_technical_comparison(["React", "Vue.js"])
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "react" in result.lower()
        assert "vue" in result.lower()
