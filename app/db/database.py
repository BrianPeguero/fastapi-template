"""_summary_
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

DATABASE_URL = f"{settings.PG_DRIVER}://{settings.PG_USERNAME}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}"

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.PG_DEBUG_FLAG,
    future=True,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
    pool_timeout=30,
)


async def init_db():
    """_summary_

    Returns:
        AsyncSession: _description_
    """

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """getting async session

    Returns:
        AsyncSession: _description_

    Yields:
        Iterator[AsyncSession]: _description_
    """

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


async def close_db():
    """closing connection to db"""

    await engine.dispose()
