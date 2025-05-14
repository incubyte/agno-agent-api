from routers import router as index_router

def test_read_root():
    response = index_router.read_root()

    assert isinstance(response, dict)
    assert "message" in response
    assert response["message"] == "Hello, FastAPI!"
    assert response == {"message": "Hello, FastAPI!"}