@echo off
REM Sales Pitch Assistant Startup Script for Windows
echo 🚀 Starting AI Sales Pitch Assistant...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Install dependencies if needed
echo 📦 Installing dependencies...

REM Install Python dependencies
echo Installing Python dependencies...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

REM Install Node.js dependencies
echo Installing Node.js dependencies...
call npm run install-all

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  Warning: backend\.env file not found.
    echo Please create backend\.env with your API keys:
    echo GROQ_API_KEY=your_groq_api_key_here
    echo SERPER_API_KEY=your_serper_api_key_here
    echo.
    echo You can copy from backend\env.example
)

REM Test the setup
echo 🧪 Testing setup...
cd backend
call venv\Scripts\activate.bat
python test_setup.py
cd ..

echo.
echo 🎉 Setup complete!
echo.
echo To start the application:
echo 1. Make sure you have set up your API keys in backend\.env
echo 2. Run: npm run dev
echo.
echo This will start:
echo - API server on http://localhost:3001
echo - Frontend on http://localhost:3000
echo.
echo Or start components individually:
echo - API only: npm run start-api
echo - Frontend only: npm run start-frontend

pause
