"""
Claude Coder Agent
Responsible for Step 4 of Phase 3: Code generation using 5-prompt development plan
"""

import asyncio
from typing import Dict, Any, List
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from templates.design_archetypes import generate_design_instructions
from templates.backend_archetypes import generate_backend_instructions

load_dotenv()

class ClaudeCoder:
    """Claude Coder agent for generating complete application code"""
    
    # DEBUG MODE: Set to True for faster testing with minimal iterations
    DEBUG_MODE = True  # Set to False for full code generation
    
    def __init__(self):
        # Check for required API keys - try multiple options
        openai_api_key = os.getenv("OPENAI_API_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        deep_ai_api_key = os.getenv("DEEP_AI_API_KEY")
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        
        # Initialize LLMs with proper error handling
        self.primary_llm = None
        self.backup_llms = []
        
        # Primary LLM (DeepSeek - more cost-effective for debugging)
        if openai_api_key:
            try:
                self.primary_llm = ChatOpenAI(
                    model="deepseek-chat",
                    temperature=0.2,
                    openai_api_key=openai_api_key,
                    base_url="https://api.deepseek.com/v1"
                )
                print("  ✅ DeepSeek primary LLM configured for Claude Coder")
            except Exception as e:
                print(f"  ⚠️ Failed to configure DeepSeek: {e}")
        else:
            print("  ⚠️ OPENAI_API_KEY not found - DeepSeek not available")
        
        # Add Gemini if API key is available
        if google_api_key:
            try:
                gemini_llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",  # Updated model name
                    temperature=0.1,
                    google_api_key=google_api_key
                )
                self.backup_llms.append(gemini_llm)
                print("  ✅ Gemini Pro backup LLM configured")
            except Exception as e:
                print(f"  ⚠️ Failed to configure Gemini Pro: {e}")
        else:
            print("  ⚠️ GOOGLE_API_KEY/GEMINI_API_KEY not found - Gemini Pro not available")
        
        # Add Hugging Face if API key is available
        if huggingface_api_key:
            try:
                from langchain_huggingface import ChatHuggingFace
                huggingface_llm = ChatHuggingFace(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    temperature=0.1,
                    huggingfacehub_api_token=huggingface_api_key,
                    task="text-generation"  # Added required field
                )
                self.backup_llms.append(huggingface_llm)
                print("  ✅ Hugging Face LLM configured for Claude Coder")
            except Exception as e:
                print(f"  ⚠️ Failed to configure Hugging Face: {e}")
        else:
            print("  ⚠️ HUGGINGFACE_API_KEY not found - Hugging Face not available")
        
        # Add Mistral if API key is available
        if mistral_api_key:
            try:
                from langchain_community.chat_models import ChatOpenAI
                mistral_llm = ChatOpenAI(
                    model="mistral-large-latest",
                    temperature=0.1,
                    openai_api_key=mistral_api_key,
                    base_url="https://api.mistral.ai/v1"
                )
                self.backup_llms.append(mistral_llm)
                print("  ✅ Mistral LLM configured for Claude Coder")
            except Exception as e:
                print(f"  ⚠️ Failed to configure Mistral: {e}")
        else:
            print("  ⚠️ MISTRAL_API_KEY not found - Mistral not available")
        
        # Add GPT-3.5 as backup if OpenAI key is available
        if openai_api_key:
            try:
                gpt_llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=openai_api_key
                )
                self.backup_llms.append(gpt_llm)
                print("  ✅ GPT-3.5 Turbo backup LLM configured")
            except Exception as e:
                print(f"  ⚠️ Failed to configure GPT-3.5 Turbo: {e}")
        
        # Check if we have any working LLMs
        if not self.primary_llm and not self.backup_llms:
            print("  ❌ No LLMs available! Please set one of: OPENAI_API_KEY, GEMINI_API_KEY, HUGGINGFACE_API_KEY, MISTRAL_API_KEY")
            raise ValueError("No LLMs available for Claude Coder")
        
        # Set primary LLM to first available backup if primary failed
        if not self.primary_llm and self.backup_llms:
            self.primary_llm = self.backup_llms[0]
            self.backup_llms = self.backup_llms[1:]
            print("  ✅ Using backup LLM as primary")
        
        print(f"  ✅ Claude Coder: {len(self.backup_llms) + 1} LLM(s) configured")
        
        self.current_llm_index = 0
    
    async def generate_complete_application(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate complete application code using 5-prompt development plan"""
        
        print(f"🚀 Starting code generation for {project_name}")
        
        # In debug mode, use fewer prompts for faster testing
        if self.DEBUG_MODE:
            print("  ⚙️ DEBUG_MODE: Using minimal prompts for faster testing")
            prompts_to_run = [
                ("Backend Architecture", self._prompt1_backend_architecture),
                ("Frontend Implementation", self._prompt2_frontend_implementation)
            ]
        else:
            print("  🔄 Using full 5-prompt development plan")
            prompts_to_run = [
                ("Backend Architecture", self._prompt1_backend_architecture),
                ("Frontend Implementation", self._prompt2_frontend_implementation),
                ("Integration & API", self._prompt3_integration_connections),
                ("Deployment & DevOps", self._prompt4_deployment_configuration),
                ("Final Polish & Testing", self._prompt5_final_polish)
            ]
        
        all_code = {}
        
        for section_name, prompt_func in prompts_to_run:
            print(f"\n📝 Generating {section_name}...")
            
            # Handle different parameter requirements
            if section_name == "Backend Architecture":
                result = await self._generate_with_fallback(
                    section_name, 
                    lambda: prompt_func(project_name, project_brief, prompt_template, market_research)
                )
            elif section_name == "Frontend Implementation":
                # Pass backend_code from previous step
                backend_code = all_code.get("backend", {})
                result = await self._generate_with_fallback(
                    section_name, 
                    lambda: prompt_func(project_name, project_brief, prompt_template, market_research, backend_code)
                )
            else:
                result = await self._generate_with_fallback(
                    section_name, 
                    lambda: prompt_func(project_name, project_brief, prompt_template, market_research)
                )
            
            all_code.update(result)
            
            # In debug mode, add a small delay between prompts
            if self.DEBUG_MODE:
                await asyncio.sleep(1)
        
        print(f"\n✅ Code generation completed for {project_name}")
        return all_code
    
    async def _generate_with_fallback(self, section_name: str, prompt_func) -> Dict[str, str]:
        """Generate code with LLM fallback system"""
        
        try:
            print(f"  🔄 Generating with primary LLM for {section_name}...")
            result = await prompt_func()
            
            # Check if we got actual files (not just fallback)
            if self._has_real_files(result):
                print(f"  ✅ Primary LLM succeeded for {section_name}")
                return result
            else:
                print(f"  ⚠️ Primary LLM created fallback for {section_name}, trying backup...")
                
        except Exception as e:
            print(f"  ❌ Primary LLM failed for {section_name}: {e}")
        
        # Try backup LLMs
        backup_names = []
        if len(self.backup_llms) >= 2:
            backup_names = ["Gemini Pro", "GPT-3.5 Turbo"]
        elif len(self.backup_llms) == 1:
            backup_names = ["GPT-3.5 Turbo"]
        
        for i, backup_llm in enumerate(self.backup_llms):
            try:
                print(f"  🔄 Trying backup LLM {i+1} ({backup_names[i]}) for {section_name}...")
                
                # Temporarily switch to backup LLM
                original_llm = self.primary_llm
                self.primary_llm = backup_llm
                
                result = await prompt_func()
                
                # Restore primary LLM
                self.primary_llm = original_llm
                
                if self._has_real_files(result):
                    print(f"  ✅ Backup LLM {i+1} ({backup_names[i]}) succeeded for {section_name}")
                    return result
                else:
                    print(f"  ⚠️ Backup LLM {i+1} ({backup_names[i]}) also created fallback for {section_name}")
                    
            except Exception as e:
                print(f"  ❌ Backup LLM {i+1} ({backup_names[i]}) failed for {section_name}: {e}")
                # Restore primary LLM if we switched it
                if hasattr(self, 'original_llm'):
                    self.primary_llm = self.original_llm
            
            # In debug mode, limit to first backup LLM only
            if self.DEBUG_MODE:
                print("  ⚙️ DEBUG_MODE: Limiting to first backup LLM only")
                break
        
        # If all LLMs failed, return the last result (even if it's a fallback)
        print(f"  🚨 All LLMs failed for {section_name}, using last result")
        if 'result' in locals():
            return result
        else:
            # Create a minimal fallback if no result was generated
            return {f"{section_name}_fallback.txt": f"Failed to generate {section_name} code"}
    
    def _has_real_files(self, result: Dict[str, str]) -> bool:
        """Check if the result contains real files (not just fallbacks)"""
        if not result:
            return False
        
        # Check if we have any files that aren't fallbacks
        for filename in result.keys():
            if not filename.endswith('_fallback.txt'):
                return True
        
        return False
    
    async def _prompt1_backend_architecture(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any]
    ) -> Dict[str, str]:
        """Prompt 1: Backend architecture and API design"""
        
        prompt = f"""
        You are a senior backend architect. Create a complete backend implementation for the following project:

        PROJECT: {project_name}
        PROJECT BRIEF: {project_brief}
        APP TYPE: {prompt_template.get('app_type', 'CRUD')}
        TECH STACK: {prompt_template.get('tech_stack', '')}
        KEY FEATURES: {prompt_template.get('key_features', '')}

        MARKET RESEARCH CONTEXT:
        - Target Audience: {market_research.get('target_audience', '')}
        - API Sources: {market_research.get('api_sources', '')}
        - Data Sources: {market_research.get('data_sources', '')}

        BACKEND ARCHITECTURE INSTRUCTIONS:
        {generate_backend_instructions(prompt_template.get('app_type', 'CRUD'))}

        REQUIREMENTS:
        1. Follow the specified backend archetype and architecture pattern
        2. Implement all core features listed in the archetype
        3. Use the recommended database with proper configuration
        4. Add all specified integrations and third-party services
        5. Implement proper authentication and authorization
        6. Design RESTful API endpoints with comprehensive documentation
        7. Include database models, migrations, and seed data
        8. Add proper error handling, validation, and logging
        9. Include environment configuration and deployment setup
        10. Add comprehensive testing (unit, integration, API tests)

        OUTPUT FORMAT:
        You MUST use this EXACT format for each file:

        **File:** main.py
        ```python
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="Code Review API")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/")
        async def root():
            return {{"message": "Code Review API is running"}}
        
        @app.get("/health")
        async def health_check():
            return {{"status": "healthy"}}
        ```

        **File:** database.py
        ```python
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        SQLALCHEMY_DATABASE_URL = "sqlite:///./code_review.db"
        
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        Base = declarative_base()
        
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        ```

        Include these essential files:
        - main.py (FastAPI app entry point)
        - database.py (database configuration)
        - models.py (SQLAlchemy models)
        - schemas.py (Pydantic schemas)
        - auth.py (authentication logic)
        - routers/ (API route modules)
        - requirements.txt
        - .env.example
        - README.md

        Focus on production-ready, scalable architecture.
        """
        
        response = await self._generate_code_response(prompt)
        return self._parse_code_files(response, "backend")
    
    async def _prompt2_frontend_implementation(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any],
        backend_code: Dict[str, str]
    ) -> Dict[str, str]:
        """Prompt 2: Frontend UI/UX implementation"""
        
        # Extract backend API endpoints for frontend integration
        api_endpoints = self._extract_api_endpoints(backend_code)
        
        prompt = f"""
        You are a senior frontend developer. Create a complete frontend implementation for the following project:

        PROJECT: {project_name}
        PROJECT BRIEF: {project_brief}
        APP TYPE: {prompt_template.get('app_type', 'CRUD')}
        TECH STACK: {prompt_template.get('tech_stack', '')}
        KEY FEATURES: {prompt_template.get('key_features', '')}

        BACKEND API ENDPOINTS:
        {api_endpoints}

        MARKET RESEARCH CONTEXT:
        - Target Audience: {market_research.get('target_audience', '')}
        - Key Features: {market_research.get('key_features', '')}

        DESIGN INSTRUCTIONS:
        {generate_design_instructions(prompt_template.get('app_type', 'CRUD'))}

        REQUIREMENTS:
        1. Use Next.js 14 with TypeScript
        2. Implement project-specific design system (see DESIGN INSTRUCTIONS below)
        3. Add proper authentication integration
        4. Create reusable components
        5. Include proper error handling and loading states
        6. Add form validation and user feedback
        7. Ensure accessibility and SEO optimization
        8. Follow the exact design archetype specifications

        OUTPUT FORMAT:
        You MUST use this EXACT format for each file:

        **File:** package.json
        ```json
        {{
          "name": "ai-code-review",
          "version": "1.0.0",
          "scripts": {{
            "dev": "next dev",
            "build": "next build",
            "start": "next start"
          }},
          "dependencies": {{
            "next": "14.0.0",
            "react": "18.0.0",
            "react-dom": "18.0.0"
          }}
        }}
        ```

        **File:** app/layout.tsx
        ```tsx
        import React from 'react';
        import './globals.css';
        
        export default function RootLayout({{
          children,
        }}: {{
          children: React.ReactNode;
        }}) {{
          return (
            <html lang="en">
              <body className="min-h-screen" style={{{{ backgroundColor: 'var(--background-color)' }}}}>
                <div className="container mx-auto px-4 py-8">
                  {{children}}
                </div>
              </body>
            </html>
          );
        }}
        ```

        **File:** app/globals.css
        ```css
        @tailwind base;
        @tailwind components;
        @tailwind utilities;

        /* Design System CSS Variables */
        :root {{
          /* Color Scheme - Update these based on design archetype */
          --primary-color: #2563eb;
          --secondary-color: #64748b;
          --accent-color: #0ea5e9;
          --success-color: #10b981;
          --warning-color: #f59e0b;
          --error-color: #ef4444;
          --background-color: #f8fafc;
          --surface-color: #ffffff;
          --text-primary: #1e293b;
          --text-secondary: #64748b;
        }}

        /* Typography */
        body {{
          font-family: 'Inter', system-ui, sans-serif;
          color: var(--text-primary);
          background-color: var(--background-color);
        }}

        h1, h2, h3, h4, h5, h6 {{
          font-family: 'Inter', system-ui, sans-serif;
          font-weight: 600;
          color: var(--text-primary);
        }}

        /* Component Styles */
        .btn-primary {{
          background-color: var(--primary-color);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 0.375rem;
          font-weight: 500;
          transition: all 0.2s;
        }}

        .btn-primary:hover {{
          background-color: var(--accent-color);
        }}

        .card {{
          background-color: var(--surface-color);
          border-radius: 0.5rem;
          box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
          padding: 1.5rem;
        }}
        ```

        **File:** app/page.tsx
        ```tsx
        'use client';
        
        import React, {{ useState, useEffect }} from 'react';
        import CodeReviewDashboard from '../components/CodeReviewDashboard';
        import Header from '../components/Header';
        
        export default function CodeReviewPage() {{
          const [reviews, setReviews] = useState([]);
          const [loading, setLoading] = useState(true);
          
          useEffect(() => {{
            // Fetch code reviews from API
            fetch('/api/reviews')
              .then(res => res.json())
              .then(data => {{
                setReviews(data);
                setLoading(false);
              }})
              .catch(err => {{
                console.error('Error fetching reviews:', err);
                setLoading(false);
              }});
          }}, []);
          
          return (
            <div className="min-h-screen bg-gray-50">
              <Header />
              <main className="container mx-auto px-4 py-8">
                <CodeReviewDashboard reviews={{reviews}} loading={{loading}} />
              </main>
            </div>
          );
        }}
        ```

        **File:** components/Header.tsx
        ```tsx
        import React from 'react';
        
        export default function Header() {{
          return (
            <header className="shadow-sm border-b" style={{{{ backgroundColor: 'var(--surface-color)' }}}}>
              <div className="container mx-auto px-4 py-4">
                <h1 className="text-2xl font-bold" style={{{{ color: 'var(--text-primary)' }}}}>
                  AI Code Review Assistant
                </h1>
                <p className="mt-1" style={{{{ color: 'var(--text-secondary)' }}}}>
                  Automated code analysis and refactoring suggestions
                </p>
              </div>
            </header>
          );
        }}
        ```

        **File:** components/CodeReviewDashboard.tsx
        ```tsx
        import React from 'react';
        
        interface Review {{
          id: string;
          title: string;
          status: 'pending' | 'completed' | 'error';
          score: number;
          suggestions: string[];
        }}
        
        interface Props {{
          reviews: Review[];
          loading: boolean;
        }}
        
        export default function CodeReviewDashboard({{ reviews, loading }}: Props) {{
          if (loading) {{
            return (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-2 text-gray-600">Loading reviews...</span>
              </div>
            );
          }}
          
          return (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-900">Code Reviews</h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                  New Review
                </button>
              </div>
              
              <div className="grid gap-4">
                {{reviews.map((review) => (
                  <div key={{review.id}} className="bg-white p-6 rounded-lg shadow-sm border">
                    <div className="flex justify-between items-start">
                      <h3 className="text-lg font-medium text-gray-900">{{review.title}}</h3>
                      <span className="px-2 py-1 rounded-full text-sm bg-gray-100 text-gray-800">
                        {{review.status}}
                      </span>
                    </div>
                    <div className="mt-2">
                      <span className="text-sm text-gray-600">Score: {{review.score}}/100</span>
                    </div>
                    {{review.suggestions.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Suggestions:</h4>
                        <ul className="space-y-1">
                          {{review.suggestions.map((suggestion, index) => (
                            <li key={{index}} className="text-sm text-gray-600">• {{suggestion}}</li>
                          ))}}
                        </ul>
                      </div>
                    )}}
                  </div>
                ))}}
              </div>
            </div>
          );
        }}
        ```

        Include these essential files:
        - package.json
        - next.config.js
        - tailwind.config.js
        - app/layout.tsx
        - app/page.tsx
        - components/ (reusable UI components)
        - lib/ (utilities and hooks)
        - types/ (TypeScript definitions)
        - README.md

        Focus on modern, user-friendly interface design with functional components.
        """
        
        response = await self._generate_code_response(prompt)
        return self._parse_code_files(response, "frontend")
    
    async def _prompt3_integration_connections(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any],
        backend_code: Dict[str, str],
        frontend_code: Dict[str, str]
    ) -> Dict[str, str]:
        """Prompt 3: Integration and API connections"""
        
        prompt = f"""
        You are a full-stack integration specialist. Create integration code to connect the frontend and backend:

        PROJECT: {project_name}
        PROJECT BRIEF: {project_brief}
        APP TYPE: {prompt_template.get('app_type', 'CRUD')}

        REQUIREMENTS:
        1. Create API client utilities for frontend
        2. Add proper error handling and retry logic
        3. Implement authentication flow
        4. Add data fetching hooks and state management
        5. Create middleware for API requests
        6. Add proper TypeScript types for API responses
        7. Implement real-time features if needed

        OUTPUT FORMAT:
        You MUST use this EXACT format for each file:

        **File:** lib/api-client.ts
        ```typescript
        import axios from 'axios';

        const apiClient = axios.create({{
          baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
          timeout: 10000,
          headers: {{
            'Content-Type': 'application/json',
          }},
        }});

        // Add request interceptor for auth
        apiClient.interceptors.request.use((config) => {{
          const token = localStorage.getItem('auth_token');
          if (token) {{
            config.headers.Authorization = `Bearer ${{token}}`;
          }}
          return config;
        }});

        export default apiClient;
        ```

        **File:** lib/auth.ts
        ```typescript
        import apiClient from './api-client';

        export interface User {{
          id: string;
          email: string;
          name: string;
        }}

        export const auth = {{
          async login(email: string, password: string): Promise<User> {{
            const response = await apiClient.post('/auth/login', {{ email, password }});
            const {{ token, user }} = response.data;
            localStorage.setItem('auth_token', token);
            return user;
          }},

          async logout(): Promise<void> {{
            localStorage.removeItem('auth_token');
          }},

          async getCurrentUser(): Promise<User | null> {{
            try {{
              const response = await apiClient.get('/auth/me');
              return response.data;
            }} catch {{
              return null;
            }}
          }},
        }};
        ```

        Include these essential files:
        - lib/api-client.ts (API client utilities)
        - lib/auth.ts (authentication utilities)
        - hooks/use-api.ts (custom hooks for API calls)
        - types/api.ts (API response types)
        - middleware.ts (Next.js middleware)

        Ensure seamless frontend-backend integration.
        """
        
        response = await self._generate_code_response(prompt)
        return self._parse_code_files(response, "integration")
    
    async def _prompt4_deployment_configuration(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any]
    ) -> Dict[str, str]:
        """Prompt 4: Deployment and configuration"""
        
        prompt = f"""
        You are a DevOps engineer. Create deployment configuration for the following project:

        PROJECT: {project_name}
        PROJECT BRIEF: {project_brief}
        APP TYPE: {prompt_template.get('app_type', 'CRUD')}

        REQUIREMENTS:
        1. Create Vercel deployment configuration for frontend
        2. Create Render deployment configuration for backend
        3. Add Docker configuration if needed
        4. Include environment variable templates
        5. Add CI/CD pipeline configuration
        6. Create database migration scripts
        7. Add monitoring and logging configuration

        OUTPUT FORMAT:
        You MUST use this EXACT format for each file:

        **File:** vercel.json
        ```json
        {{
          "version": 2,
          "builds": [
            {{
              "src": "package.json",
              "use": "@vercel/next"
            }}
          ],
          "env": {{
            "NEXT_PUBLIC_API_URL": "@api-url"
          }}
        }}
        ```

        **File:** render.yaml
        ```yaml
        services:
          - type: web
            name: ai-code-review-backend
            env: python
            buildCommand: pip install -r requirements.txt
            startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
            envVars:
              - key: PYTHON_VERSION
                value: 3.9.0
        ```

        **File:** Dockerfile
        ```dockerfile
        FROM python:3.9-slim

        WORKDIR /app

        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        COPY . .

        EXPOSE 8000

        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        ```

        Include these essential files:
        - vercel.json (Vercel configuration)
        - render.yaml (Render configuration)
        - Dockerfile (if needed)
        - docker-compose.yml (if needed)
        - .github/workflows/deploy.yml (GitHub Actions)
        - scripts/deploy.sh (deployment scripts)
        - .env.production.example

        Focus on production-ready deployment setup.
        """
        
        response = await self._generate_code_response(prompt)
        return self._parse_code_files(response, "deployment")
    
    async def _prompt5_final_polish(
        self, 
        project_name: str, 
        project_brief: str, 
        prompt_template: Dict[str, Any], 
        market_research: Dict[str, Any],
        backend_code: Dict[str, str],
        frontend_code: Dict[str, str],
        integration_code: Dict[str, str],
        deployment_code: Dict[str, str]
    ) -> Dict[str, str]:
        """Prompt 5: Final polish and testing"""
        
        prompt = f"""
        You are a senior software engineer. Perform final polish and add testing for the following project:

        PROJECT: {project_name}
        PROJECT BRIEF: {project_brief}
        APP TYPE: {prompt_template.get('app_type', 'CRUD')}

        REQUIREMENTS:
        1. Add comprehensive test suites
        2. Implement error boundaries and fallbacks
        3. Add performance optimizations
        4. Include security best practices
        5. Add comprehensive documentation
        6. Implement logging and monitoring
        7. Add accessibility improvements

        OUTPUT FORMAT:
        You MUST use this EXACT format for each file:

        **File:** .eslintrc.js
        ```javascript
        module.exports = {{
          extends: [
            'next/core-web-vitals',
            'eslint:recommended',
            '@typescript-eslint/recommended'
          ],
          rules: {{
            '@typescript-eslint/no-unused-vars': 'error',
            '@typescript-eslint/no-explicit-any': 'warn'
          }}
        }};
        ```

        **File:** jest.config.js
        ```javascript
        module.exports = {{
          testEnvironment: 'jsdom',
          setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
          testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/'],
          moduleNameMapping: {{
            '^@/(.*)$': '<rootDir>/$1'
          }}
        }};
        ```

        **File:** tests/api.test.ts
        ```typescript
        import apiClient from '../lib/api-client';

        describe('API Client', () => {{
          it('should create axios instance with correct config', () => {{
            expect(apiClient.defaults.baseURL).toBeDefined();
            expect(apiClient.defaults.timeout).toBe(10000);
          }});
        }});
        ```

        Include these essential files:
        - tests/ (test suites)
        - docs/ (documentation)
        - scripts/ (utility scripts)
        - .eslintrc.js (linting configuration)
        - jest.config.js (testing configuration)
        - README.md (comprehensive documentation)

        Focus on production quality and maintainability.
        """
        
        response = await self._generate_code_response(prompt)
        return self._parse_code_files(response, "final")
    
    async def _generate_code_response(self, prompt: str) -> str:
        """Generate code response from Claude"""
        
        messages = [
            SystemMessage(content="You are a senior software engineer. Generate complete, production-ready code files."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self.primary_llm.agenerate([messages])
            return response.generations[0][0].text
        except Exception as e:
            print(f"Code generation error: {e}")
            return f"Error generating code: {str(e)}"
    
    def _parse_code_files(self, response: str, section: str) -> Dict[str, str]:
        """Parse code files from Claude's response"""
        
        files = {}
        lines = response.split('\n')
        current_file = None
        current_content = []
        in_code_block = False
        
        for line in lines:
            # Check for code block markers
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block, save the file
                    if current_file and current_content:
                        files[current_file] = '\n'.join(current_content)
                    current_file = None
                    current_content = []
                    in_code_block = False
                else:
                    # Start of code block, look for filename
                    in_code_block = True
                    # Check if there's a filename after ```
                    code_block_line = line.strip()
                    if ':' in code_block_line:
                        # Extract filename from ```filename: or ```filename
                        filename = code_block_line.replace('```', '').split(':')[0].strip()
                        if filename and not filename.startswith('```'):
                            current_file = filename
                continue
            
            # Check for file path indicators
            if not in_code_block and (line.startswith('**File:**') or line.startswith('File:') or 
                                     line.startswith('**Filename:**') or line.startswith('Filename:') or
                                     line.startswith('**Path:**') or line.startswith('Path:')):
                # Save previous file
                if current_file and current_content:
                    files[current_file] = '\n'.join(current_content)
                
                # Extract file path
                file_path = (line.replace('**File:**', '').replace('File:', '')
                           .replace('**Filename:**', '').replace('Filename:', '')
                           .replace('**Path:**', '').replace('Path:', '').strip())
                if file_path:
                    current_file = file_path
                    current_content = []
                continue
            
            # Add content to current file
            if current_file and in_code_block:
                current_content.append(line)
            elif current_file and not in_code_block and line.strip():
                # If we have a current file but not in code block, still collect content
                current_content.append(line)
        
        # Save last file
        if current_file and current_content:
            files[current_file] = '\n'.join(current_content)
        
        # If no files were parsed, create a fallback
        if not files:
            print(f"Warning: No files parsed from {section} response. Creating fallback.")
            files[f"{section}_fallback.txt"] = response
        
        return files
    
    def _extract_api_endpoints(self, backend_code: Dict[str, str]) -> str:
        """Extract API endpoints from backend code for frontend integration"""
        
        endpoints = []
        
        # Look for router files and main.py
        for file_path, content in backend_code.items():
            if 'router' in file_path.lower() or 'main.py' in file_path:
                # Simple extraction of route patterns
                lines = content.split('\n')
                for line in lines:
                    if '@app.' in line or '@router.' in line:
                        endpoints.append(line.strip())
        
        return '\n'.join(endpoints[:10])  # Limit to first 10 endpoints
