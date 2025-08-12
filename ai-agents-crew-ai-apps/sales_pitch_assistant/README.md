# 🤖 AI Sales Pitch Assistant

> **by Derril Filemon - AI Engineer**

A powerful AI-powered sales pitch generation system that leverages CrewAI's multi-agent framework to create personalized, research-driven sales strategies for any executive and company combination.

![AI Sales Pitch Assistant](https://img.shields.io/badge/AI-Powered%20Sales%20Assistant-blue?style=for-the-badge&logo=robot)
![CrewAI](https://img.shields.io/badge/Built%20with-CrewAI-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge&logo=fastapi)

## ✨ Features

- 🧠 **AI-Powered Research**: Advanced multi-agent system conducts comprehensive company and executive research
- 🎯 **Personalized Pitches**: Tailored sales strategies based on specific company needs and executive profiles
- 📊 **Real-time Intelligence**: Live web research provides up-to-date company insights and market intelligence
- 📄 **Professional Reports**: Structured markdown reports ready for immediate use in sales meetings
- 🌐 **Modern Web Interface**: Beautiful React frontend with real-time generation capabilities
- ⚡ **Fast API**: High-performance FastAPI backend with async processing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend│    │   CrewAI Agents  │
│   (Port 3000)   │◄──►│   (Port 3001)   │◄──►│   (Multi-Agent) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐            ┌────▼────┐            ┌────▼────┐
    │  Form   │            │  API    │            │ Research│
    │  Input  │            │  Routes │            │  Agents │
    └─────────┘            └─────────┘            └─────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key (or other supported LLM provider)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-agents-crew-ai-apps/sales_pitch_assistant
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment (Windows)
   .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   python -m uvicorn api_server:app --host 127.0.0.1 --port 3001
   ```

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001
   - API Documentation: http://localhost:3001/docs

## 🎯 Usage

1. **Open the web interface** at http://localhost:3000
2. **Enter the executive name** (e.g., "Marc Benioff")
3. **Enter the company name** (e.g., "Salesforce")
4. **Click "Generate Report"** to start the AI-powered analysis
5. **Wait for the comprehensive report** to be generated
6. **Review and use the generated sales pitch** for your meetings

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Alternative LLM Providers
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional: User Agent for web scraping
USER_AGENT=YourApp/1.0 (your@email.com)
```

### Supported LLM Providers

- OpenAI GPT-4/GPT-3.5
- Groq (fast inference)
- Google Gemini
- Anthropic Claude (via CrewAI)

## 🏛️ Project Structure

```
sales_pitch_assistant/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── styles/          # CSS and styling
│   │   └── App.jsx          # Main application component
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                  # FastAPI backend application
│   ├── sales_meeting_preparation/
│   │   ├── crew.py          # CrewAI crew definition
│   │   ├── agents/          # AI agent definitions
│   │   └── tools/           # Custom tools for agents
│   ├── api_server.py        # FastAPI server
│   ├── main.py              # CLI interface
│   ├── requirements.txt     # Python dependencies
│   └── outputs/             # Generated reports
├── README.md                # This file
└── start.sh                 # Quick start script
```

## 🤖 AI Agents Overview

The system uses multiple specialized AI agents:

### 🔍 **Research Agent**
- Conducts comprehensive company research
- Analyzes recent news and developments
- Gathers market intelligence

### 👤 **Executive Profiler**
- Researches executive background and interests
- Identifies decision-making patterns
- Finds personal and professional connections

### 💼 **Sales Strategist**
- Develops personalized sales approaches
- Creates compelling value propositions
- Identifies pain points and solutions

### 📝 **Report Generator**
- Compiles all research into structured reports
- Formats content for professional presentation
- Ensures consistency and quality

## 📊 API Endpoints

### POST `/api/generate-sales-pitch`
Generate a sales pitch report for a specific executive and company.

**Request Body:**
```json
{
  "person": "Marc Benioff",
  "company": "Salesforce"
}
```

**Response:**
```json
{
  "success": true,
  "report": "# Sales Meeting Preparation Report...",
  "filename": "sales_meeting_prep_salesforce_2025-08-12_10-30.md",
  "person": "Marc Benioff",
  "company": "Salesforce",
  "timestamp": "2025-08-12_10-30"
}
```

### GET `/api/health`
Health check endpoint for monitoring.

## 🛠️ Development

### Adding New Agents

1. Create a new agent file in `backend/sales_meeting_preparation/agents/`
2. Define the agent's role, goals, and tools
3. Add the agent to the crew in `crew.py`
4. Test the integration

### Customizing Tools

1. Create custom tools in `backend/sales_meeting_preparation/tools/`
2. Register tools with the appropriate agents
3. Update the crew configuration

### Frontend Customization

The React frontend is built with:
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **React Markdown** for report rendering
- **Axios** for API communication

## 📈 Performance

- **Typical generation time**: 2-5 minutes
- **Concurrent requests**: Supported via async processing
- **Report quality**: Professional-grade, ready for immediate use
- **Scalability**: Designed for production deployment

## 🔒 Security

- API key management via environment variables
- CORS protection for frontend-backend communication
- Input validation and sanitization
- Rate limiting capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI** for the powerful multi-agent framework
- **OpenAI** for advanced language models
- **FastAPI** for the high-performance web framework
- **React** for the modern frontend framework

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the repository
- Contact: [Your Contact Information]

---

**Made with ❤️ by Derril Filemon - AI Engineer**

*Transform your sales process with AI-powered intelligence*
