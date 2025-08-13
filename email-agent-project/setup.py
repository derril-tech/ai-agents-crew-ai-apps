# setup.py
"""
Setup script for Email Agent Project
Run this to initialize the development environment
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def run_command(command, shell=False):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def check_python_version():
    """Check if Python version is correct"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 12:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"❌ Python 3.12+ required, found {version.major}.{version.minor}")
        return False


def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("\n🔍 Checking prerequisites...")
    
    checks = {
        "Python 3.12+": check_python_version(),
        "PostgreSQL": run_command(["psql", "--version"])[0],
        "Redis/Memurai": run_command(["redis-cli", "ping"], shell=True)[0],
        "Node.js": run_command(["node", "--version"], shell=True)[0],
        "uv": run_command(["uv", "--version"], shell=True)[0]
    }
    
    all_good = True
    for name, status in checks.items():
        if status:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - Please install")
            all_good = False
    
    return all_good


def setup_database():
    """Initialize PostgreSQL database"""
    print("\n🗄️ Setting up PostgreSQL database...")
    
    db_setup_sql = """
    -- Create user if not exists
    DO
    $do$
    BEGIN
       IF NOT EXISTS (
          SELECT FROM pg_catalog.pg_user
          WHERE usename = 'emailagent') THEN
          CREATE USER emailagent WITH PASSWORD 'emailagent123';
       END IF;
    END
    $do$;

    -- Create database if not exists
    SELECT 'CREATE DATABASE emailagent_db OWNER emailagent'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'emailagent_db')\\gexec
    
    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE emailagent_db TO emailagent;
    """
    
    # Save SQL to file
    with open("init_db.sql", "w") as f:
        f.write(db_setup_sql)
    
    # Execute SQL
    success, output = run_command(["psql", "-U", "postgres", "-f", "init_db.sql"], shell=True)
    
    if success or "already exists" in output:
        print("  ✅ Database configured")
        os.remove("init_db.sql")
        return True
    else:
        print(f"  ⚠️ Database setup issue: {output}")
        return False


def setup_python_environment():
    """Set up Python virtual environment and install dependencies"""
    print("\n🐍 Setting up Python environment...")
    
    # Create virtual environment with uv
    print("  Creating virtual environment...")
    success, output = run_command(["uv", "venv"], shell=True)
    if not success:
        print(f"  ❌ Failed to create venv: {output}")
        return False
    
    # Install dependencies
    print("  Installing Python dependencies...")
    
    # Create a minimal requirements.txt for Phase 1
    requirements = """
# Core
crewai==0.86.0
crewai-tools>=0.17.0
python-dotenv>=1.0.0

# LLM Providers
openai>=1.54.0
google-generativeai>=0.8.0
langchain>=0.3.0
langchain-community>=0.3.0
langchain-openai>=0.2.0
langchain-google-genai>=2.0.0

# Gmail
google-api-python-client>=2.149.0
google-auth>=2.35.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0

# Database
sqlalchemy>=2.0.35
psycopg2-binary>=2.9.9
redis>=5.0.0

# Web framework (minimal for Phase 1)
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
httpx>=0.27.0
pydantic>=2.9.0
"""
    
    with open("backend/requirements.txt", "w") as f:
        f.write(requirements)
    
    # Install with uv
    if os.name == 'nt':  # Windows
        pip_path = ".venv\\Scripts\\pip"
    else:  # Unix
        pip_path = ".venv/bin/pip"
    
    success, output = run_command([pip_path, "install", "-r", "backend/requirements.txt"])
    
    if success:
        print("  ✅ Python dependencies installed")
        return True
    else:
        print(f"  ❌ Failed to install dependencies: {output}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n📝 Setting up environment variables...")
    
    env_path = Path(".env")
    if env_path.exists():
        print("  ⚠️ .env file already exists, skipping")
        return True
    
    env_content = """# Email Agent Configuration
# IMPORTANT: Add your actual API keys here

# LLM Providers
OPENAI_API_KEY=sk-YOUR_KEY_HERE
GOOGLE_API_KEY=YOUR_GEMINI_KEY_HERE
MODEL=gpt-4o

# Search Tools
SERPER_API_KEY=YOUR_SERPER_KEY_HERE
TAVILY_API_KEY=tvly-YOUR_TAVILY_KEY_HERE

# Gmail
GMAIL_CREDENTIALS_PATH=./credentials.json
MY_EMAIL=your_email@gmail.com

# Database
DATABASE_URL=postgresql://emailagent:emailagent123@localhost:5432/emailagent_db
REDIS_URL=redis://localhost:6379/0

# Application
APP_ENV=development
API_PORT=8000
AGENT_CHECK_INTERVAL=180
AGENT_BATCH_SIZE=10

# User Context
USER_NAME=Your Name
USER_COMPANY=Your Company
USER_ROLE=Your Role
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("  ✅ .env file created - PLEASE ADD YOUR API KEYS")
    return True


def verify_gmail_credentials():
    """Check if Gmail credentials.json exists"""
    print("\n🔐 Checking Gmail credentials...")
    
    if Path("credentials.json").exists():
        print("  ✅ credentials.json found")
        return True
    else:
        print("  ⚠️ credentials.json not found")
        print("  📋 Please follow these steps:")
        print("     1. Go to https://console.cloud.google.com/")
        print("     2. Create a new project or select existing")
        print("     3. Enable Gmail API")
        print("     4. Create OAuth 2.0 credentials (Desktop App)")
        print("     5. Download and save as 'credentials.json' in project root")
        return False


def test_imports():
    """Test that all critical imports work"""
    print("\n🧪 Testing imports...")
    
    try:
        import crewai
        print("  ✅ CrewAI imported")
    except ImportError as e:
        print(f"  ❌ CrewAI import failed: {e}")
        return False
    
    try:
        import openai
        print("  ✅ OpenAI imported")
    except ImportError as e:
        print(f"  ❌ OpenAI import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("  ✅ Google Generative AI imported")
    except ImportError as e:
        print(f"  ❌ Google AI import failed: {e}")
        return False
    
    return True


def main():
    """Main setup function"""
    print("="*60)
    print("🚀 EMAIL AGENT PROJECT - PHASE 1 SETUP")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Please install missing prerequisites first")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    # Setup Python environment
    if not setup_python_environment():
        print("\n❌ Python environment setup failed")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check Gmail credentials
    gmail_ok = verify_gmail_credentials()
    
    # Test imports
    test_ok = test_imports()
    
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    if gmail_ok and test_ok:
        print("✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Add your API keys to .env file")
        print("2. Add Gmail credentials.json if not present")
        print("3. Run: python backend/agents/flows/email_flow.py")
    else:
        print("⚠️ Setup completed with warnings")
        print("Please address the issues above before running the agent")
    
    print("\n💡 To test the setup:")
    print("   python backend/test_setup.py")


if __name__ == "__main__":
    main()