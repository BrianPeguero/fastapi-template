from app.models.security.user import User
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Optional

from app.core.auth import oauth2_scheme
from app.core.config import settings
from app.db.database import get_session


class TokenData(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    username: Optional[str] = None


async def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    results = await db.execute(select(User).where(User.username == token.username))

    user = results.scalar().first()

    if user is None:
        raise credentials_exception

    return user
