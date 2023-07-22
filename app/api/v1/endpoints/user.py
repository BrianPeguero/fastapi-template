from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any

from models.user.user import User as UserModel
from schemas.user import User as UserSchema

from api import deps


router = APIRouter()


@router.get("/{user_id}", status_code=200, response_model=UserSchema)
def get_user(*, user_id:int, db: Session = Depends(deps.get_db)) -> Any:
    """
    Gets a single user by ID
    """

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    return user