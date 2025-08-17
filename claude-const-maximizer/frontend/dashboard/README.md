# 🎯 60 AI Apps Pipeline - Progress Dashboard

A real-time, interactive dashboard for monitoring the progress of 60 AI applications being built by the CrewAI automation pipeline.

## 🚀 Overview

This dashboard serves as the **mission control center** for the 60 AI Apps Pipeline. It provides real-time visibility into the automated process of building 60 full-stack AI applications using CrewAI agents, Claude code generation, and automated deployment.

## ✨ Features

### 📊 Real-Time Progress Tracking
- **Live Updates**: Refreshes every 2 seconds to show current status
- **Progress Visualization**: Visual progress bars and percentage completion
- **Status Indicators**: Clear visual states (Not Started, In Progress, Complete, Failed)
- **Agent Activity**: Shows which CrewAI agents are currently working

### 🎮 Interactive Controls
- **Start Pipeline**: Trigger the real automation pipeline
- **Stop Pipeline**: Halt automation and clear active agents
- **Reset All**: Reset all projects to initial state
- **Project Details**: Click any project for detailed progress view

### 📈 Statistics Dashboard
- **Total Projects**: 60 AI applications
- **Completed**: Ready for deployment
- **In Progress**: Currently being built
- **Not Started**: Waiting to begin
- **Failed**: Projects with errors

### 🤖 Agent Simulation
- **Test Mode**: Simulate agent activity without real API calls
- **Visual Feedback**: Animated indicators for active agents
- **Milestone Tracking**: Individual task completion status
- **Debug Mode**: Test pipeline functionality safely

## 🏗️ Architecture

### Frontend Stack
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations and transitions
- **Recharts** - Data visualization components
- **Radix UI** - Accessible, unstyled UI components

### Backend Integration
- **API Routes** - Next.js API endpoints for data fetching
- **File System** - Reads project data from `projects.json`
- **Pipeline Data** - Real-time progress from `pipeline-todos.json`
- **Agent Simulator** - Testing and demonstration capabilities

### Data Flow
```
Backend Pipeline → API Endpoints → Dashboard → Live Updates
     ↓                    ↓              ↓           ↓
projects.json    → /api/projects → React State → UI Updates
pipeline-todos.json → /api/pipeline → Progress Data → Visual Feedback
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Access to the 60 AI Apps Pipeline backend

### Installation
```bash
# Navigate to dashboard directory
cd frontend/dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access the Dashboard
Open your browser and navigate to:
```
http://localhost:3000
```

## 📋 Usage Guide

### 1. Viewing Project Status
- **Project Cards**: Each card shows a project with current status
- **Progress Bars**: Visual representation of completion percentage
- **Status Badges**: Color-coded status indicators
- **Agent Indicators**: Blinking animation shows active agents

### 2. Monitoring Pipeline Progress
- **Real-time Updates**: Dashboard refreshes automatically every 2 seconds
- **Statistics Cards**: Overview of total progress across all projects
- **Detailed Views**: Click projects to see individual milestone progress

### 3. Controlling the Pipeline
- **Start Simulation**: Begin the automated pipeline execution
- **Stop Simulation**: Halt automation and clear active agents
- **Reset All**: Return all projects to initial state

### 4. Understanding Status Indicators

#### Project Status
- **⚪ Not Started** (Gray): Project hasn't begun yet
- **🟡 In Progress** (Yellow): Currently being worked on
- **🟢 Complete** (Green): Finished and ready for deployment
- **🔴 Failed** (Red): Encountered an error

#### Agent Activity
- **Blinking Badge**: Agent is currently working on this project
- **Agent Names**: Shows which specific agent is active:
  - `MarketResearcher` - Conducting market analysis
  - `PromptEngineer` - Creating Claude prompts
  - `ClaudeCoder` - Generating code
  - `PreCodeValidator` - Validating specifications

