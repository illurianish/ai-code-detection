#!/usr/bin/env python3
"""
Simple run script for the AI Code Detection Backend
"""

import os
from app import app, load_model
from predict import create_dummy_model
import pickle

def create_dummy_model_file():
    """Create a dummy model file if none exists."""
    model_path = 'model.pkl'
    if not os.path.exists(model_path):
        print("No model.pkl found. Creating dummy model for testing...")
        dummy_model = create_dummy_model()
        with open(model_path, 'wb') as f:
            pickle.dump(dummy_model, f)
        print("Dummy model created successfully!")

if __name__ == '__main__':
    print("🤖 Starting AI Code Detection Backend...")
    
    # Create dummy model if needed
    create_dummy_model_file()
    
    # Load the model
    load_model()
    
    # Get configuration from environment
    host = os.environ.get('API_HOST', 'localhost')
    port = int(os.environ.get('API_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f"🚀 Server starting on http://{host}:{port}")
    print("📊 API endpoints:")
    print("  GET  /        - Health check")
    print("  POST /detect  - Analyze code")
    print("  GET  /stats   - API statistics")
    print("  GET  /health  - Detailed health check")
    print("\n💡 Tip: Update API_BASE_URL in frontend/script.js to match this URL")
    
    # Run the Flask app
    app.run(host=host, port=port, debug=debug) 