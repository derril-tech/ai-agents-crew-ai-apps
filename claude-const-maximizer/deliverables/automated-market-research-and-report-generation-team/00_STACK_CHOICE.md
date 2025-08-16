# Stack Choice: Automated Market Research and Report Generation Team

## Archetype: media_content
Video/audio generation and content creation

## Backend Choice: express
- **Framework**: EXPRESS
- **Rationale**: Optimized for video/audio generation and content creation

## Services Required
- openai
- anthropic
- assemblyai
- cloudflare_r2

## Environment Variables
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- ASSEMBLYAI_API_KEY
- R2_BUCKET
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
