from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from blog.authentication.token import verify_token
from blog.database import get_db
from blog.models import Blog, User
from blog.repository.base import (
    delete_object_by_id,
    get_all,
    get_details_by_id,
    update_object_by_id,
)
from blog.repository.blog import create_blog
from blog.schemas import BlogSchema, ResponseBlogSchema

router = APIRouter(
    prefix="/blog",
    tags=["Blog"],
)


@router.get("/", response_model=List[BlogSchema])
def get_all_blogs(db: Session = Depends(get_db), _=Depends(verify_token)):
    return get_all(Blog, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_blog(
    request_data: BlogSchema, db: Session = Depends(get_db), _=Depends(verify_token)
):
    return create_blog(request_data, db)


@router.get("/{blog_id}", response_model=ResponseBlogSchema)
def get_blog_details(
    blog_id: int, db: Session = Depends(get_db), _=Depends(verify_token)
):
    return get_details_by_id(Blog, blog_id, db)


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    blog_id: int,
    blog: BlogSchema,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    return update_object_by_id(Blog, blog_id, blog, db)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db), _=Depends(verify_token)):
    return delete_object_by_id(Blog, blog_id, db)
