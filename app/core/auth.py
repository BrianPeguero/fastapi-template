from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from models.user.user import User
from core.config import settings
from core.security import verify_password


JWTPayloadMapping = MutableMapping[
    str, 
    Union[
        datetime, 
        bool, 
        str, 
        List[str], 
        List[int]
    ]
]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


def authenticate(*,
                 email:str,
                 password:str,
                 db:Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return  None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_access_token(*, sub:str) -> str:
    return _create_token(
        token_type="access token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )


def _create_token(
        token_type:str,
        lifetime:timedelta,
        sub:str
        ) -> str:
    
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload['type'] = token_type

    payload["exp"] = expire

    payload["iat"] = datetime.utcnow()

    payload["sub"] = str(sub)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)