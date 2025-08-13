#!/usr/bin/env python
"""
Test script to verify the sales pitch assistant setup
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import crewai
        print("✓ crewai imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import crewai: {e}")
        print("💡 Install with: pip install crewai")
        return False
    
    try:
        import crewai_tools
        print("✓ crewai_tools imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import crewai_tools: {e}")
        print("💡 Install with: pip install crewai-tools")
        return False
    
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        print("✓ langchain_community imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain_community: {e}")
        print("💡 Install with: pip install langchain-community")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✓ langchain_openai imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain_openai: {e}")
        print("💡 Install with: pip install langchain-openai")
        return False
    
    try:
        import yaml
        print("✓ pyyaml imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pyyaml: {e}")
        print("💡 Install with: pip install pyyaml")
        return False
    
    return True

def test_config_files():
    """Test if configuration files exist and are valid"""
    print("\nTesting configuration files...")
    
    config_dir = Path("config")
    if not config_dir.exists():
        print("✗ config directory not found")
        return False
    
    agents_file = config_dir / "agents.yaml"
    if not agents_file.exists():
        print("✗ agents.yaml not found")
        return False
    else:
        print("✓ agents.yaml found")
    
    tasks_file = config_dir / "tasks.yaml"
    if not tasks_file.exists():
        print("✗ tasks.yaml not found")
        return False
    else:
        print("✓ tasks.yaml found")
    
    # Test YAML parsing
    try:
        import yaml
        with open(agents_file, 'r') as f:
            yaml.safe_load(f)
        print("✓ agents.yaml is valid YAML")
        
        with open(tasks_file, 'r') as f:
            yaml.safe_load(f)
        print("✓ tasks.yaml is valid YAML")
    except Exception as e:
        print(f"✗ YAML parsing failed: {e}")
        return False
    
    return True

def test_environment():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("✗ OPENAI_API_KEY not set or using placeholder value")
        print("💡 Get API key from: https://platform.openai.com/api-keys")
        print("💡 Set in .env file or environment variable")
        return False
    else:
        print("✓ OPENAI_API_KEY is set")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your_groq_api_key_here":
        print("⚠️ GROQ_API_KEY not set (optional for this setup)")
    else:
        print("✓ GROQ_API_KEY is set")
    
    serper_key = os.getenv("SERPER_API_KEY")
    if not serper_key or serper_key == "your_serper_api_key_here":
        print("⚠️ SERPER_API_KEY not set (optional for this setup)")
    else:
        print("✓ SERPER_API_KEY is set")
    
    return True

def test_crew_import():
    """Test if the crew module can be imported"""
    print("\nTesting crew module...")
    
    try:
        from sales_meeting_preparation.crew import SalesMeetingPreparation
        print("✓ SalesMeetingPreparation imported successfully")
        
        # Test crew instantiation (without running)
        crew_instance = SalesMeetingPreparation()
        print("✓ SalesMeetingPreparation instantiated successfully")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import or instantiate crew: {e}")
        return False

def main():
    """Run all tests"""
    print("Sales Pitch Assistant Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config_files,
        test_environment,
        test_crew_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The setup is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
