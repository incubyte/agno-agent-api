#!/usr/bin/env python3
"""
Critical validation test - Tests if the app can actually start without errors
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_application_startup():
    """Test if the application can start without import/syntax errors"""
    
    try:
        print("🔍 Testing application startup...")
        
        # Test basic imports
        print("  - Testing core imports...")
        from app.core.config import settings
        print("    ✓ Config imported")
        
        from app.core.setup import create_application
        print("    ✓ Setup imported")
        
        # Test creating the app
        print("  - Testing application creation...")
        app = create_application()
        print("    ✓ Application created successfully")
        
        # Test main import
        print("  - Testing main module...")
        import main
        print("    ✓ Main module imported")
        print("    ✓ App instance available:", hasattr(main, 'app'))
        
        print("\n✅ ALL STARTUP TESTS PASSED!")
        print("🚀 The application is ready to run!")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print("Fix the import issue before running.")
        return False
        
    except Exception as e:
        print(f"\n❌ STARTUP ERROR: {e}")
        print("Fix the application setup issue before running.")
        return False

if __name__ == "__main__":
    success = test_application_startup()
    
    if success:
        print("\n" + "="*50)
        print("🎉 READY TO RUN!")
        print("Start the application with:")
        print("  python main.py")
        print("  # or")
        print("  uvicorn main:app --reload")
        print("="*50)
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("❌ APPLICATION NOT READY")
        print("Fix the errors above before running.")
        print("="*50)
        sys.exit(1)
