from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.models import db
from app.routes import app_router
from app.auth import jwt
import config


# added at runtime to make more testable
def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
    app.config["SECRET_KEY"] = config.SECRET_KEY
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db, command="db")
    app.register_blueprint(app_router)
    return app


app = create_app()


CORS(app)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=config.PORT)
