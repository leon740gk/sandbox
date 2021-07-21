from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from blog.database import get_db
from blog.models import User
from blog.repository.base import get_details_by_id
from blog.repository.user import create_user
from blog.schemas import ResponseUserSchema_v1, ResponseUserSchema_v2, UserSchema

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema_v1,
)
def create_new_user(user: UserSchema, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.get("/{user_id}", response_model=ResponseUserSchema_v2)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    return get_details_by_id(User, user_id, db)
