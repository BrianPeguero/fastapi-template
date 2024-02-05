from sqlalchemy import BIGINT, Boolean, Identity, PrimaryKeyConstraint, String
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class User(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "user"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pkey"),
        {"schema": "security"},
    )

    id = mapped_column(
        BIGINT,
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
    first_name = mapped_column(String(256))
    last_name = mapped_column(String(256))
    email = mapped_column(String(256))
    is_superuser = mapped_column(Boolean)
    hashed_password = mapped_column(String(256))
    username = mapped_column(String(256))
