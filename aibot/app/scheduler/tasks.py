from datetime import datetime, timezone, timedelta
from sqlalchemy import update
from app.database import SessionLocal
from app.models import ScheduledPost
from app.telegram.bot import TelegramBot
from app.scheduler.instance import scheduler
import logging

logger = logging.getLogger(__name__)


async def send_scheduled_post(post_id: int):
    db = SessionLocal()

    try:
        # ATOMIC LOCK
        result = db.execute(
            update(ScheduledPost)
            .where(
                ScheduledPost.id == post_id,
                ScheduledPost.status.in_(["scheduled", "retrying"])
            )
            .values(status="processing")
        )
        db.commit()

        if result.rowcount == 0:
            logger.warning(f"Post {post_id} skipped (already processed)")
            return

        post = db.get(ScheduledPost, post_id)
        bot = TelegramBot()

        logger.info(f"Sending post {post_id}")
        await bot.send_message(post.text)

        # SUCCESS
        post.status = "sent"
        post.last_error = None
        db.commit()

        logger.info(f"Post {post_id} sent successfully")

    except Exception as e:
        db.rollback()
        post = db.get(ScheduledPost, post_id)

        post.retry_count += 1
        post.last_error = str(e)

        if post.retry_count < post.max_retries:
            post.status = "retrying"

            retry_time = datetime.now(timezone.utc) + timedelta(minutes=5)

            scheduler.add_job(
                send_scheduled_post,
                trigger="date",
                run_date=retry_time,
                args=[post.id],
                id=f"post_retry_{post.id}_{post.retry_count}",
                replace_existing=False
            )

            logger.error(
                f"Post {post_id} failed, retry {post.retry_count}/{post.max_retries}"
            )
        else:
            post.status = "failed"
            logger.critical(f"Post {post_id} permanently failed")

        db.commit()

    finally:
        db.close()
