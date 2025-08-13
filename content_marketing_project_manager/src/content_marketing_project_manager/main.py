#!/usr/bin/env python
from pprint import pprint
from content_marketing_project_manager.crew import ContentMarketingProjectManager

# Inputs you can tweak freely
inputs = {
    "project_type": "Multi-Channel Content Marketing Campaign",
    "industry": "B2B SaaS",
    "project_objectives": "Drive awareness and leads across blog, email, social, and webinars.",
    "project_requirements": """
- Blog series solving key B2B SaaS pain points
- Lead magnet (eBook + checklist) for gated campaigns
- 4-part email nurture sequence
- Social promo assets (LinkedIn, X, Instagram)
- 2-minute feature explainer video
- Live webinar with two guest speakers
- Brand guidelines compliance + SEO optimization
- Quarterly theme: "Scaling with Smart Systems"
- Shared editorial calendar with deadlines
""",
    "team_members": """
- Sarah Lee (Content Strategist)
- Mark Johnson (SEO Writer)
- Priya Desai (Graphic Designer)
- Carlos Rivera (Email Marketing Specialist)
- Emma Chen (Social Media Manager)
- Liam Brown (Video Producer)
""",
}

def run():
    crew = ContentMarketingProjectManager().crew()
    result = crew.kickoff(inputs=inputs)

    # Try usage metrics (CrewAI provides this when available)
    try:
        crew.calculate_usage_metrics()
        usage = crew.usage_metrics
        if usage:
            print("\n--- Usage ---")
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Completion tokens: {usage.completion_tokens}")
    except Exception:
        pass

    # If the last task produced a Pydantic model, expose it nicely
    plan = getattr(result, "pydantic", result)
    plan_dict = plan.dict() if hasattr(plan, "dict") else plan

    print("\n--- Tasks ---")
    pprint(plan_dict.get("tasks", []))
    print("\n--- Assignments ---")
    pprint(plan_dict.get("assignments", []))
    print("\n--- Milestones ---")
    pprint(plan_dict.get("milestones", []))
    print("\n--- Content Calendar ---")
    print(plan_dict.get("content_calendar") or "N/A")

if __name__ == "__main__":
    run()
