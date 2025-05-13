import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
import os
import json
from service.agent_service import AgentService
from service.pdf_service import PdfService
from service.email_service import EmailService

client = TestClient(app)

# Mock classes for services
class MockAgentService:
    def generate_response(self, prompt: str) -> str:
        return f"Mocked e2e response for: {prompt}"

class MockPdfService:
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown_text
        return

    def save_pdf_file(self):
        # Create mock PDF file for testing
        os.makedirs('pdf', exist_ok=True)
        with open('pdf/output.pdf', 'w') as f:
            f.write("Mock PDF content")
        return

class MockEmailService:
    def connect(self):
        return

    def send_email(self, to_email, subject, body, pdf_path=None):
        return

    def disconnect(self):
        return

class MockEmailServiceWithError:
    def connect(self):
        return
    
    def send_email(self, to_email, subject, body, pdf_path=None):
        raise Exception("Email service error")
    
    def disconnect(self):
        return


@pytest.fixture(scope="function")
def setup_mocks():
    # Save original dependencies
    original_overrides = app.dependency_overrides.copy()
    
    # Set mock dependencies
    app.dependency_overrides[AgentService] = lambda: MockAgentService()
    app.dependency_overrides[PdfService] = lambda: MockPdfService()
    app.dependency_overrides[EmailService] = lambda: MockEmailService()
    
    # Ensure the pdf directory exists
    os.makedirs('pdf', exist_ok=True)
    
    yield
    
    # Cleanup
    app.dependency_overrides = original_overrides
    
    # Clean up test PDF if it exists
    if os.path.exists('pdf/output.pdf'):
        os.remove('pdf/output.pdf')


def test_agent_endpoint_successful_request(setup_mocks):
    """Test that the agent endpoint successfully processes a valid request."""
    # Arrange
    payload = {"prompt": "Analyze AAPL stock", "user_email": "test@example.com"}
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked e2e response for: Analyze AAPL stock"}
    assert os.path.exists('pdf/output.pdf'), "PDF file should be created"


def test_agent_endpoint_empty_prompt(setup_mocks):
    """Test that the agent endpoint rejects requests with empty prompts."""
    # Arrange
    payload = {"prompt": "", "user_email": "test@example.com"}
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "prompt must not be empty"}


def test_agent_endpoint_empty_email(setup_mocks):
    """Test that the agent endpoint rejects requests with empty email addresses."""
    # Arrange
    payload = {"prompt": "Analyze AAPL stock", "user_email": ""}
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "user_email must not be empty"}


def test_agent_endpoint_missing_fields(setup_mocks):
    """Test that the agent endpoint validates required fields."""
    # Arrange
    payload_missing_prompt = {"user_email": "test@example.com"}
    payload_missing_email = {"prompt": "Analyze AAPL stock"}
    
    # Act
    response1 = client.post("/agent", json=payload_missing_prompt)
    response2 = client.post("/agent", json=payload_missing_email)
    
    # Assert
    assert response1.status_code == 422  # Validation error
    assert response2.status_code == 422  # Validation error


def test_agent_endpoint_email_failure(setup_mocks):
    """Test that the agent endpoint handles email service failures correctly."""
    # Override the email service with one that throws an exception
    app.dependency_overrides[EmailService] = lambda: MockEmailServiceWithError()
    
    # Arrange
    payload = {"prompt": "Analyze AAPL stock", "user_email": "test@example.com"}
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to send email"}
    
    # Reset the mock for other tests
    app.dependency_overrides[EmailService] = lambda: MockEmailService()


def test_agent_endpoint_invalid_email_format(setup_mocks):
    """Test that requests with invalid email formats are handled."""
    # Arrange
    payload = {"prompt": "Analyze AAPL stock", "user_email": "invalid-email"}
    
    # Act
    response = client.post("/agent", json=payload)
    
    # Note: This test may fail if the API doesn't validate email formats.
    # If email validation is added later, this test should pass.
    # For now, we expect it to succeed since current implementation doesn't validate email format
    
    # Assert
    assert response.status_code == 200  # Currently no email validation


def test_agent_endpoint_unsupported_methods(setup_mocks):
    """Test that unsupported HTTP methods are rejected."""
    # Act
    response_get = client.get("/agent")
    response_put = client.put("/agent")
    response_delete = client.delete("/agent")
    
    # Assert
    assert response_get.status_code == 405  # Method not allowed
    assert response_put.status_code == 405  # Method not allowed
    assert response_delete.status_code == 405  # Method not allowed