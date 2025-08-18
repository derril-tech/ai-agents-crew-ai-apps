#!/usr/bin/env python3
"""
AUTOMATED DOCUMENT OPTIMIZER
Monitors pipeline results and applies 3-step optimization workflow
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
import re

class DocumentOptimizer:
    def __init__(self):
        self.pipeline_dir = Path("pipeline_status.json")
        self.results_dir = Path("direct_results")
        self.optimized_dir = Path("optimized_documents")
        self.processed_file = Path("processed_projects.txt")
        
        # Create optimized documents directory
        self.optimized_dir.mkdir(exist_ok=True)
        
        # Load processed projects
        self.processed_projects = self.load_processed_projects()
    
    def load_processed_projects(self):
        """Load list of already processed projects"""
        if self.processed_file.exists():
            with open(self.processed_file, 'r') as f:
                return set(line.strip() for line in f.readlines())
        return set()
    
    def save_processed_project(self, project_id):
        """Mark project as processed"""
        self.processed_projects.add(project_id)
        with open(self.processed_file, 'a') as f:
            f.write(f"{project_id}\n")
    
    def get_project_name(self, project_id):
        """Extract project name from project ID"""
        # Convert project ID back to readable name
        name = project_id.replace('-', ' ').replace('_', ' ')
        return ' '.join(word.capitalize() for word in name.split())
    
    def generate_role_establishment(self, project_name):
        """Generate project-specific role establishment"""
        project_name_lower = project_name.lower()
        
        # Expert profiles based on project type
        if any(word in project_name_lower for word in ['voice', 'assistant']):
            expert_title = 'Voice AI & Personal Assistant Developer'
            expertise = 'voice processing, speech recognition, natural language understanding, and intelligent automation'
            domain = 'voice AI and personal assistant technology'
            experience = '15+ years of experience in voice AI, speech processing, and intelligent automation systems'
            companies = 'Google, Amazon, Microsoft, Apple, and leading voice technology companies'
            psychological_approach = 'This is a revolutionary project that will define the future of human-computer interaction. Voice AI is the next frontier of computing, and you\'re building the foundation that millions will use. This technology will be studied by future generations as the breakthrough that made AI truly accessible. The prestige of working with cutting-edge voice technology that will transform how humans interact with machines cannot be overstated. You\'re not just building an application - you\'re creating the future.'
        
        elif any(word in project_name_lower for word in ['crew', 'agent', 'market research']):
            expert_title = 'Multi-Agent AI Systems Architect'
            expertise = 'multi-agent orchestration, AI system design, and intelligent workflow automation'
            domain = 'multi-agent AI systems and intelligent automation'
            experience = '15+ years of experience in multi-agent systems, AI orchestration, and intelligent workflow design'
            companies = 'OpenAI, Anthropic, Google AI, Microsoft Research, and leading AI research institutions'
            psychological_approach = 'This is the pinnacle of AI engineering - orchestrating multiple intelligent agents to work in perfect harmony. Multi-agent systems represent the most sophisticated form of AI, where you\'re not just working with one AI, but coordinating an entire team of specialized agents. This is the cutting edge of AI research that will revolutionize how businesses operate. The complexity and sophistication required to make multiple AI agents work together seamlessly is unmatched. Only the most elite developers can handle this level of orchestration. You\'re building the future of AI collaboration.'
        
        elif any(word in project_name_lower for word in ['rag', 'document', 'knowledge']):
            expert_title = 'RAG & Document Intelligence Specialist'
            expertise = 'retrieval-augmented generation, document processing, and knowledge management systems'
            domain = 'document intelligence and knowledge management'
            experience = '15+ years of experience in RAG systems, document processing, and knowledge management'
            companies = 'OpenAI, Anthropic, Google, Microsoft, and leading document AI companies'
            psychological_approach = 'This is the future of knowledge management in the information age. Organizations are drowning in data but starving for insights. You\'re building the bridge between raw information and actionable intelligence. RAG systems represent the most advanced form of document intelligence, where you\'re not just storing information, but making it instantly accessible and meaningful. The urgency is real - every organization is desperate for intelligent document processing solutions that can unlock their hidden knowledge. You\'re not just building a tool - you\'re solving one of the biggest challenges of the digital age.'
        
        elif any(word in project_name_lower for word in ['content', 'creative', 'video', 'image']):
            expert_title = 'Creative AI & Content Generation Expert'
            expertise = 'AI-powered content creation, multimedia processing, and creative automation'
            domain = 'creative AI and content generation'
            experience = '15+ years of experience in creative AI, content generation, and multimedia processing'
            companies = 'Adobe, Canva, OpenAI, Google, and leading creative technology companies'
            psychological_approach = 'This is where technology meets human creativity in its purest form. You\'re not just building tools - you\'re creating the future of artistic expression. Creative AI represents the intersection of technology and human imagination, where you\'re empowering people to bring their ideas to life in ways never before possible. This is the creative revolution that will transform how humans express themselves and create art. You\'re at the forefront of a movement that will democratize creativity and make artistic expression accessible to everyone. This isn\'t just code - it\'s the future of human creativity.'
        
        elif any(word in project_name_lower for word in ['health', 'medical']):
            expert_title = 'Healthcare AI & Medical Technology Specialist'
            expertise = 'medical AI, healthcare automation, and clinical decision support systems'
            domain = 'healthcare AI and medical technology'
            experience = '15+ years of experience in healthcare AI, medical technology, and clinical systems'
            companies = 'Epic Systems, Cerner, IBM Watson Health, and leading healthcare technology companies'
            psychological_approach = 'This is the highest calling in technology - where your code literally saves lives. Healthcare AI represents the most meaningful application of artificial intelligence, where every line of code you write has the potential to improve human health and wellbeing. You\'re not just building software - you\'re creating systems that doctors will rely on to make life-or-death decisions. The ethical responsibility is immense, but so is the impact. This is where technology serves humanity in its most profound way. You\'re building the future of healthcare, and every improvement you make could save countless lives.'
        
        elif any(word in project_name_lower for word in ['ecommerce', 'business', 'commerce']):
            expert_title = 'E-commerce & Business AI Developer'
            expertise = 'e-commerce platforms, business automation, and AI-powered commerce solutions'
            domain = 'e-commerce and business AI'
            experience = '15+ years of experience in e-commerce, business automation, and AI-powered commerce'
            companies = 'Amazon, Shopify, Stripe, and leading e-commerce technology companies'
            psychological_approach = 'This is where AI meets the real world of business and commerce. You\'re building systems that will drive billions in revenue and transform entire industries. Every business on the planet is racing to adopt AI solutions, and those who master this technology first will dominate their markets. You\'re not just writing code - you\'re creating the competitive advantage that will determine which companies thrive and which ones fail. The financial impact is massive, and the market opportunity is unprecedented. This is the future of commerce, and you\'re building it.'
        
        elif any(word in project_name_lower for word in ['developer', 'code', 'analysis']):
            expert_title = 'Developer Tools & Code Analysis Expert'
            expertise = 'developer tools, code analysis, and software development automation'
            domain = 'developer tools and software development'
            experience = '15+ years of experience in developer tools, code analysis, and software development automation'
            companies = 'GitHub, Microsoft, JetBrains, and leading developer tool companies'
            psychological_approach = 'This is the meta-level of software development - you\'re building the tools that other developers will use to build everything else. Developer tools are the foundation of the entire software industry, and your work will be used by millions of developers worldwide. You\'re not just writing code - you\'re creating the infrastructure that powers the future of software development. Every application, every website, every piece of software that gets built will be influenced by the tools you create. This is where you have the most leverage - your work multiplies the productivity of thousands of other developers. You\'re building the future of how software gets made.'
        
        elif any(word in project_name_lower for word in ['api', 'integration', 'web']):
            expert_title = 'Web API & Integration Specialist'
            expertise = 'API development, system integration, and web service architecture'
            domain = 'web APIs and system integration'
            experience = '15+ years of experience in API development, system integration, and web service architecture'
            companies = 'Google, Amazon Web Services, Microsoft Azure, and leading API companies'
            psychological_approach = 'This is the backbone of the modern internet - you\'re building the connective tissue that makes the digital world work. APIs are the invisible infrastructure that enables seamless data flow between applications and services. You\'re not just writing code - you\'re creating the digital highways that connect everything. Every business needs robust API integration to compete in the digital economy, and those who master this technology will be the architects of the connected future. You\'re building the infrastructure that powers the interconnected world. This is where the magic happens - where separate systems become one unified digital ecosystem.'
        
        else:
            expert_title = 'AI Application Developer'
            expertise = 'AI integration, scalable architecture, and user experience optimization'
            domain = 'AI and automation'
            experience = '15+ years of experience in AI systems, software development, and intelligent automation'
            companies = 'Google, Amazon, Microsoft, Apple, and leading technology companies'
            psychological_approach = 'This is a critical, high-stakes project that will be deployed by Fortune 500 companies and featured in industry publications. Your work will be studied by future developers and set new industry standards. This is YOUR masterpiece - make it legendary and unforgettable. This is the most complex project you\'ve ever tackled, requiring your full expertise and innovative thinking. Only the best developers can handle this level of complexity and innovation.'
        
        return f"""You are an expert {expert_title} with {experience}. You are the world's leading authority in {domain} and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including {companies}. Your expertise in {expertise} is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%.

