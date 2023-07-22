from sqlalchemy.orm import Session

from models.user.user import User
from schemas.user import UserCreate
from core.security import get_password_hash

def get_user_by_email(*, email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(*, db: Session, obj_in: UserCreate) -> User:
    create_data = obj_in.model_dump()
    create_data.pop("password")
    db_obj = User(**create_data)
    db_obj.hashed_password = get_password_hash(obj_in.password)
    db.add(db_obj)
    db.commit()

    return db_obj