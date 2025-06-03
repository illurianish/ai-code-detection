"""
Root-level app.py - Entry point for deployment
This ensures compatibility with default Render configurations
"""

# Import the app from our WSGI module
from wsgi import app

# This allows 'gunicorn app:app' to work
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 