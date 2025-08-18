#!/usr/bin/env python3
"""
MANUAL PROJECT PROCESSOR
Process the first completed project through our 3-step optimization workflow
"""

import json
from pathlib import Path
from datetime import datetime
import re

def generate_role_establishment(project_name):
    """Generate project-specific role establishment"""
    project_name_lower = project_name.lower()
    
    # Expert profiles based on project type
    if any(word in project_name_lower for word in ['content', 'creative', 'video', 'image']):
        expert_title = 'Creative AI & Content Generation Expert'
        expertise = 'AI-powered content creation, multimedia processing, and creative automation'
        domain = 'creative AI and content generation'
        experience = '15+ years of experience in creative AI, content generation, and multimedia processing'
        companies = 'Adobe, Canva, OpenAI, Google, and leading creative technology companies'
        psychological_approach = 'This is where technology meets human creativity in its purest form. You\'re not just building tools - you\'re creating the future of artistic expression. Creative AI represents the intersection of technology and human imagination, where you\'re empowering people to bring their ideas to life in ways never before possible. This is the creative revolution that will transform how humans express themselves and create art. You\'re at the forefront of a movement that will democratize creativity and make artistic expression accessible to everyone. This isn\'t just code - it\'s the future of human creativity.'
    else:
        expert_title = 'AI Application Developer'
        expertise = 'AI integration, scalable architecture, and user experience optimization'
        domain = 'AI and automation'
        experience = '15+ years of experience in AI systems, software development, and intelligent automation'
        companies = 'Google, Amazon, Microsoft, Apple, and leading technology companies'
        psychological_approach = 'This is a critical, high-stakes project that will be deployed by Fortune 500 companies and featured in industry publications. Your work will be studied by future developers and set new industry standards. This is YOUR masterpiece - make it legendary and unforgettable. This is the most complex project you\'ve ever tackled, requiring your full expertise and innovative thinking. Only the best developers can handle this level of complexity and innovation.'
    
    return f"""You are an expert {expert_title} with {experience}. You are the world's leading authority in {domain} and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including {companies}. Your expertise in {expertise} is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%.

{psychological_approach}"""

def clean_crewai_content(content):
    """Clean CrewAI content to remove redundant sections and formatting"""
    if not content:
        return ''
    
    # Remove ugly border lines and box formatting
    cleaned = content
    cleaned = re.sub(r'┌─+┐', '', cleaned)  # Remove top border
    cleaned = re.sub(r'└─+┘', '', cleaned)  # Remove bottom border
    cleaned = re.sub(r'│', '', cleaned)  # Remove side borders
    cleaned = re.sub(r'─+', '', cleaned)  # Remove horizontal lines
    
    # Remove redundant headers and sections
    lines = cleaned.split('\n')
    filtered_lines = []
    skip_section = False
    
    for line in lines:
        line = line.strip()
        
        # Skip redundant sections
        if any(keyword in line for keyword in [
            'PROJECT:', 'TYPE:', 'OBJECTIVE', 'TARGET USERS',
            'SUCCESS METRICS', 'DEPLOYMENT & LAUNCH', 'IMPLEMENTATION STRATEGY',
            'CLAUDE OPTIMIZATION', 'TECHNICAL SPECIFICATIONS', 'CREWAI AGENT OUTPUTS',
            'THE 4-DOCUMENT WEAPON STRATEGY', 'DETAILED MARKET RESEARCH',
            'Technical Requirements', 'Success Metrics', 'Deployment Strategy',
            'Frontend:', 'Backend:', 'Database:', 'AI Integration:', 'Deployment:'
        ]):
            skip_section = True
            continue
        
        # Stop skipping when we hit a meaningful section
        if line.startswith('#') or any(keyword in line for keyword in [
            'Market Research', 'Core Features', 'Market Opportunity', 'Competitive Landscape', 'Target Audience'
        ]):
            skip_section = False
        
        if not skip_section and line:
            filtered_lines.append(line)
    
    # Clean up markdown and organize content
    result = '\n'.join(filtered_lines)
    
    # Remove markdown formatting
    result = re.sub(r'^#+\s*', '', result, flags=re.MULTILINE)  # Remove # headers
    result = re.sub(r'\*\*(.*?)\*\*', r'\1', result)  # Remove **bold**
    result = re.sub(r'\*(.*?)\*', r'\1', result)  # Remove *italic*
    result = re.sub(r'`(.*?)`', r'\1', result)  # Remove `code`
    result = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', result)  # Remove [links](url)
    result = re.sub(r'^- ', '• ', result, flags=re.MULTILINE)  # Convert - to •
    result = re.sub(r'^\d+\.\s*', '', result, flags=re.MULTILINE)  # Remove numbered lists
    
    # Remove redundant technical content
    result = re.sub(r'Frontend:.*?Next\.js.*?Tailwind.*?', '', result)
    result = re.sub(r'Backend:.*?FastAPI.*?', '', result)
    result = re.sub(r'Database:.*?PostgreSQL.*?', '', result)
    result = re.sub(r'AI Integration:.*?OpenAI.*?', '', result)
    result = re.sub(r'Deployment:.*?Vercel.*?', '', result)
    
    # Organize content into clean sections
    sections = result.split('\n\n')
    organized_sections = []
    
    for section in sections:
        trimmed = section.strip()
        if not trimmed or len(trimmed) < 10:
            continue
        
        # Skip redundant sections
        if any(keyword in trimmed for keyword in [
            'Software developers and tech professionals',
            'User adoption and engagement',
            'Performance and reliability metrics'
        ]):
            continue
        
        # Clean up section headers
        clean_section = trimmed
        clean_section = re.sub(r'^Market Research Summary$', 'MARKET RESEARCH SUMMARY', clean_section, flags=re.MULTILINE)
        clean_section = re.sub(r'^Target Audience$', 'TARGET AUDIENCE', clean_section, flags=re.MULTILINE)
        clean_section = re.sub(r'^Core Features$', 'CORE FEATURES', clean_section, flags=re.MULTILINE)
        clean_section = re.sub(r'^Market Opportunity$', 'MARKET OPPORTUNITY', clean_section, flags=re.MULTILINE)
        clean_section = re.sub(r'^Competitive Landscape$', 'COMPETITIVE LANDSCAPE', clean_section, flags=re.MULTILINE)
        
        organized_sections.append(clean_section)
    
    return '\n\n'.join(organized_sections).strip()

