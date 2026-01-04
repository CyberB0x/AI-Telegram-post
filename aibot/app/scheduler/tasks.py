from app.database import SessionLocal
from app.models import ScheduledPost
from app.telegram.bot import TelegramBot


async def send_scheduled_post(post_id: int):
    db = SessionLocal()

    try:
        post = db.query(ScheduledPost).filter(
            ScheduledPost.id == post_id
        ).first()

        # защита от дублей (idempotency)
        if not post or post.status != "scheduled":
            return

        bot = TelegramBot()
        await bot.send_message(post.text)

        post.status = "sent"
        db.commit()

    except Exception:
        db.rollback()
        if post:
            post.status = "failed"
            db.commit()

    finally:
        db.close()
