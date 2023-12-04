from passlib.hash import pbkdf2_sha256
from app.models import User
from app.pydantic_models import UserSchema
from sqlalchemy.exc import IntegrityError
import logging


class UserService:
    @classmethod
    def create_user(
        cls,
        email: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        try:
            hashed_password = pbkdf2_sha256.hash(password)
            user = User(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
            ).create()
            return user
        except IntegrityError:
            raise Exception("User already exists")

    @classmethod
    def get_user_by_email(cls, email: str) -> User:
        user = User.query.filter_by(email=email).first()
        return user

    @classmethod
    def get_user_by_id(cls, id: int) -> User:
        user = User.query.filter_by(id=id).first()
        return user
