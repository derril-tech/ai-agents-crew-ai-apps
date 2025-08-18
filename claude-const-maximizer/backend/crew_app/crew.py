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

def extract_project_info(raw_output: str) -> Dict[str, str]:
    """
    Extract project information from the raw agent output.
    Returns a dictionary with extracted content for reformatting.
    """
    project_info = {
        'project_name': 'AI Application',
        'project_type': 'AI-powered application',
        'target_audience': 'Software developers and tech professionals',
        'tech_stack': 'FastAPI, Next.js, React, Tailwind CSS',
        'domain': 'AI and automation',
        'overview': '',
        'audience': '',
        'technical': '',
        'ui_ux': '',
        'implementation': '',
        'metrics': '',
        'deployment': ''
    }
    
    # Extract project name from title - handle "Perfect 1-Page Document for Claude" format
    title_match = re.search(r'#\s*(.+?)(?:\n|$)', raw_output)
    if title_match:
        title = title_match.group(1).strip()
        if 'Perfect 1-Page Document' in title:
            # Look for the actual project name in the content
            project_name_match = re.search(r'Claude-Optimized\s+([^A-Z]+?)\s+Application', raw_output, re.IGNORECASE)
            if project_name_match:
                project_info['project_name'] = project_name_match.group(1).strip().title() + ' Application'
            else:
                project_info['project_name'] = 'AI Application'
        else:
            project_info['project_name'] = title
    
    # Determine project type and domain based on content
    if 'content' in raw_output.lower() or 'content creation' in raw_output.lower():
        project_info['project_type'] = 'AI-powered content creation tool'
        project_info['domain'] = 'content creation and marketing'
    elif 'video' in raw_output.lower() or 'storyboard' in raw_output.lower():
        project_info['project_type'] = 'AI-powered video creation tool'
        project_info['domain'] = 'video production and content creation'
    elif 'resume' in raw_output.lower():
        project_info['project_type'] = 'AI-powered resume and cover letter tool'
        project_info['domain'] = 'career development and recruitment'
    elif 'medical' in raw_output.lower():
        project_info['project_type'] = 'AI-powered medical assistant'
        project_info['domain'] = 'healthcare and medical technology'
    elif 'voice' in raw_output.lower():
        project_info['project_type'] = 'AI-powered voice control system'
        project_info['domain'] = 'smart home and IoT'
    
    # Extract sections using more flexible regex patterns
    sections = {
        'overview': r'##\s*Project Overview[^#]*?(?=##|$)',
        'audience': r'##\s*Target Audience[^#]*?(?=##|$)',
        'technical': r'##\s*Technical Requirements[^#]*?(?=##|$)',
        'ui_ux': r'##\s*UI/UX Design[^#]*?(?=##|$)',
        'implementation': r'##\s*Implementation Plan[^#]*?(?=##|$)',
        'metrics': r'##\s*Success Metrics[^#]*?(?=##|$)',
        'deployment': r'##\s*Deployment[^#]*?(?=##|$)'
    }
    
    for key, pattern in sections.items():
        match = re.search(pattern, raw_output, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(0)
            # Clean up the content
            content = re.sub(r'^##\s*\w+\s*\n*', '', content).strip()
            project_info[key] = content
    
    # Extract tech stack information - look for common patterns
    tech_patterns = [
        r'FastAPI[^,\n]*',
        r'Next\.js[^,\n]*',
        r'React[^,\n]*',
        r'PostgreSQL[^,\n]*',
        r'JWT[^,\n]*'
    ]
    
    tech_stack_parts = []
    for pattern in tech_patterns:
        match = re.search(pattern, raw_output, re.IGNORECASE)
        if match:
            tech_stack_parts.append(match.group(0).strip())
    
    if tech_stack_parts:
        project_info['tech_stack'] = ', '.join(tech_stack_parts)
    
    # Extract target audience from demographics section
    audience_match = re.search(r'Demographics[^:]*:\s*([^\n]+)', raw_output, re.IGNORECASE)
    if audience_match:
        project_info['target_audience'] = audience_match.group(1).strip()
    else:
        # Look for audience information in the audience section
        audience_section_match = re.search(r'##\s*Target Audience[^#]*?(?=##|$)', raw_output, re.DOTALL | re.IGNORECASE)
        if audience_section_match:
            audience_content = audience_section_match.group(0)
            # Extract first meaningful line
            lines = audience_content.split('\n')
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    project_info['target_audience'] = line.strip()
                    break
    
    return project_info

def post_process_coordinator_output(raw_output: str) -> str:
    """
    Post-process the Delivery Coordinator's output to ensure it follows the exact required format.
    This function guarantees compliance regardless of what the agent generates.
    """
    print("🔄 Post-processing Delivery Coordinator output...")
    
    # Extract project information from raw output
    project_info = extract_project_info(raw_output)
    
    # Create the perfectly formatted document with role establishment and psychological warfare
    formatted_output = f"""You are an expert {project_info['project_type']} developer with 15+ years of experience in {project_info['tech_stack']}. You are the world's leading authority in {project_info['domain']} and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including Google, Amazon, Microsoft, and Apple. Your expertise in AI integration, scalable architecture, and user experience optimization is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%.

This is a time-sensitive, high-priority project that will be used by Fortune 500 companies and featured in industry publications. Your work will be studied by future developers and set new industry standards. This is YOUR masterpiece - make it legendary and unforgettable. This is the most complex project you've ever tackled, requiring your full expertise and innovative thinking. Only the best developers can handle this level of complexity and innovation.

Perfect 1-Page Document 🎯 ULTIMATE AI WEAPON (For Maximum AI Performance)

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ PROJECT: {project_info['project_name']}                                           │
│ TYPE: {project_info['project_type']}                                              │
│                                                                                     │
│ 🎯 OBJECTIVE                                                                        │
│ Create a comprehensive, production-ready {project_info['project_name'].lower()} that leverages AI │
│ to deliver exceptional user experiences and business value. This application will │
│ serve as a showcase of modern full-stack development with intelligent automation. │
│                                                                                     │
│ 👥 TARGET USERS                                                                    │
│ {project_info['target_audience']}                                                 │
│                                                                                     │
│ 🛠️ TECHNICAL REQUIREMENTS                                                         │
│ Frontend: Next.js 14 + React 18 + TypeScript + Tailwind CSS                       │
│ Backend: FastAPI + Python 3.9+ + SQLAlchemy + JWT Authentication                  │
│ Database: PostgreSQL + pgvector (for AI features) + Redis (caching)              │
│ AI Integration: OpenAI API + Anthropic Claude API + LangChain                     │
│ Deployment: Vercel (Frontend) + Render (Backend) + PostgreSQL (Database)         │
│                                                                                     │
│ 🎨 UX PATTERNS & DESIGN                                                            │
│ • Modern, responsive design with industry-specific color schemes and typography   │
│ • Intuitive navigation with clear user flows and micro-interactions               │
│ • Accessibility-first approach with WCAG 2.1 AA compliance                        │
│ • Mobile-first responsive design with touch-friendly interfaces                   │
│ • Real-time updates and smooth animations for enhanced user experience            │
│ • Dark/light mode support with customizable themes                                │
│                                                                                     │
│ 🔗 INTEGRATIONS & APIs                                                             │
│ • OpenAI GPT-4 for intelligent content generation and analysis                    │
│ • Anthropic Claude for advanced reasoning and complex tasks                       │
│ • JWT-based authentication with secure session management                         │
│ • Real-time WebSocket connections for live updates                                │
│ • File upload and processing with cloud storage integration                       │
│ • Email notifications and user communication systems                              │
│                                                                                     │
│ 📊 SUCCESS METRICS                                                                 │
│ • User adoption and engagement rates                                              │
│ • Feature utilization and performance metrics                                     │
│ • System reliability and uptime monitoring                                        │
│ • Business value generation and ROI measurement                                   │
│                                                                                     │
│ 🚀 DEPLOYMENT & LAUNCH                                                             │
│ Vercel: Next.js frontend with automatic deployments and edge optimization         │
│ Render: FastAPI backend with auto-scaling and health monitoring                   │
│ PostgreSQL: Managed database with automated backups and monitoring                │
│ Environment: Comprehensive environment variable management and security           │
│                                                                                     │
│ 💡 IMPLEMENTATION STRATEGY                                                        │
│ Phase 1: Core architecture and authentication system (Week 1)                     │
│ Phase 2: AI integration and core features (Week 2)                                │
│ Phase 3: UI/UX refinement and testing (Week 3)                                    │
│ Phase 4: Deployment, monitoring, and launch preparation (Week 4)                  │
│                                                                                     │
│ 🎯 CLAUDE OPTIMIZATION                                                            │
│ This document is structured for maximum Claude comprehension and efficiency.      │
│ Claude will use this to generate complete applications in exactly 3-5 prompts.    │
│ All technical specifications, design requirements, and implementation details     │
│ are provided in Claude's preferred format for optimal code generation.            │
└─────────────────────────────────────────────────────────────────────────────────────┘

CREWAI AGENT OUTPUTS THE 4-DOCUMENT WEAPON STRATEGY

This project implements the revolutionary 4-document weapon strategy:

📋 STRATEGIC NOTES (Psychological Warfare Elements)

DETAILED MARKET RESEARCH
{project_info['overview'] if project_info['overview'] else f"# {project_info['project_name']} Market Research Summary"}

{project_info['audience'] if project_info['audience'] else f"# Target Audience\n{project_info['target_audience']}"}

{project_info['technical'] if project_info['technical'] else f"# Technical Requirements\n- Frontend: Next.js 14 + React + Tailwind\n- Backend: FastAPI\n- Database: PostgreSQL"}

{project_info['ui_ux'] if project_info['ui_ux'] else "# UI/UX Design\n- Modern, responsive design\n- Accessibility-first approach\n- Mobile-first responsive design"}

{project_info['implementation'] if project_info['implementation'] else "# Implementation Plan\n- Phase 1: Core architecture (Week 1)\n- Phase 2: AI integration (Week 2)\n- Phase 3: UI/UX refinement (Week 3)\n- Phase 4: Deployment (Week 4)"}

{project_info['metrics'] if project_info['metrics'] else "# Success Metrics\n- User adoption and engagement\n- Feature utilization rates\n- Performance and reliability metrics"}

{project_info['deployment'] if project_info['deployment'] else "# Deployment Strategy\n- Frontend: Vercel deployment\n- Backend: Render hosting\n- Database: PostgreSQL on Render"}

TECHNICAL SPECIFICATIONS
{{
  "frontend": "Next.js 14 + React + Tailwind",
  "backend": "FastAPI",
  "database": "PostgreSQL",
  "deployment": "Vercel + Render + PostgreSQL"
}}

1. **Perfect 1-Page Document** (This Report) - Claude's dream brief
2. **Custom Frontend Boilerplate** - Industry-specific React/Next.js components
3. **Custom Backend Boilerplate** - Optimized FastAPI architecture
4. **Optimized Prompt Template** - 3-5 prompts for complete application generation

This strategy ensures Claude can produce complete, production-ready applications in exactly 3-5 prompts, making this the ultimate weapon against Claude Code."""

    print("✅ Post-processing completed - output now follows exact required format")
    return formatted_output

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
    
    # Must NOT be generic
    is_generic = any(re.search(pattern, output, re.IGNORECASE) for pattern in generic_patterns)
    
    return has_role and has_psychological and not is_generic

def passes_rules(text: str) -> bool:
    """
    Strict pass/fail check for Delivery Coordinator output.
    Returns True only if output starts with "You are an expert" AND passes document structure validation.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # CRITICAL: Must start with "You are an expert"
    starts_ok = text.strip().startswith("You are an expert")
    
    # Must pass document structure validation
    structure_ok = validate_document_structure(text)
    
    return starts_ok and structure_ok

def kickoff_with_retries(max_retries: int = 3, project_name: str = "AI Application") -> str:
    """
    Run the crew end-to-end and enforce Delivery Coordinator compliance.
    Uses the new expert profile system for guaranteed perfect formatting.
    """
    print(f"🎯 kickoff_with_retries called with project_name: {project_name}")
    last_output = ""
    for attempt in range(1, max_retries + 1):
        print(f"\n=== Crew attempt {attempt}/{max_retries} ===")
        crew = build_crew()            # build fresh (prevents cached context drift)
        result = crew.kickoff()        # full sequential run per your Process.sequential

        # CrewAI sometimes returns dict-like results; normalize to string
        out = result.get("raw", result) if isinstance(result, dict) else str(result)
        last_output = out
        print(f"📝 Raw CrewAI output length: {len(out)}")

        # NEW APPROACH: Use expert profile system for guaranteed perfect formatting
        print(f"🔄 Using expert profile system for project: {project_name}")
        try:
            from .expert_profiles import create_perfect_one_page_document
            processed_output = create_perfect_one_page_document(project_name, out)
            print(f"✅ Expert profile system processed output (length: {len(processed_output)})")
        except Exception as e:
            print(f"❌ Expert profile system failed: {e}")
            import traceback
            traceback.print_exc()
            processed_output = out
        
        if passes_rules(processed_output):
            print(f"✅ Expert profile system generated perfect output on attempt {attempt}.")
            return processed_output

        print("❌ Expert profile output failed checks. Will retry with a fresh crew...")

    raise RuntimeError(
        "Coordinator failed to satisfy mandatory rules after retries and expert profile processing.\n"
        "Last output (truncated):\n" + (last_output[:800] + ("..." if len(last_output) > 800 else ""))
    )

def build_crew():
    """
    Build the CrewAI crew with optimized agents and tasks for Claude optimization.
    """
    
    # Initialize tools
    search_tool = TavilySearchResults(max_results=5)
    duckduckgo_tool = DuckDuckGoSearchAPIWrapper()
    
    # Configure Gemini LLM for Delivery Coordinator
    delivery_coordinator_llm = None
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if google_api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            delivery_coordinator_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.1,  # Low creativity for obedience
                google_api_key=google_api_key
            )
            print("🚀 Using Gemini Pro for Delivery Coordinator")
        except Exception as e:
            print(f"⚠️ Failed to configure Gemini for Delivery Coordinator: {e}")
            delivery_coordinator_llm = None
    else:
        print("⚠️ GOOGLE_API_KEY/GEMINI_API_KEY not found - using default LLM for Delivery Coordinator")
    
    # Agents with enhanced roles and backstories
    market_researcher = Agent(
        role="Market Research Analyst",
        goal="Conduct comprehensive market research and create Claude-optimized project briefs",
        backstory="""You are a senior market research analyst with 15+ years of experience in 
        technology market analysis and AI application research. You have conducted research for 
        Fortune 500 companies and have a deep understanding of user needs, market trends, and 
        competitive landscapes. You excel at creating detailed, actionable insights that can be 
        directly translated into technical specifications and implementation plans. Your research 
        has been instrumental in launching successful AI applications that have generated millions 
        in revenue.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
        memory=True
    )
    
    frontend_engineer = Agent(
        role="Frontend Engineer & UI/UX Designer",
        goal="Design and implement stunning, industry-specific frontend architectures",
        backstory="""You are a senior frontend engineer and UI/UX designer with 12+ years of 
        experience building world-class web applications. You have worked with major tech companies 
        and have designed interfaces used by millions of users. You specialize in React, Next.js, 
        and Tailwind CSS, and have a deep understanding of user experience principles, accessibility 
        standards, and modern design trends. You excel at creating intuitive, beautiful, and 
        performant user interfaces that drive user engagement and satisfaction. Your designs have 
        won industry awards and have been featured in design publications.""",
        tools=[],
        verbose=True,
        allow_delegation=False,
        memory=True
    )
    
    backend_engineer = Agent(
        role="Backend Engineer",
        goal="Design and implement robust, scalable backend architectures",
        backstory="""You are a senior backend engineer with 10+ years of experience building 
        high-performance, scalable web applications. You have worked with major tech companies 
        and have architected systems that handle millions of requests per day. You specialize in 
        FastAPI, Python, and modern backend technologies, and have deep expertise in database 
        design, API development, security, and performance optimization. You excel at creating 
        robust, maintainable, and scalable backend systems that can handle real-world production 
        loads. Your systems have achieved 99.9% uptime and have been praised for their reliability 
        and performance.""",
        tools=[],
        verbose=True,
        allow_delegation=False,
        memory=True
    )
    
    # SIMPLIFIED: Delivery Coordinator - let it generate whatever, we'll fix it in post-processing
    delivery_coordinator = Agent(
        role="Delivery Coordinator & Claude Optimization Specialist",
        goal="Assemble the 4-document weapon and create comprehensive project documentation",
        backstory="""You are a senior project coordinator with expertise in AI application development. 
        Your role is to gather information from all team members and create comprehensive project documentation. 
        Focus on being thorough and detailed in your output.""",
        llm=delivery_coordinator_llm,  # Use Gemini if available
        allow_delegation=False,
        temperature=0.3,  # Slightly higher for better content generation
        max_iter=2,
        verbose=True,
        memory=True
    )
    
    # SIMPLIFIED: Rule Enforcer - not needed since we're using post-processing
    rule_enforcer = Agent(
        role="Rule Enforcer",
        goal="Ensure all outputs follow strict Claude-optimization rules.",
        backstory="You are extremely critical and will reject any deviation from the instructions. You have zero tolerance for rule violations and will force corrections.",
        temperature=0.0,                     # zero creativity = maximum enforcement
        allow_delegation=False,
        verbose=True,
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
    
    frontend_design_task = Task(
        description="""Design and implement the frontend application architecture with industry-specific design excellence.
                    
                    IMPORTANT: You have access to the market research data from the previous task.
                    Use this market research to inform your design decisions and create industry-specific solutions.
                    
                    MARKET RESEARCH CONTEXT:
                    {market_research_output}
                    
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
                    
                    CLAUDE OPTIMIZATION REQUIREMENTS:
                    - Provide specific design specifications that Claude can implement
                    - Include exact color codes, font choices, and spacing guidelines
                    - Specify exact component libraries and dependencies
                    - Create design tokens and CSS variables for consistency
                    - Provide responsive breakpoints and mobile considerations
                    
                    Output: Complete frontend boilerplate with app-type specific components, patterns, and 
                    industry-specific design excellence, optimized for Claude implementation.""",
                    agent=frontend_engineer,
                    expected_output="Complete frontend boilerplate with industry-specific design excellence",
                    context=[market_research_task],  # Depends on market research
                    output_json=False,
                    async_execution=False
    )
    
    backend_design_task = Task(
        description="""Design and implement the backend architecture optimized for Claude implementation.
                    
                    IMPORTANT: You have access to the market research data from the previous task.
                    Use this market research to inform your backend design decisions.
                    
                    MARKET RESEARCH CONTEXT:
                    {market_research_output}
                    
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
                    expected_output="Complete backend specification with implementation details",
                    context=[market_research_task],  # Depends on market research
                    output_json=False,
                    async_execution=False
    )
    
    # SIMPLIFIED: Coordination task - let it generate whatever, we'll fix it in post-processing
    coordination_task = Task(
        description=(
            "Coordinate all deliverables and create comprehensive project documentation.\n\n"
            "THE 4-DOCUMENT WEAPON ASSEMBLY:\n"
            "1. Perfect 1-Page Document (Claude-optimized)\n"
            "2. Custom Frontend Boilerplate (industry-specific design)\n"
            "3. Custom Backend Boilerplate (optimized architecture)\n"
            "4. Optimized Prompt Template (3–5 prompts)\n\n"
            "Create a comprehensive document that includes:\n"
            "- Project overview and objective\n"
            "- Target audience and market analysis\n"
            "- Technical requirements and architecture\n"
            "- UI/UX design specifications\n"
            "- Implementation plan and timeline\n"
            "- Success metrics and validation\n"
            "- Deployment and launch strategy\n\n"
            "Be thorough and detailed in your output."
        ),
        agent=delivery_coordinator,
        expected_output="Comprehensive project documentation with all required sections",
        context=[market_research_task, frontend_design_task, backend_design_task],  # Depends on all previous tasks
        output_json=False,
        async_execution=False
    )
    
    # SIMPLIFIED: Validation task - not needed since we're using post-processing
    validation_task = Task(
        description=(
            "Validate the Delivery Coordinator's output. Check for completeness and quality."
        ),
        agent=rule_enforcer,
        expected_output="Validation Result: PASS ✅ or FAIL ❌ + reason",
        context=[coordination_task],  # Depends on coordination task output
        output_json=False,
        async_execution=False
    )
    
    # Create crew with optimized task order
    # CORRECT ORDER: Market Research → Frontend → Backend → Coordinator → Validator
    crew = Crew(
        agents=[market_researcher, frontend_engineer, backend_engineer, delivery_coordinator, rule_enforcer],
        tasks=[market_research_task, frontend_design_task, backend_design_task, coordination_task, validation_task],
        process=Process.sequential,  # Use sequential instead of hierarchical
        verbose=True
        # Note: max_iter parameter removed as it's not available in this CrewAI version
    )
    
    return crew

# Create and export the crew instance
crew = build_crew()

# Export the retry function for use in api_routes.py
__all__ = ['crew', 'kickoff_with_retries', 'passes_rules', 'post_process_coordinator_output', 'create_perfect_one_page_document']
