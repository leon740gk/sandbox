from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Blog
from .schemas import BlogSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogSchema, db: Session = Depends(get_db)) -> dict:
    new_blog = Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{blog_id}")
def detail(blog_id: int, db: Session = Depends(get_db)) -> dict:
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found"
        )
    return blog


@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, blog: BlogSchema, db: Session = Depends(get_db)):
    blog_obj = db.query(Blog).filter(Blog.id == blog_id)
    if not blog_obj.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found"
        )

    blog_obj.update(blog.to_dict())
    db.commit()

    return {"result": f"Blog {blog_id} updated."}


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found"
        )

    blog.delete()
    db.commit()

    return {"result": f"Blog {blog_id} deleted."}
