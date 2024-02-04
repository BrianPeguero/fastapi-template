from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import authenticate, create_access_token
from app.crud import user_crud
from app.db.database import get_session
from app.endpoints.deps import get_current_user
from app.schemas.user import User, UserCreate
from app.utils.logging import logger

router = APIRouter()


@router.post("/signup", status_code=201, response_model=User)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_session)) -> Any:
    """_summary_

    Args:
        user_in (UserCreate): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Raises:
        HTTPException: _description_

    Returns:
        Any: _description_
    """

    user = await user_crud.get_user_by_email(email=user_in.email, db=db)

    if user:
        logger.debug("A user with email %s, already exists.", user_in.email)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A user with email {user_in.email}, already exists.",
        )

    user = await user_crud.create_user(obj_in=user_in, db=db)

    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """_summary_

    Args:
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Raises:
        HTTPException: _description_

    Returns:
        Any: _description_
    """

    user = await authenticate(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        logger.debug("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {"access_token": create_access_token(sub=user.id), "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_users_me(current_user: User = Depends(get_current_user)):
    """_summary_

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """

    user = current_user
    return user
