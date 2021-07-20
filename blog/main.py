import uvicorn
from fastapi import FastAPI

from blog.schemas import BlogCreate
from .database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/blogs")
def index(limit: int = 10, published: bool = True):
    return {"data": {"amount": limit, "published": published}}


@app.post("/blogs")
def index(blog: BlogCreate) -> dict:
    response = {"data": {"title": blog.title, "body": blog.body}}
    if pub_date := blog.pub_date:
        response["data"].update({"pub_date": pub_date})
    return response


@app.get("/blogs/unpublished")
def get_unpublished_blogs():
    return {"data": "all unpublished blogs..."}


@app.get("/blog/{blog_id}")
def detail(blog_id: int) -> dict:
    return {"data": {"type": f"details for blog # {blog_id}", "details": blog_id}}


@app.get("/blog/{blog_id}/comments")
def detail(blog_id: int) -> dict:
    return {
        "data": {
            "type": f"comments for blog # {blog_id}",
            "comments": [x for x in range(4)],
        }
    }


if __name__ == "__main__":
    # for debugging purposes only
    uvicorn.run(app, host="127.0.0.1", port=8080)
