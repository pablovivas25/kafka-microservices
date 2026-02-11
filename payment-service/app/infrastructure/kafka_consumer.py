import os
import json
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import PaymentRepository
import uuid

def create_consumer():
    return KafkaConsumer(
        "orders",
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        group_id="payment-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

def start_consumer():
    consumer = create_consumer()
    
    for message in consumer:
        event = message.value
        handle_event(event)

def handle_event(event):
    db: Session = SessionLocal()

    try:
        repo = PaymentRepository(db)
        event_id = uuid.UUID(event["event_id"])

        if repo.event_already_processed(event_id):
            print("Evento duplicado, ignorando...")
            return

        repo.create_payment(
            order_id=uuid.UUID(event["order_id"]),
            amount=event["amount"]
        )

        repo.mark_event_processed(event_id)

        db.commit()
        print("Pago creado correctamente")

    except Exception as e:
        db.rollback()
        print("Error procesando evento:", e)

    finally:
        db.close()
