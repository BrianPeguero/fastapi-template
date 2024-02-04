"""_summary_
"""

from datetime import datetime, timedelta
from typing import List, MutableMapping, Union

from app.models.security.user import User
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_password

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


async def authenticate(email: str, password: str, db: AsyncSession):
    """_summary_

    Args:
        email (str): _description_
        password (str): _description_
        db (AsyncSession): _description_

    Returns:
        _type_: _description_
    """

    results = await db.execute(select(User).where(User.email == email))

    user = results.scalar().first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(sub: str) -> str:
    """_summary_

    Args:
        sub (str): _description_

    Returns:
        str: _description_
    """

    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    """_summary_

    Args:
        token_type (str): _description_
        lifetime (timedelta): _description_
        sub (str): _description_

    Returns:
        str: _description_
    """

    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
