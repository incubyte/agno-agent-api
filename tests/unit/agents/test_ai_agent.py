"""
Unit tests for agent functionality using centralized mocks from conftest.py
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional


# Create the FastAPI application for testing
app = FastAPI()


# Define request model
class AgentRequest(BaseModel):
    prompt: str
    user_email: Optional[str] = None


# Create the endpoint using dependency injection
@app.post("/agent")
async def run_agent(
    request: AgentRequest,
    agent_service = Depends(lambda: None),  # Will be overridden in tests
    email_service = Depends(lambda: None),  # Will be overridden in tests
    pdf_service = Depends(lambda: None)     # Will be overridden in tests
):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="prompt must not be empty")
    if not request.user_email:
        raise HTTPException(status_code=400, detail="user_email must not be empty")
    
    response = agent_service.generate_response(request.prompt)
    
    try:
        email_service.connect()
        email_service.send_email(request.user_email, "Agent Response", response)
        email_service.disconnect()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return {"response": response}


# Test client fixture using the centralized mocks
@pytest.fixture
def test_client_with_overrides(mock_agent_service, mock_email_service, mock_pdf_service):
    """Test client with dependency overrides"""
    from app.service.agent_service import AgentService
    from app.service.email_service import EmailService
    from app.service.pdf_service import PdfService
    
    app.dependency_overrides = {
        AgentService: lambda: mock_agent_service,
        EmailService: lambda: mock_email_service,
        PdfService: lambda: mock_pdf_service
    }
    
    client = TestClient(app)
    yield client
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests using centralized fixtures
def test_run_agent(test_client_with_overrides, sample_test_data):
    """Test successful agent response"""
    payload = sample_test_data["sample_agent_request"]
    response = test_client_with_overrides.post("/agent", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked response to: Hello agent!"}


def test_run_agent_empty_prompt_throw_error(test_client_with_overrides):
    """Test error handling for empty prompt"""
    payload = {"prompt": "", "user_email": "test@example.com"}
    response = test_client_with_overrides.post("/agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "prompt must not be empty"}


def test_run_agent_empty_user_email_throw_error(test_client_with_overrides):
    """Test error handling for empty user email"""
    payload = {"prompt": "Hello world!", "user_email": ""}
    response = test_client_with_overrides.post("/agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "user_email must not be empty"}


def test_run_agent_with_email_service_exception(mock_agent_service, mock_email_service_with_error, mock_pdf_service):
    """Test error handling when email service fails"""
    from app.service.agent_service import AgentService
    from app.service.email_service import EmailService
    from app.service.pdf_service import PdfService
    
    # Override with error-throwing email service
    app.dependency_overrides = {
        AgentService: lambda: mock_agent_service,
        EmailService: lambda: mock_email_service_with_error,
        PdfService: lambda: mock_pdf_service
    }
    
    client = TestClient(app)
    
    payload = {"prompt": "Hello agent!", "user_email": "test@example.com"}
    response = client.post("/agent", json=payload)
    
    # Cleanup
    app.dependency_overrides.clear()
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to send email"}


def test_run_agent_with_missing_email(test_client_with_overrides):
    """Test error handling for missing email field"""
    payload = {"prompt": "Hello agent!"}
    response = test_client_with_overrides.post("/agent", json=payload)
    assert response.status_code == 400
