"""_summary_
"""

from app.models.security.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate
from app.utils.logging import logger


async def get_user_by_email(email: str, db: AsyncSession) -> Optional[User]:
    """_summary_

    Args:
        email (str): _description_
        db (AsyncSession): _description_

    Returns:
        Optional[User]: _description_
    """

    logger.debug("Get user by email")

    result = await db.execute(select(User).where(User.email == email))

    return result.scalar().first()


async def get_user_by_id(user_id: int, db: AsyncSession) -> Optional[User]:
    """_summary_

    Args:
        user_id (int): _description_
        db (AsyncSession): _description_

    Returns:
        Optional[User]: _description_
    """

    logger.debug("Get user by id")

    results = await db.execute(select(User).where(User.id == user_id))

    return results.scalar().first()


async def create_user(obj_in: UserCreate, db: AsyncSession) -> User:
    """_summary_

    Args:
        obj_in (UserCreate): _description_
        db (AsyncSession): _description_

    Returns:
        User: _description_
    """

    create_data = obj_in.model_dump()
    create_data.pop("password")

    db_obj = User(**create_data)

    db_obj.hashed_password = get_password_hash(obj_in.password)

    await db.add(db_obj)
    await db.commit()

    return db_obj


def update(
    db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]], db: AsyncSession
) -> User:
    """_summary_

    Args:
        db_obj (User): _description_
        obj_in (_type_): _description_

    Returns:
        User: _description_
    """

    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)

    return super.update(db, db_obj=db_obj, obj_in=obj_in)


def is_superuser(user: User) -> bool:
    """_summary_

    Args:
        user (User): _description_

    Returns:
        bool: _description_
    """

    return user.is_superuser
