from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, get_current_user
from app.services import UserService, PostService, CommentService
from pydantic import ValidationError
from app.auth import authenticate
from app.pydantic_models import (
    UserCreate,
    UserLogin,
    PostCreate,
    PostSchema,
    UserSchema,
    CommentCreate,
    CommentSchema,
    QueryParams,
)
import logging


app_router = Blueprint("app_router", __name__)


@app_router.post("/register")
def register():
    """Register a new user"""
    try:
        user_create = UserCreate(**request.json)
        user_model = UserService.create_user(**user_create.model_dump())
        user = UserSchema.model_construct(
            id=user_model.id,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
        )
        return jsonify(user.model_dump()), 201
    except ValidationError:
        return jsonify({"message": "Invalid data"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app_router.post("/login")
def login():
    """Login a user"""
    try:
        user_login = UserLogin(**request.form)
        access_token = authenticate(**user_login.model_dump())
        return jsonify(access_token=access_token), 200
    except ValidationError:
        return jsonify({"message": "Invalid data"}), 400
    except Exception as e:
        import traceback

        print(traceback.print_exc())
        return jsonify({"message": str(e)}), 400


@app_router.post("/posts/create")  # can be used as /posts/ as well
@jwt_required()
def create_post():
    """Create a new post"""
    try:
        user = get_current_user()
        post_create = PostCreate(**request.json, author_id=user.id)
        PostService.create_post(**post_create.model_dump())
        return Response(status=201)
    except ValidationError:
        return jsonify({"message": "Invalid data, Validation error"}), 400
    except Exception as e:
        import traceback

        logging.error(traceback.print_exc())
        return jsonify({"message": str(e)}), 400


@app_router.get("/posts")
@jwt_required()
def get_all_posts():
    try:
        user = get_current_user()
        filters = QueryParams(**request.args.to_dict())
        posts = PostService.get_posts_by_author(user.id, **filters.model_dump())
        return (
            jsonify([PostSchema(**post.__dict__).model_dump() for post in posts]),
            200,
        )
    except ValidationError as e:
        return jsonify({"message": "validation error"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app_router.get("/posts/<post_id>")
def get_single_post(post_id: int):
    try:
        post_model = PostService.get_post(post_id)
        post = PostSchema(
            author_id=post_model.author_id,
            id=post_model.id,
            content=post_model.content,
            title=post_model.title,
            created_at=post_model.created_at,
            updated_at=post_model.updated_at,
            is_published=post_model.is_published,
        )
        return jsonify(post.model_dump()), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"message": str(e)}), 400


@app_router.post("/posts/<post_id>/comments")
@jwt_required()
def add_comment(post_id: int):
    try:
        user = get_current_user()
        comment_create = CommentCreate(
            **request.json, author_id=user.id, post_id=post_id
        )
        CommentService.create_comment(**comment_create.model_dump())
        return Response(status=201)
    except ValidationError as e:
        return jsonify({"message": "Invalid data"}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({"message": str(e)}), 400


@app_router.get("/posts/<post_id>/comments")
@jwt_required()
def get_comments_by_post(post_id: int):
    try:
        filters = QueryParams(**request.args.to_dict())
        comments = CommentService.get_comments_by_post(
            post_id=post_id, **filters.model_dump()
        )
        return (
            jsonify(
                [CommentSchema(**comment.__dict__).model_dump() for comment in comments]
            ),
            200,
        )
    except ValidationError as e:
        return jsonify({"message": "Invalid data"}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({"message": str(e)}), 400
