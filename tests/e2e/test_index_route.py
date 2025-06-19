"""
E2E tests for the index router endpoints.
Tests the actual behavior of the index router in routers/index.py
"""
import os
import sys
import time
import pytest
from fastapi.testclient import TestClient

# Add the project root to sys.path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app

client = TestClient(app)


@pytest.mark.e2e
def test_hello_root_get():
    """Test that the root endpoint returns the expected message with 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


@pytest.mark.e2e
def test_hello_root_unsupported_methods():
    """Test that unsupported HTTP methods are rejected appropriately."""
    # Test POST method
    response = client.post("/")
    assert response.status_code == 405
    
    # Test PUT method
    response = client.put("/")
    assert response.status_code == 405
    
    # Test DELETE method
    response = client.delete("/")
    assert response.status_code == 405
    
    # Test PATCH method
    response = client.patch("/")
    assert response.status_code == 405





 # Should respond within 1 second


@pytest.mark.e2e
def test_hello_root_response_structure():
    """Test that the response has the correct structure and data types."""
    response = client.get("/")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Verify response structure
    assert isinstance(json_response, dict)
    assert "message" in json_response
    assert isinstance(json_response["message"], str)
    assert json_response["message"] == "Hello, FastAPI!"

