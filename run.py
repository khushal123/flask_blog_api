from flask import Flask
from flask_blog_api.app.models import db
import config


def create_app():
    app = Flask(config.APP_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.POSTGRESQL_URL
    db.init_app(app)
    return app

app = create_app()

with app.app_context():
    db.create_all()
