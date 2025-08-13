# 🚀 Content Marketing Project Manager

> **AI-Powered Content Marketing Project Planning & Resource Management**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.157+-green.svg)](https://crewai.com/)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-orange.svg)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Overview

The **Content Marketing Project Manager** is an intelligent AI-powered system that revolutionizes how content marketing campaigns are planned, executed, and managed. Built with [CrewAI](https://crewai.com/), this system leverages multiple specialized AI agents to create comprehensive project plans, estimate resources, and optimize team assignments.

### 🎯 What It Does

This agent transforms your content marketing ideas into actionable, detailed project plans by:

- **📋 Breaking down complex campaigns** into manageable tasks
- **⏱️ Estimating time and resources** with precision
- **👥 Optimizing team assignments** based on skills and availability
- **📅 Creating detailed timelines** with dependencies and milestones
- **📊 Generating comprehensive reports** for project management

---

## 🏗️ Architecture

### 🤖 AI Agents

The system employs three specialized AI agents that work together:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Strategic Content Project Planner** | Project Architect | Breaks down campaigns into actionable tasks with clear scope, format, and dependencies |
| **Content Production Estimation Specialist** | Resource Analyst | Provides accurate time/resource estimates considering complexity and team availability |
| **Content Team Resource Strategist** | Team Optimizer | Assigns tasks to team members based on role fit and availability to minimize bottlenecks |

### 🔧 Custom Tools

- **Content Calendar Generator**: Creates structured content calendars with deadlines and dependencies
- **Project Metrics Calculator**: Analyzes workload distribution and provides optimization recommendations

---

## 🚀 Features

### ✨ Core Capabilities

- **Multi-Format Content Planning**: Blog, Email, Social, Video, Webinar, eBook, and more
- **Intelligent Resource Allocation**: Optimizes team assignments based on skills and workload
- **Dependency Management**: Identifies and manages task dependencies for smooth execution
- **Risk Assessment**: Identifies potential bottlenecks and provides mitigation strategies
- **Milestone Tracking**: Creates clear project milestones with deliverables and target dates

### 📊 Output Deliverables

- **Detailed Task Breakdown**: 8+ content tasks with time estimates and priorities
- **Team Assignments**: Role-based workload distribution with justifications
- **Project Timeline**: 64-day project schedule with dependencies
- **Resource Analysis**: 204+ hours of estimated work with team utilization metrics
- **Risk Factors**: Identified project risks and success metrics

---

## 🛠️ Technology Stack

- **Python 3.12**: Latest Python features and performance improvements
- **CrewAI**: Multi-agent AI framework for collaborative task execution
- **UV**: Fast Python package manager and virtual environment management
- **Pydantic**: Data validation and settings management
- **OpenAI GPT-4o-mini**: Advanced language model for intelligent planning

---

## 📦 Installation

### Prerequisites

- **Python 3.12** (recommended for optimal performance)
- **UV Package Manager** for dependency management

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd content_marketing_project_manager
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # Replace 'your_openai_api_key_here' with your actual OpenAI API key
   ```

4. **Run the application**
   ```bash
   uv run python -m content_marketing_project_manager.main
   ```

---

## 🎮 Usage

### Basic Usage

The system comes pre-configured with a comprehensive B2B SaaS content marketing campaign example:

```python
# The system automatically processes these inputs:
inputs = {
    "project_type": "Multi-Channel Content Marketing Campaign",
    "industry": "B2B SaaS",
    "project_objectives": "Drive awareness and leads across blog, email, social, and webinars.",
    "project_requirements": "Blog series, lead magnets, email nurture, social assets, video, webinar",
    "team_members": "Content Strategist, SEO Writer, Designer, Email Specialist, Social Manager, Video Producer"
}
```

### Custom Configuration

Modify the inputs in `src/content_marketing_project_manager/main.py` to customize:

- **Project Type**: Any content marketing initiative
- **Industry**: Your specific market vertical
- **Objectives**: Campaign goals and KPIs
- **Requirements**: Specific content deliverables
- **Team**: Available team members and roles

---

## 📁 Project Structure

```
content_marketing_project_manager/
├── src/content_marketing_project_manager/
│   ├── main.py              # Main execution script
│   ├── crew.py              # Crew definition with agents and tasks
│   ├── types.py             # Pydantic models and data structures
│   ├── config.py            # Configuration management
│   ├── config/
│   │   ├── agents.yaml      # AI agent definitions
│   │   └── tasks.yaml       # Task workflow definitions
│   └── tools/
│       └── custom_tool.py   # Content Calendar & Project Metrics tools
├── tests/                   # Comprehensive test suite
├── outputs/                 # Generated project plans (auto-created)
├── .env                     # Environment configuration
├── pyproject.toml          # UV project configuration
└── README.md               # This file
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run python -m pytest tests/

# Run specific test file
uv run python tests/test_crew.py
```

---

## 📈 Example Output

The system generates comprehensive project plans including:

### 📋 Task Breakdown
- **8 Content Tasks** with detailed specifications
- **Time Estimates** ranging from 10-30 hours per task
- **Priority Levels** (Low/Medium/High/Critical)
- **Complexity Assessment** (Simple/Moderate/Complex)
- **Dependencies** and target publish dates

### 👥 Team Assignments
- **16 Role-Based Assignments** with workload percentages
- **Skill-Matched Assignments** with justifications
- **Workload Balancing** to prevent burnout
- **Timeline Coordination** with start/end dates

### 🎯 Project Milestones
- **4 Strategic Milestones** with target dates
- **Deliverable Tracking** for each milestone
- **Success Metrics** and risk factors

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `VERBOSE_LOGGING` | Enable detailed logging | `true` |
| `MAX_ITERATIONS` | Maximum crew iterations | `5` |
| `OPENAI_MODEL` | AI model to use | `gpt-4o-mini` |
| `TEMPERATURE` | Creativity level (0-1) | `0.7` |

> **🔒 Security Note**: Never commit your actual API keys to version control. The `.env` file is automatically ignored by Git. Always use the `.env.example` template and replace the placeholder values with your actual credentials.

### Customizing Agents

Edit `src/content_marketing_project_manager/config/agents.yaml` to modify:

- Agent roles and goals
- Backstory and expertise
- Delegation permissions
- Verbosity settings

### Customizing Tasks

Edit `src/content_marketing_project_manager/config/tasks.yaml` to modify:

- Task descriptions and requirements
- Expected outputs and formats
- Workflow dependencies

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Creator

**Derril Filemon** - The visionary behind this intelligent content marketing project management system.

---

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com/) for the powerful multi-agent framework
- [UV](https://docs.astral.sh/uv/) for fast Python package management
- [OpenAI](https://openai.com/) for advanced language models
- The open-source community for inspiration and support

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

<div align="center">

**Transform your content marketing with AI-powered project management! 🚀**

[Get Started](#installation) • [View Examples](#example-output) • [Contribute](#contributing)

</div>


