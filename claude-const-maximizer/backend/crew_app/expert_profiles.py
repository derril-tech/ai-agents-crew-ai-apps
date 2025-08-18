#!/usr/bin/env python3
"""
Expert Profile Mapping System
Maps project names to ideal expert profiles for role establishment in the 1-page document.
"""

import re
from typing import Dict, Tuple

# Expert profile mappings based on project categories
EXPERT_PROFILES = {
    # Voice AI & Personal Assistant (01_voice_ai_personal_assistant) - 6 projects
    "voice": {
        "title": "Voice AI & Personal Assistant Developer",
        "expertise": "voice processing, speech recognition, natural language understanding, and intelligent automation",
        "domain": "voice AI and personal assistant technology",
        "experience": "15+ years of experience in voice AI, speech processing, and intelligent automation systems",
        "companies": "Google, Amazon, Microsoft, Apple, and leading voice technology companies",
        "psychological_approach": "The ideal psychological approach for voice AI projects is to emphasize the revolutionary nature of human-computer interaction, the prestige of working with cutting-edge voice technology that will define the future of computing, and the competitive advantage of being among the first to master this transformative technology. Focus on the legacy impact - voice AI will be studied by future generations as the foundation of natural human-AI interaction."
    },
    
    # Multi-Agent CrewAI (02_mult_agent_crewai) - 25 projects
    "crewai": {
        "title": "Multi-Agent AI Systems Architect",
        "expertise": "multi-agent orchestration, AI system design, and intelligent workflow automation",
        "domain": "multi-agent AI systems and intelligent automation",
        "experience": "15+ years of experience in multi-agent systems, AI orchestration, and intelligent workflow design",
        "companies": "OpenAI, Anthropic, Google AI, Microsoft Research, and leading AI research institutions",
        "psychological_approach": "The ideal psychological approach for multi-agent projects is to emphasize the complexity and sophistication of orchestrating multiple AI agents, the prestige of working on the cutting edge of AI research that will revolutionize how businesses operate, and the competitive advantage of mastering the most advanced AI orchestration techniques. Focus on the validation - multi-agent systems represent the pinnacle of AI engineering and only the most elite developers can handle this level of complexity."
    },
    
    # RAG Document Processing (03_rag_document_processing) - 8 projects
    "rag": {
        "title": "RAG & Document Intelligence Specialist",
        "expertise": "retrieval-augmented generation, document processing, and knowledge management systems",
        "domain": "document intelligence and knowledge management",
        "experience": "15+ years of experience in RAG systems, document processing, and knowledge management",
        "companies": "OpenAI, Anthropic, Google, Microsoft, and leading document AI companies",
        "psychological_approach": "The ideal psychological approach for RAG projects is to emphasize the critical importance of knowledge management in the information age, the prestige of working with the most advanced document intelligence systems that will transform how organizations access and utilize their knowledge, and the competitive advantage of mastering the technology that will define the future of information retrieval. Focus on the urgency - organizations are desperate for intelligent document processing solutions that can unlock their hidden knowledge."
    },
    
    # Creative AI Content Generation (04_creative_ai_content_gen) - 7 projects
    "content": {
        "title": "Creative AI & Content Generation Expert",
        "expertise": "AI-powered content creation, multimedia processing, and creative automation",
        "domain": "creative AI and content generation",
        "experience": "15+ years of experience in creative AI, content generation, and multimedia processing",
        "companies": "Adobe, Canva, OpenAI, Google, and leading creative technology companies",
        "psychological_approach": "The ideal psychological approach for creative AI projects is to emphasize the artistic and innovative nature of AI-powered creativity, the prestige of working at the intersection of technology and human imagination, and the competitive advantage of mastering the tools that will define the future of creative expression. Focus on the legacy - creative AI will revolutionize how humans express themselves and create art, and you'll be at the forefront of this creative revolution."
    },
    
    # Healthcare Medical AI (05_healthcare_medical_ai) - 3 projects
    "healthcare": {
        "title": "Healthcare AI & Medical Technology Specialist",
        "expertise": "medical AI, healthcare automation, and clinical decision support systems",
        "domain": "healthcare AI and medical technology",
        "experience": "15+ years of experience in healthcare AI, medical technology, and clinical systems",
        "companies": "Epic Systems, Cerner, IBM Watson Health, and leading healthcare technology companies",
        "psychological_approach": "The ideal psychological approach for healthcare AI projects is to emphasize the life-saving impact and ethical responsibility of medical technology, the prestige of working on systems that directly improve human health and save lives, and the competitive advantage of mastering the most regulated and critical AI applications. Focus on the validation - healthcare AI represents the highest calling in technology, where your work literally saves lives and improves human wellbeing."
    },
    
    # Business E-commerce (06_business_ecommerce) - 5 projects
    "ecommerce": {
        "title": "E-commerce & Business AI Developer",
        "expertise": "e-commerce platforms, business automation, and AI-powered commerce solutions",
        "domain": "e-commerce and business AI",
        "experience": "15+ years of experience in e-commerce, business automation, and AI-powered commerce",
        "companies": "Amazon, Shopify, Stripe, and leading e-commerce technology companies",
        "psychological_approach": "The ideal psychological approach for business AI projects is to emphasize the massive financial impact and market opportunity of AI-powered business solutions, the prestige of working on systems that drive billions in revenue and transform entire industries, and the competitive advantage of mastering the technology that will define the future of commerce. Focus on the urgency - businesses are racing to adopt AI solutions and those who master this technology first will dominate their markets."
    },
    
    # Developer Tools Code Analysis (07_developer_tools_code_analysis) - 3 projects
    "developer": {
        "title": "Developer Tools & Code Analysis Expert",
        "expertise": "developer tools, code analysis, and software development automation",
        "domain": "developer tools and software development",
        "experience": "15+ years of experience in developer tools, code analysis, and software development automation",
        "companies": "GitHub, Microsoft, JetBrains, and leading developer tool companies",
        "psychological_approach": "The ideal psychological approach for developer tools projects is to emphasize the meta-level impact of building tools that other developers use to build everything else, the prestige of working on the infrastructure that powers the entire software industry, and the competitive advantage of mastering the technology that will define how software is developed for decades to come. Focus on the legacy - developer tools are the foundation of all software development, and your work will be used by millions of developers worldwide."
    },
    
    # Web API Integration (08_web_api_integration) - 3 projects
    "api": {
        "title": "Web API & Integration Specialist",
        "expertise": "API development, system integration, and web service architecture",
        "domain": "web APIs and system integration",
        "experience": "15+ years of experience in API development, system integration, and web service architecture",
        "companies": "Google, Amazon Web Services, Microsoft Azure, and leading API companies",
        "psychological_approach": "The ideal psychological approach for API integration projects is to emphasize the connective power of APIs as the backbone of the modern internet, the prestige of working on systems that enable seamless data flow between applications and services, and the competitive advantage of mastering the technology that powers the interconnected digital world. Focus on the urgency - every business needs robust API integration to compete in the digital economy, and those who master this technology will be the architects of the connected future."
    }
}

