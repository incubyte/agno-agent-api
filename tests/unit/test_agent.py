import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional


# Define simple service classes
class AgentService:
    def generate_response(self, prompt: str) -> str:
        return f"Mocked response to: {prompt}"


class PdfService:
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown_text
        return

    def save_pdf_file(self):
        return


class EmailService:
    def connect(self):
        return

    def send_email(self, to_email, subject, body, pdf_path=None):
        return

    def disconnect(self):
        return


# Mock error class for testing exceptions
class EmailServiceWithError(EmailService):
    def send_email(self, to_email, subject, body, pdf_path=None):
        raise Exception("Email service error")


# Create the FastAPI application
app = FastAPI()


# Define request model
class AgentRequest(BaseModel):
    prompt: str
    user_email: Optional[str] = None


# Create the endpoint
@app.post("/agent")
async def run_agent(
    request: AgentRequest,
    agent_service: AgentService = Depends(AgentService),
    email_service: EmailService = Depends(EmailService),
    pdf_service: PdfService = Depends(PdfService)
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


# Test client fixture
@pytest.fixture
def test_client():
    client = TestClient(app)
    return client


# Tests
def test_run_agent(test_client):
    payload = {"prompt": "Hello agent!", "user_email": "test@example.com"}
    response = test_client.post("/agent", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked response to: Hello agent!"}


def test_run_agent_empty_prompt_throw_error(test_client):
    payload = {"prompt": "", "user_email": "test@example.com"}
    response = test_client.post("/agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "prompt must not be empty"}


def test_run_agent_empty_user_email_throw_error(test_client):
    payload = {"prompt": "Hello world!", "user_email": ""}
    response = test_client.post("/agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "user_email must not be empty"}


def test_run_agent_with_email_service_exception(test_client):
    # Override the dependency with our error-raising version
    original_dependency = app.dependency_overrides.get(EmailService, None)
    app.dependency_overrides[EmailService] = lambda: EmailServiceWithError()
    
    payload = {"prompt": "Hello agent!", "user_email": "test@example.com"}
    response = test_client.post("/agent", json=payload)
    
    # Reset the dependency override
    if original_dependency:
        app.dependency_overrides[EmailService] = original_dependency
    else:
        del app.dependency_overrides[EmailService]
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to send email"}


def test_run_agent_with_missing_email(test_client):
    payload = {"prompt": "Hello agent!"}
    response = test_client.post("/agent", json=payload)
    assert response.status_code == 400
