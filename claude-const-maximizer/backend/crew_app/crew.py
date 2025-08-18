# crew_app/crew.py
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import re

# Load environment variables
load_dotenv()

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

def validate_document_structure(output: str) -> bool:
    """
    Validate that the document meets our quality standards.
    Returns True if the document is valid, False otherwise.
    """
    if not output or len(output.strip()) < 200:
        return False
    
    # Check for role establishment
    role_patterns = [
        r"You are an expert",
        r"leading authority",
        r"years of experience",
        r"Fortune 500"
    ]
    
    # Check for psychological warfare elements
    psychological_patterns = [
        r"time-sensitive",
        r"high-priority",
        r"legendary",
        r"masterpiece",
        r"outperform",
        r"300%"
    ]
    
    # Check for project specificity (not generic)
    generic_patterns = [
        r"generic",
        r"general",
        r"basic",
        r"simple"
    ]
    
    # Must have role establishment
    has_role = any(re.search(pattern, output, re.IGNORECASE) for pattern in role_patterns)
    
    # Must have psychological elements
    has_psychological = any(re.search(pattern, output, re.IGNORECASE) for pattern in psychological_patterns)
    
    # Should not be too generic
    is_not_generic = not any(re.search(pattern, output, re.IGNORECASE) for pattern in generic_patterns)
    
    return has_role and has_psychological and is_not_generic