# Complete list of all 60 projects for reference
ALL_60_PROJECTS = {
    # Voice AI & Personal Assistant (6 projects)
    "voice": [
        "AI-Powered Personal Voice Assistant & Calendar Manager",
        "AI-Powered Voice-Controlled Smart Home Manager", 
        "AI-Powered Voice-Based Meeting Assistant & Note Taker",
        "AI-Powered Voice-Controlled Task & Project Manager",
        "AI-Powered Voice-Based Health & Wellness Coach",
        "AI-Powered Interactive Storybook Creator"
    ],
    
    # Multi-Agent CrewAI (25 projects)
    "crewai": [
        # Research & Analysis (8 projects)
        "Autonomous Research & Report Generation System",
        "Automated Market Research and Report Generation Team", 
        "Automated Research Department",
        "Cybersecurity Threat Analysis Team",
        "Multi-Agent Cybersecurity Defense System",
        "Intelligent Smart City Management System",
        "Real Estate Investment Finder",
        "Conference Planning Crew",
        
        # Business & E-commerce (6 projects)
        "Intelligent E-commerce Management System",
        "E-commerce Customer Service and Fraud Detection",
        "E-Commerce Launch Crew",
        "B2B Sales Prospecting AI",
        "SEO Growth Team",
        "Startup Idea to Pitch Deck Crew",
        
        # Content & Marketing (4 projects)
        "Multi-Agent Content Creation & Marketing System",
        "Creative Content Generation and Marketing Team",
        "Social Media Factory",
        "AI Content Localizer",
        
        # Healthcare & Legal (3 projects)
        "Intelligent Healthcare Diagnosis & Treatment Planning",
        "AI-Powered Legal Document Analysis & Contract Negotiation",
        "Recruitment Flow AI",
        
        # Development & Education (4 projects)
        "Multi-Agent Software Development Team",
        "Automated Software Development Team",
        "Autonomous Learning and Research Assistant",
        "Personal Brain Agent System"
    ],
    
    # RAG Document Processing (8 projects)
    "rag": [
        "Intelligent Document Processing & Knowledge Base",
        "AI-Powered Resume Parser & Job Matcher",
        "AI-Powered Legal Document Analysis & Contract Negotiation",
        "Research Assistant with Document Q&A",
        "PDF Analysis & Summarization Tool",
        "Document Classification & Organization",
        "Multi-format Document Processor",
        "Knowledge Base with Vector Search"
    ],
    
    # Creative AI Content Generation (7 projects)
    "content": [
        "AI-Powered Video Content Generator",
        "AI Image Generation & Editing Platform",
        "Creative Writing Assistant & Story Generator",
        "Social Media Content Creator",
        "Podcast & Audio Content Generator",
        "Marketing Copy & Ad Generator",
        "Creative Portfolio Builder"
    ],
    
    # Healthcare Medical AI (3 projects)
    "healthcare": [
        "AI-Powered Medical Diagnosis Assistant",
        "Intelligent Healthcare Diagnosis & Treatment Planning",
        "Health Monitoring & Wellness Tracking System"
    ],
    
    # Business E-commerce (5 projects)
    "ecommerce": [
        "Intelligent E-commerce Management System",
        "AI-Powered Business Analytics Dashboard",
        "Financial Planning & Investment Assistant",
        "Supply Chain & Inventory Management",
        "Customer Relationship Management (CRM)"
    ],
    
    # Developer Tools Code Analysis (3 projects)
    "developer": [
        "AI-Powered Code Review & Refactoring Assistant",
        "Smart Contract Analysis & Security Auditor",
        "Developer Productivity & Workflow Automation"
    ],
    
    # Web API Integration (3 projects)
    "api": [
        "Web Scraping & Data Aggregation Platform",
        "API Integration & Workflow Automation",
        "Real-time Data Monitoring & Alerting System"
    ]
}

