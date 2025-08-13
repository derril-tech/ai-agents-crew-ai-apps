#!/bin/bash

# Sales Pitch Assistant Startup Script
echo "🚀 Starting AI Sales Pitch Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install dependencies if needed
echo "📦 Installing dependencies..."

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm run install-all

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found."
    echo "Please create backend/.env with your API keys:"
    echo "GROQ_API_KEY=your_groq_api_key_here"
    echo "SERPER_API_KEY=your_serper_api_key_here"
    echo ""
    echo "You can copy from backend/env.example"
fi

# Test the setup
echo "🧪 Testing setup..."
cd backend
source venv/bin/activate
python test_setup.py
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Make sure you have set up your API keys in backend/.env"
echo "2. Run: npm run dev"
echo ""
echo "This will start:"
echo "- API server on http://localhost:3001"
echo "- Frontend on http://localhost:3000"
echo ""
echo "Or start components individually:"
echo "- API only: npm run start-api"
echo "- Frontend only: npm run start-frontend"
