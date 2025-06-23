"""
Base test configuration for the Agno AI API test suite.
This file contains only shared utilities and path setup.
Specific mocking is handled in unit/conftest.py and e2e/conftest.py
"""
import os
import sys
import pytest

# Add the parent directory to sys.path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# =============================================================================
# SHARED CONFIGURATION FOR ALL TEST TYPES
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


# =============================================================================
# SHARED ENVIRONMENT SETUP
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Session-wide fixture to set up the test environment"""
    # Set test environment variables
    os.environ.setdefault("ENVIRONMENT", "test")
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
# SHARED UTILITY FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing the path to test data directory"""
    return os.path.join(os.path.dirname(__file__), "data")


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
