"""
This module handles the creation and configuration of the flask app,
which is our backend and database.
"""

from flask import Flask

from models import db
from routes import register_endpoints


def create_test_app() -> Flask:
    """
    Creates a flask app that can be used for testing.

    Returns:
        Flask: The test app.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./test.db"
    app.config["TESTING"] = True

    db.init_app(app)

    register_endpoints(app, db)

    app.app_context().push()
    db.create_all()

    return app


def create_app() -> Flask:
    """
    Creates a flask app that can be used in production.

    Returns:
        Flask: The app.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./our.db"
    db.init_app(app)

    register_endpoints(app, db)

    app.app_context().push()
    db.create_all()

    return app
