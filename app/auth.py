from flask_jwt_extended import create_access_token
from hashlib import sha256
from passlib.hash import pbkdf2_sha256
from app.services import UserService
from app.services import UserService
from app.models import User
import logging
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def authenticate(username: str, password: str) -> str | Exception:
    try:
        logging.warning(username)
        user = UserService.get_user_by_email(email=username)
        if user and pbkdf2_sha256.verify(password, user.password):
            access_token = generate_access_token(identity=user)
            return access_token
        else:
            raise Exception("invalid credentials")
    except Exception as e:  # we dont want to expose the cause of the error to the user
        logging.error(str(e))
        raise Exception("invalid credentials")


def generate_access_token(identity: User = None):
    return create_access_token(identity=identity)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserService.get_user_by_id(id=identity)
