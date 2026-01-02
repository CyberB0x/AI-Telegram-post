from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/telegram", tags=["Telegram"])


class TelegramMessage(BaseModel):
    text: str


@router.post("/send")
async def send_message(data: TelegramMessage):
    return {"status": "ok", "text": data.text}