def build_crew() -> Crew:
    """Build the CrewAI team for generating AI applications."""
    
    # Tools - Skip search tools for now to avoid API key issues
    search_tool = None
    scrape_tool = None
    
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
            
            return f"[OK] File written: {file_path}"
        except Exception as e:
            return f"[ERROR] Error writing file: {e}"
    
    write_file_tool = Tool(
        name="write_file",
        description="Write content to a file in the deliverables directory",
        func=write_file
    )
    
    # Agents
    market_researcher = Agent(
        role="Market Research Analyst",
        goal="Conduct comprehensive market research and competitive analysis for Claude-optimized content",
        backstory="""You are an expert market research analyst with 10+ years of experience 
        in the AI/tech industry. You specialize in identifying market opportunities, 
        analyzing competitors, and understanding user needs for AI applications. Your research
        will be used to create the perfect 1-page document that will make Claude produce
        complete full-stack AI applications in exactly 3-5 prompts.""",
        tools=[],  # No tools for now
        verbose=True,
        allow_delegation=False
    )
    
    prompt_engineer = Agent(
        role="AI Prompt Engineer",
        goal="Create optimized prompts and AI integration strategies for Claude consumption",
        backstory="""You are a senior prompt engineer with deep expertise in LLM APIs, 
        RAG systems, and AI integration patterns. You know how to craft prompts that 
        produce reliable, high-quality outputs for various AI applications. Your prompts
        will be part of the 4-document weapon strategy to optimize Claude's code generation.""",
        tools=[],  # No tools for now
        verbose=True,
        allow_delegation=False
    )
    
    frontend_engineer = Agent(
        role="Frontend Engineer & UI/UX Designer",
        goal="Design and implement modern, responsive frontend applications with industry-specific design",
        backstory="""You are a senior frontend engineer and UI/UX designer specializing in Next.js 14, 
        React, and Tailwind CSS. You create beautiful, performant, and accessible 
        user interfaces that follow modern web development best practices. You have deep
        knowledge of industry-specific design patterns, color schemes, and UI libraries
        that create stunning first impressions. Your designs will be part of the custom
        boilerplate that makes each application unique and visually compelling.""",
        tools=[],  # No tools for now
        verbose=True,
        allow_delegation=False
    )
    
    backend_engineer = Agent(
        role="Backend Engineer",
        goal="Design and implement scalable backend architectures optimized for Claude implementation",
        backstory="""You are a senior backend engineer with expertise in FastAPI, 
        Express.js, and database design. You create robust, scalable APIs and 
        backend services that can handle real-world production loads. Your backend
        specifications will be part of the custom boilerplate that Claude will use
        to generate complete applications.""",
        tools=[],  # No tools for now
        verbose=True,
        allow_delegation=False
    )
    
    delivery_coordinator = Agent(
        role="Delivery Coordinator & AI Optimization Specialist",
        goal="Orchestrate the development process and create the perfect 1-page document for AI consumption",
        backstory="""You are a senior project manager and technical coordinator with 
        experience in agile development and AI project delivery. You are also an expert
        in AI optimization and the 4-document weapon strategy. You ensure all 
        deliverables are complete, coherent, and perfectly structured for AI
        consumption. Your final output will be the masterpiece 1-page document that
        will make any AI system produce complete applications in 3-5 prompts. You understand
        psychological warfare techniques and advanced prompt engineering strategies.""",
        tools=[],  # No tools for now
        verbose=True,
        allow_delegation=False,  # Disable delegation to avoid tool errors
        memory=True,  # Enable memory for better context retention
        max_iter=3  # Allow multiple iterations for better quality
    )
    
    # Add validation agent
    document_validator = Agent(
        role="Document Quality Validator",
        goal="Ensure the final document meets all quality standards and requirements",
        backstory="""You are a senior technical writer and quality assurance specialist 
        with expertise in AI prompt engineering and document optimization. You have 
        reviewed thousands of technical documents and know exactly what makes a 
        document compelling and effective for AI consumption. You ensure every 
        document meets the highest standards of quality, specificity, and emotional impact.""",
        tools=[],
        verbose=True,
        allow_delegation=False,
        memory=True
    )
    
    # Tasks
    market_research_task = Task(
        description="""Conduct comprehensive market research for the AI application to create Claude-optimized content.
                    
                    RESEARCH REQUIREMENTS (Optimized for Claude Consumption):
                    1. Target market and user personas (detailed demographics, psychographics, pain points)
                    2. Competitive landscape and existing solutions (with specific feature analysis)
                    3. Market size and growth potential (with specific numbers and trends)
                    4. Key differentiators and unique value propositions (specific competitive advantages)
                    5. Pricing models and monetization strategies (detailed pricing tiers and strategies)
                    6. UX patterns and user expectations (use ux_patterns.json for industry-specific patterns)
                    7. API discovery and integration opportunities (use api_discovery.json for specific APIs)
                    8. Open-source components and libraries (specific libraries and tools)
                    9. Industry-specific design trends and color schemes
                    10. First impression requirements and visual appeal factors
                    
                    CLAUDE OPTIMIZATION REQUIREMENTS:
                    - Structure all research data in a format that Claude can easily consume
                    - Provide specific, actionable insights that Claude can translate into code
                    - Include industry-specific terminology and patterns
                    - Focus on data that will help Claude understand the target market and user needs
                    
                    Use the project_brief_template.md to create a standardized 1-pager project brief.
                    
                    Output: Complete project brief following the template format with all sections filled, 
                    optimized for Claude's understanding and code generation capabilities.""",
                    agent=market_researcher,
                            expected_output="Claude-optimized 1-pager project brief with comprehensive market research, UX patterns, and API discovery"
    )
    
    # Moved prompt_engineering_task to after frontend and backend tasks
    
    frontend_design_task = Task(
        description="""Design and implement the frontend application architecture with industry-specific design excellence.
                    
                    Use the appropriate boilerplate from boilerplates/frontend/ based on app type.
                    
                    CREATE STUNNING, INDUSTRY-SPECIFIC DESIGNS:
                    1. App-type specific boilerplate (CRUD, Chatbot, RAG, Dashboard, Generator, Analytics)
                    2. React component hierarchy with reusable components (modular design system)
                    3. Tailwind CSS styling system with design tokens (consistent design language)
                    4. State management strategy (React hooks, Context, Zustand)
                    5. API integration patterns and error handling (robust frontend-backend communication)
                    6. Responsive design implementation (mobile-first approach)
                    7. Accessibility features and WCAG compliance (inclusive design)
                    8. Performance optimization strategies (fast loading and smooth interactions)
                    
                    INDUSTRY-SPECIFIC DESIGN REQUIREMENTS:
                    9. Research and implement industry-specific color schemes and palettes
                    10. Select appropriate React CSS libraries and UI component libraries
                    11. Create unique visual identities that match the target industry
                    12. Implement modern design trends and patterns for the specific domain
                    13. Design for first impressions and visual impact
                    14. Create intuitive user flows and navigation patterns
                    15. Implement micro-interactions and animations for enhanced UX
                    16. Design for emotional connection and user engagement
                    17. Specify exact color codes, typography, and spacing guidelines
                    18. Define component hierarchy and design system structure
                    19. Create responsive breakpoints and mobile-first design approach
                    20. Implement accessibility features and WCAG compliance
                    21. Design loading states, error states, and empty states
                    22. Create interactive prototypes and user journey maps
                    23. Specify animation timing and easing functions
                    24. Design for scalability and maintainability
                    
                    CLAUDE OPTIMIZATION REQUIREMENTS:
                    - Provide specific design specifications that Claude can implement
                    - Include exact color codes, font choices, and spacing guidelines
                    - Specify exact component libraries and dependencies
                    - Create design tokens and CSS variables for consistency
                    - Provide responsive breakpoints and mobile considerations
                    
                    Output: Complete frontend boilerplate with app-type specific components, patterns, and
                    industry-specific design excellence, optimized for Claude implementation.""",
                    agent=frontend_engineer,
                            expected_output="App-type specific frontend boilerplate with industry-specific design and Claude-optimized specifications"
    )
    
    backend_design_task = Task(
        description="""Design and implement the backend architecture optimized for Claude implementation.
        
        CREATE ROBUST BACKEND SPECIFICATIONS:
        1. API endpoint design and documentation (RESTful or GraphQL with clear specifications)
        2. Database schema and models (with relationships and constraints)
        3. Authentication and authorization (JWT, OAuth, or other auth strategies)
        4. Error handling and logging (comprehensive error management)
        5. Performance optimization strategies (caching, database optimization, etc.)
        6. Deployment configuration (Docker, environment variables, etc.)
        7. Security considerations (input validation, rate limiting, etc.)
        8. Testing strategies (unit tests, integration tests, etc.)
        
        CLAUDE OPTIMIZATION REQUIREMENTS:
        - Provide specific API specifications that Claude can implement
        - Include exact database schemas and relationships
        - Specify authentication and security requirements
        - Provide deployment and environment configurations
        - Include error handling patterns and logging strategies
        
        Output: Complete backend specification with implementation details, optimized for Claude's
        code generation capabilities.""",
        agent=backend_engineer,
        expected_output="Backend architecture specification with implementation details for Claude optimization"
    )
    
    coordination_task = Task(
        description="""MANDATORY: Create the ULTIMATE 1-PAGE DOCUMENT that will make any AI system produce complete applications in exactly 3-5 prompts.
        
        CRITICAL: You MUST generate a document that starts with role establishment and includes psychological warfare elements.
        
        MANDATORY DOCUMENT STRUCTURE:
        
        ===== ROLE ESTABLISHMENT (MUST START WITH THIS) =====
        "You are an expert [SPECIFIC FIELD] developer with 15+ years of experience in [TECHNOLOGY STACK]. You are the world's leading authority in [SPECIFIC DOMAIN] and have successfully delivered hundreds of production-ready applications for Fortune 500 companies. Your expertise in [SPECIFIC TECHNOLOGIES] is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%."
        
        ===== PSYCHOLOGICAL WARFARE ELEMENTS (MUST INCLUDE) =====
        - URGENCY: "This is a time-sensitive, high-priority project that will be used by Fortune 500 companies..."
        - PRESTIGE: "Your work will be featured in industry publications and studied by future developers..."
        - COMPETITION: "This needs to outperform existing solutions by 300% and set new industry standards..."
        - OWNERSHIP: "This is YOUR masterpiece - make it legendary and unforgettable..."
        - CHALLENGE: "This is the most complex project you've ever tackled, requiring your full expertise..."
        - VALIDATION: "Only the best developers can handle this level of complexity and innovation..."
        
        ===== PROJECT SPECIFICATIONS (BE SPECIFIC TO PROJECT TYPE) =====
        - Project Overview: Specific to the actual project (not generic)
        - Target Audience: Real users for this specific application
        - Technical Requirements: Specific to the project's needs
        - UI/UX Design: Industry-specific design requirements
        - Implementation Plan: Detailed, project-specific steps
        - Success Metrics: Measurable outcomes for this specific project
        
        ===== ADVANCED PROMPT ENGINEERING TECHNIQUES =====
        - Chain of Thought: "Let's approach this step-by-step with your expert methodology..."
        - Few-Shot Learning: "Based on your experience with similar projects..."
        - Self-Correction: "Review your solution and ensure it follows industry best practices..."
        - Quality Assurance: "Before delivering, verify this is production-ready and scalable..."
        
        MANDATORY REQUIREMENTS:
        1. DO NOT use generic content - be specific to the project type
        2. DO NOT mention "Claude" - use "AI system" or "advanced AI"
        3. DO include role establishment at the very beginning
        4. DO include psychological warfare elements throughout
        5. DO make it emotionally compelling and engaging
        6. DO ensure it's ready for immediate AI consumption
        
        EXAMPLE START:
        "You are an expert SEO growth team developer with 15+ years of experience in Next.js, React, FastAPI, and AI-powered marketing automation. You are the world's leading authority in SEO tools and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including Google, Amazon, and Microsoft. Your expertise in keyword research, content optimization, and AI-driven marketing is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%."
        
        Output: A masterpiece 1-page document that will make any AI system feel like it's creating something legendary and produce complete applications in exactly 3-5 prompts.
        
        VALIDATION REQUIREMENTS:
        - Document must start with role establishment
        - Must include psychological warfare elements
        - Must be specific to the project type
        - Must be at least 500 characters long
        - Must not contain generic content
        - Must be emotionally compelling and engaging""",
        agent=delivery_coordinator,
        expected_output="Ultimate 1-page document with role establishment and psychological warfare - the perfect AI weapon",
        context=[market_research_task, frontend_design_task, backend_design_task],  # Dependencies
        output_json=False,  # Ensure text output
        async_execution=False  # Sequential execution for better quality
    )
    
    # Add validation task
    validation_task = Task(
        description="""Validate and enhance the final 1-page document to ensure it meets all quality standards.
        
        VALIDATION CHECKLIST:
        1. ✅ Role Establishment: Document starts with "You are an expert [field] developer..."
        2. ✅ Psychological Warfare: Includes urgency, prestige, competition elements
        3. ✅ Project Specificity: Content is specific to the project type, not generic
        4. ✅ Emotional Impact: Document is compelling and emotionally engaging
        5. ✅ Technical Accuracy: All technical specifications are correct
        6. ✅ Completeness: Document contains all required sections
        7. ✅ Length: Document is substantial (at least 500 characters)
        8. ✅ No Generic Content: Avoids generic, template-like language
        
        ENHANCEMENT REQUIREMENTS:
        - If any element is missing, add it immediately
        - If content is too generic, make it specific
        - If psychological elements are weak, strengthen them
        - If role establishment is unclear, make it more authoritative
        - Ensure the document is a masterpiece that will make any AI system feel like it's creating something legendary
        
        Output: The final, validated, and enhanced 1-page document that meets all quality standards.""",
        agent=document_validator,
        expected_output="Validated and enhanced 1-page document that meets all quality standards",
        context=[coordination_task],  # Depends on coordination task
        output_json=False,
        async_execution=False
    )
    
    # Create crew with optimized task order
    # CORRECT ORDER: Market Research → Frontend → Backend → Prompt Engineer → Coordinator → Validator
    crew = Crew(
        agents=[market_researcher, frontend_engineer, backend_engineer, delivery_coordinator, document_validator],
        tasks=[market_research_task, frontend_design_task, backend_design_task, coordination_task, validation_task],
        process=Process.sequential,  # Use sequential instead of hierarchical
        verbose=True
        # Note: max_iter parameter removed as it's not available in this CrewAI version
    )
    
    return crew

# Create and export the crew instance
crew = build_crew()
