# Services Signup Checklist for 60 AI Apps

This checklist covers all third-party services needed for the 60 AI applications. Each service should be signed up for once and the API keys captured for reuse across all projects.

## 🔑 Core AI Services

### OpenAI
- **URL**: https://platform.openai.com/
- **Purpose**: GPT-4o for text generation, code analysis, and general AI tasks
- **API Key**: `sk-openai-...`
- **Cost**: Pay-per-use, starts at ~$0.01/1K tokens
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Anthropic (Claude)
- **URL**: https://console.anthropic.com/
- **Purpose**: Claude 3.7 Sonnet for research, analysis, and complex reasoning
- **API Key**: `sk-ant-...`
- **Cost**: Pay-per-use, starts at ~$0.003/1K tokens
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Google (Gemini) - Optional
- **URL**: https://makersuite.google.com/
- **Purpose**: Backup for multimodal needs (vision, audio)
- **API Key**: `AIza...`
- **Cost**: Free tier available
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 🔍 Research & Data Services

### Tavily
- **URL**: https://tavily.com/
- **Purpose**: Web search and research for Market Researcher agent
- **API Key**: `tvly-...`
- **Cost**: Free tier (100 searches/month), then $0.01/search
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### ScrapingAnt
- **URL**: https://scrapingant.com/
- **Purpose**: Robust web scraping for competitor analysis
- **API Key**: `scrapingant_...`
- **Cost**: Free tier (100 requests/month), then $0.01/request
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 🏗️ Infrastructure & Hosting

### Vercel
- **URL**: https://vercel.com/
- **Purpose**: Frontend hosting for all Next.js applications
- **Team ID**: `team_...` (optional, for team projects)
- **Token**: Generate in Account Settings → Tokens
- **Cost**: Free tier (100GB bandwidth, 100 serverless functions)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Render
- **URL**: https://render.com/
- **Purpose**: Backend hosting and PostgreSQL databases
- **API Key**: Generate in Account Settings → API Keys
- **Owner ID**: `usr-...` (found in API response)
- **Cost**: Free tier (750 hours/month for web services, 90 days for databases)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Cloudflare R2
- **URL**: https://dash.cloudflare.com/
- **Purpose**: File storage for documents, media, and assets
- **API Key**: Generate in R2 → Manage R2 API tokens
- **Account ID**: Found in dashboard
- **Cost**: $0.015/GB/month (cheaper than S3)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 🔐 Authentication & Security

### Clerk
- **URL**: https://clerk.com/
- **Purpose**: Authentication for user management
- **Publishable Key**: `pk_test_...`
- **Secret Key**: `sk_test_...`
- **Cost**: Free tier (5,000 monthly active users)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Auth.js (NextAuth) - Alternative
- **URL**: https://next-auth.js.org/
- **Purpose**: Self-hosted authentication (no external dependency)
- **Setup**: npm install next-auth
- **Cost**: Free (self-hosted)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 💰 Payments & Monetization

### Stripe
- **URL**: https://stripe.com/
- **Purpose**: Payment processing for monetized apps
- **Publishable Key**: `pk_test_...`
- **Secret Key**: `sk_test_...`
- **Cost**: 2.9% + $0.30 per transaction
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 📧 Communication & Notifications

### Resend
- **URL**: https://resend.com/
- **Purpose**: Email delivery for notifications and transactional emails
- **API Key**: `re_...`
- **Cost**: Free tier (3,000 emails/month), then $0.80/1K emails
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Pusher
- **URL**: https://pusher.com/
- **Purpose**: Real-time notifications and live updates
- **App ID**: `...`
- **Key**: `...`
- **Secret**: `...`
- **Cost**: Free tier (200K messages/day)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Ably - Alternative to Pusher
- **URL**: https://ably.com/
- **Purpose**: Real-time messaging alternative
- **API Key**: `...`
- **Cost**: Free tier (6M messages/month)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 🎵 Media & Content Services

### AssemblyAI
- **URL**: https://www.assemblyai.com/
- **Purpose**: Speech-to-text and audio processing
- **API Key**: `...`
- **Cost**: $0.00025/second of audio
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### UploadThing
- **URL**: https://uploadthing.com/
- **Purpose**: File upload handling for Next.js
- **API Key**: `sk_live_...`
- **Cost**: Free tier (2GB storage, 100 uploads/month)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 📊 Analytics & Monitoring