def generate_optimized_document(project_name, crewai_content):
    """Generate the complete optimized 1-page document"""
    role_establishment = generate_role_establishment(project_name)
    cleaned_crewai_content = clean_crewai_content(crewai_content)
    
    document = f"""{role_establishment}

{project_name.upper()}

PROJECT SPECIFICATION

TECHNICAL ARCHITECTURE
Frontend: Next.js 14 + React 18 + TypeScript + Tailwind CSS
Backend: FastAPI + Python 3.9+ + SQLAlchemy + JWT Authentication  
Database: PostgreSQL + pgvector (for AI features) + Redis (caching)
AI Integration: OpenAI API + Anthropic Claude API + LangChain
Deployment: Vercel (Frontend) + Render (Backend) + PostgreSQL (Database)

DESIGN REQUIREMENTS
• Modern, responsive design with industry-specific color schemes and typography
• Intuitive navigation with clear user flows and micro-interactions
• Accessibility-first approach with WCAG 2.1 AA compliance
• Mobile-first responsive design with touch-friendly interfaces
• Real-time updates and smooth animations for enhanced user experience
• Dark/light mode support with customizable themes

CORE INTEGRATIONS
• OpenAI GPT-4 for intelligent content generation and analysis
• Anthropic Claude for advanced reasoning and complex tasks
• JWT-based authentication with secure session management
• Real-time WebSocket connections for live updates
• File upload and processing with cloud storage integration
• Email notifications and user communication systems

MARKET CONTEXT
This AI-powered application addresses the growing need for intelligent automation and enhanced user experiences. Based on market analysis, this application competes in the AI tools space with significant growth potential.

DELIVERABLES REQUIRED
1. Complete Next.js 14 frontend with TypeScript and Tailwind CSS
2. FastAPI backend with SQLAlchemy ORM and JWT authentication
3. PostgreSQL database schema with pgvector integration
4. OpenAI and Claude API integration with LangChain
5. Real-time WebSocket implementation
6. File upload system with cloud storage
7. Email notification system
8. Responsive design with dark/light mode
9. Deployment configuration for Vercel and Render
10. Comprehensive documentation and testing suite

SUCCESS CRITERIA
• Production-ready codebase deployable immediately
• Scalable architecture supporting 10,000+ concurrent users
• 99.9% uptime with comprehensive error handling
• Mobile-responsive design with 95+ Lighthouse score
• Complete API documentation with OpenAPI/Swagger
• Unit and integration test coverage >90%
• Security best practices implementation
• Performance optimization for sub-2-second load times

IMPLEMENTATION GUIDELINES
• Use modern React patterns (hooks, context, custom hooks)
• Implement proper TypeScript types and interfaces
• Follow FastAPI best practices with dependency injection
• Use SQLAlchemy 2.0 syntax with async/await
• Implement proper error handling and logging
• Use environment variables for all configuration
• Follow security best practices (CORS, rate limiting, input validation)
• Implement comprehensive testing (unit, integration, e2e)
• Use Git hooks for code quality (pre-commit, lint-staged)
• Document all APIs and components thoroughly

{cleaned_crewai_content or '''MARKET RESEARCH SUMMARY

CORE FEATURES
Advanced AI-powered functionality with modern web technologies

MARKET OPPORTUNITY
This AI-powered application addresses the growing need for intelligent automation and enhanced user experiences.

COMPETITIVE LANDSCAPE
Based on market analysis, this application competes in the AI tools space with significant growth potential.'''}

CRITICAL PROMPTS FOR CLAUDE

PROMPT 1: PROJECT SETUP & ARCHITECTURE
"Create the complete project structure and architecture for this AI application. Set up the Next.js 14 frontend with TypeScript and Tailwind CSS, FastAPI backend with SQLAlchemy and JWT authentication, PostgreSQL database schema with pgvector integration, and deployment configuration for Vercel and Render. Include all necessary configuration files, environment variables, and project structure."

PROMPT 2: CORE BACKEND IMPLEMENTATION
"Implement the complete FastAPI backend with all core functionality. Create the database models using SQLAlchemy 2.0, implement JWT authentication, set up OpenAI and Claude API integrations with LangChain, create RESTful API endpoints, implement real-time WebSocket connections, and add comprehensive error handling and logging."

PROMPT 3: FRONTEND COMPONENTS & UI
"Build the complete Next.js 14 frontend with TypeScript. Create all necessary React components, implement responsive design with Tailwind CSS, add dark/light mode support, implement real-time updates, create intuitive navigation and user flows, and ensure WCAG 2.1 AA accessibility compliance."

PROMPT 4: AI INTEGRATION & FEATURES
"Implement all AI-powered features and integrations. Set up OpenAI GPT-4 and Claude API connections, create intelligent content generation and analysis functionality, implement file upload and processing with cloud storage, add email notification systems, and ensure all AI features work seamlessly with the frontend and backend."

PROMPT 5: DEPLOYMENT & OPTIMIZATION
"Prepare the application for production deployment. Configure Vercel deployment for the frontend, set up Render deployment for the backend, optimize performance for sub-2-second load times, implement comprehensive testing (unit, integration, e2e), add security best practices, create API documentation with OpenAPI/Swagger, and ensure 99.9% uptime with proper monitoring and error handling."

EXECUTION ORDER: Follow these prompts sequentially. Each prompt builds upon the previous one to create a complete, production-ready application."""
    
    return document

