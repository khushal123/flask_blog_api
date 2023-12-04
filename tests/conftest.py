import pytest
import logging
from faker import Faker
from run import create_app
from app.models import db
from app.services import UserService, PostService
from app.auth import generate_access_token


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():  # teardown
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def fake_user_data(app):
    fake_data = Faker()
    valid_credentials = {
        "email": fake_data.email(),
        "password": fake_data.password(),
        "first_name": fake_data.first_name(),
        "last_name": fake_data.last_name(),
    }
    with app.app_context():
        UserService.create_user(**valid_credentials)
        db.session.commit()
    return valid_credentials


@pytest.fixture()
def access_token(app, fake_user_data):
    with app.app_context():
        user = UserService.get_user_by_email(email=fake_user_data["email"])
        return generate_access_token(user)


@pytest.fixture()
def fake_post(app, fake_user_data):
    fake_data = Faker()
    post_data = {
        "title": fake_data.name(),
        "content": fake_data.text(),
    }
    with app.app_context():
        author = UserService.get_user_by_email(email=fake_user_data["email"])
        post_data["author_id"] = author.id
        post = PostService.create_post(**post_data)
        db.session.commit()
        post_data["id"] = post.id
    return post_data


@pytest.fixture()
def fake_posts(app, fake_user_data):
    fake_data = Faker()
    posts = []  # List to hold the created post data

    with app.app_context():
        author = UserService.get_user_by_email(email=fake_user_data["email"])
        for _ in range(5):
            post_data = {
                "title": fake_data.name(),
                "content": fake_data.text(),
                "author_id": author.id,
            }
            post = PostService.create_post(**post_data)
            db.session.add(post)
            post_data["id"] = post.id
            posts.append(post_data)

        db.session.commit()

    return posts
