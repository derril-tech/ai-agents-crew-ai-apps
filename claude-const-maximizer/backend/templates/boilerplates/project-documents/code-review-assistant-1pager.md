# AI-Powered Code Review & Refactoring Assistant

## 🎯 OBJECTIVE
Build a comprehensive code analysis platform that automatically detects security vulnerabilities, performance issues, and provides AI-powered refactoring suggestions. Target developers and teams who need automated code quality assurance.

## 👥 TARGET USERS
**Primary**: Software developers, DevOps engineers, and development teams
**Needs**: Automated code review, security scanning, performance optimization, and refactoring suggestions
**Pain Points**: Manual code reviews are time-consuming, security vulnerabilities are missed, performance issues go undetected

## 🛠️ TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS + Radix UI components
- **Code Editor**: Monaco Editor with syntax highlighting
- **State Management**: React Query + Zustand
- **Authentication**: Clerk integration
- **File Upload**: UploadThing for code file handling

### Backend Stack
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: OpenAI GPT-4 + Anthropic Claude for code analysis
- **Security Scanning**: Bandit, Semgrep, Safety integration
- **Performance Analysis**: Custom AST parsing + memory profiling
- **File Processing**: Support for Python, JavaScript, TypeScript, Java, C++, Go, Rust

### Key Integrations
- **OpenAI API**: Code analysis and refactoring suggestions
- **Anthropic Claude**: Security vulnerability detection
- **GitHub API**: Repository integration and commit analysis
- **Clerk**: User authentication and team management
- **UploadThing**: Secure file upload and storage

## 🎨 UX PATTERNS

### 1. Code Editor Interface
- **Monaco Editor** with syntax highlighting and line numbers
- **Real-time analysis** with inline annotations
- **Tabbed interface** for Editor/Analysis/History views
- **File tree sidebar** for project navigation

### 2. Analysis Dashboard
- **Security Issues**: Red/yellow/green severity indicators
- **Performance Metrics**: Complexity, maintainability, testability scores
- **Refactoring Suggestions**: Before/after code comparisons
- **AI Insights**: Contextual improvement recommendations

### 3. Project Management
- **Repository Connection**: GitHub/GitLab integration
- **Team Collaboration**: Shared analysis results and comments
- **History Tracking**: Analysis history and trend visualization
- **Export Options**: PDF reports, JSON data, integration APIs

## 🔗 INTEGRATIONS

### Core APIs
- **OpenAI GPT-4**: Advanced code analysis and suggestions
- **Anthropic Claude**: Security-focused code review
- **GitHub API**: Repository access and commit analysis
- **Clerk**: Authentication and user management

### Security Tools
- **Bandit**: Python security scanning
- **Semgrep**: Multi-language security analysis
- **Safety**: Dependency vulnerability checking
- **Custom AST Parser**: Language-specific security patterns

### Performance Tools
- **Memory Profiler**: Memory usage analysis
- **Complexity Calculator**: Cyclomatic complexity measurement
- **Code Metrics**: Lines of code, function count, etc.
- **Optimization Detector**: Performance anti-patterns

## 📊 SUCCESS METRICS
1. **Detection Accuracy**: 95%+ vulnerability detection rate
2. **Performance Impact**: <2 second analysis time for typical files
3. **User Adoption**: 100+ active users within first month
4. **Code Quality Improvement**: 30% reduction in security issues

## 🚀 DEPLOYMENT

### Vercel Configuration
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": "${CLERK_PUBLISHABLE_KEY}",
    "NEXT_PUBLIC_UPLOADTHING_SECRET": "${UPLOADTHING_SECRET}",
    "NEXT_PUBLIC_API_BASE_URL": "${API_BASE_URL}"
  }
}
```

### Render Configuration
```yaml
services:
  - type: web
    name: code-review-assistant-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: ${DATABASE_URL}
      - key: OPENAI_API_KEY
        value: ${OPENAI_API_KEY}
      - key: ANTHROPIC_API_KEY
        value: ${ANTHROPIC_API_KEY}
```

### Environment Variables
```bash
# Frontend (Vercel)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_UPLOADTHING_SECRET=sk_live_...
NEXT_PUBLIC_API_BASE_URL=https://code-review-assistant-api.onrender.com

# Backend (Render)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
CLERK_SECRET_KEY=sk_test_...
UPLOADTHING_SECRET=sk_live_...
```

## 🎯 CLAUDE PROMPT OPTIMIZATION

### Prompt 1: Backend Architecture
"Create the FastAPI backend for the AI Code Review Assistant with code analysis, security scanning, and performance analysis endpoints. Include OpenAI and Anthropic integration for AI-powered insights."

### Prompt 2: Frontend Implementation  
"Build the Next.js frontend with Monaco Editor, analysis dashboard, and project management features. Include real-time code analysis and security vulnerability display."

### Prompt 3: AI Integration & Polish
"Integrate the AI analysis services, add file upload functionality, and implement the complete user experience with authentication and team collaboration features."

---

**This 1-page document provides Claude with everything needed to build a production-ready AI Code Review Assistant in exactly 3 prompts!** 🚀
