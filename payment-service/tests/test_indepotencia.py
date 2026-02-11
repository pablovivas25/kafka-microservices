import uuid

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
    repo = PaymentRepository(db)

    payments = repo.get_all_by_order_id(order_id)

    assert len(payments) == 1

    db.close()
