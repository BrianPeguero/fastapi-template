"""_summary_
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False


class userCreate(UserBase):
    """_summary_

    Args:
        UserBase (_type_): _description_
    """

    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """_summary_

    Args:
        UserBase (_type_): _description_
    """


class UserInDBBase(UserBase):
    """_summary_

    Args:
        UserBase (_type_): _description_
    """

    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserInDBBase):
    """_summary_

    Args:
        UserInDBBase (_type_): _description_
    """

    hashed_password: str


class User(UserInDBBase):
    """_summary_

    Args:
        UserInDBBase (_type_): _description_
    """
