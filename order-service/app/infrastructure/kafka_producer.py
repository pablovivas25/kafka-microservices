import os
import json
import uuid
from kafka import KafkaProducer
from kafka.errors import KafkaError

def create_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",        # Espera confirmación de todos los replicas
        retries=5,         # Reintentos automáticos
    )

def get_producer():
  return create_producer()

def publish_order_created(order):
    producer=get_producer()
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "OrderCreated",
        "order_id": str(order.id),
        "user_id": str(order.user_id),
        "amount": float(order.amount)
    }

    try:
        future = producer.send("orders", event)
        record_metadata = future.get(timeout=10)  # Espera confirmación real

        print(
            f"Evento enviado a {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}"
        )

    except KafkaError as e:
        print("Error enviando evento a Kafka:", e)
        raise
