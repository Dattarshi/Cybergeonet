from flask import Flask
from src.routes import main
import os

def create_app():
    # Auto-detect project base directory
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder=os.path.join(BASE_DIR, 'static'),
        template_folder=os.path.join(os.path.dirname(__file__), 'templates')
    )
    app.register_blueprint(main)
    return app