### 5. Milestone Tracking
Each project follows this pipeline:
1. **🔍 Market Research** - Competitive analysis and user research
2. **📋 Project Brief** - Detailed project specification
3. **🎯 Prompt Template** - Claude-ready prompt creation
4. **⚙️ Backend Code** - API and database generation
5. **🎨 Frontend Code** - UI and user interface
6. **🔗 Integration** - Connect frontend and backend
7. **🚀 Deployment** - Cloud deployment configuration
8. **✅ Validation** - Testing and quality assurance

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file in the dashboard directory:
```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_REFRESH_INTERVAL=2000

# Pipeline Configuration
NEXT_PUBLIC_MAX_PROJECTS=60
NEXT_PUBLIC_SIMULATION_MODE=false
```

### Customization
- **Refresh Interval**: Modify the 2-second update frequency
- **Project Display**: Adjust how many projects to show at once
- **Animation Speed**: Customize agent activity animations
- **Color Scheme**: Modify status indicator colors

## 🧪 Testing & Development

### Agent Simulation
The dashboard includes a built-in agent simulator for testing:

```bash
# Start simulation mode
npm run dev:simulation

# Test specific scenarios
npm run test:agents
```

### Development Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Type checking
npm run type-check
```

## 📊 API Endpoints

### GET `/api/projects`
Returns the list of all 60 projects from `projects.json`

**Response:**
```json
[
  {
    "project_name": "AI-Powered Code Review Assistant",
    "description": "Automated code analysis and refactoring",
    "tech_stack": "Python, FastAPI, React, OpenAI",
    "status": "in_progress",
    "progress": 45
  }
]
```

### GET `/api/pipeline`
Returns real-time pipeline progress data

**Response:**
```json
{
  "project-id": {
    "progress": 45,
    "activeAgents": ["MarketResearcher"],
    "items": [
      {
        "id": "market-research",
        "status": "completed",
        "agent": "MarketResearcher"
      }
    ]
  }
}
```

### POST `/api/run-pipeline`
Triggers the actual pipeline execution

### POST `/api/stop-pipeline`
Stops the pipeline and clears active agents

## 🎯 Use Cases

### 1. Project Management
- **Track Progress**: Monitor 60 projects simultaneously
- **Identify Blockers**: Quickly spot projects that are stuck
- **Resource Allocation**: See which agents are busy vs. available

### 2. Quality Assurance
- **Real-time Monitoring**: Catch issues as they happen
- **Progress Validation**: Ensure projects are actually being built
- **Performance Tracking**: Measure how long each step takes

### 3. Demonstration
- **Client Presentations**: Show pipeline progress to stakeholders
- **Team Updates**: Keep team informed of automation status
- **Training**: Demonstrate how the AI pipeline works

### 4. Debugging
- **Error Identification**: Quickly spot failed projects
- **Agent Monitoring**: See which agents are working vs. idle
- **Pipeline Validation**: Ensure the automation is functioning

## 🔍 Troubleshooting

### Common Issues

#### Dashboard Not Loading
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify projects.json exists
ls -la projects.json

# Check API endpoints
curl http://localhost:3000/api/projects
```

#### No Real-time Updates
- Verify the pipeline is running
- Check browser console for errors
- Ensure `pipeline-todos.json` is being updated

#### Agent Simulation Not Working
- Check browser console for JavaScript errors
- Verify `agent-simulator.ts` is properly imported
- Ensure `todo-manager.ts` is functioning

### Debug Mode
Enable debug logging by setting:
```bash
NEXT_PUBLIC_DEBUG_MODE=true
```

This will show detailed console logs for:
- API calls and responses
- Agent activity simulation
- Pipeline status updates
- Error details

## 🚀 Deployment

### Production Build
```bash
# Build the application
npm run build

# Start production server
npm start
```

### Environment Configuration
For production deployment, configure:
- **API Base URL**: Point to your production backend
- **Refresh Interval**: Adjust based on server load
- **Error Reporting**: Add Sentry or similar service
- **Analytics**: Add Google Analytics or PostHog

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Use TypeScript for all new code
- Follow the existing component patterns
- Add proper error handling
- Include JSDoc comments for functions

## 📄 License

This dashboard is part of the 60 AI Apps Pipeline project. See the main project README for licensing information.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the browser console for errors
3. Verify the backend pipeline is running
4. Check the main project documentation

---

**🎯 The dashboard is your mission control center for the AI application factory!**
