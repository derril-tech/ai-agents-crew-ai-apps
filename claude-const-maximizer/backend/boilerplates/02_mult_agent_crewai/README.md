# Multi-Agent CrewAI Backend Boilerplate

**Covers 25 projects (42% of all projects)**

## 🎯 Overview

This boilerplate provides a robust foundation for multi-agent AI systems using CrewAI. It includes agent orchestration, task management, and complex workflow automation.

## 📋 Covered Projects

### **Research & Analysis (8 projects)**
- Autonomous Research & Report Generation System
- Automated Market Research and Report Generation Team
- Automated Research Department
- Cybersecurity Threat Analysis Team
- Multi-Agent Cybersecurity Defense System
- Intelligent Smart City Management System
- Real Estate Investment Finder
- Conference Planning Crew

### **Business & E-commerce (6 projects)**
- Intelligent E-commerce Management System
- E-commerce Customer Service and Fraud Detection
- E-Commerce Launch Crew
- B2B Sales Prospecting AI
- SEO Growth Team
- Startup Idea to Pitch Deck Crew

### **Content & Marketing (4 projects)**
- Multi-Agent Content Creation & Marketing System
- Creative Content Generation and Marketing Team
- Social Media Factory
- AI Content Localizer

### **Healthcare & Legal (3 projects)**
- Intelligent Healthcare Diagnosis & Treatment Planning
- AI-Powered Legal Document Analysis & Contract Negotiation
- Recruitment Flow AI

### **Development & Education (4 projects)**
- Multi-Agent Software Development Team
- Automated Software Development Team
- Autonomous Learning and Research Assistant
- Personal Brain Agent System

## 🏗️ Architecture

```
02_mult_agent_crewai/
├── README.md
├── requirements.txt
├── main.py                          # FastAPI application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Environment and app settings
│   └── database.py                  # Database configuration
├── models/
│   ├── __init__.py
│   ├── base.py                      # Base SQLAlchemy model
│   ├── user.py                      # User management
│   ├── project.py                   # Project tracking
│   ├── agent.py                     # Agent definitions
│   ├── task.py                      # Task management
│   └── workflow.py                  # Workflow orchestration
├── schemas/
│   ├── __init__.py
│   ├── user.py                      # User Pydantic schemas
│   ├── project.py                   # Project schemas
│   ├── agent.py                     # Agent schemas
│   ├── task.py                      # Task schemas
│   └── workflow.py                  # Workflow schemas
├── api/
│   ├── __init__.py
│   ├── deps.py                      # Dependencies and auth
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication endpoints
│   │   ├── users.py                 # User management
│   │   ├── projects.py              # Project management
│   │   ├── agents.py                # Agent management
│   │   ├── tasks.py                 # Task management
│   │   └── workflows.py             # Workflow orchestration
├── core/
│   ├── __init__.py
│   ├── security.py                  # Security utilities
│   └── config.py                    # Core configuration
├── services/
│   ├── __init__.py
│   ├── agent_service.py             # Agent orchestration
│   ├── task_service.py              # Task management
│   ├── workflow_service.py          # Workflow execution
│   └── notification_service.py      # Notifications
├── agents/
│   ├── __init__.py
│   ├── base_agent.py                # Base agent class
│   ├── research_agent.py            # Research agent
│   ├── analysis_agent.py            # Analysis agent
│   ├── writing_agent.py             # Writing agent
│   ├── marketing_agent.py           # Marketing agent
│   ├── development_agent.py         # Development agent
│   └── specialized_agents/          # Domain-specific agents
│       ├── __init__.py
│       ├── healthcare_agent.py
│       ├── legal_agent.py
│       ├── ecommerce_agent.py
│       └── cybersecurity_agent.py
├── workflows/
│   ├── __init__.py
│   ├── base_workflow.py             # Base workflow class
│   ├── research_workflow.py         # Research automation
│   ├── marketing_workflow.py        # Marketing automation
│   ├── development_workflow.py      # Development automation
│   └── business_workflow.py         # Business automation
├── utils/
│   ├── __init__.py
│   ├── logger.py                    # Logging utilities
│   ├── validators.py                # Data validation
│   └── helpers.py                   # Helper functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Test configuration
│   ├── test_api/                    # API tests
│   ├── test_services/               # Service tests
│   └── test_agents/                 # Agent tests
├── alembic/
│   ├── versions/                    # Database migrations
│   ├── env.py
│   └── alembic.ini
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── scripts/
    ├── setup.sh                     # Setup script
    └── deploy.sh                    # Deployment script
```

## 🔧 Core Features

### **Agent Management**
- Dynamic agent creation and configuration
- Agent role definition and specialization
- Agent communication and coordination
- Agent performance monitoring

### **Task Orchestration**
- Task definition and assignment
- Task dependencies and sequencing
- Task status tracking and updates
- Task result aggregation

### **Workflow Automation**
- Predefined workflow templates
- Custom workflow creation
- Workflow execution monitoring
- Error handling and recovery

### **Integration Patterns**
- Third-party API integration
- Database connectivity
- External service communication
- Real-time updates and notifications

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```bash
   alembic upgrade head
   ```

3. **Run Application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access API Documentation**
   ```
   http://localhost:8000/docs
   ```

## 📊 Database Schema

### **Core Tables**
- `users` - User management
- `projects` - Project tracking
- `agents` - Agent definitions
- `tasks` - Task management
- `workflows` - Workflow definitions
- `executions` - Workflow executions
- `results` - Task and workflow results

### **Relationships**
- Users can have multiple projects
- Projects can have multiple workflows
- Workflows contain multiple tasks
- Tasks are assigned to agents
- Executions track workflow runs

## 🔌 API Endpoints

### **Authentication**
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Token refresh

### **Project Management**
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### **Agent Management**
- `GET /api/v1/agents` - List agents
- `POST /api/v1/agents` - Create agent
- `GET /api/v1/agents/{id}` - Get agent details
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent

### **Workflow Management**
- `GET /api/v1/workflows` - List workflows
- `POST /api/v1/workflows` - Create workflow
- `GET /api/v1/workflows/{id}` - Get workflow details
- `POST /api/v1/workflows/{id}/execute` - Execute workflow
- `GET /api/v1/workflows/{id}/status` - Get execution status

## 🎨 Customization Guide

### **Adding New Agents**
1. Create agent class in `agents/` directory
2. Inherit from `BaseAgent`
3. Implement required methods
4. Register agent in agent registry

### **Creating Workflows**
1. Define workflow in `workflows/` directory
2. Specify task sequence and dependencies
3. Configure agent assignments
4. Add error handling and recovery

### **Integrating APIs**
1. Add API client in `services/` directory
2. Create integration service
3. Update agent to use integration
4. Add error handling and retry logic

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- API rate limiting
- Input validation and sanitization
- Secure environment variable handling
- Database connection security

## 📈 Monitoring & Logging

- Structured logging with different levels
- Performance metrics collection
- Error tracking and alerting
- Agent execution monitoring
- Workflow performance analytics

## 🚀 Deployment

### **Docker Deployment**
```bash
docker-compose up -d
```

### **Environment Variables**
```bash
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
CREWAI_API_KEY=your-crewai-key
```

## 📝 Testing

### **Run Tests**
```bash
pytest tests/
```

### **Test Coverage**
```bash
pytest --cov=app tests/
```

## 🔄 Version Control

- Git hooks for code quality
- Automated testing on commit
- Deployment automation
- Environment-specific configurations

## 📚 Documentation

- API documentation with OpenAPI/Swagger
- Code documentation with docstrings
- Architecture decision records
- Deployment guides
- Troubleshooting guides
