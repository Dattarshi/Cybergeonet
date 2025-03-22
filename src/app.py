from flask import Flask
from src.routes import main

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = 'super-secret-key'  # Needed for flash messages
    app.register_blueprint(main)
    return app