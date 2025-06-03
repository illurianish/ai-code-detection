"""
Feature extraction module for AI code detection.
Analyzes code structure, style, and patterns to create feature vectors.
"""

import re
import ast
import keyword
from typing import Dict, Any, List
import math
import logging

logger = logging.getLogger(__name__)


def extract_code_features(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Extract comprehensive features from code for AI detection.
    
    Args:
        code: Source code string
        language: Programming language (python, javascript, java, etc.)
    
    Returns:
        Dictionary of extracted features
    """
    features = {}
    
    # Basic metrics
    features.update(extract_basic_metrics(code))
    
    # Comment analysis
    features.update(extract_comment_features(code, language))
    
    # Language-specific features
    if language.lower() == "python":
        features.update(extract_python_features(code))
    elif language.lower() in ["javascript", "js"]:
        features.update(extract_javascript_features(code))
    else:
        features.update(extract_generic_features(code))
    
    # Style and pattern analysis
    features.update(extract_style_features(code))
    
    # AI-specific pattern detection
    features.update(detect_ai_patterns(code, language))
    
    return features


def extract_basic_metrics(code: str) -> Dict[str, Any]:
    """Extract basic code metrics."""
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    return {
        "lines_of_code": len(lines),
        "non_empty_lines": len(non_empty_lines),
        "blank_lines": len(lines) - len(non_empty_lines),
        "blank_line_ratio": (len(lines) - len(non_empty_lines)) / max(len(lines), 1),
        "avg_line_length": sum(len(line) for line in lines) / max(len(lines), 1),
        "max_line_length": max((len(line) for line in lines), default=0),
        "total_characters": len(code),
        "avg_chars_per_line": len(code) / max(len(lines), 1)
    }


def extract_comment_features(code: str, language: str) -> Dict[str, Any]:
    """Extract comment-related features."""
    features = {}
    
    # Language-specific comment patterns
    if language.lower() == "python":
        single_line_pattern = r"#.*"
        multi_line_pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
    elif language.lower() in ["javascript", "js", "java", "cpp", "c"]:
        single_line_pattern = r"//.*"
        multi_line_pattern = r"/\*[\s\S]*?\*/"
    else:
        single_line_pattern = r"#.*|//.*"
        multi_line_pattern = r"/\*[\s\S]*?\*/|'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\""
    
    # Count comments
    single_comments = re.findall(single_line_pattern, code)
    multi_comments = re.findall(multi_line_pattern, code, re.MULTILINE)
    
    all_comments = single_comments + multi_comments
    comment_text = ' '.join(all_comments)
    
    features["comment_count"] = len(all_comments)
    features["comment_lines"] = sum(comment.count('\n') + 1 for comment in multi_comments) + len(single_comments)
    features["comment_ratio"] = features["comment_lines"] / max(len(code.split('\n')), 1)
    features["avg_comment_length"] = sum(len(comment) for comment in all_comments) / max(len(all_comments), 1)
    
    # AI-typical comment patterns
    ai_comment_indicators = [
        "here's", "here is", "this code", "this function", "this will",
        "note that", "make sure", "don't forget", "remember to",
        "you can", "you should", "you might", "if you want",
        "alternatively", "optionally", "example usage"
    ]
    
    features["ai_comment_patterns"] = sum(
        1 for pattern in ai_comment_indicators 
        if pattern.lower() in comment_text.lower()
    )
    
    return features


def extract_python_features(code: str) -> Dict[str, Any]:
    """Extract Python-specific features."""
    if not code or not code.strip():
        return {
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "loop_count": 0,
            "if_count": 0,
            "try_count": 0,
            "complexity_score": 0.0
        }
    
    features = {}
    
    try:
        tree = ast.parse(code)
        
        # Count different node types
        node_counts = {}
        function_names = []
        variable_names = []
        class_names = []
        
        for node in ast.walk(tree):
            node_type = type(node).__name__
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
            
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variable_names.append(node.id)
            elif isinstance(node, ast.ClassDef):
                class_names.append(node.name)
        
        features["function_count"] = node_counts.get("FunctionDef", 0)
        features["class_count"] = node_counts.get("ClassDef", 0)
        features["import_count"] = node_counts.get("Import", 0) + node_counts.get("ImportFrom", 0)
        features["loop_count"] = node_counts.get("For", 0) + node_counts.get("While", 0)
        features["if_count"] = node_counts.get("If", 0)
        features["try_count"] = node_counts.get("Try", 0)
        
        # Naming analysis
        features.update(analyze_naming_patterns(function_names, variable_names, class_names))
        
        # Calculate complexity
        features["complexity_score"] = calculate_complexity(node_counts)
        
    except SyntaxError as e:
        logger.warning(f"Syntax error in Python code: {e}")
        features.update({
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "loop_count": 0,
            "if_count": 0,
            "try_count": 0,
            "complexity_score": 0.0
        })
    except Exception as e:
        logger.error(f"Unexpected error in Python feature extraction: {e}")
        features.update({
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "loop_count": 0,
            "if_count": 0,
            "try_count": 0,
            "complexity_score": 0.0
        })
    
    return features


def extract_javascript_features(code: str) -> Dict[str, Any]:
    """Extract JavaScript-specific features."""
    features = {}
    
    # Function patterns
    function_patterns = [
        r"function\s+\w+",
        r"const\s+\w+\s*=\s*\(",
        r"let\s+\w+\s*=\s*\(",
        r"var\s+\w+\s*=\s*\(",
        r"=>\s*{",
    ]
    
    features["function_count"] = sum(len(re.findall(pattern, code)) for pattern in function_patterns)
    features["arrow_function_count"] = len(re.findall(r"=>\s*{", code))
    features["const_count"] = len(re.findall(r"\bconst\b", code))
    features["let_count"] = len(re.findall(r"\blet\b", code))
    features["var_count"] = len(re.findall(r"\bvar\b", code))
    
    # Control structures
    features["if_count"] = len(re.findall(r"\bif\s*\(", code))
    features["for_count"] = len(re.findall(r"\bfor\s*\(", code))
    features["while_count"] = len(re.findall(r"\bwhile\s*\(", code))
    features["try_count"] = len(re.findall(r"\btry\s*{", code))
    
    return features


def extract_generic_features(code: str) -> Dict[str, Any]:
    """Extract generic features for any language."""
    features = {}
    
    # Count braces and brackets
    features["brace_count"] = code.count("{") + code.count("}")
    features["paren_count"] = code.count("(") + code.count(")")
    features["bracket_count"] = code.count("[") + code.count("]")
    
    # Control keywords (common across languages)
    control_keywords = ["if", "else", "for", "while", "switch", "case", "break", "continue", "return"]
    for keyword in control_keywords:
        features[f"{keyword}_count"] = len(re.findall(rf"\b{keyword}\b", code, re.IGNORECASE))
    
    return features


def extract_style_features(code: str) -> Dict[str, Any]:
    """Extract code style and formatting features."""
    lines = code.split('\n')
    
    # Indentation analysis
    indentations = []
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            indentations.append(indent)
    
    # Spacing patterns
    spaces_after_comma = len(re.findall(r',\s', code))
    spaces_around_operators = len(re.findall(r'\s[+\-*/=]\s', code))
    
    return {
        "indentation_consistency": calculate_indentation_consistency(indentations),
        "avg_indentation": sum(indentations) / max(len(indentations), 1),
        "max_indentation": max(indentations, default=0),
        "spaces_after_comma": spaces_after_comma,
        "spaces_around_operators": spaces_around_operators,
        "camelCase_count": len(re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b', code)),
        "snake_case_count": len(re.findall(r'\b[a-z]+_[a-z_]+\b', code)),
        "UPPER_CASE_count": len(re.findall(r'\b[A-Z][A-Z_]+\b', code))
    }


def detect_ai_patterns(code: str, language: str) -> Dict[str, Any]:
    """Detect patterns commonly found in AI-generated code."""
    features = {}
    
    # AI-typical variable names
    ai_variable_names = [
        "result", "output", "data", "value", "item", "element", "temp", "tmp",
        "response", "request", "params", "config", "settings", "options"
    ]
    
    features["ai_variable_names"] = sum(
        len(re.findall(rf'\b{name}\b', code, re.IGNORECASE)) 
        for name in ai_variable_names
    )
    
    # AI-typical function names
    ai_function_names = [
        "process", "handle", "execute", "run", "perform", "calculate",
        "generate", "create", "build", "construct", "initialize"
    ]
    
    features["ai_function_names"] = sum(
        len(re.findall(rf'\b{name}\b', code, re.IGNORECASE)) 
        for name in ai_function_names
    )
    
    # Overly descriptive comments (AI tends to over-explain)
    long_comments = re.findall(r'#[^\n]{50,}|//[^\n]{50,}|/\*[\s\S]{100,}\*/', code)
    features["long_comment_count"] = len(long_comments)
    
    # Perfect formatting (AI often generates perfectly formatted code)
    features["perfect_formatting_score"] = calculate_formatting_perfection(code)
    
    return features


def analyze_naming_patterns(function_names: List[str], variable_names: List[str], class_names: List[str]) -> Dict[str, Any]:
    """Analyze naming patterns for AI detection."""
    features = {}
    
    all_names = function_names + variable_names + class_names
    
    if not all_names:
        return {
            "avg_name_length": 0,
            "generic_name_ratio": 0,
            "descriptive_name_ratio": 0
        }
    
    # Average name length
    features["avg_name_length"] = sum(len(name) for name in all_names) / len(all_names)
    
    # Generic names (AI often uses generic variable names)
    generic_names = ["data", "result", "value", "item", "temp", "var", "obj"]
    generic_count = sum(1 for name in all_names if name.lower() in generic_names)
    features["generic_name_ratio"] = generic_count / len(all_names)
    
    # Very descriptive names (AI sometimes over-describes)
    descriptive_count = sum(1 for name in all_names if len(name) > 15)
    features["descriptive_name_ratio"] = descriptive_count / len(all_names)
    
    return features


def calculate_complexity(node_counts: Dict[str, int]) -> float:
    """Calculate a complexity score based on AST node counts."""
    if not node_counts:
        return 0.0
        
    complexity_weights = {
        "If": 1, "For": 2, "While": 2, "Try": 1,
        "FunctionDef": 1, "ClassDef": 2, "Lambda": 1
    }
    
    total_complexity = sum(
        node_counts.get(node_type, 0) * weight
        for node_type, weight in complexity_weights.items()
    )
    
    return float(total_complexity)


def calculate_indentation_consistency(indentations: List[int]) -> float:
    """Calculate how consistent the indentation is (0-1 score)."""
    if len(indentations) < 2:
        return 1.0
    
    # Calculate variance in indentation
    mean_indent = sum(indentations) / len(indentations)
    variance = sum((x - mean_indent) ** 2 for x in indentations) / len(indentations)
    
    # Convert to consistency score (lower variance = higher consistency)
    consistency = 1 / (1 + math.sqrt(variance))
    return consistency


def calculate_formatting_perfection(code: str) -> float:
    """Calculate how 'perfectly' formatted the code is (AI tends to be very consistent)."""
    if not code or not code.strip():
        return 0.0
        
    lines = code.split('\n')
    
    # Check various formatting aspects
    perfect_aspects = 0
    total_aspects = 0
    
    try:
        # Consistent spacing around operators
        operators_with_spaces = len(re.findall(r'\s[+\-*/=<>!]=?\s', code))
        operators_without_spaces = len(re.findall(r'[^\s][+\-*/=<>!]=?[^\s]', code))
        if operators_with_spaces + operators_without_spaces > 0:
            total_aspects += 1
            if operators_with_spaces > operators_without_spaces:
                perfect_aspects += 1
        
        # Consistent comma spacing
        commas_with_space = len(re.findall(r',\s', code))
        commas_without_space = len(re.findall(r',[^\s]', code))
        if commas_with_space + commas_without_space > 0:
            total_aspects += 1
            if commas_with_space > commas_without_space:
                perfect_aspects += 1
        
        # Line length consistency (AI often keeps lines under certain limits)
        line_lengths = [len(line) for line in lines if line.strip()]
        if line_lengths:
            avg_length = sum(line_lengths) / len(line_lengths)
            long_lines = sum(1 for length in line_lengths if length > 100)
            total_aspects += 1
            if long_lines / len(line_lengths) < 0.1:  # Less than 10% long lines
                perfect_aspects += 1
    except Exception as e:
        logger.warning(f"Error calculating formatting perfection: {e}")
        return 0.0
    
    return perfect_aspects / max(total_aspects, 1) 