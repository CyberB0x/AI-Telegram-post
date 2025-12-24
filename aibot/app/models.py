from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
