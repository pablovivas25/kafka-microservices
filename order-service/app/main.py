import os
import threading

from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.api.routes import router
from app.infrastructure.outbox_publisher import publish_events


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup_event():
    if os.getenv("ENV") != "test":
        thread = threading.Thread(target=publish_events)
        thread.daemon = True
        thread.start()

@app.get("/health")
def health():
    return {"status": "ok"}
