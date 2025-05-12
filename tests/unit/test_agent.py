import pytest
from fastapi.testclient import TestClient
from service.agent_service import AgentService
from main import app


class MockAgentService:
    def generate_response(self, prompt: str) -> str:
        return f"Mocked response to: {prompt}"


@pytest.fixture(scope="class")
def test_client():
    app.dependency_overrides[AgentService] = lambda: MockAgentService()
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.mark.usefixtures("test_client")
class TestAgent:
    def test_run_agent(self, test_client):
        payload = {"prompt": "Hello agent!"}
        response = test_client.post("/agent", json=payload)
        assert response.status_code == 200
        assert response.json() == {"response": "Mocked response to: Hello agent!"}

    def test_run_agent_empty_prompt_throw_error(self, test_client):
        payload = {"prompt": ""}
        response = test_client.post("/agent", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "prompt must not be empty"}
