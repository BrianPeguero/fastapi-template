from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

uri = f"{settings.PG_DRIVER}://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}"

engine = create_engine(uri,
                       echo=settings.PG_DEBUG_FLAG,
                       pool_size=10,
                       max_overflow=5,
                       pool_recycle=300,
                       pool_pre_ping=True,
                       pool_use_lifo=True,
                       )

SessionLocal = sessionmaker(autoflush=settings.PG_AUTOFLUSH, bind=engine)