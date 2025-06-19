"""
Unit tests for the index router.
Tests the index router functionality in isolation from routers/index.py
"""
import os
import sys
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the project root to sys.path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.routers.index import router as index_router


@pytest.fixture
def test_app():
    """Create a test FastAPI app with only the index router."""
    app = FastAPI()
    app.include_router(index_router)
    return app


@pytest.fixture
def test_client(test_app):
    """Create a test client for the index router."""
    return TestClient(test_app)


@pytest.mark.unit
def test_index_router_get_root(test_client):
    """Test that the index router root endpoint returns the expected response."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


@pytest.mark.unit
def test_index_router_unsupported_methods(test_client):
    """Test that unsupported HTTP methods return 405 Method Not Allowed."""
    # Test POST
    response = test_client.post("/")
    assert response.status_code == 405
    
    # Test PUT
    response = test_client.put("/")
    assert response.status_code == 405
    
    # Test DELETE
    response = test_client.delete("/")
    assert response.status_code == 405
    
    # Test PATCH
    response = test_client.patch("/")
    assert response.status_code == 405


@pytest.mark.unit
def test_index_router_response_type(test_client):
    """Test that the response is JSON with the correct content type."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert isinstance(response.json(), dict)


@pytest.mark.unit
def test_index_router_message_content(test_client):
    """Test the specific content of the response message."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Verify response structure
    assert "message" in json_response
    assert len(json_response) == 1  # Only one key
    assert json_response["message"] == "Hello, FastAPI!"
    assert isinstance(json_response["message"], str)


@pytest.mark.unit
def test_index_router_consistency(test_client):
    """Test that multiple calls return consistent results."""
    responses = [test_client.get("/") for _ in range(5)]
    
    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, FastAPI!"}


@pytest.mark.unit
def test_index_router_isolation():
    """Test that the index router works in isolation without other routers."""
    app = FastAPI()
    app.include_router(index_router)
    client = TestClient(app)
    
    # Should work
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}
    
    # Other routes should not exist
    response = client.get("/agent")
    assert response.status_code == 404  # Not found since agent router not included
