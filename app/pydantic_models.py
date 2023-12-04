from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import List


class BaseSchemaMode(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseTimestampModel(BaseSchemaMode):
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseSchemaMode):
    username: str  # this is the email
    password: str


class UserCreate(BaseSchemaMode):
    password: str
    email: str
    first_name: str
    last_name: str


class UserSchema(BaseSchemaMode):
    id: int
    email: str
    first_name: str
    last_name: str


class PostCreate(BaseSchemaMode):
    title: str
    content: str
    author_id: int


class PostUpdate(BaseSchemaMode):
    title: str = None
    content: str = None
    is_published: bool = True


class CommentCreate(BaseSchemaMode):
    content: str
    post_id: int
    author_id: int


class CommentSchema(BaseTimestampModel):
    id: int
    content: str
    post_id: int
    author_id: int


class PostSchema(BaseTimestampModel):
    id: int
    title: str
    content: str
    is_published: bool
    author_id: int


class PostWithCommentSchema(PostSchema):
    comments: List[CommentSchema] = []


class QueryParams(BaseSchemaMode):
    page: int = 1
    limit: int = 10
    sort: str = "created_at"
    order: str = "desc"

    @field_validator("order")
    def order_must_be_asc_or_desc(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError('Order must be "asc" or "desc"')
        return v

