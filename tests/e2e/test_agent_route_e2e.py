import pytest
import os
import json
import sys
from fastapi.testclient import TestClient
import asyncio
from dotenv import load_dotenv

# Add the parent directory to sys.path to make the main module importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now we can import from the root of the project
from main import app

# Load environment variables from .env.test file (create this file for testing)
load_dotenv(".env.test")

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_environment():
    """
    Set up the test environment for E2E tests.
    This includes ensuring required environment variables are set.
    """
    # Check if required environment variables are set for E2E tests
    required_vars = ["ANTHROPIC_API_KEY", "SENDER_EMAIL", "SENDER_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        pytest.skip(f"E2E tests skipped. Missing environment variables: {', '.join(missing_vars)}")
    
    # Create output directory if it doesn't exist
    os.makedirs("pdf", exist_ok=True)
    
    yield
    
    # Clean up any test artifacts (if needed)
    if os.path.exists("pdf/output.pdf"):
        try:
            os.remove("pdf/output.pdf")
        except Exception as e:
            print(f"Warning: Could not remove test PDF: {e}")

@pytest.mark.e2e
def test_agent_endpoint_e2e(setup_test_environment):
    """
    True E2E test that tests the complete flow with real services.
    This test actually calls Claude API, generates a PDF, and attempts to send an email.
    """
    # Check if we should run full E2E tests including external API calls
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    # Use a test email that you control
    test_email = os.environ.get("TEST_EMAIL", "test@example.com")
    
    # Arrange - prepare a simple query
    payload = {
        "prompt": "Give a brief summary of Apple Inc.",
        "user_email": test_email
    }
    
    # Act - make the actual API call
    response = client.post("/agent", json=payload)
    
    # Assert - verify the response and side effects
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}: {response.text}"
    assert "response" in response.json(), "Response should contain a 'response' field"
    assert len(response.json()["response"]) > 0, "Response should not be empty"
    
    # Verify PDF was created
    assert os.path.exists("pdf/output.pdf"), "PDF file should have been created"
    assert os.path.getsize("pdf/output.pdf") > 0, "PDF file should not be empty"
    
    # Note: We can't easily verify email delivery in an automated test
    # In a complete E2E testing setup, you might have an email inbox API to check delivery

@pytest.mark.e2e
def test_agent_endpoint_error_handling_e2e(setup_test_environment):
    """
    Test error handling in the agent endpoint in a real environment.
    """
    # Check if we should run full E2E tests
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    # Test with a deliberately malformed request
    payload = {
        "prompt": "",  # Empty prompt should cause a validation error
        "user_email": "test@example.com"
    }
    
    response = client.post("/agent", json=payload)
    
    # Check that we get the expected error
    assert response.status_code == 400, f"Expected 400 error but got {response.status_code}"
    assert response.json() == {"detail": "prompt must not be empty"}, "Unexpected error message"

@pytest.mark.e2e
def test_agent_endpoint_performance_e2e(setup_test_environment):
    """
    Test the performance characteristics of the agent endpoint.
    This is useful to catch significant regressions in response time.
    """
    # Check if we should run full E2E tests
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    import time
    
    # Use a test email that you control
    test_email = os.environ.get("TEST_EMAIL", "test@example.com")
    
    # Arrange - prepare a simple query
    payload = {
        "prompt": "What is the current price of Apple stock?",
        "user_email": test_email
    }
    
    # Act - time the API call
    start_time = time.time()
    response = client.post("/agent", json=payload)
    end_time = time.time()
    
    # Assert - verify response time is within acceptable limits
    response_time = end_time - start_time
    
    # Assert basic response validity
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}: {response.text}"
    
    # Log the response time - in a real CI/CD environment, this could be tracked over time
    print(f"E2E Agent endpoint response time: {response_time:.2f} seconds")
    
    # Optional: Set a maximum acceptable response time
    # Note: This might need adjustment based on your specific API and requirements
    # max_response_time = 30  # seconds
    # assert response_time < max_response_time, f"Response time {response_time:.2f}s exceeds maximum allowed {max_response_time}s"

# Note: The following are integration tests that use the real API but mock out parts like email sending
# They're a middle ground between unit tests and full E2E tests

@pytest.fixture(scope="function")
def mock_email_service(monkeypatch):
    """Mock just the email service while using real Claude API and PDF generation"""
    class MockEmailConnection:
        def __init__(self, *args, **kwargs):
            self.messages = []
        
        def starttls(self):
            pass
            
        def login(self, *args, **kwargs):
            pass
            
        def sendmail(self, from_addr, to_addrs, msg):
            self.messages.append((from_addr, to_addrs, msg))
        
        def send_message(self, msg):
            self.messages.append(msg)
            
        def quit(self):
            pass
    
    # Create a mock SMTP instance
    mock_smtp = MockEmailConnection()
    
    # Replace the SMTP class with our mock
    monkeypatch.setattr("smtplib.SMTP", lambda *args, **kwargs: mock_smtp)
    
    return mock_smtp

@pytest.mark.integration
def test_agent_integration_with_mock_email(setup_test_environment, mock_email_service):
    """
    Integration test that uses real Claude API and PDF generation but mocks email sending.
    This is useful when you want to test most of the real system but don't want to send actual emails.
    """
    # Check if we should run integration tests with external APIs
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    # Arrange
    payload = {
        "prompt": "What is the current stock price of Microsoft?",
        "user_email": "test@example.com"
    }
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert "response" in response.json()
    assert os.path.exists("pdf/output.pdf")
    
    # Verify the mock email service was called
    # In a real test, you might want to verify the email contents more thoroughly
    assert len(mock_email_service.messages) > 0, "No emails were sent"
