"""
Flask backend for AI Code Detection Bot
Provides REST API endpoints for code analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from extract_features import extract_code_features
from predict import predict_ai_code

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "message": "AI Code Detection Bot API",
        "version": "1.0.0",
        "model_loaded": True
    })

@app.route('/detect', methods=['POST'])
def detect_ai_code():
    """
    Main endpoint for AI code detection.
    Expects JSON: {"code": "code_string", "language": "python"}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        if len(code) < 10:
            return jsonify({"error": "Code too short for analysis"}), 400
        
        # Extract features from the code
        features = extract_code_features(code, language)
        
        # Make prediction (model is loaded in predict module)
        prediction_result = predict_ai_code(features)
        
        # Format response
        response = {
            "prediction": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "is_ai_generated": prediction_result["prediction"] == "AI",
            "ai_probability": prediction_result.get("ai_probability", 0.5),
            "human_probability": prediction_result.get("human_probability", 0.5),
            "features": features,
            "analysis": {
                "lines_of_code": features.get("lines_of_code", 0),
                "comment_ratio": features.get("comment_ratio", 0),
                "avg_line_length": features.get("avg_line_length", 0),
                "complexity_score": features.get("complexity_score", 0)
            },
            "reasons": prediction_result.get("reasons", [])
        }
        
        logger.info(f"Prediction: {prediction_result['prediction']} ({prediction_result['confidence']:.2f})")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API usage statistics."""
    return jsonify({
        "model_loaded": True,
        "supported_languages": ["python", "javascript", "java", "cpp", "go"],
        "max_code_length": 50000,
        "features_analyzed": [
            "lines_of_code",
            "comment_ratio", 
            "function_count",
            "avg_line_length",
            "complexity_score",
            "indentation_consistency",
            "variable_naming_patterns"
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Detailed health check for monitoring."""
    return jsonify({
        "status": "healthy",
        "model_status": "loaded",
        "api_version": "1.0.0"
    })

if __name__ == '__main__':
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development') 