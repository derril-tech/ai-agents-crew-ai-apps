# Backend Applications & Scripts

This directory contains all backend applications, scripts, and automation tools for the 60 AI Apps Pipeline.

## Applications

### 1. CrewAI Pipeline (`crew_app/`)
**Location:** `crew_app/`

The main CrewAI orchestration system that builds all 60 AI applications using a team of specialized AI agents.

**Features:**
- Multi-agent workflow orchestration
- Automated project generation
- Market research and analysis
- Code generation and deployment
- Quality assurance and testing

**Tech Stack:**
- Python 3.9+
- CrewAI framework
- Anthropic Claude API
- OpenAI API
- LangChain
- FastAPI/Express.js templates

### 2. Automation Scripts (`scripts/`)
**Location:** `scripts/`

Collection of Python scripts for automating various aspects of the pipeline.

**Scripts:**
- `project_tagger.py` - Assigns archetypes and tech stacks to projects
- `progress_dashboard.py` - Generates HTML progress dashboard
- `services_bootstrapper.py` - Automates cloud service setup

### 3. Main Runner (`run_all.py`)
**Location:** `run_all.py`

The main entry point for running the entire pipeline to build all 60 applications.

## Setup

### Prerequisites
- Python 3.9+
- Virtual environment
- API keys for AI services

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys
```

### Running the Pipeline
```bash
# Run all 60 projects
python run_all.py

# Run individual scripts
python scripts/project_tagger.py
python scripts/progress_dashboard.py
python scripts/services_bootstrapper.py
```

## Configuration

### Environment Variables
See `env.example` for required environment variables:
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic Claude API key
- `TAVILY_API_KEY` - Tavily search API key
- And more...

### Project Configuration
- `projects.json` - List of all 60 projects
- `archetypes.json` - Tech stack and service mappings
- `tagged_projects.json` - Projects with assigned archetypes

## Architecture

The backend follows a modular architecture:
1. **Project Management** - Project tagging and configuration
2. **Agent Orchestration** - CrewAI multi-agent workflows
3. **Code Generation** - Automated full-stack app creation
4. **Deployment** - Cloud service automation
5. **Monitoring** - Progress tracking and dashboards
