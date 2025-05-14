import pytest
from unittest.mock import MagicMock, patch, ANY
from app.service import AgentService, tools, instructions


class TestAgentService:

    @patch('app.service.agent_service.Agent')
    @patch('app.service.agent_service.Claude')
    def test_init(self, mock_claude, mock_agent):
        """Test that AgentService initializes with correct parameters"""
        mock_claude_instance = MagicMock()
        mock_claude.return_value = mock_claude_instance
        
        service = AgentService()
        
        mock_claude.assert_called_once()
        mock_agent.assert_called_once_with(
            model=mock_claude_instance,
            tools=tools,
            instructions=instructions,
            markdown=True
        )

    @patch('app.service.agent_service.Agent')
    @patch('app.service.agent_service.Claude')
    def test_init_with_custom_params(self, mock_claude, mock_agent):
        """Test that AgentService initializes with custom parameters"""

        mock_claude_instance = MagicMock()
        mock_claude.return_value = mock_claude_instance
        custom_tools = [MagicMock()]
        custom_instructions = ["Custom instruction"]
        
        service = AgentService(
            model_id='custom-model',
            tools=custom_tools,
            instructions=custom_instructions,
            markdown=False
        )   

        mock_claude.assert_called_once_with(
            id='custom-model', 
            api_key=ANY
        )
        mock_agent.assert_called_once_with(
            model=mock_claude_instance,
            tools=custom_tools,
            instructions=custom_instructions,
            markdown=False
        )

    @patch('app.service.agent_service.Agent')
    @patch('app.service.agent_service.Claude')
    def test_generate_response(self, mock_claude, mock_agent):
        """Test generate_response method returns expected content"""
        mock_claude_instance = MagicMock()
        mock_claude.return_value = mock_claude_instance
        
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        
        mock_response = MagicMock()
        mock_response.content = "Test response content"
        mock_agent_instance.run.return_value = mock_response
        mock_agent_instance.markdown = True
        
        service = AgentService()
        
        result = service.generate_response("Test query")
        
        mock_agent_instance.run.assert_called_once_with(
            "Test query",
            markdown=True
        )
        assert result == "Test response content"

    @patch('app.service.agent_service.Agent')
    @patch('app.service.agent_service.Claude')
    def test_generate_response_with_markdown_disabled(self, mock_claude, mock_agent):
        """Test generate_response method with markdown disabled"""
        mock_claude_instance = MagicMock()
        mock_claude.return_value = mock_claude_instance
        
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        
        mock_response = MagicMock()
        mock_response.content = "Test response content"
        mock_agent_instance.run.return_value = mock_response
        mock_agent_instance.markdown = False
        
        service = AgentService(markdown=False)
        
        result = service.generate_response("Test query")
        
        mock_agent_instance.run.assert_called_once_with(
            "Test query",
            markdown=False
        )
        assert result == "Test response content"