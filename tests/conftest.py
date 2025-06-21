"""
Centralized test configuration and fixtures for the Agno AI API test suite.
This file contains all common mocks, fixtures, and test utilities to avoid duplication.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from typing import Generator, Any

# Add the parent directory to sys.path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# =============================================================================
# MOCK SERVICE CLASSES
# =============================================================================

class MockAgentService:
    """Mock for AgentService class"""
    
    def generate_response(self, prompt: str) -> str:
        return f"Mocked response to: {prompt}"
    
    def get_all_agents(self):
        return [
            {"id": 1, "name": "Test Agent 1", "slug": "test-agent-1"},
            {"id": 2, "name": "Test Agent 2", "slug": "test-agent-2"}
        ]
    
    def get_agent_by_id(self, agent_id: int):
        if agent_id == 1:
            return {
                "agent": {"id": 1, "name": "Test Agent 1", "slug": "test-agent-1"},
                "prompt": "Test prompt for agent 1"
            }
        return None
    
    def create_agent(self, agent):
        """Mock agent creation"""
        return {
            "id": 1,
            "name": agent.name,
            "slug": agent.slug,
            "description": agent.description,
            "image": agent.image,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    def run_agent_by_id(self, agent_id: int, prompt: str, user_email: str):
        """Mock agent execution"""
        if not prompt:
            raise ValueError("Prompt must not be empty")
        if not user_email:
            raise ValueError("User email must not be empty")
        return f"Mocked response to '{prompt}' for agent {agent_id}"
    
    def update_agent(self, agent_id: int, updated_data: dict):
        """Mock agent update"""
        if agent_id == 999:
            return None  # Simulate agent not found
        return {
            "id": agent_id,
            "name": updated_data.get("name", "Test Agent"),
            "slug": "test-agent",
            "description": updated_data.get("description"),
            "updated_at": "2024-01-01T00:00:00"
        }
    
    def delete_agent(self, agent_id: int):
        """Mock agent deletion"""
        if agent_id == 999:
            return False  # Simulate agent not found
        return True
    
    def get_agent_by_slug(self, slug: str):
        """Mock get agent by slug"""
        if slug == "test-agent-1":
            return {"id": 1, "name": "Test Agent 1", "slug": "test-agent-1"}
        return None
    
    def agent_exists_by_slug(self, slug: str):
        """Mock check agent exists"""
        return slug == "test-agent-1"
    
    def get_agent_count(self):
        """Mock get agent count"""
        return 2


class MockPdfService:
    """Mock for PdfService class"""
    
    def __init__(self):
        self.html_content = None
    
    def convert_markdown_to_html(self, markdown_text: str):
        self.html_content = f"<html><body>{markdown_text}</body></html>"
        return
    
    def save_pdf_file(self):
        # Mock PDF file creation
        return "pdf/output.pdf"


class MockEmailService:
    """Mock for EmailService class"""
    
    def __init__(self):
        self.connected = False
        self.sent_emails = []
    
    def connect(self):
        self.connected = True
        return
    
    def send_email(self, to_email: str, subject: str, body: str, logo_path=None, pdf_path=None):
        if not self.connected:
            raise Exception("Email service not connected")
        
        email_data = {
            "to_email": to_email,
            "subject": subject,
            "body": body,
            "logo_path": logo_path,
            "pdf_path": pdf_path
        }
        self.sent_emails.append(email_data)
        return
    
    def disconnect(self):
        self.connected = False
        return


class MockEmailServiceWithError(MockEmailService):
    """Mock EmailService that raises an exception on send_email"""
    
    def send_email(self, to_email: str, subject: str, body: str, logo_path=None, pdf_path=None):
        raise Exception("Email service error")


class MockMarketingAgent:
    """Mock for MarketingAgent class"""
    
    def run_marketing_agent(self, url: str) -> str:
        return f"Mocked marketing analysis for: {url}"


class MockLifestyleBlogWriterAgent:
    """Mock for LifestyleBlogWriterAgent class"""
    
    def __init__(self):
        self.lifestyle_blog_writer = Mock()
    
    def get_response(self, prompt: str) -> str:
        return "Mocked lifestyle blog post content"
    
    def generate_lifestyle_blog_post(self, topic: str, style: str = "conversational") -> str:
        return f"Mocked lifestyle blog post about {topic} in {style} style"


class MockTechBlogWriterAgent:
    """Mock for TechBlogWriterAgent class"""
    
    def get_response(self, prompt: str) -> str:
        return "Mocked tech blog post content"


class MockLinkedinWriterAgent:
    """Mock for LinkedinWriterAgent class"""
    
    def get_response(self, prompt: str) -> str:
        return "Mocked LinkedIn post content"


# =============================================================================
# ENHANCED MOCKS FOR AGENT ROUTER E2E TESTS
# =============================================================================

class MockAgentRepository:
    """Mock for AgentRepository to simulate database operations"""
    
    def __init__(self):
        self.agents = {}
        self.next_id = 1
    
    def get_all(self):
        return list(self.agents.values())
    
    def get_by_id(self, agent_id: int):
        return self.agents.get(agent_id)
    
    def create(self, agent):
        agent.id = self.next_id
        agent.created_at = "2024-01-01T00:00:00"
        agent.updated_at = "2024-01-01T00:00:00"
        self.agents[self.next_id] = agent
        self.next_id += 1
        return agent
    
    def update(self, agent):
        if agent.id in self.agents:
            agent.updated_at = "2024-01-01T00:00:00"
            self.agents[agent.id] = agent
            return agent
        return None
    
    def delete(self, agent_id: int):
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False
    
    def get_by_slug(self, slug: str):
        for agent in self.agents.values():
            if agent.slug == slug:
                return agent
        return None
    
    def exists_by_slug(self, slug: str):
        return any(agent.slug == slug for agent in self.agents.values())
    
    def count(self):
        return len(self.agents)


class MockAgentFactory:
    """Mock for AgentFactory to avoid external API calls"""
    
    @staticmethod
    def get_agent(agent_type):
        """Return a mock agent that simulates AI responses"""
        class MockAIAgent:
            def get_response(self, prompt: str) -> str:
                return f"Mocked AI response to: {prompt}"
        
        return MockAIAgent()


class EnhancedMockAgentService(MockAgentService):
    """Enhanced mock for comprehensive agent router testing"""
    
    def __init__(self):
        super().__init__()
        self.repository = MockAgentRepository()
        self.call_log = []  # Track method calls for verification
    
    def get_all_agents(self):
        self.call_log.append("get_all_agents")
        agents = self.repository.get_all()
        if not agents:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="No agents found")
        return agents
    
    def get_agent_by_id(self, agent_id: int):
        self.call_log.append(f"get_agent_by_id({agent_id})")
        agent = self.repository.get_by_id(agent_id)
        if not agent:
            return None
        return {
            "agent": agent,
            "prompt": f"Prompt for {agent.slug}"
        }
    
    def create_agent(self, agent):
        self.call_log.append(f"create_agent({agent.name})")
        # Simulate validation
        if not agent.name or not agent.slug:
            raise ValueError("Agent name and slug are required")
        
        if self.repository.exists_by_slug(agent.slug):
            raise ValueError(f"Agent with slug '{agent.slug}' already exists")
        
        return self.repository.create(agent)


# =============================================================================
# PYTEST FIXTURES
# =============================================================================

@pytest.fixture
def mock_agent_service():
    """Fixture providing a mock AgentService instance"""
    return MockAgentService()


@pytest.fixture
def mock_pdf_service():
    """Fixture providing a mock PdfService instance"""
    return MockPdfService()


@pytest.fixture
def mock_email_service():
    """Fixture providing a mock EmailService instance"""
    return MockEmailService()


@pytest.fixture
def mock_email_service_with_error():
    """Fixture providing a mock EmailService that raises errors"""
    return MockEmailServiceWithError()


@pytest.fixture
def mock_marketing_agent():
    """Fixture providing a mock MarketingAgent instance"""
    return MockMarketingAgent()


@pytest.fixture
def mock_lifestyle_blog_writer_agent():
    """Fixture providing a mock LifestyleBlogWriterAgent instance"""
    return MockLifestyleBlogWriterAgent()


@pytest.fixture
def mock_tech_blog_writer_agent():
    """Fixture providing a mock TechBlogWriterAgent instance"""
    return MockTechBlogWriterAgent()


@pytest.fixture
def mock_linkedin_writer_agent():
    """Fixture providing a mock LinkedinWriterAgent instance"""
    return MockLinkedinWriterAgent()


@pytest.fixture
def enhanced_mock_agent_service():
    """Fixture providing an enhanced mock AgentService for comprehensive testing"""
    return EnhancedMockAgentService()


@pytest.fixture
def mock_agent_repository():
    """Fixture providing a mock AgentRepository instance"""
    return MockAgentRepository()


@pytest.fixture
def mock_agent_factory():
    """Fixture providing a mock AgentFactory instance"""
    return MockAgentFactory()


# =============================================================================
# TEST CLIENT FIXTURES
# =============================================================================

@pytest.fixture
def test_client():
    """Fixture providing a FastAPI TestClient for the main application"""
    from app.main import app
    client = TestClient(app)
    return client


@pytest.fixture
def test_client_with_mocks(mock_agent_service, mock_email_service, mock_pdf_service):
    """Fixture providing a TestClient with dependency overrides for mocked services"""
    from app.main import app
    from app.service.agent_service import AgentService
    from app.service.email_service import EmailService
    from app.service.pdf_service import PdfService
    
    # Override dependencies with mocks
    app.dependency_overrides[AgentService] = lambda: mock_agent_service
    app.dependency_overrides[EmailService] = lambda: mock_email_service
    app.dependency_overrides[PdfService] = lambda: mock_pdf_service
    
    client = TestClient(app)
    
    yield client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
def test_client_for_agent_router():
    """Fixture providing a TestClient specifically configured for agent router testing"""
    from app.main import app
    from app.service.agent_service import AgentService
    
    # Create enhanced mock for agent router tests
    enhanced_mock = MockAgentService()
    
    # Override only the AgentService dependency
    app.dependency_overrides[AgentService] = lambda: enhanced_mock
    
    client = TestClient(app)
    
    yield client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


# =============================================================================
# UTILITY FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing the path to test data directory"""
    return os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def temp_pdf_dir():
    """Fixture providing a temporary directory for PDF files"""
    pdf_dir = "pdf"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    yield pdf_dir
    
    # Cleanup
    if os.path.exists("pdf/output.pdf"):
        try:
            os.remove("pdf/output.pdf")
        except Exception:
            pass


