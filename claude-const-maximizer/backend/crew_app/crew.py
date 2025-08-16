# crew_app/crew.py
import os
from pathlib import Path
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Claude Code Constitution - Rules for code generation
CLAUDE_CODE_CONSTITUTION = """
# Claude Code Constitution

## Naming Conventions
- Use descriptive, camelCase for variables and functions
- Use PascalCase for components and classes
- Use kebab-case for file names and URLs
- Use UPPER_SNAKE_CASE for constants

## Folder Structure
```
project/
├── frontend/          # Next.js 14 + React + Tailwind
│   ├── app/          # App router pages
│   ├── components/   # Reusable UI components
│   ├── lib/          # Utilities and helpers
│   └── public/       # Static assets
├── backend/          # FastAPI or Express.js
│   ├── app/          # Main application
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   └── utils/        # Utilities
└── docs/             # Documentation
```

## State Management
- Use React hooks for local state
- Use Context API for global state
- Use Zustand for complex state management
- Use React Query for server state

## API Patterns
- RESTful endpoints with proper HTTP methods
- Consistent error handling and status codes
- Input validation and sanitization
- Rate limiting and authentication

## Output Format
Always provide:
1. Complete, runnable code
2. Clear file structure
3. Installation instructions
4. Environment variables
5. API documentation
"""

def build_crew() -> Crew:
    """Build the CrewAI team for generating AI applications."""
    
                    # Tools
                search_tool = TavilySearchResults()
                scrape_tool = DuckDuckGoSearchAPIWrapper()
    
    # Custom tool for writing files
    def write_file(content: str, filename: str) -> str:
        """Write content to a file."""
        try:
            # Create deliverables directory
            deliverables_dir = Path("../../deliverables")
            deliverables_dir.mkdir(exist_ok=True)
            
            # Create project directory
            project_dir = deliverables_dir / "current_project"
            project_dir.mkdir(exist_ok=True)
            
            # Write file
            file_path = project_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✅ File written: {file_path}"
        except Exception as e:
            return f"❌ Error writing file: {e}"
    
    write_file_tool = Tool(
        name="write_file",
        description="Write content to a file in the deliverables directory",
        func=write_file
    )
    
    # Agents
    market_researcher = Agent(
        role="Market Research Analyst",
        goal="Conduct comprehensive market research and competitive analysis",
        backstory="""You are an expert market research analyst with 10+ years of experience 
        in the AI/tech industry. You specialize in identifying market opportunities, 
        analyzing competitors, and understanding user needs for AI applications.""",
        tools=[search_tool, scrape_tool],
        verbose=True,
        allow_delegation=False
    )
    
    prompt_engineer = Agent(
        role="AI Prompt Engineer",
        goal="Create optimized prompts and AI integration strategies",
        backstory="""You are a senior prompt engineer with deep expertise in LLM APIs, 
        RAG systems, and AI integration patterns. You know how to craft prompts that 
        produce reliable, high-quality outputs for various AI applications.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
    frontend_engineer = Agent(
        role="Frontend Engineer",
        goal="Design and implement modern, responsive frontend applications",
        backstory="""You are a senior frontend engineer specializing in Next.js 14, 
        React, and Tailwind CSS. You create beautiful, performant, and accessible 
        user interfaces that follow modern web development best practices.""",
        tools=[write_file_tool],
        verbose=True,
        allow_delegation=False
    )
    
    backend_engineer = Agent(
        role="Backend Engineer",
        goal="Design and implement scalable backend architectures",
        backstory="""You are a senior backend engineer with expertise in FastAPI, 
        Express.js, and database design. You create robust, scalable APIs and 
        backend services that can handle real-world production loads.""",
        tools=[write_file_tool],
        verbose=True,
        allow_delegation=False
    )
    
    delivery_coordinator = Agent(
        role="Delivery Coordinator",
        goal="Orchestrate the development process and ensure quality deliverables",
        backstory="""You are a senior project manager and technical coordinator with 
        experience in agile development and AI project delivery. You ensure all 
        deliverables are complete, coherent, and ready for implementation.""",
        tools=[write_file_tool],
        verbose=True,
        allow_delegation=True
    )
    
    # Tasks
                    market_research_task = Task(
                    description="""Conduct comprehensive market research for the AI application.
                    
                    Research:
                    1. Target market and user personas
                    2. Competitive landscape and existing solutions
                    3. Market size and growth potential
                    4. Key differentiators and unique value propositions
                    5. Pricing models and monetization strategies
                    6. UX patterns and user expectations (use ux_patterns.json)
                    7. API discovery and integration opportunities (use api_discovery.json)
                    8. Open-source components and libraries
                    
                    Use the project_brief_template.md to create a standardized 1-pager project brief.
                    
                    Output: Complete project brief following the template format with all sections filled.""",
                    agent=market_researcher,
                    expected_output="Standardized 1-pager project brief with market research, UX patterns, and API discovery"
                )
    
                    prompt_engineering_task = Task(
                    description="""Create optimized AI prompts and integration strategy.
                    
                    Use prompt_templates.json to select the appropriate app type template.
                    
                    Develop:
                    1. App-type specific prompt templates (CRUD, Chatbot, RAG, Dashboard, Generator, Analytics)
                    2. Claude coding instructions with constitution rules
                    3. Integration patterns for selected APIs and services
                    4. Error handling and fallback strategies
                    5. Prompt optimization techniques
                    6. Reusable prompt components for different features
                    
                    Output: Complete prompt template customized for the specific app type with Claude coding instructions.""",
                    agent=prompt_engineer,
                    expected_output="App-type specific prompt template with Claude coding instructions"
                )
    
                    frontend_design_task = Task(
                    description="""Design and implement the frontend application architecture.
                    
                    Use the appropriate boilerplate from boilerplates/frontend/ based on app type.
                    
                    Create:
                    1. App-type specific boilerplate (CRUD, Chatbot, RAG, Dashboard, Generator, Analytics)
                    2. React component hierarchy with reusable components
                    3. Tailwind CSS styling system with design tokens
                    4. State management strategy (React hooks, Context, Zustand)
                    5. API integration patterns and error handling
                    6. Responsive design implementation
                    7. Accessibility features and WCAG compliance
                    8. Performance optimization strategies
                    
                    Output: Complete frontend boilerplate with app-type specific components and patterns.""",
                    agent=frontend_engineer,
                    expected_output="App-type specific frontend boilerplate with components and patterns"
                )
    
    backend_design_task = Task(
        description="""Design and implement the backend architecture.
        
        Create:
        1. API endpoint design and documentation
        2. Database schema and models
        3. Authentication and authorization
        4. Error handling and logging
        5. Performance optimization strategies
        6. Deployment configuration
        
        Output: Complete backend specification with implementation details.""",
        agent=backend_engineer,
        expected_output="Backend architecture specification with implementation details"
    )
    
    coordination_task = Task(
        description="""Coordinate all deliverables and create implementation plan.
        
        Tasks:
        1. Review all agent outputs for consistency
        2. Create 5-prompt development plan
        3. Generate deployment checklist
        4. Create project index and overview
        5. Ensure all deliverables are complete and coherent
        
        Output: Complete project package ready for implementation.""",
        agent=delivery_coordinator,
        expected_output="Complete project package with implementation plan"
    )
    
    # Create crew
    crew = Crew(
        agents=[market_researcher, prompt_engineer, frontend_engineer, backend_engineer, delivery_coordinator],
        tasks=[market_research_task, prompt_engineering_task, frontend_design_task, backend_design_task, coordination_task],
        process=Process.hierarchical,
        verbose=True
    )
    
    return crew
