# Website Content Refresher

## 🎯 OBJECTIVE
Build a comprehensive content generation platform that provides AI-powered automation, intelligent analysis, and advanced capabilities. Target organizations and users who need content generation solutions for improved efficiency and productivity.

## 👥 TARGET USERS
**Primary**: Organizations, professionals, and users requiring content generation solutions
**Needs**: AI-powered automation, intelligent analysis, and advanced capabilities
**Pain Points**: Manual processes, inefficient workflows, lack of intelligent automation

## 🛠️ TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS + Radix UI components
- **AI Tools**: content generation specific components and interfaces
- **Real-time Updates**: WebSocket connections for live data
- **Integration**: React components for content generation functionality
- **Responsive Design**: Mobile-first approach for accessibility

### Backend Stack
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with specialized extensions
- **Real-time Data**: WebSocket server for live updates
- **AI Integration**: OpenAI GPT-4 + Anthropic Claude for content generation analysis
- **Specialized Processing**: content generation specific processing pipeline
- **Caching**: Redis for performance optimization

### Key Integrations
- **OpenAI API**: content generation analysis and processing
- **Anthropic Claude**: Intelligent insights and automation
- **Specialized APIs**: content generation specific integrations
- **Data Sources**: content generation relevant data and services
- **Clerk**: Secure authentication and user management

## 🎨 UX PATTERNS

### 1. Main Interface
- **Intuitive dashboard** with content generation specific metrics
- **Real-time monitoring** with live data updates
- **User-friendly controls** for content generation operations
- **Responsive design** for all device types

### 2. AI Integration Interface
- **Intelligent analysis** with AI-powered insights
- **Automated processing** with smart workflows
- **User feedback** with interactive elements
- **Progress tracking** with real-time status

### 3. Management Interface
- **Comprehensive management** of content generation operations
- **Data visualization** with charts and analytics
- **Configuration options** for customization
- **Reporting tools** for insights and analysis

## 🔗 INTEGRATIONS

### Core APIs
- **OpenAI GPT-4**: content generation analysis and processing
- **Anthropic Claude**: Intelligent automation and insights
- **Specialized Services**: content generation specific integrations
- **Data Sources**: Relevant data and information services

### Content Generation Specific
- **Content Generation APIs**: Specialized integrations and services
- **Data Processing**: content generation specific data handling
- **Analytics**: content generation focused analytics and reporting
- **Automation**: content generation workflow automation

### Business Intelligence
- **Google BigQuery**: Large-scale content generation analytics
- **Tableau**: Advanced visualization and insights
- **Power BI**: Microsoft content generation analytics
- **Looker**: Data exploration and business intelligence

## 📊 SUCCESS METRICS
1. **Efficiency**: 50% improvement in content generation processes
2. **Accuracy**: 90% improvement in content generation accuracy
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
    "NEXT_PUBLIC_CONTENT_GENERATION_PLATFORM": "${PLATFORM_KEY}"
  }
}
```

### Render Configuration
```yaml
services:
  - type: web
    name: website-content-refresher-api
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
NEXT_PUBLIC_API_BASE_URL=https://website-content-refresher-api.onrender.com
NEXT_PUBLIC_CONTENT_GENERATION_PLATFORM=...

# Backend (Render)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
REDIS_URL=redis://...
CLERK_SECRET_KEY=sk_test_...
```

## 🎯 CLAUDE PROMPT OPTIMIZATION

### Prompt 1: Backend Architecture
"Create the FastAPI backend for the Website Content Refresher with content generation specific endpoints and integrations. Include AI processing and specialized functionality."

### Prompt 2: Frontend Implementation
"Build the Next.js frontend with content generation specific interface, components, and user experience. Include real-time updates and responsive design."

### Prompt 3: AI Integration & Polish
"Integrate the AI content generation system, add specialized integrations, and implement the complete content generation platform experience with intelligent automation and insights."

---

**This 1-page document provides Claude with everything needed to build a production-ready Website Content Refresher in exactly 3 prompts!** 🚀
