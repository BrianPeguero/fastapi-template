from sqlalchemy import (
    BigInteger,
    Boolean,
    Identity,
    PrimaryKeyConstraint,
    Text,
    Time,
    text,
)
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Notification(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "notification"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="notification_pkey"),
        {"schema": "security"},
    )

    id = mapped_column(
        BigInteger,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
    )

    user_id_from = mapped_column(BigInteger)
    user_id_to = mapped_column(BigInteger)
    message = mapped_column(Text)
    created_at = mapped_column(Time, server_default=text("now()"))
    read_at = mapped_column(Time)
    is_read = mapped_column(Boolean)
