# 60 AI Apps Pipeline - Windows Setup Script
# Run this script in PowerShell to set up the development environment

Write-Host "🚀 Setting up 60 AI Apps Pipeline..." -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}

python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your API keys" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create necessary directories
Write-Host "Creating project directories..." -ForegroundColor Yellow
$directories = @("deliverables", "dashboard", "scripts")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Test CrewAI installation
Write-Host "Testing CrewAI installation..." -ForegroundColor Yellow
try {
    python -c "import crewai; print('✅ CrewAI imported successfully')"
} catch {
    Write-Host "❌ CrewAI import failed. Please check the installation." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Copy your 60 projects to projects.json" -ForegroundColor White
Write-Host "3. Run: python scripts/project_tagger.py" -ForegroundColor White
Write-Host "4. Run: python scripts/progress_dashboard.py" -ForegroundColor White
Write-Host "5. Run: python run_all.py" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Cyan
Write-Host "For services signup checklist, see SERVICES_SIGNUP_CHECKLIST.md" -ForegroundColor Cyan

