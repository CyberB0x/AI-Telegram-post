from app.database import SessionLocal
from app.models import ScheduledPost
from app.telegram.bot import TelegramBot


async def send_scheduled_post(post_id: int):
    db = SessionLocal()

    try:
        post = db.query(ScheduledPost).get(post_id)

        if not post:
            return

        bot = TelegramBot()
        await bot.send_message(post.text)

        post.status = "sent"
        db.commit()

    except Exception as e:
        db.rollback()
        post.status = "failed"
        db.commit()
        print("SEND ERROR:", e)

    finally:
        db.close()
