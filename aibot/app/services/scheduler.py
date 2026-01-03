import asyncio
from datetime import datetime, timezone
from app.telegram.bot import TelegramBot


async def schedule_post(text: str, publish_at: datetime):
    now = datetime.now(timezone.utc)

    delay = (publish_at - now).total_seconds()

    if delay <= 0:
        raise ValueError("publish_at must be in the future")

    await asyncio.sleep(delay)

    bot = TelegramBot()
    await bot.send_message(text)
