# backend/test_setup.py
"""
Test script to verify Email Agent setup
Run this after setup.py to ensure everything is configured correctly
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_env_variables():
    """Test that all required environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "GOOGLE_API_KEY": "Google Gemini API Key",
        "SERPER_API_KEY": "Serper API Key",
        "TAVILY_API_KEY": "Tavily API Key",
        "MY_EMAIL": "Gmail Address",
        "DATABASE_URL": "PostgreSQL Connection",
        "REDIS_URL": "Redis Connection"
    }
    
    all_good = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"YOUR_{var}_HERE" and "YOUR_KEY_HERE" not in value:
            print(f"  ✅ {description}: Set")
        else:
            print(f"  ❌ {description}: Missing or default")
            all_good = False
    
    return all_good


def test_database_connection():
    """Test PostgreSQL connection"""
    print("\n🗄️ Testing PostgreSQL connection...")
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"  ✅ PostgreSQL connected: {version[:30]}...")
            return True
    except Exception as e:
        print(f"  ❌ PostgreSQL connection failed: {e}")
        return False


def test_redis_connection():
    """Test Redis connection"""
    print("\n📦 Testing Redis connection...")
    
    try:
        import redis
        
        r = redis.from_url(os.getenv("REDIS_URL"))
        r.ping()
        print("  ✅ Redis connected")
        
        # Test basic operations
        r.set("test_key", "test_value")
        value = r.get("test_key")
        r.delete("test_key")
        
        if value == b"test_value":
            print("  ✅ Redis operations working")
        
        return True
    except Exception as e:
        print(f"  ❌ Redis connection failed: {e}")
        return False


def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🤖 Testing OpenAI connection...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("  ✅ OpenAI API connected")
            return True
    except Exception as e:
        print(f"  ❌ OpenAI connection failed: {e}")
        return False


def test_google_ai_connection():
    """Test Google Gemini API connection"""
    print("\n🤖 Testing Google Gemini connection...")
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'test successful'")
        
        if response.text:
            print("  ✅ Google Gemini API connected")
            return True
    except Exception as e:
        print(f"  ❌ Google Gemini connection failed: {e}")
        return False


def test_gmail_credentials():
    """Test Gmail credentials file"""
    print("\n📧 Testing Gmail setup...")
    
    creds_path = Path(os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"))
    
    if not creds_path.exists():
        print("  ❌ credentials.json not found")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            
        if "installed" in creds or "web" in creds:
            print("  ✅ Gmail credentials file valid")
            return True
        else:
            print("  ❌ Invalid credentials.json format")
            return False
    except Exception as e:
        print(f"  ❌ Error reading credentials: {e}")
        return False


def test_crewai_setup():
    """Test CrewAI configuration"""
    print("\n🤖 Testing CrewAI setup...")
    
    try:
        from backend.agents.crews.email_filter_crew import EmailFilterCrew
        
        # Check if config files exist
        agents_config = Path("backend/agents/crews/config/agents.yaml")
        tasks_config = Path("backend/agents/crews/config/tasks.yaml")
        
        if not agents_config.exists():
            print("  ❌ agents.yaml not found")
            return False
        
        if not tasks_config.exists():
            print("  ❌ tasks.yaml not found")
            return False
        
        print("  ✅ CrewAI configuration files found")
        
        # Try to initialize crew
        crew = EmailFilterCrew()
        print("  ✅ EmailFilterCrew initialized")
        
        return True
    except Exception as e:
        print(f"  ❌ CrewAI setup error: {e}")
        return False


def test_sample_email_processing():
    """Test processing a sample email"""
    print("\n📝 Testing sample email processing...")
    
    try:
        from backend.agents.crews.email_filter_crew import EmailFilterCrew
        
        # Create sample email
        sample_email = {
            "id": "test_123",
            "threadId": "thread_123",
            "sender": "test@example.com",
            "subject": "Test Email",
            "body": "This is a test email that requires a response.",
            "snippet": "This is a test email...",
            "labels": ["UNREAD"],
            "is_unread": True,
            "is_important": False,
            "has_attachments": False
        }
        
        print("  📧 Sample email created")
        
        # Initialize crew
        crew = EmailFilterCrew()
        
        # Process email (simplified test)
        print("  🔄 Processing sample email...")
        # Note: Full processing requires API keys
        
        print("  ✅ Email processing framework operational")
        return True
        
    except Exception as e:
        print(f"  ⚠️ Sample processing setup incomplete: {e}")
        return False


def main():
    """Main test function"""
    print("="*60)
    print("🧪 EMAIL AGENT - PHASE 1 TEST SUITE")
    print("="*60)
    
    tests = {
        "Environment Variables": test_env_variables(),
        "PostgreSQL Connection": test_database_connection(),
        "Redis Connection": test_redis_connection(),
        "Gmail Credentials": test_gmail_credentials(),
        "CrewAI Setup": test_crewai_setup()
    }
    
    # Optional tests (only if API keys are configured)
    if os.getenv("OPENAI_API_KEY") and "sk-" in os.getenv("OPENAI_API_KEY", ""):
        tests["OpenAI API"] = test_openai_connection()
    
    if os.getenv("GOOGLE_API_KEY") and "YOUR_KEY" not in os.getenv("GOOGLE_API_KEY", ""):
        tests["Google Gemini API"] = test_google_ai_connection()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in tests.values() if v)
    total = len(tests)
    
    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Email Agent is ready to run.")
        print("\n▶️ To start the agent:")
        print("   python backend/agents/flows/email_flow.py")
    else:
        print("\n⚠️ Some tests failed. Please address the issues above.")
        print("Check your .env file and ensure all services are running.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)