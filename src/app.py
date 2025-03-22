from flask import Flask
from src.routes import main
import os

def create_app():
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../static')),
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    )
    app.register_blueprint(main)
    return app
