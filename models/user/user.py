from sqlalchemy.types import BIGINT, VARCHAR, Boolean, TEXT
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from core.config import settings

from models.base import Base

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": settings.PG_USER_SCHEMA}
    id = Column(BIGINT, primary_key=True, index=True)
    first_name = Column(VARCHAR(256), nullable=True)
    last_name = Column(VARCHAR(256), nullable=True)
    email = Column(TEXT, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(TEXT, nullable=False)