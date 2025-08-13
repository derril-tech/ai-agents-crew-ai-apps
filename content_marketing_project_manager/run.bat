@echo off
REM Content Marketing Project Manager - Run Script for Windows

echo 🚀 Content Marketing Project Manager
echo ======================================

REM Check if UV is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ UV is not installed. Please install it with: pip install uv
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ Created .env file from template
        echo 📝 Please edit .env file and add your OPENAI_API_KEY
        echo    Then run this script again.
        pause
        exit /b 0
    ) else (
        echo ❌ .env.example template not found
        pause
        exit /b 1
    )
)

REM Check if OPENAI_API_KEY is set in .env
findstr /C:"OPENAI_API_KEY=your_openai_api_key_here" .env >nul
if not errorlevel 1 (
    echo ❌ Please set your OPENAI_API_KEY in the .env file
    pause
    exit /b 1
)

findstr /C:"OPENAI_API_KEY=" .env >nul
if errorlevel 1 (
    echo ❌ Please set your OPENAI_API_KEY in the .env file
    pause
    exit /b 1
)

echo ✅ Environment validated
echo 🔄 Running Content Marketing Project Manager...
echo.

REM Run the application
uv run python -m content_marketing_project_manager.main

echo.
echo ✅ Execution completed!
echo 📁 Check the 'outputs' directory for generated project plans
pause
