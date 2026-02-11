import uuid
from app.infrastructure.kafka_consumer import handle_event
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import PaymentRepository

def test_payment_created():
    event_id = uuid.uuid4()
    order_id = uuid.uuid4()

    event = {
        "event_id": str(event_id),
        "event_type": "OrderCreated",
        "order_id": str(order_id),
        "amount": 150.0
    }

    handle_event(event)

    db = SessionLocal()
    repo = PaymentRepository(db)

    payment = repo.get_by_order_id(order_id)

    assert payment is not None
    assert payment.amount == 150.0

    db.close()

