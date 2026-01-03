from fastapi import FastAPI
from datetime import datetime, timezone

from app.config import settings
from app.database import engine, SessionLocal, Base
from app.models import ScheduledPost

from app.api.endpoints import router as api_router
from app.api.schedule import router as schedule_router

from app.scheduler.instance import scheduler
from app.scheduler.tasks import send_scheduled_post

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(api_router)
app.include_router(schedule_router)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

    scheduler.start()

    db = SessionLocal()
    now = datetime.now(timezone.utc)

    posts = db.query(ScheduledPost).filter(
        ScheduledPost.status == "scheduled"
    ).all()

    for post in posts:
        publish_at = post.publish_at

        # SQLite → UTC
        if publish_at.tzinfo is None:
            publish_at = publish_at.replace(tzinfo=timezone.utc)

        if publish_at <= now:
            post.status = "failed"
            continue

        scheduler.add_job(
            send_scheduled_post,
            trigger="date",
            run_date=publish_at,
            args=[post.id],
            id=f"post_{post.id}",
            replace_existing=True,
            misfire_grace_time=300
        )

    db.commit()
    db.close()


@app.get("/")
def healthcheck():
    return {"status": "ok"}
