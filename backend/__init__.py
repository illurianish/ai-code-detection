"""
AI Code Detection Bot - Backend Package
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from .app import app

# Import other modules to make them available
from . import extract_features
from . import predict

__version__ = "1.0.0"
__all__ = ['app', 'extract_features', 'predict'] 