@pytest.fixture
def sample_test_data():
    """Fixture providing common test data"""
    return {
        "sample_prompt": "Create a blog post about productivity",
        "sample_email": "test@example.com",
        "sample_url": "https://example.com",
        "sample_markdown": "# Test Content\n\nThis is a test markdown content.",
        "sample_agent_request": {
            "prompt": "Hello agent!",
            "user_email": "test@example.com"
        },
        "sample_marketing_request": {
            "url": "https://example.com",
            "user_email": "test@example.com"
        }
    }


# =============================================================================
# MOCK PATCHES
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


# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Session-wide fixture to set up the test environment"""
    # Set test environment variables
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
    os.environ.setdefault("SENDER_EMAIL", "test@example.com")
    os.environ.setdefault("SENDER_PASSWORD", "test-password")
    
    yield
    
    # Cleanup after all tests
    test_files = ["test.db", "agents_storage.db", "agent_storage.db"]
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception:
                pass


# =============================================================================
# CONFIGURATION FOR DIFFERENT TEST TYPES
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_runtest_setup(item):
    """Setup for each test run"""
    # Skip external API calls in unit tests unless explicitly requested
    if "unit" in item.keywords and os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true":
        for marker in item.iter_markers():
            if marker.name == "external_api":
                pytest.skip("Skipping external API calls in unit tests")