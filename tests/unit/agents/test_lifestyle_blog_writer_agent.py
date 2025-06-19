import pytest
from unittest.mock import Mock, patch
from app.agents.lifestyle_blog_writer_agent import LifestyleBlogWriterAgent


def test_lifestyle_blog_writer_agent_initialization():
    """Test that LifestyleBlogWriterAgent initializes correctly"""
    agent = LifestyleBlogWriterAgent()
    assert agent is not None
    assert agent.lifestyle_blog_writer is not None


def test_lifestyle_blog_writer_agent_get_response():
    """Test the get_response method with a simple prompt"""
    agent = LifestyleBlogWriterAgent()
    
    # Mock the agent response to avoid actual API calls in tests
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked lifestyle blog post content"
        
        result = agent.get_response("Create a blog post about morning routines")
        
        assert result == "Mocked lifestyle blog post content"
        mock_generate.assert_called_once()


def test_lifestyle_blog_writer_agent_detects_styles():
    """Test that the agent correctly detects writing styles"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test formal detection
        agent.get_response("Create a formal post about productivity")
        args, kwargs = mock_generate.call_args
        assert args[1] == "formal"  # style parameter
        
        # Test inspirational detection
        mock_generate.reset_mock()
        agent.get_response("Write an inspirational piece about self-care")
        args, kwargs = mock_generate.call_args
        assert args[1] == "inspirational"
        
        # Test conversational detection
        mock_generate.reset_mock()
        agent.get_response("Create a conversational post about mindfulness")
        args, kwargs = mock_generate.call_args
        assert args[1] == "conversational"
        
        # Test casual (default)
        mock_generate.reset_mock()
        agent.get_response("Write about healthy habits")
        args, kwargs = mock_generate.call_args
        assert args[1] == "casual"


def test_lifestyle_blog_writer_agent_detects_length():
    """Test that the agent correctly detects post length"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test short detection
        agent.get_response("Write a short post about meditation")
        args, kwargs = mock_generate.call_args
        assert args[2] == "short"  # length parameter
        
        # Test long detection
        mock_generate.reset_mock()
        agent.get_response("Create a comprehensive guide to wellness")
        args, kwargs = mock_generate.call_args
        assert args[2] == "long"
        
        # Test medium (default)
        mock_generate.reset_mock()
        agent.get_response("Write about work-life balance")
        args, kwargs = mock_generate.call_args
        assert args[2] == "medium"


def test_lifestyle_blog_writer_agent_detects_focus_areas():
    """Test that the agent correctly detects focus areas"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test wellness detection
        agent.get_response("Create a post about wellness and health")
        args, kwargs = mock_generate.call_args
        assert args[3] == "wellness"  # focus_area parameter
        
        # Test productivity detection
        mock_generate.reset_mock()
        agent.get_response("Write about productivity tips")
        args, kwargs = mock_generate.call_args
        assert args[3] == "productivity"
        
        # Test relationships detection
        mock_generate.reset_mock()
        agent.get_response("Share advice about relationships")
        args, kwargs = mock_generate.call_args
        assert args[3] == "relationships"
        
        # Test personal growth detection
        mock_generate.reset_mock()
        agent.get_response("Write about personal growth strategies")
        args, kwargs = mock_generate.call_args
        assert args[3] == "personal_growth"
        
        # Test mindfulness detection
        mock_generate.reset_mock()
        agent.get_response("Create content about mindfulness practices")
        args, kwargs = mock_generate.call_args
        assert args[3] == "mindfulness"
        
        # Test fitness detection
        mock_generate.reset_mock()
        agent.get_response("Write about fitness and exercise")
        args, kwargs = mock_generate.call_args
        assert args[3] == "fitness"


def test_lifestyle_blog_writer_agent_series_detection():
    """Test that the agent correctly detects series requests"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'create_lifestyle_series') as mock_series:
        mock_series.return_value = "Mocked series content"
        
        result = agent.get_response("Create a series about self-care routines")
        
        assert result == "Mocked series content"
        mock_series.assert_called_once()


