# Stack Choice: Recruitment Flow AI

## Archetype: hr_recruitment
HR tools, resume matching, and recruitment automation

## Backend Choice: fastapi
- **Framework**: FASTAPI
- **Rationale**: Optimized for hr tools, resume matching, and recruitment automation

## Services Required
- openai
- anthropic
- resend

## Environment Variables
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- RESEND_API_KEY
- DATABASE_URL

## Vector Database
- **Vector DB**: pgvector

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
