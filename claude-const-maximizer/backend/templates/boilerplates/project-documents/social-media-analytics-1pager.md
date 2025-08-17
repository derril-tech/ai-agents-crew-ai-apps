# AI-Powered Social Media Analytics Platform

## 🎯 OBJECTIVE
Build a comprehensive social media analytics platform that provides real-time social media monitoring, sentiment analysis, trend tracking, and AI-powered content optimization. Target social media managers, marketing teams, and businesses who need advanced social media insights and performance tracking.

## 👥 TARGET USERS
**Primary**: Social media managers, marketing teams, brand managers, and content creators
**Needs**: Social media performance tracking, sentiment analysis, content optimization, and competitor monitoring
**Pain Points**: Manual social media tracking is time-consuming, insights are fragmented, content performance is unpredictable

## 🛠️ TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS + Radix UI components
- **Social Media Charts**: Recharts + ApexCharts for social data visualization
- **Real-time Updates**: WebSocket connections for live social media data
- **Word Clouds**: React Wordcloud for trending topics visualization
- **Responsive Design**: Mobile-first approach for social media managers

### Backend Stack
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with TimescaleDB for social media time-series data
- **Real-time Data**: WebSocket server for live social media updates
- **AI Integration**: OpenAI GPT-4 + Anthropic Claude for sentiment analysis
- **Social APIs**: Twitter, Facebook, Instagram, LinkedIn integration
- **Caching**: Redis for performance optimization

### Key Integrations
- **OpenAI API**: Content optimization and trend analysis
- **Anthropic Claude**: Sentiment analysis and brand monitoring
- **Twitter API**: Twitter data integration and monitoring
- **Facebook Graph API**: Facebook and Instagram data
- **LinkedIn API**: LinkedIn professional network data
- **Clerk**: Secure social media manager authentication

## 🎨 UX PATTERNS

### 1. Social Media Dashboard Interface
- **Real-time social media monitoring** with platform-specific metrics
- **Sentiment analysis** with color-coded sentiment indicators
- **Trend tracking** with word clouds and hashtag analysis
- **Mobile-responsive** design for social media managers on-the-go

### 2. Content Analytics Interface
- **Content performance** tracking across all platforms
- **Engagement metrics** with detailed breakdowns
- **Audience insights** with demographic analysis
- **Content optimization** recommendations from AI

### 3. Competitor Analysis Interface
- **Competitor monitoring** with performance comparisons
- **Brand mention tracking** with sentiment analysis
- **Market share analysis** with trend visualization
- **Opportunity identification** with AI insights

## 🔗 INTEGRATIONS

### Core APIs
- **OpenAI GPT-4**: Content optimization and trend prediction
- **Anthropic Claude**: Sentiment analysis and brand monitoring
- **Twitter API v2**: Twitter data and engagement metrics
- **Facebook Graph API**: Facebook and Instagram insights

### Social Media Platforms
- **Instagram Basic Display API**: Instagram content and engagement
- **LinkedIn Marketing API**: LinkedIn professional insights
- **YouTube Data API**: YouTube video performance
- **TikTok API**: TikTok trending content and metrics

### Analytics Tools
- **Google Analytics**: Website traffic from social media
- **Hootsuite API**: Social media management integration
- **Buffer API**: Social media scheduling and analytics
- **Sprout Social API**: Advanced social media analytics

## 📊 SUCCESS METRICS
1. **Engagement Rate**: 30% increase in social media engagement
2. **Content Performance**: 25% improvement in content reach
3. **Brand Sentiment**: 40% improvement in positive sentiment
4. **Time Efficiency**: 50% reduction in social media management time

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
    "NEXT_PUBLIC_TWITTER_CLIENT_ID": "${TWITTER_CLIENT_ID}",
    "NEXT_PUBLIC_FACEBOOK_APP_ID": "${FACEBOOK_APP_ID}"
  }
}
```

### Render Configuration
```yaml
services:
  - type: web
    name: social-media-analytics-api
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
      - key: TWITTER_BEARER_TOKEN
        value: ${TWITTER_BEARER_TOKEN}
      - key: FACEBOOK_ACCESS_TOKEN
        value: ${FACEBOOK_ACCESS_TOKEN}
      - key: REDIS_URL
        value: ${REDIS_URL}
```

### Environment Variables
```bash
# Frontend (Vercel)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_BASE_URL=https://social-media-analytics-api.onrender.com
NEXT_PUBLIC_TWITTER_CLIENT_ID=...
NEXT_PUBLIC_FACEBOOK_APP_ID=...

# Backend (Render)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
TWITTER_BEARER_TOKEN=...
FACEBOOK_ACCESS_TOKEN=...
INSTAGRAM_ACCESS_TOKEN=...
LINKEDIN_ACCESS_TOKEN=...
REDIS_URL=redis://...
CLERK_SECRET_KEY=sk_test_...
```

## 🎯 CLAUDE PROMPT OPTIMIZATION

### Prompt 1: Backend Architecture
"Create the FastAPI backend for the AI-Powered Social Media Analytics Platform with social media monitoring, sentiment analysis, and trend tracking endpoints. Include Twitter, Facebook, and Instagram API integration."

### Prompt 2: Frontend Implementation
"Build the Next.js frontend with social media dashboard, sentiment analysis, and content analytics interface. Include real-time charts and word cloud visualizations."

### Prompt 3: AI Integration & Polish
"Integrate the AI sentiment analysis system, add social media platform integrations, and implement the complete social media analytics experience with content optimization and brand monitoring."

---

**This 1-page document provides Claude with everything needed to build a production-ready AI-Powered Social Media Analytics Platform in exactly 3 prompts!** 🚀
