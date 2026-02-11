import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Importante: modo test
os.environ["ENV"] = "test"

@pytest.fixture
def client():
    return TestClient(app)
