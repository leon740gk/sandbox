from typing import List, Optional

from pydantic import BaseModel


class ORMBaseModel(BaseModel):
    def to_dict(self):
        return dict(self)

    class Config:
        orm_mode = True


class UserSchema(ORMBaseModel):
    name: str
    email: str
    password: str


class BlogSchema(ORMBaseModel):
    title: str
    body: str


class ResponseUserSchema_v1(ORMBaseModel):
    name: str
    email: str


class ResponseUserSchema_v2(ResponseUserSchema_v1):
    name: str
    email: str
    blogs: List[BlogSchema]


class ResponseBlogSchema(ORMBaseModel):
    title: str
    body: str
    creator: ResponseUserSchema_v1


class LoginSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
