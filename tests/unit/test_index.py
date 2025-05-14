import os
import sys
from unittest.mock import MagicMock

# Mock all the necessary modules before they are imported
sys.modules['routers'] = MagicMock()
sys.modules['routers.agent'] = MagicMock()
sys.modules['core'] = MagicMock()
sys.modules['core.settings'] = MagicMock()

# Mock the app modules to avoid circular imports
sys.modules['app.main'] = MagicMock()
sys.modules['app.core'] = MagicMock()

# Add the project root to the Python path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import only the specific module we want to test
import importlib.util
spec = importlib.util.spec_from_file_location(
    "index",
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/routers/index.py'))
)
index_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index_module)

def test_read_root():
    # In FastAPI, the route handler is not a method of the router
    # We need to access the function directly from the module
    response = index_module.read_root()

    assert isinstance(response, dict)
    assert "message" in response
    assert response["message"] == "Hello, FastAPI!"
    assert response == {"message": "Hello, FastAPI!"}