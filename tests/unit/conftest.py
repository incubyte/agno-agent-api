"""
Unit test specific configuration and fixtures.
This file contains only fixtures and utilities - NO module mocking.
Module mocking must be done in individual test files after imports succeed.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch

# =============================================================================
# MOCK CLASSES FOR UNIT TESTING
# =============================================================================

class MockAgent:
    """Mock for Agent model class"""
    def __init__(self, id=None, name=None, slug=None, description=None, image=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.image = image
        self.created_at = created_at or "2024-01-01T00:00:00"
        self.updated_at = updated_at or "2024-01-01T00:00:00"

class MockAgentRepository:
    """Mock for AgentRepository class"""
    def __init__(self):
        self.agents = {}
        self.next_id = 1
    
    def get_all(self):
        """Mock get_all method"""
        return list(self.agents.values())
    
    def get_by_id(self, agent_id: int):
        """Mock get_by_id method"""
        return self.agents.get(agent_id)
    
    def create(self, agent):
        """Mock create method"""
        agent.id = self.next_id
        agent.created_at = "2024-01-01T00:00:00"
        agent.updated_at = "2024-01-01T00:00:00"
        self.agents[self.next_id] = agent
        self.next_id += 1
        return agent
    
    def update(self, agent):
        """Mock update method"""
        if agent.id in self.agents:
            agent.updated_at = "2024-01-01T00:00:00"
            self.agents[agent.id] = agent
            return agent
        return None
    
    def delete(self, agent):
        """Mock delete method"""
        if agent.id in self.agents:
            del self.agents[agent.id]
            return agent
        return None
    
    def get_by_slug(self, slug: str):
        """Mock get_by_slug method"""
        for agent in self.agents.values():
            if agent.slug == slug:
                return agent
        return None
    
    def exists_by_slug(self, slug: str):
        """Mock exists_by_slug method"""
        return any(agent.slug == slug for agent in self.agents.values())
    
    def agent_count(self):
        """Mock agent_count method"""
        return {"count": len(self.agents)}


# =============================================================================
# UNIT TEST FIXTURES
# =============================================================================

@pytest.fixture
def mock_agent():
    """Fixture providing a mock Agent class"""
    return MockAgent

@pytest.fixture
def mock_agent_repository():
    """Fixture providing a mock AgentRepository instance"""
    return MockAgentRepository()

@pytest.fixture
def agent_service_mocks():
    """Fixture providing all agent service related mocks"""
    return {
        'Agent': MockAgent,
        'AgentRepository': MockAgentRepository
    }

# =============================================================================
# MOCK PATCHES FOR UNIT TESTS
# =============================================================================

@pytest.fixture
def mock_anthropic_api():
    """Fixture to mock Anthropic API calls"""
    with patch('anthropic.Client') as mock_client:
        mock_instance = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Mocked AI response")]
        mock_instance.messages.create.return_value = mock_response
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_database():
    """Fixture to mock database operations"""
    with patch('app.db.engine.get_db') as mock_db:
        mock_session = Mock()
        mock_db.return_value = mock_session
        yield mock_session


def pytest_runtest_setup(item):
    """Setup for each unit test run"""
    # Skip external API calls in unit tests unless explicitly requested
    if "unit" in item.keywords and os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true":
        for marker in item.iter_markers():
            if marker.name == "external_api":
                pytest.skip("Skipping external API calls in unit tests")
