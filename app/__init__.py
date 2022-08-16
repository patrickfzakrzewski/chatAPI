from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()

def create_app():
    """
    Flask app factory method.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import endpoints
    endpoints.init_app(app)

    db.init_app(app)
    from models import User

    with app.app_context():
        db.create_all()

    return app