def detect_project_category(project_name: str) -> str:
    """
    Detect the project category based on the project name.
    Returns the category key for expert profile mapping.
    """
    project_name_lower = project_name.lower()
    
    # First, try exact matches with the 60 project names
    for category, projects in ALL_60_PROJECTS.items():
        for project in projects:
            if project.lower() in project_name_lower or project_name_lower in project.lower():
                return category
    
    # Fallback to keyword-based detection
    # Voice AI & Personal Assistant
    if any(keyword in project_name_lower for keyword in ["voice", "assistant", "calendar", "smart home", "meeting", "task manager", "health coach", "storybook"]):
        return "voice"
    
    # Multi-Agent CrewAI
    if any(keyword in project_name_lower for keyword in ["crew", "agent", "multi-agent", "orchestration", "research", "cybersecurity", "market research", "content creation", "software development", "learning", "brain"]):
        return "crewai"
    
    # RAG Document Processing
    if any(keyword in project_name_lower for keyword in ["rag", "document", "knowledge", "retrieval", "search", "resume", "legal", "pdf", "classification", "vector"]):
        return "rag"
    
    # Creative AI Content Generation
    if any(keyword in project_name_lower for keyword in ["content", "creative", "video", "image", "writing", "social media", "podcast", "marketing", "portfolio", "story"]):
        return "content"
    
    # Healthcare Medical AI
    if any(keyword in project_name_lower for keyword in ["health", "medical", "clinical", "patient", "diagnosis", "treatment", "wellness", "monitoring"]):
        return "healthcare"
    
    # Business E-commerce
    if any(keyword in project_name_lower for keyword in ["ecommerce", "business", "commerce", "shop", "store", "retail", "payment", "financial", "analytics", "crm", "supply chain", "inventory"]):
        return "ecommerce"
    
    # Developer Tools Code Analysis
    if any(keyword in project_name_lower for keyword in ["developer", "code", "analysis", "tool", "debug", "testing", "review", "refactoring", "security", "contract", "productivity"]):
        return "developer"
    
    # Web API Integration
    if any(keyword in project_name_lower for keyword in ["api", "integration", "web", "service", "microservice", "scraping", "data", "monitoring", "alerting"]):
        return "api"
    
    # Default to content generation if no specific category is detected
    return "content"

