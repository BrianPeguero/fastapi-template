"""_summary_
"""

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """


class NotificationCreate(NotificationBase):
    """_summary_

    Args:
        NotificationBase (_type_): _description_
    """

    user_id_from: Optional[int] = None
    user_id_to: int
    message: str


class NotificationUpdate(NotificationBase):
    """_summary_

    Args:
        NotificationBase (_type_): _description_
    """


class NotificationInDBBase(NotificationBase):
    """_summary_

    Args:
        NotificationBase (_type_): _description_
    """

    id: Optional[int] = None
    user_id_from: Optional[int] = None
    user_id_to: int
    message: str
    created_at: Optional[datetime.time] = datetime.datetime.now()
    read_at: Optional[datetime.time] = datetime.datetime.now()
    is_read: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class Notification(NotificationInDBBase):
    """_summary_

    Args:
        NotificationInDBBase (_type_): _description_
    """
