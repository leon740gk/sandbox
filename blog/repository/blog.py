from sqlalchemy.orm import Session

from blog.models import Blog
from blog.schemas import BlogSchema


def create_blog(request_data: BlogSchema, db: Session):
    new_blog = Blog(title=request_data.title, body=request_data.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
