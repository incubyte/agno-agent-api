import pytest
from fastapi.testclient import TestClient
from app.service import AgentService
from app.service import PdfService
from app.service import EmailService
from app.main import app


class MockAgentService:
    def generate_response(self, prompt: str) -> str:
        return f"Mocked response to: {prompt}"


class MockPdfService:
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown_text
        return

    def save_pdf_file(self):
        return


class MockEmailService:
    def connect(self):
        return

    def send_email(self, to_email, subject, body, pdf_path=None):
        return

    def disconnect(self):
        return


@pytest.fixture(scope="class")
def test_client():
    # Override all dependencies with mocks
    app.dependency_overrides[AgentService] = lambda: MockAgentService()
    app.dependency_overrides[PdfService] = lambda: MockPdfService()
    app.dependency_overrides[EmailService] = lambda: MockEmailService()
    
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.mark.usefixtures("test_client")
class TestAgent:
    def test_run_agent(self, test_client):
        payload = {"prompt": "Hello agent!", "user_email": "test@example.com"}
        response = test_client.post("/agent", json=payload)
        assert response.status_code == 200
        assert response.json() == {"response": "Mocked response to: Hello agent!"}    

    def test_run_agent_empty_prompt_throw_error(self, test_client):
        payload = {"prompt": "", "user_email": "test@example.com"}
        response = test_client.post("/agent", json=payload)
        print(response)
        assert response.status_code == 400
        assert response.json() == {"detail": "prompt must not be empty"}

    def test_run_agent_empty_user_email_throw_error(self, test_client):
        payload = {"prompt": "Hello world!", "user_email": ""}
        response = test_client.post("/agent", json=payload)
        print(response)
        assert response.status_code == 400
        assert response.json() == {"detail": "user_email must not be empty"}
    
    def test_run_agent_with_email_service_exception(self, test_client, monkeypatch):
        class MockEmailServiceWithError:
            def connect(self):
                return
            
            def send_email(self, to_email, subject, body, pdf_path=None):
                raise Exception("Email service error")
            
            def disconnect(self):
                return

        app.dependency_overrides[EmailService] = lambda: MockEmailServiceWithError()
        
        payload = {"prompt": "Hello agent!", "user_email": "test@example.com"}
        response = test_client.post("/agent", json=payload)
        
        app.dependency_overrides[EmailService] = lambda: MockEmailService()
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to send email"}
    
    def test_run_agent_with_missing_email(self, test_client):
        payload = {"prompt": "Hello agent!"}
        response = test_client.post("/agent", json=payload)
        assert response.status_code == 422
