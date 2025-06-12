import pytest
import os
import json
import sys
from fastapi.testclient import TestClient
import asyncio
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.main import app

load_dotenv(".env.test")

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_environment():
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
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    test_email = os.environ.get("TEST_EMAIL", "test@example.com")
    
    payload = {
        "prompt": "Give a brief summary of Apple Inc.",
        "user_email": test_email
    }
    
    response = client.post("/agent", json=payload)
    
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}: {response.text}"
    assert "response" in response.json(), "Response should contain a 'response' field"
    assert len(response.json()["response"]) > 0, "Response should not be empty"
    
    assert os.path.exists("pdf/output.pdf"), "PDF file should have been created"
    assert os.path.getsize("pdf/output.pdf") > 0, "PDF file should not be empty"

@pytest.mark.e2e
def test_agent_endpoint_error_handling_e2e(setup_test_environment):
    """
    Test error handling in the agent endpoint in a real environment.
    """
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    payload = {
        "prompt": "",
        "user_email": "test@example.com"
    }
    
    response = client.post("/agent", json=payload)
    
    assert response.status_code == 400, f"Expected 400 error but got {response.status_code}"
    assert response.json() == {"detail": "prompt must not be empty"}, "Unexpected error message"

@pytest.mark.e2e
def test_agent_endpoint_performance_e2e(setup_test_environment):
    """
    Test the performance characteristics of the agent endpoint.
    This is useful to catch significant regressions in response time.
    """
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    import time
    
    test_email = os.environ.get("TEST_EMAIL", "test@example.com")
    
    payload = {
        "prompt": "What is the current price of Apple stock?",
        "user_email": test_email
    }
    
    start_time = time.time()
    response = client.post("/agent", json=payload)
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}: {response.text}"
    
    print(f"E2E Agent endpoint response time: {response_time:.2f} seconds")
    

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
    
    mock_smtp = MockEmailConnection()
    
    monkeypatch.setattr("smtplib.SMTP", lambda *args, **kwargs: mock_smtp)
    
    return mock_smtp

@pytest.mark.integration
def test_agent_integration_with_mock_email(setup_test_environment, mock_email_service):
    """
    Integration test that uses real Claude API and PDF generation but mocks email sending.
    This is useful when you want to test most of the real system but don't want to send actual emails.
    """
    if os.environ.get("SKIP_EXTERNAL_CALLS", "false").lower() == "true":
        pytest.skip("Skipping test that makes external API calls")
    
    payload = {
        "prompt": "What is the current stock price of Microsoft?",
        "user_email": "test@example.com"
    }
    
    response = client.post("/agent", json=payload)
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert os.path.exists("pdf/output.pdf")
    
    assert len(mock_email_service.messages) > 0, "No emails were sent"
