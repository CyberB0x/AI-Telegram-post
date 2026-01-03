from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.schedule import SchedulePostRequest
from app.services.scheduler import schedule_post

router = APIRouter(prefix="/api", tags=["Scheduler"])


@router.post("/schedule")
async def schedule_message(
    data: SchedulePostRequest,
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(
            schedule_post,
            data.text,
            data.publish_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "scheduled",
        "publish_at": data.publish_at
    }
