from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.scheduler_manage import (
    list_scheduled_posts,
    cancel_scheduled_post
)

router = APIRouter(prefix="/api/schedule", tags=["Scheduler"])


@router.get("")
def get_scheduled_posts(db: Session = Depends(get_db)):
    posts = list_scheduled_posts(db)
    return posts


@router.delete("/{post_id}")
def cancel_post(post_id: int, db: Session = Depends(get_db)):
    post = cancel_scheduled_post(post_id, db)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "status": post.status,
        "post_id": post.id
    }
