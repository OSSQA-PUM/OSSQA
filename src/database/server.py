from flask import Flask

from .models import db
from .routes import register_endpoints


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./our.db"

    db.init_app(app)

    register_endpoints(app, db)

    # Create database if it doesn't exist
    app.app_context().push()
    db.create_all()

    return app
