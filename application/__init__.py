from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application.routes import bp
from application.auth import auth
from application.model import Item
# from application.config import Config
from dotenv import load_dotenv

load_dotenv()
migrate = Migrate()

def populate_items(app, db):
    app.app_context().push()
    items_to_add = [
        {'name': 'Item 1', 'priority': 1},
        {'name': 'Item 2', 'priority': 2},
        {'name': 'Item 3', 'priority': 3},
        {'name': 'Item 4', 'priority': 4},
        {'name': 'Item 5', 'priority': 5},
        # Add more items as needed
    ]

    try:
        # Add items to the database
        for item_data in items_to_add:
            item = Item(name=item_data['name'], priority=item_data['priority'])
            db.session.add(item)
        db.session.commit()  # Commit the transaction
        print("Items added successfully!")

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print(f"An error occurred: {e}")


def create_app(test_config=None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__)
    app.config.from_object('application.config.Config')
    
    app.register_blueprint(auth)
    app.register_blueprint(bp)

    from application.model import db
    db.init_app(app)

    migrate.db = db
    migrate.init_app(app)

    with app.app_context():
        db.create_all()

    populate_items(app, db)

    return app
