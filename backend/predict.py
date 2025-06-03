"""
Prediction module for AI Code Detection Bot
"""

import os
import logging
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Define the feature names that the model expects (in order)
FEATURE_NAMES = [
    "lines_of_code", "avg_line_length", "comment_ratio", "function_count",
    "complexity_score", "indentation_consistency", "ai_variable_names",
    "ai_function_names", "generic_name_ratio", "perfect_formatting_score",
    "ai_comment_patterns", "blank_line_ratio", "avg_comment_length",
    "camelCase_count", "snake_case_count", "long_comment_count"
]

def create_dummy_model():
    """Create a simple dummy model for testing or when main model is unavailable."""
    class DummyModel:
        def predict(self, X):
            return [1]  # Always predict AI for demo
            
        def predict_proba(self, X):
            return [[0.3, 0.7]]  # 70% confidence in AI prediction
    
    return DummyModel()

def load_model():
    """Load the trained model or return a dummy model if not available."""
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    
    try:
        if os.path.exists(model_path):
            import pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info("Loaded production model")
            return model
    except Exception as e:
        logger.warning(f"Error loading model: {e}")
    
    logger.info("Using dummy model for predictions")
    return create_dummy_model()

# Load model at module level
MODEL = load_model()

def predict_ai_code(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict if code is AI-generated using the trained model.
    
    Args:
        features: Dictionary of extracted features
    
    Returns:
        Dictionary containing prediction and confidence
    """
    try:
        # Prepare feature vector
        feature_vector = prepare_feature_vector(features)
        
        # Make prediction
        prediction_proba = MODEL.predict_proba([feature_vector])[0]
        prediction = MODEL.predict([feature_vector])[0]
        
        # Get confidence (probability of predicted class)
        if prediction == 1:  # AI-generated
            confidence = prediction_proba[1]
            prediction_label = "AI"
        else:  # Human-generated
            confidence = prediction_proba[0]
            prediction_label = "Human"
        
        # Generate reasoning based on features
        reasons = generate_reasoning(features, prediction_label, confidence)
        
        return {
            "prediction": prediction_label,
            "confidence": float(confidence),
            "ai_probability": float(prediction_proba[1]),
            "human_probability": float(prediction_proba[0]),
            "reasons": reasons
        }
        
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return {
            "prediction": "Unknown",
            "confidence": 0.5,
            "ai_probability": 0.5,
            "human_probability": 0.5,
            "reasons": [f"Using fallback prediction due to error: {str(e)}"]
        }


def prepare_feature_vector(features: Dict[str, Any]) -> np.ndarray:
    """
    Convert feature dictionary to numpy array in the correct order for the model.
    
    Args:
        features: Dictionary of extracted features
    
    Returns:
        Numpy array of features
    """
    feature_vector = []
    
    for feature_name in FEATURE_NAMES:
        value = features.get(feature_name, 0)
        
        # Handle potential None values
        if value is None:
            value = 0
        
        # Ensure numeric type
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0.0
        
        # Handle potential inf or nan values
        if np.isnan(value) or np.isinf(value):
            value = 0.0
        
        feature_vector.append(value)
    
    return np.array(feature_vector)


def generate_reasoning(features: Dict[str, Any], prediction: str, confidence: float) -> List[str]:
    """
    Generate human-readable reasoning for the prediction.
    
    Args:
        features: Dictionary of extracted features
        prediction: "AI" or "Human"
        confidence: Confidence score (0-1)
    
    Returns:
        List of reasoning strings
    """
    reasons = []
    
    # High-level confidence explanation
    if confidence > 0.9:
        reasons.append(f"Very high confidence ({confidence:.1%}) in {prediction.lower()} authorship")
    elif confidence > 0.75:
        reasons.append(f"High confidence ({confidence:.1%}) in {prediction.lower()} authorship")
    elif confidence > 0.6:
        reasons.append(f"Moderate confidence ({confidence:.1%}) in {prediction.lower()} authorship")
    else:
        reasons.append(f"Low confidence ({confidence:.1%}) - results uncertain")
    
    # Feature-specific reasoning
    if prediction == "AI":
        reasons.extend(generate_ai_reasoning(features))
    else:
        reasons.extend(generate_human_reasoning(features))
    
    return reasons


def generate_ai_reasoning(features: Dict[str, Any]) -> List[str]:
    """Generate reasoning for AI classification."""
    reasons = []
    
    # Perfect formatting
    formatting_score = features.get("perfect_formatting_score", 0)
    if formatting_score > 0.8:
        reasons.append("Consistently perfect formatting suggests AI generation")
    
    # AI-typical variable names
    ai_vars = features.get("ai_variable_names", 0)
    if ai_vars > 2:
        reasons.append(f"High use of AI-typical variable names (found {ai_vars})")
    
    # Generic naming patterns
    generic_ratio = features.get("generic_name_ratio", 0)
    if generic_ratio > 0.3:
        reasons.append(f"High ratio of generic variable names ({generic_ratio:.1%})")
    
    # AI comment patterns
    ai_comments = features.get("ai_comment_patterns", 0)
    if ai_comments > 0:
        reasons.append(f"Contains AI-typical comment patterns ({ai_comments} found)")
    
    # Long explanatory comments
    long_comments = features.get("long_comment_count", 0)
    if long_comments > 0:
        reasons.append("Contains overly detailed explanatory comments")
    
    # Perfect indentation consistency
    indent_consistency = features.get("indentation_consistency", 0)
    if indent_consistency > 0.95:
        reasons.append("Extremely consistent indentation typical of AI")
    
    # Moderate complexity with high structure
    complexity = features.get("complexity_score", 0)
    function_count = features.get("function_count", 0)
    if complexity > 5 and function_count > 2:
        reasons.append("Well-structured code with moderate complexity typical of AI")
    
    # High comment ratio
    comment_ratio = features.get("comment_ratio", 0)
    if comment_ratio > 0.3:
        reasons.append(f"High comment-to-code ratio ({comment_ratio:.1%}) suggests AI")
    
    return reasons


def generate_human_reasoning(features: Dict[str, Any]) -> List[str]:
    """Generate reasoning for human classification."""
    reasons = []
    
    # Imperfect formatting
    formatting_score = features.get("perfect_formatting_score", 0)
    if formatting_score < 0.5:
        reasons.append("Inconsistent formatting suggests human authorship")
    
    # Low AI patterns
    ai_vars = features.get("ai_variable_names", 0)
    ai_comments = features.get("ai_comment_patterns", 0)
    if ai_vars <= 1 and ai_comments == 0:
        reasons.append("Lacks typical AI code generation patterns")
    
    # Inconsistent indentation
    indent_consistency = features.get("indentation_consistency", 0)
    if indent_consistency < 0.8:
        reasons.append("Inconsistent indentation patterns suggest human writing")
    
    # Variable naming diversity
    generic_ratio = features.get("generic_name_ratio", 0)
    if generic_ratio < 0.2:
        reasons.append("Diverse, specific variable naming typical of humans")
    
    # Natural comment patterns
    comment_ratio = features.get("comment_ratio", 0)
    long_comments = features.get("long_comment_count", 0)
    if comment_ratio < 0.2 and long_comments == 0:
        reasons.append("Natural commenting style suggests human authorship")
    
    # Code complexity patterns
    complexity = features.get("complexity_score", 0)
    lines_of_code = features.get("lines_of_code", 0)
    if complexity > 0 and lines_of_code > 20:
        if complexity / lines_of_code < 0.3:  # Lower complexity per line
            reasons.append("Code complexity patterns suggest human writing style")
    
    # Mixed formatting styles
    camel_case = features.get("camelCase_count", 0)
    snake_case = features.get("snake_case_count", 0)
    if camel_case > 0 and snake_case > 0:
        reasons.append("Mixed naming conventions suggest human inconsistency")
    
    return reasons 