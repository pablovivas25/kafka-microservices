import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    os.environ["ENV"] = "test"  # Evita que levante threads
    return TestClient(app)
