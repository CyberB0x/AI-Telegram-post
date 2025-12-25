from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine

from app import models

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
