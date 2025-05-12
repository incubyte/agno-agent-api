from service.agent_service import AgentService
from fastapi.testclient import TestClient
from main import app


# Mock the AgentService for testing
class MockAgentService:
    def generate_response(self, prompt: str) -> str:
        return f"Mocked response to: {prompt}"
    
app.dependency_overrides[AgentService] = lambda: MockAgentService()

client = TestClient(app)

def test_run_agent():
    payload = {"prompt": "Hello agent!"}
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked response to: Hello agent!"}

def test_run_agent_empty_prompt_throw_error():
    payload = {"prompt": ""}
    response = client.post("/agent", json=payload)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "prompt must not be empty"
    }

