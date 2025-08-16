# Stack Choice: Realistic Synthetic Data Generator

## Archetype: rag_kb
RAG/Knowledge Base apps with document processing and semantic search

## Backend Choice: fastapi
- **Framework**: FASTAPI
- **Rationale**: Optimized for rag/knowledge base apps with document processing and semantic search

## Services Required
- openai
- anthropic
- tavily
- cloudflare_r2
- render_pg

## Environment Variables
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- TAVILY_API_KEY
- R2_BUCKET
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
