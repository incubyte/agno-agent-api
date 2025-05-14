import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello_root_get():
    """Test that the root endpoint returns the expected message with 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_hello_root_unsupported_methods():
    """Test that unsupported HTTP methods are rejected appropriately."""
    response = client.post("/")
    assert response.status_code == 405

    response = client.put("/")
    
    response = client.delete("/")
    assert response.status_code == 405


def test_hello_root_response_headers():
    """Test that the response includes the expected headers."""
    response = client.get("/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_hello_root_response_time():
    """Test that the root endpoint responds within a reasonable time."""
    start_time = time.time()
    response = client.get("/")
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 1.0