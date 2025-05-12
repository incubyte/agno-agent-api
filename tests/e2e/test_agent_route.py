import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_run_agent():    
    payload = {"prompt": "write some poem"}
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json().get("response"), str)