def test_lifestyle_blog_writer_agent_seasonal_detection():
    """Test that the agent correctly detects seasonal content requests"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'create_seasonal_content') as mock_seasonal:
        mock_seasonal.return_value = "Mocked seasonal content"
        
        # Test spring detection
        result = agent.get_response("Create spring wellness content")
        
        assert result == "Mocked seasonal content"
        mock_seasonal.assert_called_once_with("spring")


def test_lifestyle_blog_writer_agent_guide_detection():
    """Test that the agent correctly detects guide requests"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'create_lifestyle_guide') as mock_guide:
        mock_guide.return_value = "Mocked guide content"
        
        result = agent.get_response("Create a comprehensive guide to healthy living")
        
        assert result == "Mocked guide content"
        mock_guide.assert_called_once()


def test_lifestyle_blog_writer_agent_chat_detection():
    """Test that the agent correctly detects chat/advice requests"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'chat_lifestyle_advice') as mock_chat:
        mock_chat.return_value = "Mocked chat response"
        
        result = agent.get_response("Help me with work-life balance advice")
        
        assert result == "Mocked chat response"
        mock_chat.assert_called_once()


def test_lifestyle_blog_writer_agent_series_length_detection():
    """Test that the agent correctly detects series length"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'create_lifestyle_series') as mock_series:
        mock_series.return_value = "Mocked series content"
        
        # Test specific number detection
        agent.get_response("Create a 7-part series about mindfulness")
        args, kwargs = mock_series.call_args
        assert args[1] == 7  # series_length parameter
        
        # Test default length
        mock_series.reset_mock()
        agent.get_response("Create a series about wellness")
        args, kwargs = mock_series.call_args
        assert args[1] == 5  # default series_length


def test_lifestyle_blog_writer_agent_parameter_combinations():
    """Test complex parameter combinations"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Mocked content"
        
        # Test multiple parameters
        agent.get_response("Create a long inspirational post about wellness and personal growth")
        args, kwargs = mock_generate.call_args
        
        # Check all parameters are correctly detected
        assert args[1] == "inspirational"  # style
        assert args[2] == "long"           # length
        assert args[3] == "wellness"       # focus_area


def test_lifestyle_blog_writer_agent_error_handling():
    """Test error handling in the agent"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        # Simulate an exception
        mock_run.side_effect = Exception("API Error")
        
        result = agent.get_response("Create a blog post about wellness")
        
        assert "Error generating lifestyle blog post" in result
        assert "API Error" in result


def test_lifestyle_blog_writer_agent_method_specific_tests():
    """Test individual methods of the agent"""
    agent = LifestyleBlogWriterAgent()
    
    # Test generate_lifestyle_blog_post with specific parameters
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Test content")])
        
        result = agent.generate_lifestyle_blog_post(
            topic="Morning Routines",
            style="inspirational",
            length="medium",
            focus_area="wellness"
        )
        
        assert result == "Test content"
        mock_run.assert_called_once()
    
    # Test create_lifestyle_series
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Series content")])
        
        result = agent.create_lifestyle_series("Self-Care", 4, "wellness")
        
        assert result == "Series content"
        mock_run.assert_called_once()
    
    # Test create_seasonal_content
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Seasonal content")])
        
        result = agent.create_seasonal_content("spring", "wellness")
        
        assert result == "Seasonal content"
        mock_run.assert_called_once()
    
    # Test create_lifestyle_guide
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Guide content")])
        
        result = agent.create_lifestyle_guide("Healthy Living", "busy professionals")
        
        assert result == "Guide content"
        mock_run.assert_called_once()
    
    # Test chat_lifestyle_advice
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Chat response")])
        
        result = agent.chat_lifestyle_advice("How do I balance work and life?", [])
        
        assert result == "Chat response"
        mock_run.assert_called_once()


