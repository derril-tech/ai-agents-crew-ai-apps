#!/bin/bash
# Content Marketing Project Manager - Run Script

echo "🚀 Content Marketing Project Manager"
echo "======================================"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it with: pip install uv"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo "📝 Please edit .env file and add your OPENAI_API_KEY"
        echo "   Then run this script again."
        exit 0
    else
        echo "❌ .env.example template not found"
        exit 1
    fi
fi

# Check if OPENAI_API_KEY is set in .env
if ! grep -q "OPENAI_API_KEY=" .env || grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
    echo "❌ Please set your OPENAI_API_KEY in the .env file"
    exit 1
fi

echo "✅ Environment validated"
echo "🔄 Running Content Marketing Project Manager..."
echo ""

# Run the application
uv run python -m content_marketing_project_manager.main

echo ""
echo "✅ Execution completed!"
echo "📁 Check the 'outputs' directory for generated project plans"
