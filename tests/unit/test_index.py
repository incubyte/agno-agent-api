import os
import sys
from unittest.mock import MagicMock

sys.modules['routers'] = MagicMock()
sys.modules['routers.agent'] = MagicMock()
sys.modules['core'] = MagicMock()
sys.modules['core.settings'] = MagicMock()

sys.modules['app.main'] = MagicMock()
sys.modules['app.core'] = MagicMock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "index",
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/routers/index.py'))
)
index_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index_module)

def test_read_root():
    response = index_module.read_root()

    assert isinstance(response, dict)
    assert "message" in response
    assert response["message"] == "Hello, FastAPI!"
    assert response == {"message": "Hello, FastAPI!"}