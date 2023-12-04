from app.models import Post, Comment
from sqlalchemy import desc, text, asc
from typing import List
from app.models import db


class PostService:
    @classmethod
    def create_post(self, title: str, content: str, author_id: int):
        # already implemented with db.session.add(model)
        post = Post(title=title, content=content, author_id=author_id).create()
        return post

    @classmethod
    def get_post(cls, post_id: int) -> Post:
        return db.session.get(Post, post_id)

    @classmethod
    def get_posts_by_author(
        cls,
        author_id: int,
        page: int = None,
        limit: int = None,
        sort=None,
        order="desc",
    ) -> List[Post]:
        """Get all posts by author
        page: int
        limit: int
        sort: str
        order: str = "desc"
        """
        query = db.session.query(Post).filter(Post.author_id == author_id)
        if sort:
            sort_column = getattr(Post, sort, None)
            if sort_column:
                if order.lower() == "asc":
                    query = query.order_by(asc(sort_column))
                else:
                    query = query.order_by(desc(sort_column))

        if page is not None and limit is not None:
            query = query.limit(limit).offset((page - 1) * limit)

        return query.all()

    @classmethod
    def update_post(cls, post_id: int, title=None, content=None) -> Post:
        post = cls.get_post(post_id)
        if post:
            if title:
                post.title = title
            if content:
                post.content = content
            post.update()
        return post


class CommentService:
    @classmethod
    def create_comment(cls, content: str, post_id: int, author_id: int) -> Comment:
        comment = Comment(
            content=content, post_id=post_id, author_id=author_id
        ).create()
        return comment

    @classmethod
    def get_comments_by_post(
        cls,
        post_id: int,
        page: int = None,
        limit: int = None,
        sort=None,
        order="desc",
    ) -> List[Post]:
        """Get all posts by author
        page: int
        limit: int
        sort: str
        order: str = "desc"
        """
        query = db.session.query(Comment).filter(Comment.post_id == post_id)
        if sort:
            sort_column = getattr(Comment, sort, None)
            if sort_column:
                if order.lower() == "asc":
                    query = query.order_by(asc(sort_column))
                else:
                    query = query.order_by(desc(sort_column))

        if page is not None and limit is not None:
            query = query.limit(limit).offset((page - 1) * limit)

        return query.all()

    @classmethod
    def get_comment(cls, comment_id: int) -> Comment:
        return db.session.query(Comment).get(comment_id)

    # @classmethod
    # def update_comment(cls, comment_id: int, content: str = None):
    #     comment = cls.get_comment(comment_id)
    #     if comment:
    #         if content:
    #             comment.content = content
    #             comment.update()
    #     return comment
