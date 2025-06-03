"""
WSGI entry point for the AI Code Detection Bot
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the project directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logger.info(f"Project root: {project_root}")
logger.info(f"Python path: {sys.path[:3]}")

try:
    # Import the Flask app from the backend package
    from backend.app import app
    logger.info("Successfully imported Flask app")
except ImportError as e:
    logger.error(f"Failed to import Flask app: {e}")
    # Try alternative import
    try:
        sys.path.insert(0, os.path.join(project_root, 'backend'))
        from app import app
        logger.info("Successfully imported Flask app using alternative method")
    except ImportError as e2:
        logger.error(f"Failed alternative import: {e2}")
        raise e2

# Ensure the app is properly configured
if hasattr(app, 'config'):
    app.config['DEBUG'] = False
    logger.info("App configured for production")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 