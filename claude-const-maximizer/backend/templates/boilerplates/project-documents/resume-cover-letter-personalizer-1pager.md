# Resume & Cover Letter Personalizer

## 🎯 OBJECTIVE
Build a comprehensive hr tech platform that provides AI-powered automation, intelligent analysis, and advanced capabilities. Target organizations and users who need hr tech solutions for improved efficiency and productivity.

## 👥 TARGET USERS
**Primary**: Organizations, professionals, and users requiring hr tech solutions
**Needs**: AI-powered automation, intelligent analysis, and advanced capabilities
**Pain Points**: Manual processes, inefficient workflows, lack of intelligent automation

## 🛠️ TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS + Radix UI components
- **AI Tools**: hr tech specific components and interfaces
- **Real-time Updates**: WebSocket connections for live data
- **Integration**: React components for hr tech functionality
- **Responsive Design**: Mobile-first approach for accessibility

### Backend Stack
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with specialized extensions
- **Real-time Data**: WebSocket server for live updates
- **AI Integration**: OpenAI GPT-4 + Anthropic Claude for hr tech analysis
- **Specialized Processing**: hr tech specific processing pipeline
- **Caching**: Redis for performance optimization

### Key Integrations
- **OpenAI API**: hr tech analysis and processing
- **Anthropic Claude**: Intelligent insights and automation
- **Specialized APIs**: hr tech specific integrations
- **Data Sources**: hr tech relevant data and services
- **Clerk**: Secure authentication and user management

## 🎨 UX PATTERNS

### 1. Main Interface
- **Intuitive dashboard** with hr tech specific metrics
- **Real-time monitoring** with live data updates
- **User-friendly controls** for hr tech operations
- **Responsive design** for all device types

### 2. AI Integration Interface
- **Intelligent analysis** with AI-powered insights
- **Automated processing** with smart workflows
- **User feedback** with interactive elements
- **Progress tracking** with real-time status

### 3. Management Interface
- **Comprehensive management** of hr tech operations
- **Data visualization** with charts and analytics
- **Configuration options** for customization
- **Reporting tools** for insights and analysis

## 🔗 INTEGRATIONS

### Core APIs
- **OpenAI GPT-4**: hr tech analysis and processing
- **Anthropic Claude**: Intelligent automation and insights
- **Specialized Services**: hr tech specific integrations
- **Data Sources**: Relevant data and information services

### HR Tech Specific
- **HR Tech APIs**: Specialized integrations and services
- **Data Processing**: hr tech specific data handling
- **Analytics**: hr tech focused analytics and reporting
- **Automation**: hr tech workflow automation

### Business Intelligence
- **Google BigQuery**: Large-scale hr tech analytics
- **Tableau**: Advanced visualization and insights
- **Power BI**: Microsoft hr tech analytics
- **Looker**: Data exploration and business intelligence

## 📊 SUCCESS METRICS
1. **Efficiency**: 50% improvement in hr tech processes
2. **Accuracy**: 90% improvement in hr tech accuracy
3. **Productivity**: 60% increase in user productivity
4. **Automation**: 80% reduction in manual tasks

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
    "NEXT_PUBLIC_API_BASE_URL": "${API_BASE_URL}",
    "NEXT_PUBLIC_HR_TECH_PLATFORM": "${PLATFORM_KEY}"
  }
}
```

### Render Configuration
```yaml
services:
  - type: web
    name: resume-cover-letter-personalizer-api
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
      - key: REDIS_URL
        value: ${REDIS_URL}
```

### Environment Variables
```bash
# Frontend (Vercel)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_BASE_URL=https://resume-cover-letter-personalizer-api.onrender.com
NEXT_PUBLIC_HR_TECH_PLATFORM=...

# Backend (Render)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
REDIS_URL=redis://...
CLERK_SECRET_KEY=sk_test_...
```

## 🎯 CLAUDE PROMPT OPTIMIZATION

### Prompt 1: Backend Architecture
"Create the FastAPI backend for the Resume & Cover Letter Personalizer with hr tech specific endpoints and integrations. Include AI processing and specialized functionality."

### Prompt 2: Frontend Implementation
"Build the Next.js frontend with hr tech specific interface, components, and user experience. Include real-time updates and responsive design."

### Prompt 3: AI Integration & Polish
"Integrate the AI hr tech system, add specialized integrations, and implement the complete hr tech platform experience with intelligent automation and insights."

---

**This 1-page document provides Claude with everything needed to build a production-ready Resume & Cover Letter Personalizer in exactly 3 prompts!** 🚀
