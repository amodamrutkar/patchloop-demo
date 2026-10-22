import os
from flask import Flask
from .config import SECRET_KEY, DATABASE_PATH
from .db import init_db, get_db
from .routes import bp as routes_bp

def create_app(db_path: str | None = None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', SECRET_KEY)
    # Use provided db_path or default
    db_path = db_path or DATABASE_PATH
    init_db(db_path)
    app.db = get_db(db_path)
    app.register_blueprint(routes_bp)
    return app