### PostHog
- **URL**: https://posthog.com/
- **Purpose**: Product analytics and user behavior tracking
- **API Key**: `phc_...`
- **Cost**: Free tier (1M events/month)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Sentry
- **URL**: https://sentry.io/
- **Purpose**: Error monitoring and performance tracking
- **DSN**: `https://...@.../...`
- **Cost**: Free tier (5K errors/month)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## ⛓️ Blockchain & Web3

### Alchemy
- **URL**: https://www.alchemy.com/
- **Purpose**: Blockchain API for smart contract analysis
- **API Key**: `...`
- **Cost**: Free tier (300M compute units/month)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Infura - Alternative
- **URL**: https://infura.io/
- **Purpose**: Ethereum API alternative
- **Project ID**: `...`
- **Cost**: Free tier (100K requests/day)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 📈 Market Data (Finance Apps)

### Finnhub
- **URL**: https://finnhub.io/
- **Purpose**: Stock market data and financial APIs
- **API Key**: `...`
- **Cost**: Free tier (60 API calls/minute)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

### Polygon.io - Alternative
- **URL**: https://polygon.io/
- **Purpose**: Market data alternative
- **API Key**: `...`
- **Cost**: Free tier (5 API calls/minute)
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 🔧 Development Tools

### GitHub (for GitHub Apps)
- **URL**: https://github.com/
- **Purpose**: Code repository integration for dev tools
- **Personal Access Token**: `ghp_...`
- **Cost**: Free for public repos
- **Owner**: [ASSIGN TO TEAM MEMBER]
- **Status**: ⏳ Pending

## 📋 Setup Instructions

### 1. Priority Order
1. **Core AI Services** (OpenAI, Anthropic) - Required for all projects
2. **Infrastructure** (Vercel, Render) - Required for deployment
3. **Research Services** (Tavily) - Required for market research
4. **Authentication** (Clerk) - Required for user management
5. **Storage** (Cloudflare R2) - Required for file uploads
6. **Communication** (Resend) - Required for notifications
7. **Analytics** (PostHog, Sentry) - Recommended for monitoring
8. **Specialized Services** (AssemblyAI, Stripe, etc.) - As needed per project

### 2. Environment Variables Template
Create a `.env` file with all the captured API keys:

```bash
# Core AI
OPENAI_API_KEY=sk-openai-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# Research
TAVILY_API_KEY=tvly-...
SCRAPINGANT_API_KEY=scrapingant_...

# Infrastructure
VERCEL_TOKEN=...
VERCEL_TEAM_ID=team_...  # Optional
RENDER_API_KEY=...
RENDER_OWNER_ID=usr-...

# Storage
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...

# Authentication
CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Payments
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Communication
RESEND_API_KEY=re_...
PUSHER_APP_ID=...
PUSHER_KEY=...
PUSHER_SECRET=...

# Analytics
POSTHOG_API_KEY=phc_...
SENTRY_DSN=https://...@.../...

# Blockchain
ALCHEMY_API_KEY=...

# Media
ASSEMBLYAI_API_KEY=...

# Development
GITHUB_TOKEN=ghp_...
```

### 3. Team Assignment
Assign each service to a team member for signup:

- **Team Member 1**: Core AI services, Infrastructure
- **Team Member 2**: Research, Authentication, Storage
- **Team Member 3**: Communication, Analytics
- **Team Member 4**: Specialized services (Finance, Media, Blockchain)

### 4. Cost Estimation
**Monthly costs for 60 apps:**
- OpenAI: ~$50-100 (depending on usage)
- Anthropic: ~$20-50
- Vercel: Free tier should cover most projects
- Render: Free tier should cover most projects
- Other services: ~$20-50 total

**Total estimated monthly cost: $90-200**

### 5. Security Notes
- Use test/development API keys initially
- Store all keys securely (not in code)
- Rotate keys regularly
- Monitor usage to avoid unexpected charges
- Use environment variables for all sensitive data

## ✅ Completion Checklist

- [ ] Core AI services signed up
- [ ] Infrastructure services configured
- [ ] Research services activated
- [ ] Authentication service ready
- [ ] Storage service configured
- [ ] Communication services set up
- [ ] Analytics services configured
- [ ] Specialized services ready
- [ ] All API keys captured in `.env`
- [ ] Team members assigned and trained
- [ ] Cost monitoring set up
- [ ] Security practices documented

## 🚀 Next Steps

1. **Complete signups** for all required services
2. **Capture all API keys** in the `.env` file
3. **Run project tagger** to assign archetypes
4. **Test services** with a sample project
5. **Start the CrewAI pipeline** for all 60 projects
6. **Monitor costs** and usage throughout development

---

**Last Updated**: [DATE]
**Status**: Ready for team assignment

