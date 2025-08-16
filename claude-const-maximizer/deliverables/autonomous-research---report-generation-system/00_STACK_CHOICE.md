# Stack Choice: Autonomous Research & Report Generation System

## Archetype: agentic
Multi-agent orchestration and autonomous workflows

## Backend Choice: fastapi
- **Framework**: FASTAPI
- **Rationale**: Optimized for multi-agent orchestration and autonomous workflows

## Services Required
- openai
- anthropic
- tavily
- resend

## Environment Variables
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- TAVILY_API_KEY
- RESEND_API_KEY
- DATABASE_URL

## Vector Database
- **Vector DB**: None required

## Deployment Profile
- **Frontend**: Vercel (Next.js 14 + React + Tailwind)
- **Backend**: Render (fastapi)
- **Database**: Render PostgreSQL
- **File Storage**: Cloudflare R2 (if required)

## Next Steps
1. Review the market brief in `01_market_brief.md`
2. Check the prompt pack in `02_prompt_pack.md`
3. Follow the 5-prompts plan in `05_five_prompts_plan.md`
4. Use the deployment checklist in `06_deploy_checklist.md`
