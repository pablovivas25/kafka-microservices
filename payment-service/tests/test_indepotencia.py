import uuid
from app.infrastructure.kafka_consumer import handle_event
from app.infrastructure.database import SessionLocal
from app.domain.models.payment import Payment


def test_event_not_processed_twice():
    event_id = uuid.uuid4()
    order_id = uuid.uuid4()

    event = {
        "event_id": str(event_id),
        "event_type": "OrderCreated",
        "order_id": str(order_id),
        "amount": 200.0
    }

    handle_event(event)
    handle_event(event)  # procesamos dos veces

    db = SessionLocal()
    payments = db.query(Payment).filter_by(order_id=order_id).all()

    assert len(payments) == 1
