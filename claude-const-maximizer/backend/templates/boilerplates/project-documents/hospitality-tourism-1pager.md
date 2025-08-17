# AI-Powered Hospitality & Tourism Platform

## 🎯 OBJECTIVE
Build a comprehensive hospitality and tourism platform that provides AI-powered guest experience optimization, revenue management, operational efficiency, and destination analytics. Target hotels, resorts, travel agencies, and tourism operators who need advanced hospitality analytics and guest experience optimization.

## 👥 TARGET USERS
**Primary**: Hotel managers, travel agents, tourism operators, and hospitality professionals
**Needs**: Guest experience optimization, revenue management, operational efficiency, and destination analytics
**Pain Points**: Manual guest service is inconsistent, revenue optimization is reactive, operational efficiency is low

## 🛠️ TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS + Radix UI components
- **Hospitality Tools**: Guest management, booking systems, revenue analytics
- **Real-time Updates**: WebSocket connections for live hospitality data
- **Map Integration**: React Map GL and Leaflet for destination visualization
- **Responsive Design**: Mobile-first approach for hospitality operations

### Backend Stack
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with TimescaleDB for hospitality time-series data
- **Real-time Data**: WebSocket server for live guest updates
- **AI Integration**: OpenAI GPT-4 + Anthropic Claude for guest experience optimization
- **Booking Systems**: Reservation management and availability tracking
- **Caching**: Redis for performance optimization

### Key Integrations
- **OpenAI API**: Guest experience optimization and personalization
- **Anthropic Claude**: Revenue management and operational insights
- **Booking APIs**: Reservation systems and availability management
- **Payment Systems**: Transaction processing and financial analytics
- **Review Platforms**: Guest feedback and sentiment analysis
- **Clerk**: Secure hospitality team authentication

## 🎨 UX PATTERNS

### 1. Guest Experience Interface
- **Personalized guest profiles** with AI-powered recommendations
- **Concierge services** with automated assistance
- **Room preferences** with smart automation
- **Guest communication** with multilingual support

### 2. Revenue Management Interface
- **Dynamic pricing** with AI-powered optimization
- **Demand forecasting** with predictive analytics
- **Channel management** with distribution optimization
- **Revenue analytics** with performance tracking

### 3. Operational Efficiency Interface
- **Staff scheduling** with AI-powered optimization
- **Inventory management** with automated tracking
- **Maintenance scheduling** with predictive alerts
- **Quality control** with automated monitoring

## 🔗 INTEGRATIONS

### Core APIs
- **OpenAI GPT-4**: Guest experience optimization and personalization
- **Anthropic Claude**: Revenue management and operational insights
- **Booking APIs**: Reservation systems and availability management
- **Payment Systems**: Transaction processing and financial analytics

### Hospitality Systems
- **PMS Integration**: Property management system connectivity
- **Channel Managers**: Distribution and booking channel management
- **Review Platforms**: Guest feedback and sentiment analysis
- **CRM Systems**: Customer relationship management

### Business Intelligence
- **Google BigQuery**: Large-scale hospitality analytics
- **Tableau**: Advanced hospitality visualization
- **Power BI**: Microsoft business analytics
- **Looker**: Data exploration and insights

## 📊 SUCCESS METRICS
1. **Guest Satisfaction**: 30% improvement in guest ratings
2. **Revenue Growth**: 25% increase in average daily rate
3. **Operational Efficiency**: 40% reduction in manual tasks
4. **Occupancy Rate**: 20% improvement in room utilization

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
    "NEXT_PUBLIC_MAPBOX_TOKEN": "${MAPBOX_TOKEN}"
  }
}
```

### Render Configuration
```yaml
services:
  - type: web
    name: hospitality-tourism-api
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
      - key: MAPBOX_TOKEN
        value: ${MAPBOX_TOKEN}
      - key: REDIS_URL
        value: ${REDIS_URL}
```

### Environment Variables
```bash
# Frontend (Vercel)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_BASE_URL=https://hospitality-tourism-api.onrender.com
NEXT_PUBLIC_MAPBOX_TOKEN=pk...

# Backend (Render)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MAPBOX_TOKEN=pk...
BOOKING_API_KEY=...
PAYMENT_API_KEY=...
PMS_API_KEY=...
REVIEW_API_KEY=...
REDIS_URL=redis://...
CLERK_SECRET_KEY=sk_test_...
```

## 🎯 CLAUDE PROMPT OPTIMIZATION

### Prompt 1: Backend Architecture
"Create the FastAPI backend for the AI-Powered Hospitality & Tourism Platform with guest experience management, revenue optimization, and operational efficiency endpoints. Include booking system integration and payment processing."

### Prompt 2: Frontend Implementation
"Build the Next.js frontend with guest experience dashboard, revenue management interface, and operational efficiency tools. Include map visualization and real-time hospitality data."

### Prompt 3: AI Integration & Polish
"Integrate the AI hospitality system, add booking and payment integrations, and implement the complete hospitality platform experience with guest personalization and revenue optimization."

---

**This 1-page document provides Claude with everything needed to build a production-ready AI-Powered Hospitality & Tourism Platform in exactly 3 prompts!** 🚀
