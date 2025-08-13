#!/bin/bash

# setup.sh - Unix startup script for SDR Assistant
set -e

echo "🚀 Starting SDR Assistant Application..."
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print colored output
print_status() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_warning() {
    echo -e "\033[33m⚠️  $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ️  $1\033[0m"
}

# Check dependencies
echo "🔍 Checking dependencies..."

if ! command_exists uv; then
    print_error "uv is not installed. Please install uv first."
    echo "Visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

if ! command_exists npm; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "Dependencies verified"
echo

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
uv pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your API keys before continuing."
    read -p "Press Enter after updating .env file..."
fi

# Install CrewAI dependencies
echo "🤖 Installing CrewAI dependencies..."
crewai install

print_status "Backend setup complete"
echo

# Setup frontend
echo "🎨 Setting up frontend..."
cd ../frontend

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    print_warning ".env.local file not found. Creating from template..."
    cp .env.local.example .env.local
fi

print_status "Frontend setup complete"
echo

# Start services
echo "🚀 Starting services..."

# Start backend in background
echo "🔧 Starting backend server..."
cd ../backend
nohup uv run python run.py api --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "Backend server is running"
else
    print_error "Backend server failed to start. Check backend.log for details."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend development server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo
print_status "SDR Assistant is starting up!"
echo "🌐 Backend API: http://localhost:8000"
echo "🎨 Frontend App: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo

# Save PIDs for cleanup
echo $BACKEND_PID > ../backend.pid
echo $FRONTEND_PID > ../frontend.pid

echo "💾 Process IDs saved for cleanup"
echo

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 10

# Open browser (if available)
if command_exists open; then
    echo "🌐 Opening application in browser..."
    open http://localhost:3000
elif command_exists xdg-open; then
    echo "🌐 Opening application in browser..."
    xdg-open http://localhost:3000
fi

echo
print_status "🎉 SDR Assistant is now running!"
echo
echo "To stop the application, run: ./scripts/stop.sh"
echo "To view logs: tail -f backend/backend.log"
echo
echo "Press Ctrl+C to stop this script (services will continue running)"

# Keep script running to show status
trap 'echo; print_info "Script interrupted. Services are still running."; exit 0' INT

while true; do
    sleep 30
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend process has stopped"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend process has stopped"
        break
    fi
done