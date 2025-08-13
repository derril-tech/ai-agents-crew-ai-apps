#!/usr/bin/env python
"""
Setup script for Sales Pitch Assistant
This script helps install dependencies and set up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements from requirements.txt"):
        return False
    
    # Install additional tools packages
    if not run_command("pip install crewai-tools", "Installing crewai-tools"):
        return False
    
    if not run_command("pip install langchain-community", "Installing langchain-community"):
        return False
    
    return True

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    try:
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from env.example")
        print("💡 Please edit .env and add your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Sales Pitch Assistant Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file")
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your API keys:")
    print("   - Get Google API key from: https://makersuite.google.com/app/apikey")
    print("   - Get Groq API key from: https://console.groq.com/ (optional)")
    print("   - Get SerperDev API key from: https://serper.dev/ (optional)")
    print("2. Run test_setup.py to verify your setup:")
    print("   python test_setup.py")
    print("3. Run the crew:")
    print("   python sales_meeting_preparation/crew.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
