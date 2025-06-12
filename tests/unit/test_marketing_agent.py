import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

class MarketingAgent:
    def run_marketing_agent(self, url: str) -> str:
        return f"Mocked marketing analysis for: {url}"


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


class EmailServiceWithError(EmailService):
    def send_email(self, to_email, subject, body, pdf_path=None):
        raise Exception("Email service error")


app = FastAPI()


class MarketingAgentRequest(BaseModel):
    url: str
    user_email: str


@app.post("/run-marketing-agent")
async def run_marketing_agent(
    request: MarketingAgentRequest,
    pdf_service: PdfService = Depends(PdfService),
    email_service: EmailService = Depends(EmailService)
):
    if not request.url:
        raise HTTPException(status_code=400, detail="url must not be empty")
    if not request.user_email:
        raise HTTPException(status_code=400, detail="user_email must not be empty")
    
    marketing_agent = MarketingAgent()
    response = marketing_agent.run_marketing_agent(request.url)
    clean_response = response.lstrip()
    
    pdf_service.convert_markdown_to_html(clean_response)
    pdf_service.save_pdf_file()
    
    try:
        email_service.connect()
        email_service.send_email(
            to_email=request.user_email,
            subject="Test Email",
            body="Please find the attached PDF.",
            pdf_path="pdf/output.pdf"
        )
        email_service.disconnect()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return {"response": clean_response}


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client


def test_run_marketing_agent(test_client):
    payload = {"url": "https://example.com", "user_email": "test@example.com"}
    response = test_client.post("/run-marketing-agent", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked marketing analysis for: https://example.com"}


def test_run_marketing_agent_empty_url_throw_error(test_client):
    payload = {"url": "", "user_email": "test@example.com"}
    response = test_client.post("/run-marketing-agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "url must not be empty"}


def test_run_marketing_agent_empty_user_email_throw_error(test_client):
    payload = {"url": "https://example.com", "user_email": ""}
    response = test_client.post("/run-marketing-agent", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "user_email must not be empty"}


@pytest.fixture
def test_client_with_email_error():
    app.dependency_overrides[EmailService] = EmailServiceWithError
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


def test_run_marketing_agent_email_service_error(test_client_with_email_error):
    payload = {"url": "https://example.com", "user_email": "test@example.com"}
    response = test_client_with_email_error.post("/run-marketing-agent", json=payload)
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to send email"}