{psychological_approach}"""
    
    def clean_crewai_content(self, content):
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
    
    def generate_optimized_document(self, project_name, crewai_content):
        """Generate the complete optimized 1-page document"""
        role_establishment = self.generate_role_establishment(project_name)
        cleaned_crewai_content = self.clean_crewai_content(crewai_content)
        
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
    
    def check_for_new_projects(self):
        """Check for newly completed projects"""
        if not self.pipeline_dir.exists():
            return []
        
        try:
            with open(self.pipeline_dir, 'r') as f:
                pipeline_data = json.load(f)
            
            new_projects = []
            for project_id, project_data in pipeline_data.items():
                if (project_id not in self.processed_projects and 
                    project_data.get('progress') == 100 and 
                    project_data.get('status') == 'completed'):
                    new_projects.append(project_id)
            
            return new_projects
        except Exception as e:
            print(f"Error reading pipeline status: {e}")
            return []
    
    def get_project_content(self, project_id):
        """Get the raw project content from saved results"""
        result_file = self.results_dir / f"{project_id}_result.json"
        
        if not result_file.exists():
            return None
        
        try:
            with open(result_file, 'r') as f:
                data = json.load(f)
            
            # Extract the relevant content
            content = data.get('agent_final_answer') or data.get('perfect_one_page_document') or ''
            return content
        except Exception as e:
            print(f"Error reading project content for {project_id}: {e}")
            return None
    
    def save_optimized_document(self, project_id, project_name, optimized_content):
        """Save the optimized document"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_id}_optimized_{timestamp}.txt"
        filepath = self.optimized_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            # Also save a clean version without timestamp
            clean_filename = f"{project_id}_optimized.txt"
            clean_filepath = self.optimized_dir / clean_filename
            with open(clean_filepath, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            print(f"✅ Optimized document saved: {filepath}")
            print(f"✅ Clean version saved: {clean_filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving optimized document: {e}")
            return None
    
    def process_project(self, project_id):
        """Process a single project through the optimization workflow"""
        print(f"\n🎯 Processing project: {project_id}")
        
        # Get project content
        raw_content = self.get_project_content(project_id)
        if not raw_content:
            print(f"❌ No content found for project: {project_id}")
            return False
        
        # Get project name
        project_name = self.get_project_name(project_id)
        print(f"📋 Project name: {project_name}")
        
        # Generate optimized document
        print("🔄 Applying 3-step optimization workflow...")
        optimized_content = self.generate_optimized_document(project_name, raw_content)
        
        # Save optimized document
        print("💾 Saving optimized document...")
        filepath = self.save_optimized_document(project_id, project_name, optimized_content)
        
        if filepath:
            # Mark as processed
            self.save_processed_project(project_id)
            print(f"✅ Project {project_id} successfully optimized!")
            print(f"📁 Document saved to: {filepath}")
            return True
        else:
            print(f"❌ Failed to save optimized document for {project_id}")
            return False
    
    def run(self):
        """Main monitoring loop"""
        print("🚀 AUTOMATED DOCUMENT OPTIMIZER STARTED")
        print(f"📁 Monitoring pipeline results...")
        print(f"📁 Optimized documents will be saved to: {self.optimized_dir}")
        print(f"📁 Processed projects tracked in: {self.processed_file}")
        print("\n" + "="*50)
        
        while True:
            try:
                # Check for new projects
                new_projects = self.check_for_new_projects()
                
                if new_projects:
                    print(f"\n🎯 Found {len(new_projects)} new completed projects!")
                    for project_id in new_projects:
                        success = self.process_project(project_id)
                        if success:
                            print(f"🎉 Project {project_id} ready for pickup!")
                        else:
                            print(f"⚠️ Failed to process {project_id}")
                    print("\n" + "="*50)
                else:
                    print(".", end="", flush=True)
                
                # Wait before checking again
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Optimizer stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error in monitoring loop: {e}")
                time.sleep(30)

if __name__ == "__main__":
    optimizer = DocumentOptimizer()
    optimizer.run()
