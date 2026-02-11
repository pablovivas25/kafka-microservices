import os
import threading
from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.infrastructure.kafka_consumer import start_consumer
from app.infrastructure.outbox_publisher import publish_events
# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

def run_consumer():
    start_consumer()


def run_outbox():
    publish_events()


@app.on_event("startup")
def startup_event():
    # No levantar threads cuando estamos corriendo tests
    if os.getenv("ENV") != "test":
        threading.Thread(target=run_consumer, daemon=True).start()
        threading.Thread(target=run_outbox, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok"}
