"""
Main application file for the Russian Noun Cases Drill.

This Flask application helps users practice Russian noun declensions through
various interactive drills.
"""

import pymorphy3
from flask import Flask

from config import Config
from routes import init_routes

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the pymorphy3 analyzer
    morph = pymorphy3.MorphAnalyzer()

    # Initialize routes
    init_routes(app, morph)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], port=5001)
