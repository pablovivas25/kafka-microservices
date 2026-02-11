import time
import json
from kafka import KafkaProducer
from app.infrastructure.database import SessionLocal
from app.domain.models.outbox import Outbox

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_events():
    while True:
        db = SessionLocal()

        events = db.query(Outbox).filter_by(published=False).all()

        for event in events:
            producer.send("payments", json.loads(event.payload))
            event.published = True

        db.commit()
        db.close()

        time.sleep(5)
