#!/usr/bin/env python3
"""
Test script for AI Code Detection Bot
Verifies that all components are working correctly
"""

import sys
import os
import importlib.util

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    required_modules = [
        'flask', 'flask_cors', 'sklearn', 'numpy', 'pandas', 'joblib', 'astroid'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} (missing)")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {missing_modules}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_backend_modules():
    """Test that backend modules can be imported."""
    print("\nTesting backend modules...")
    
    # Add backend to path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    try:
        from extract_features import extract_code_features
        from predict import predict_ai_code, create_dummy_model
        print("  ✓ extract_features")
        print("  ✓ predict")
    except ImportError as e:
        print(f"  ✗ Backend modules error: {e}")
        return False
    
    print("✅ Backend modules working!")
    return True

def test_feature_extraction():
    """Test feature extraction functionality."""
    print("\nTesting feature extraction...")
    
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    try:
        from extract_features import extract_code_features
        
        # Test valid Python code
        sample_code = '''def hello_world():
    """A simple hello world function."""
    print("Hello, World!")
    return "success"
'''
        features = extract_code_features(sample_code, "python")
        
        # Check that we got expected features
        expected_features = [
            'lines_of_code', 'comment_ratio', 'function_count', 
            'complexity_score', 'indentation_consistency'
        ]
        
        missing_features = [f for f in expected_features if f not in features]
        if missing_features:
            print(f"  ✗ Missing features: {missing_features}")
            return False
            
        # Test empty code
        empty_features = extract_code_features("", "python")
        if not all(v == 0 or v == 0.0 for v in empty_features.values()):
            print("  ✗ Empty code should return zero values")
            return False
            
        # Test invalid code
        invalid_code = "def invalid_syntax("
        invalid_features = extract_code_features(invalid_code, "python")
        if not all(isinstance(v, (int, float)) for v in invalid_features.values()):
            print("  ✗ Invalid code should return numeric values")
            return False
        
        print(f"  ✓ Extracted {len(features)} features")
        print(f"  ✓ Lines of code: {features['lines_of_code']}")
        print(f"  ✓ Function count: {features['function_count']}")
        print("  ✓ Handles empty and invalid code")
        
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        print("  ℹ Make sure you're running tests from the project root")
        return False
    except Exception as e:
        print(f"  ✗ Feature extraction error: {e}")
        return False
    
    print("✅ Feature extraction working!")
    return True

def test_prediction():
    """Test prediction functionality."""
    print("\nTesting prediction...")
    
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    try:
        from predict import create_dummy_model, predict_ai_code
        from extract_features import extract_code_features
        
        # Create dummy model
        model = create_dummy_model()
        
        # Test sample code
        sample_code = '''def fibonacci(n):
    """Generate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(f"The 10th Fibonacci number is: {result}")'''
        
        features = extract_code_features(sample_code, "python")
        prediction = predict_ai_code(model, features)
        
        # Check prediction format
        required_keys = ['prediction', 'confidence', 'ai_probability', 'human_probability', 'reasons']
        missing_keys = [k for k in required_keys if k not in prediction]
        
        if missing_keys:
            print(f"  ✗ Missing prediction keys: {missing_keys}")
            return False
        
        print(f"  ✓ Prediction: {prediction['prediction']}")
        print(f"  ✓ Confidence: {prediction['confidence']:.2f}")
        print(f"  ✓ Reasons: {len(prediction['reasons'])} provided")
        
    except Exception as e:
        print(f"  ✗ Prediction error: {e}")
        return False
    
    print("✅ Prediction working!")
    return True

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'requirements.txt',
        'README.md',
        'backend/app.py',
        'backend/extract_features.py',
        'backend/predict.py',
        'backend/run.py',
        'frontend/index.html',
        'frontend/styles.css',
        'frontend/script.js',
        'model_training/train_model.ipynb'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present!")
    return True

def main():
    """Run all tests."""
    print("🤖 AI Code Detection Bot - Project Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_backend_modules,
        test_feature_extraction,
        test_prediction
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        test_name = test.__name__.replace('test_', '').replace('_', ' ').title()
        print(f"\nRunning {test_name}...")
        try:
            if test():
                passed += 1
                print(f"✅ {test_name} passed!")
            else:
                failed += 1
                print(f"❌ {test_name} failed!")
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrupted by user")
            return 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your AI Code Detection Bot is ready!")
        print("\n🚀 Next steps:")
        print("1. Start the backend: cd backend && python run.py")
        print("2. Open frontend/index.html in your browser")
        print("3. Test with some code samples")
        print("4. Deploy to production")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1) 