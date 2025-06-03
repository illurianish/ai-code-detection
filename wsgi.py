"""
WSGI entry point for the AI Code Detection Bot
"""

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from the backend package
from backend.app import app

if __name__ == "__main__":
    app.run() 