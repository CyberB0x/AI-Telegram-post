from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine

from app import models
from app.api.endpoints import router as api_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(api_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}



