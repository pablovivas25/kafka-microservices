from app.infrastructure.database import SessionLocal
from app.domain.models.outbox import Outbox

def test_outbox_created(client):
    response = client.post("/orders", json={
        "user_id": "11111111-1111-1111-1111-111111111111",
        "amount": 50
    })

    db = SessionLocal()
    events = db.query(Outbox).all()
    db.close()
    assert events[0].event_type == "OrderCreated"
