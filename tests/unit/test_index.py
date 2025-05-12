from routes import index

def test_read_root():
    response = index.read_root()
    
    assert isinstance(response, dict)
    assert "message" in response
    assert response["message"] == "Hello, FastAPI!"
    assert response == {"message": "Hello, FastAPI!"}