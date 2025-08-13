# 🤖 SDR Assistant Flow

> **Created by Derril Filemon for DFN AI Services**
> 
> **AI-Powered Sales Development Representative Assistant using CrewAI**

Transform your sales development process with advanced AI agents that analyze leads, score prospects, and generate personalized cold emails automatically.

![SDR Assistant](https://img.shields.io/badge/AI-Powered-blue) ![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-red) ![Next.js](https://img.shields.io/badge/Next.js-Frontend-black) ![TypeScript](https://img.shields.io/badge/TypeScript-Enabled-blue)

## 🌟 Features

### Core Capabilities
- **🎯 Intelligent Lead Analysis** - Multi-agent system analyzes lead profiles and company context
- **📊 Advanced Lead Scoring** - AI-powered scoring algorithm with 0-100 point scale
- **✉️ Personalized Email Generation** - Automated cold email creation with high conversion rates
- **🔄 Bulk Processing** - Handle hundreds of leads simultaneously
- **📈 Real-time Analytics** - Comprehensive dashboards and performance tracking

### Enterprise Features
- **🔍 Lead Enrichment** - Automatic data enhancement from multiple sources
- **🧪 A/B Testing** - Email template optimization with statistical analysis
- **🔗 CRM Integration** - Ready for Salesforce, HubSpot, and Pipedrive
- **📧 Email Tracking** - Open rates, click tracking, and response monitoring
- **🚨 Compliance Monitoring** - GDPR and CAN-SPAM compliance checking
- **⚡ Smart Follow-ups** - Automated sequence management
- **📋 Template Management** - Dynamic email templates with personalization
- **🎨 Modern UI** - Beautiful, responsive React interface

## 🏗️ Architecture

### Backend (Python)
- **CrewAI Flows** - Multi-agent orchestration system
- **FastAPI** - High-performance async web framework
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Database ORM with PostgreSQL support
- **Redis** - Caching and task queue management
- **Celery** - Background task processing

### Frontend (React/Next.js)
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **SWR** - Data fetching and caching
- **Recharts** - Data visualization

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with uv package manager
- **Node.js 18+** with npm
- **API Keys**: OpenAI and Serper (for web search)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd sales_development_representative_agent
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment (if not already created in VSCode)
uv venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Test setup
python run.py test
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.local.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

### 4. Run Application
```bash
# Option 1: Use startup scripts
# Windows:
.\scripts\startup.bat

# Unix/MacOS:
chmod +x scripts/setup.sh
./scripts/setup.sh

# Option 2: Manual start
# Terminal 1 (Backend):
cd backend
python run.py api

# Terminal 2 (Frontend):
cd frontend
npm run dev
```

### 5. Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 📖 Usage Guide

### Running Lead Analysis

#### Single Lead Analysis
```python
from src.sdr_assistant_flow.main import kickoff
from src.sdr_assistant_flow.lead_types import LeadInput

# Create a lead
lead = LeadInput(
    name="John Doe",
    job_title="VP of Engineering", 
    company="Tech Corp",
    email="john@techcorp.com",
    linkedin_url="https://linkedin.com/in/johndoe"
)

# Run analysis
results = kickoff([lead])
```

#### Bulk Processing via API
```bash
curl -X POST "http://localhost:8000/api/bulk-process" \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [
      {
        "name": "John Doe",
        "job_title": "VP Engineering",
        "company": "Tech Corp", 
        "email": "john@techcorp.com"
      }
    ]
  }'
```

#### Web Interface
1. Navigate to http://localhost:3000/leads
2. Click "Add Lead" or "Import CSV"
3. Fill in lead information
4. Click "Analyze All" to process leads