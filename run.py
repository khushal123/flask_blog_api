from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_alembic import Alembic
from app.models import db
from app.routes import app_router
from app.auth import jwt
import config
import logging


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """

    app = Flask(config.APP_NAME)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.POSTGRESQL_URI
    app.config["SECRET_KEY"] = config.SECRET_KEY

    alembic = Alembic()

    db.init_app(app)
    jwt.init_app(app)
    alembic.init_app(app)

    app.register_blueprint(app_router)

    return app


app = create_app()


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=config.PORT)
