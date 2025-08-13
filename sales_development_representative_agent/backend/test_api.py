#!/usr/bin/env python
"""
Simple API Test Script
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing imports...")
        from src.sdr_assistant_flow.api.app import app
        print("✅ API app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test if the FastAPI app can be created"""
    try:
        print("Testing app creation...")
        from src.sdr_assistant_flow.api.app import app
        print(f"✅ App created: {app.title}")
        print(f"✅ App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing SDR Assistant API...")
    print("=" * 50)
    
    if not test_imports():
        return False
    
    if not test_app_creation():
        return False
    
    print("\n✅ All tests passed!")
    print("🚀 API is ready to start")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
