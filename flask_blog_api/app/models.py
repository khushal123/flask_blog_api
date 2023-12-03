from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from typing import List

db = SQLAlchemy()


class BaseMixin(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(BaseMixin):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author"
    )  # lazy="select" is the default
    comments: Mapped[List["Post"]] = relationship(back_populates="author")


class Post(BaseMixin):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    is_published: Mapped[bool] = mapped_column(default=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped["User"] = relationship(
        back_populates="posts"
    )  # lazy='joined' could be used here

    comments: Mapped[List["Comment"]] = relationship(back_populates="post")


class Comment(BaseMixin):
    __tablename__ = "comments"
    content: Mapped[str] = mapped_column()
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(
        "Post", back_populates="comments", lazy="joined"
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments", lazy="joined")
