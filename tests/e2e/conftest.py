"""
E2E specific test configuration.
This file adds E2E specific configurations and fixtures.
The main conftest.py fixtures are automatically available in E2E tests.
"""
import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project root to sys.path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load test environment variables
load_dotenv(".env.test")


@pytest.fixture(scope="module")
def setup_e2e_test_environment():
    """
    Set up the test environment for E2E tests.
    This includes ensuring required environment variables are set.
    """
    required_vars = ["ANTHROPIC_API_KEY", "SENDER_EMAIL", "SENDER_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        pytest.skip(f"E2E tests skipped. Missing environment variables: {', '.join(missing_vars)}")

    os.makedirs("pdf", exist_ok=True)
    
    yield
    
    # Cleanup
    if os.path.exists("pdf/output.pdf"):
        try:
            os.remove("pdf/output.pdf")
        except Exception as e:
            print(f"Warning: Could not remove test PDF: {e}")


@pytest.fixture
def e2e_test_client():
    """E2E specific test client that uses real services instead of mocks"""
    from app.main import app
    from fastapi.testclient import TestClient
    
    # Ensure no dependency overrides for E2E tests
    app.dependency_overrides.clear()
    
    client = TestClient(app)
    return client
