from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Imports
        from .routes import deploy
        from .routes import repository
        from .routes import ping

        # Create tables for our models
        db.create_all()

        # Return app
        return app
