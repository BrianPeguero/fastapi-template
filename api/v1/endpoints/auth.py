from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import get_db, get_current_user
from schemas.user import User, UserCreate
from crud import user_crud
from core.auth import (
    authenticate,
    create_access_token,
)


router = APIRouter()

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/signup', status_code=201, response_model=User)
def signup(*, user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = user_crud.get_user_by_email(email=user_in.email, db=db)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    user = user_crud.create(db=db, obj_in=user_in)

    return user


@router.post('/login', status_code=200)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect username or password."
        )
    
    return {
        "access_token":create_access_token(sub=user.id),
        "token_type": "bearer"
    }

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user