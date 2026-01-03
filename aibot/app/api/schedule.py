from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.schedule import SchedulePostRequest
from app.services.scheduler import schedule_post
from datetime import timezone

router = APIRouter(prefix="/api", tags=["Scheduler"])


@router.post("/schedule")
async def schedule_message(data: SchedulePostRequest):
    publish_at = data.publish_at

    # НОРМАЛИЗАЦИЯ В UTC
    if publish_at.tzinfo is None:
        publish_at = publish_at.replace(tzinfo=timezone.utc)
    else:
        publish_at = publish_at.astimezone(timezone.utc)

    try:
        await schedule_post(
            text=data.text,
            publish_at=publish_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "scheduled",
        "publish_at": publish_at
    }

