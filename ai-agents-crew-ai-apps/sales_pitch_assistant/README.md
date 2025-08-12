# AI Sales Pitch Assistant

An AI-powered sales pitch assistant built with CrewAI that generates personalized sales pitches by researching target companies and executives.

## Features

- 🤖 **AI-Powered Research**: Uses multiple AI agents to research companies and executives
- 📊 **Comprehensive Reports**: Generates detailed sales meeting preparation reports
- 🎯 **Personalized Pitches**: Tailors sales pitches to specific prospects
- 💾 **Report Management**: Save and download generated reports
- 🌐 **Web Interface**: Modern React frontend with real-time updates
- 🔌 **REST API**: Node.js backend for easy integration

## Architecture

The application consists of three main components:

1. **Backend (Python/CrewAI)**: AI agents that perform research and generate reports
2. **API Server (Node.js)**: REST API that bridges the frontend and backend
3. **Frontend (React)**: Modern web interface for user interaction

## Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- API keys for:
  - Groq (for LLM)
  - SerperDev (for web search)

## Setup Instructions

### 1. Clone and Navigate

```bash
cd ai-agents-crew-ai-apps/sales_pitch_assistant
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Or using pip with pyproject.toml
pip install -e .
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```bash
# Backend/.env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 4. API Server Setup

```bash
cd ../api

# Install Node.js dependencies
npm install

# Start the API server
npm start
```

The API server will run on `http://localhost:3001`

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Open the Application**: Navigate to `http://localhost:3000`
2. **Enter Target Information**: 
   - Target Person (e.g., "John Smith, CEO")
   - Company Name (e.g., "TechCorp Inc.")
3. **Generate Report**: Click "Generate Sales Pitch"
4. **Review Results**: View the generated report in the right panel
5. **Download Report**: Click the download button to save as markdown

## API Endpoints

- `POST /api/generate-sales-pitch` - Generate a new sales pitch report
- `GET /api/reports` - List all generated reports
- `GET /api/reports/:filename` - Download a specific report
- `GET /api/health` - Health check endpoint

## AI Agents

The system uses four specialized AI agents:

1. **Company Research Agent**: Researches target company information
2. **Executive Profile Agent**: Gathers information about the target person
3. **Sales Pitch Strategist**: Creates personalized sales pitches
4. **Report Quality Agent**: Finalizes and polishes the report

## Configuration

### Agents Configuration (`backend/config/agents.yaml`)
Define the roles, goals, and backstories for each AI agent.

### Tasks Configuration (`backend/config/tasks.yaml`)
Define the tasks each agent performs and their expected outputs.

## Development

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Build frontend
cd frontend
npm run build

# The API server will serve the built frontend in production
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all Python dependencies are installed
2. **API Key Errors**: Verify your environment variables are set correctly
3. **Port Conflicts**: Change ports in the respective configuration files
4. **CORS Issues**: The API server includes CORS middleware for development

### Logs

- Backend logs are printed to stdout
- API server logs are printed to the console
- Frontend errors appear in the browser console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.