def test_lifestyle_blog_writer_agent_seasonal_variations():
    """Test detection of different seasons"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent, 'create_seasonal_content') as mock_seasonal:
        mock_seasonal.return_value = "Mocked seasonal content"
        
        # Test different seasons
        seasons_to_test = [
            ("spring wellness tips", "spring"),
            ("summer fitness routines", "summer"),
            ("fall self-care practices", "fall"),
            ("winter mindfulness activities", "winter"),
            ("holiday stress management", "current season")  # holiday but no specific season
        ]
        
        for prompt, expected_season in seasons_to_test:
            mock_seasonal.reset_mock()
            agent.get_response(prompt)
            mock_seasonal.assert_called_once_with(expected_season)


def test_lifestyle_blog_writer_agent_chat_context():
    """Test chat functionality with context"""
    agent = LifestyleBlogWriterAgent()
    
    with patch.object(agent.lifestyle_blog_writer, 'run') as mock_run:
        mock_run.return_value = iter([Mock(content="Chat response with context")])
        
        context = [
            {"role": "user", "content": "I'm feeling stressed lately"},
            {"role": "assistant", "content": "I understand stress can be overwhelming. What specific areas are causing you the most stress?"}
        ]
        
        result = agent.chat_lifestyle_advice("It's mainly work deadlines", context)
        
        assert result == "Chat response with context"
        mock_run.assert_called_once()
        
        # Check that context was included in the prompt
        call_args = mock_run.call_args[0][0]
        assert "feeling stressed lately" in call_args
        assert "work deadlines" in call_args


# Integration test class for when you want to test with real API calls
class TestLifestyleBlogWriterAgentIntegration:
    """Integration tests that require actual API calls - run these manually or in CI"""
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_lifestyle_blog_post_generation(self):
        """Test actual lifestyle blog post generation (requires API key)"""
        agent = LifestyleBlogWriterAgent()
        result = agent.get_response("Create a blog post about morning routines for better productivity")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "morning" in result.lower()
        assert "routine" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_lifestyle_series_generation(self):
        """Test actual lifestyle series generation (requires API key)"""
        agent = LifestyleBlogWriterAgent()
        result = agent.create_lifestyle_series("Mindful Living", 3, "mindfulness")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "mindful" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_seasonal_content_generation(self):
        """Test actual seasonal content generation (requires API key)"""
        agent = LifestyleBlogWriterAgent()
        result = agent.create_seasonal_content("spring", "wellness")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "spring" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_lifestyle_guide_generation(self):
        """Test actual lifestyle guide generation (requires API key)"""
        agent = LifestyleBlogWriterAgent()
        result = agent.create_lifestyle_guide("Work-Life Balance", "working parents")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "work-life" in result.lower() or "work life" in result.lower()
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_real_chat_advice(self):
        """Test actual chat advice functionality (requires API key)"""
        agent = LifestyleBlogWriterAgent()
        result = agent.chat_lifestyle_advice("I'm struggling to maintain a healthy work-life balance")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) < 2000  # Should be conversational, not a full blog post


def test_lifestyle_blog_writer_agent_edge_cases():
    """Test edge cases and boundary conditions"""
    agent = LifestyleBlogWriterAgent()
    
    # Test empty prompt
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Default content"
        result = agent.get_response("")
        assert result == "Default content"
    
    # Test very long prompt
    with patch.object(agent, 'generate_lifestyle_blog_post') as mock_generate:
        mock_generate.return_value = "Long prompt content"
        long_prompt = "Create a blog post about " + "wellness " * 100
        result = agent.get_response(long_prompt)
        assert result == "Long prompt content"
    
    # Test prompt with multiple conflicting indicators
    with patch.object(agent, 'create_lifestyle_series') as mock_series:
        mock_series.return_value = "Series wins"
        # This has both series and guide indicators - should prioritize series
        conflicting_prompt = "Create a comprehensive guide series about wellness"
        result = agent.get_response(conflicting_prompt)
        assert result == "Series wins"
        mock_series.assert_called_once()
