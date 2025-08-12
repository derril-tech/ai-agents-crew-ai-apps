# Sales Pitch Assistant Backend

A CrewAI-powered application that prepares comprehensive sales meeting materials by researching companies and executives.

## 🚀 Quick Setup

### 1. Install Dependencies

Run the automated setup script:
```bash
python setup.py
```

Or install manually:
```bash
pip install -r requirements.txt
pip install crewai-tools langchain-community
```

### 2. Configure API Keys

Create a `.env` file from the example:
```bash
cp env.example .env
```

Edit `.env` and add your API keys:
```env
# Required for Gemini LLM
GOOGLE_API_KEY=your_google_api_key_here

# Optional - for alternative LLM
GROQ_API_KEY=your_groq_api_key_here

# Optional - for web search
SERPER_API_KEY=your_serper_api_key_here
```

**Get API Keys:**
- **Google API Key**: https://makersuite.google.com/app/apikey
- **Groq API Key**: https://console.groq.com/ (optional)
- **SerperDev API Key**: https://serper.dev/ (optional)

### 3. Test Your Setup

Run the test script to verify everything is working:
```bash
python test_setup.py
```

### 4. Run the Application

```bash
python sales_meeting_preparation/crew.py
```

## 🔧 Troubleshooting

### Missing Dependencies

If you see errors about missing modules:

```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific missing packages
pip install crewai-tools
pip install langchain-community
pip install langchain-google-genai
```

### API Key Issues

If you get authentication errors:

1. **Check your .env file exists** and has the correct API key
2. **Verify the API key is valid** by testing it in the respective console
3. **Set environment variable directly** (PowerShell):
   ```powershell
   $env:GOOGLE_API_KEY = "your-api-key-here"
   ```

### Tool Import Warnings

The application will work even if some tools are missing:
- **CrewAI tools**: Provide web search and scraping capabilities
- **LangChain community tools**: Provide backup search functionality
- **Missing tools**: The app will run with limited capabilities

## 📁 Project Structure

```
backend/
├── sales_meeting_preparation/
│   ├── crew.py              # Main crew implementation
│   └── __init__.py
├── config/
│   ├── agents.yaml          # Agent configurations
│   └── tasks.yaml           # Task configurations
├── requirements.txt         # Python dependencies
├── setup.py                 # Automated setup script
├── test_setup.py           # Setup verification
├── env.example             # Environment variables template
└── README.md               # This file
```

## 🤖 How It Works

The application uses a crew of AI agents to:

1. **Company Research Agent**: Researches the target company
2. **Executive Profile Agent**: Creates profiles of meeting participants
3. **Sales Pitch Strategist**: Develops personalized sales pitches
4. **Report Quality Agent**: Ensures final output quality

## 🛠️ Development

### Adding New Tools

To add new tools to the agents:

1. Install the tool package
2. Import it in `crew.py`
3. Add it to the `get_tools_for_agent()` method

### Modifying Agents

Edit the YAML configuration files in the `config/` directory:
- `agents.yaml`: Agent roles, goals, and backstories
- `tasks.yaml`: Task descriptions and expected outputs

## 📝 License

This project is part of the AI Agents CrewAI Apps collection.
