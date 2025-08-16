# Stack Choice: Multilingual Customer Support Reply Generator

## Archetype: support_crm
Customer support chatbots and CRM automation

## Backend Choice: express
- **Framework**: EXPRESS
- **Rationale**: Optimized for customer support chatbots and crm automation

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
- **Vector DB**: None required

## Deployment Profile
- **Frontend**: Vercel (Next.js 14 + React + Tailwind)
- **Backend**: Render (express)
- **Database**: Render PostgreSQL
- **File Storage**: Cloudflare R2 (if required)

## Next Steps
1. Review the market brief in `01_market_brief.md`
2. Check the prompt pack in `02_prompt_pack.md`
3. Follow the 5-prompts plan in `05_five_prompts_plan.md`
4. Use the deployment checklist in `06_deploy_checklist.md`
