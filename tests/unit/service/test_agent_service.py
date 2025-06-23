import pytest
import os
import sys
import importlib.util
from unittest.mock import MagicMock, patch
from fastapi import HTTPException


# Now that FastAPI imported successfully, we can mock the modules we need
sys.modules['app.core.setting'] = MagicMock()
sys.modules['app.core.settings'] = MagicMock()
sys.modules['app.db.engine'] = MagicMock()
sys.modules['app.db.models'] = MagicMock()
sys.modules['app.db.repository.agent_repository'] = MagicMock()
sys.modules['app.agents.agent_factory'] = MagicMock()
sys.modules['app.agents.agent_prompt_repository'] = MagicMock()
sys.modules['app.agents.enum.agent_enum'] = MagicMock()
sys.modules['textwrap'] = MagicMock()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import the agent service module
spec = importlib.util.spec_from_file_location(
    "agent_service",
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app/service/agent_service.py'))
)
agent_service_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_service_module)

AgentService = agent_service_module.AgentService


class TestAgentService:
    """Test class for AgentService get_all_agents method"""
    
    @patch.object(agent_service_module, 'AgentRepository')
    def test_get_all_agents_success(self, mock_agent_repository):
        """Test get_all_agents returns list of agents successfully"""
        # Setup mock repository
        mock_repo_instance = MagicMock()
        mock_agent_repository.return_value = mock_repo_instance
        
        # Mock agent data
        mock_agent_1 = MagicMock()
        mock_agent_1.id = 1
        mock_agent_1.name = "Agent 1"
        mock_agent_1.slug = "agent-1"
        
        mock_agent_2 = MagicMock()
        mock_agent_2.id = 2
        mock_agent_2.name = "Agent 2"
        mock_agent_2.slug = "agent-2"
        
        mock_agents = [mock_agent_1, mock_agent_2]
        mock_repo_instance.get_all.return_value = mock_agents
        
        # Create service instance
        service = AgentService()
        
        # Call method
        result = service.get_all_agents()
        
        # Assertions
        mock_repo_instance.get_all.assert_called_once()
        assert result == mock_agents
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
    
    @patch.object(agent_service_module, 'AgentRepository')
    def test_get_all_agents_exception(self, mock_agent_repository):
        """Test get_all_agents raises HTTPException when repository fails"""
        # Setup mock repository to raise exception
        mock_repo_instance = MagicMock()
        mock_agent_repository.return_value = mock_repo_instance
        mock_repo_instance.get_all.side_effect = Exception("Database connection failed")
        
        # Create service instance
        service = AgentService()
        
        # Call method and expect HTTPException to be raised
        with pytest.raises(HTTPException) as exc_info:
            service.get_all_agents()
        
        # Verify the repository method was called
        mock_repo_instance.get_all.assert_called_once()
        
        # Assert the exception details match what we expect
        assert exc_info.value.status_code == 500
        assert "Failed to retrieve list of agents" in exc_info.value.detail
        assert "Database connection failed" in exc_info.value.detail
    
    @patch.object(agent_service_module, 'AgentRepository')
    def test_get_all_agents_empty_list(self, mock_agent_repository):
        """Test get_all_agents returns empty list when no agents exist"""
        # Setup mock repository to return empty list
        mock_repo_instance = MagicMock()
        mock_agent_repository.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = []
        
        # Create service instance
        service = AgentService()
        
        # Call method
        result = service.get_all_agents()
        
        # Assertions
        mock_repo_instance.get_all.assert_called_once()
        assert result == []
        assert len(result) == 0

    @patch.object(agent_service_module, 'AgentRepository')
    def test_get_agent_by_id_success(self, mock_agent_repository):
        """Test get_agent_by_id returns agent when found"""
        # Setup mock repository
        mock_repo_instance = MagicMock()
        mock_agent_repository.return_value = mock_repo_instance

        # Mock agent data
        mock_agent = MagicMock()
        mock_agent.id = 1
        mock_agent.name = "Agent 1"
        mock_agent.slug = "agent-1"
        mock_repo_instance.get_by_id.return_value = mock_agent

        # Create service instance
        service = AgentService()

        # Call method
        result = service.get_agent_by_id(1)

        # Assertions
        mock_repo_instance.get_by_id.assert_called_once_with(1)
        assert result == mock_agent

    @patch.object(agent_service_module, 'AgentRepository')
    def test_get_agent_by_id_not_found(self, mock_agent_repository):
        """Test get_agent_by_id raises HTTPException when agent not found"""
        # Setup mock repository
        mock_repo_instance = MagicMock()
        mock_agent_repository.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None

        # Create service instance
        service = AgentService()

        # Call method and assert HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            service.get_agent_by_id(999)

        # Verify the exception details
        assert exc_info.value.status_code == 404
        assert "Agent with ID 999 not found" in str(exc_info.value.detail)

    def test_get_all_agents_with_conftest_fixtures(self, mock_agent, mock_agent_repository):
        """Test get_all_agents using conftest fixtures"""
        # Use conftest fixtures to create test data
        agent1 = mock_agent(id=1, name="Fixture Agent 1", slug="fixture-agent-1")
        agent2 = mock_agent(id=2, name="Fixture Agent 2", slug="fixture-agent-2")
        
        # Add agents to the mock repository
        mock_agent_repository.agents[1] = agent1
        mock_agent_repository.agents[2] = agent2
        
        # Create service instance and patch the repository
        with patch.object(agent_service_module, 'AgentRepository', return_value=mock_agent_repository):
            service = AgentService()
            result = service.get_all_agents()
            
            # Assertions
            assert len(result) == 2
            assert result[0].name == "Fixture Agent 1"
            assert result[1].name == "Fixture Agent 2"
