from flask import Flask
from src.routes import main

def create_app():
    # Initialize Flask app instance
    app = Flask(__name__)
    
    # Register the blueprint for routes
    app.register_blueprint(main)
    
    return app
