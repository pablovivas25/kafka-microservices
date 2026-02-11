import time
import json
from sqlalchemy.orm import Session
from kafka import KafkaProducer
from app.infrastructure.database import SessionLocal
from app.domain.models.outbox import Outbox


producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def publish_events():

    while True:
        db: Session = SessionLocal()

        try:
            events = db.query(Outbox).filter(Outbox.published == False).all()

            for event in events:
                producer.send("orders",{"event_id": str(event.id),  # 👈 ESTE ES EL EVENT ID
                "event_type": event.event_type,
                **json.loads(event.payload)
                })
                producer.flush()

                event.published = True
                db.commit()

        except Exception as e:
            db.rollback()
            print("Error publishing event:", e)

        finally:
            db.close()

        time.sleep(5)  # cada 5 segundos
