from pydantic import BaseModel
from datetime import datetime

class BaseTimestampModel(BaseModel):
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    username: str  # this is the email
    password: str


class UserCreate(BaseModel):
    password: str
    email: str
    first_name: str
    last_name: str
    is_active: bool = True


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str = None
    content: str = None
    is_published: bool = True


class Post(BaseTimestampModel):
    id: int
    title: str
    content: str
    is_published: bool
    author_id: int


class CommentCreate(BaseModel):
    content: str

class Comment(BaseTimestampModel):
    id: int
    content: str
    post_id: int
    author_id: int

