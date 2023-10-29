from sqlalchemy import Column, BIGINT, Text, VARCHAR, DateTime
from sqlalchemy.orm import relationship

from core.config import settings
from models.base import Base


class Notification(Base):
    __tablename__ = ""
    __table_args__ = {"schema": settings.PG_NOTIFICATION_SCHEMA}
    id = Column(BIGINT, primary_key=True, autoincrement="auto")
    message = Column(Text)
    sender_id = Column(BIGINT)
    receiver_id = Column(BIGINT)
    created_at = Column(DateTime)
    read_at = Column(DateTime)
