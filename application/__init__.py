from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from application.routes import bp
# from application.config import Config

def create_app(test_config=None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    from application.model import db
    db.init_app(app)
    app.register_blueprint(bp)

    return app