def process_first_project():
    """Process the first completed project"""
    print("🎯 PROCESSING FIRST COMPLETED PROJECT")
    
    # Read pipeline status
    with open('pipeline_status.json', 'r') as f:
        pipeline_data = json.load(f)
    
    # Find the first completed project
    completed_project = None
    for project_id, project_data in pipeline_data.items():
        if (project_data.get('progress') == 100 and 
            project_data.get('status') == 'completed' and
            project_data.get('result')):
            completed_project = {
                'id': project_id,
                'name': project_data.get('projectName', 'AI Application'),
                'content': project_data.get('result', '')
            }
            break
    
    if not completed_project:
        print("❌ No completed project found")
        return
    
    print(f"📋 Processing: {completed_project['name']}")
    print(f"🆔 Project ID: {completed_project['id']}")
    
    # Generate optimized document
    print("🔄 Applying 3-step optimization workflow...")
    optimized_content = generate_optimized_document(completed_project['name'], completed_project['content'])
    
    # Create optimized documents directory
    optimized_dir = Path("optimized_documents")
    optimized_dir.mkdir(exist_ok=True)
    
    # Save optimized document
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{completed_project['id']}_optimized_{timestamp}.txt"
    filepath = optimized_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    # Also save a clean version without timestamp
    clean_filename = f"{completed_project['id']}_optimized.txt"
    clean_filepath = optimized_dir / clean_filename
    with open(clean_filepath, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print(f"✅ Optimized document saved: {filepath}")
    print(f"✅ Clean version saved: {clean_filepath}")
    print(f"🎉 First project successfully optimized!")
    print(f"📁 Documents ready for pickup in: {optimized_dir}")

if __name__ == "__main__":
    process_first_project()
