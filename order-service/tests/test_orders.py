import os
os.environ["ENV"] = "test"

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_order():
    response = client.post("/orders", json={
        "user_id": str(uuid.uuid4()),
        "amount": 100
    })

    assert response.status_code == 201
    assert "id" in response.json()
