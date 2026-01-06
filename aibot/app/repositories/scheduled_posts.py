from sqlalchemy import update, select
from sqlalchemy.orm import Session
from app.models import ScheduledPost

def try_acquire_post_lock(db: Session, post_id: int) -> bool:
    """
    Универсальный atomic lock.
    Работает и в SQLite, и в PostgreSQL.
    В PostgreSQL позже можно заменить на SELECT FOR UPDATE.
    """

    result = db.execute(
        update(ScheduledPost)
        .where(
            ScheduledPost.id == post_id,
            ScheduledPost.status == "scheduled"
        )
        .values(status="processing")
    )

    db.commit()
    return result.rowcount == 1