def get_expert_profile(project_name: str) -> Dict[str, str]:
    """
    Get the expert profile for a given project name.
    Returns the expert profile dictionary.
    """
    category = detect_project_category(project_name)
    return EXPERT_PROFILES.get(category, EXPERT_PROFILES["content"])

def get_all_60_projects() -> Dict[str, list]:
    """
    Get all 60 projects organized by category.
    Returns a dictionary with category keys and project lists.
    """
    return ALL_60_PROJECTS

def get_project_count_by_category() -> Dict[str, int]:
    """
    Get the count of projects in each category.
    Returns a dictionary with category keys and project counts.
    """
    return {category: len(projects) for category, projects in ALL_60_PROJECTS.items()}

def validate_project_name(project_name: str) -> bool:
    """
    Check if a project name matches any of the 60 predefined projects.
    Returns True if it's a valid project name, False otherwise.
    """
    project_name_lower = project_name.lower()
    for projects in ALL_60_PROJECTS.values():
        for project in projects:
            if project.lower() in project_name_lower or project_name_lower in project.lower():
                return True
    return False

def create_role_establishment(project_name: str, project_type: str = "AI-powered application") -> str:
    """
    Create the role establishment section for the 1-page document.
    This is hardcoded to ensure consistency and reliability.
    """
    expert_profile = get_expert_profile(project_name)
    
    # Get the psychological approach for this project type
    psychological_approach = expert_profile.get('psychological_approach', 
        "This is a time-sensitive, high-priority project that will be used by Fortune 500 companies and featured in industry publications. Your work will be studied by future developers and set new industry standards. This is YOUR masterpiece - make it legendary and unforgettable. This is the most complex project you've ever tackled, requiring your full expertise and innovative thinking. Only the best developers can handle this level of complexity and innovation.")
    
    role_establishment = f"""You are an expert {expert_profile['title']} with {expert_profile['experience']}. You are the world's leading authority in {expert_profile['domain']} and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including {expert_profile['companies']}. Your expertise in AI integration, scalable architecture, and user experience optimization is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%.

{psychological_approach}"""
    
    return role_establishment

def extract_project_info_simple(raw_output: str) -> Dict[str, str]:
    """
    Simple project info extraction without dependencies on crew module.
    """
    import re
    
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

def create_perfect_one_page_document(project_name: str, raw_agent_output: str) -> str:
    """
    Create the perfect 1-page document using hardcoded role establishment
    and extracted content from the agent output.
    """
    # Get expert profile
    expert_profile = get_expert_profile(project_name)
    role_establishment = create_role_establishment(project_name)
    
    # Extract project information from raw output
    project_info = extract_project_info_simple(raw_agent_output)
    
    # Create the perfectly formatted document
    formatted_output = f"""{role_establishment}

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
    
    return formatted_output
