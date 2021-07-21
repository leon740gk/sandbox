from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from blog.hashing import Hashing
from blog.models import User
from blog.schemas import UserSchema

hashing_tools = Hashing()


def create_user(request_data: UserSchema, db: Session):
    new_user = User(
        name=request_data.name,
        email=request_data.email,
        password=hashing_tools.encrypt(request_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(email, get_db):
    db = get_db()
    return db.query(User).filter(User.email == email).first()
