from fastapi import FastAPI

from blog.database import Base, engine
from blog.routers.authentication import router as auth_router
from blog.routers.blog import router as blog_router
from blog.routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(user_router)
