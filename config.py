"""
Configuration settings for the Russian Noun Cases Drill application.
"""

import os

# Flask application settings
class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Replace with a secure key in production
    DEBUG = True

    # Application settings
    DEFAULT_LANGUAGE = 'en'
    SUPPORTED_LANGUAGES = ['en', 'ru']
