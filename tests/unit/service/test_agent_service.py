import pytest
import os
import sys
import importlib.util
from unittest.mock import MagicMock, patch, ANY

# Mock all the necessary modules before they are imported
sys.modules['routers'] = MagicMock()
sys.modules['routers.index_router'] = MagicMock()
sys.modules['routers.agent'] = MagicMock()
sys.modules['core'] = MagicMock()
sys.modules['core.settings'] = MagicMock()

# Mock the app modules to avoid circular imports
sys.modules['app.main'] = MagicMock()
sys.modules['app.core'] = MagicMock()

# Add the project root to the Python path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import agent_service module using importlib.util
spec = importlib.util.spec_from_file_location(
    "agent_service",
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app/service/agent_service.py'))
)
agent_service_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_service_module)

# Get the module components we need for testing
AgentService = agent_service_module.AgentService
tools = agent_service_module.tools
instructions = agent_service_module.instructions


class TestAgentService:    
    @patch.object(agent_service_module, 'Agent')
    @patch.object(agent_service_module, 'Claude')
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
            markdown=True)
    @patch.object(agent_service_module, 'Agent')
    @patch.object(agent_service_module, 'Claude')
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
            markdown=False        )
    @patch.object(agent_service_module, 'Agent')
    @patch.object(agent_service_module, 'Claude')
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
    @patch.object(agent_service_module, 'Agent')
    @patch.object(agent_service_module, 'Claude')
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