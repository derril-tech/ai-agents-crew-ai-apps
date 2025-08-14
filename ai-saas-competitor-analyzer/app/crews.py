import json
from typing import List, Dict, Any
from crewai import Crew, Process
from crewai_tools import tool

from .agents import (
    make_scraper_agent, make_normalizer_agent, make_feature_extractor_agent,
    make_comparison_agent, make_strategy_agent, make_report_agent, make_tasks
)
from .tools import (
    scrape_competitor, normalize_competitor, build_feature_matrix, make_comparison,
    suggest_strategy, save_price_vs_features_chart, save_feature_heatmap,
    export_pdf_and_json
)
from .models import (
    CompetitorInput, ScrapeResult, NormalizedCompetitor, FeatureMatrix,
    ComparisonInsights, StrategyRecommendations, ReportArtifacts
)

# ⬇️ NEW: import the Playwright-based discovery helper
from .tools_playwright import discover_pages

# -----------------------------
# Tool wrappers (for CrewAI)
# -----------------------------

@tool("web-scraper")
def web_scraper_tool(payload: str) -> str:
    """
    Payload JSON: { "competitors": [{ "name": "...", "pages": ["..."], "url": "..." }, ...] }
    Returns: JSON stringified List[ScrapeResult]
    """
    import asyncio
    try:
        data = json.loads(payload)
        comps = data["competitors"]

        async def run():
            results: List[ScrapeResult] = []
            for c in comps:
                name = c.get("name")
                pages = c.get("pages") or []
                url = c.get("url")

                # ⬇️ NEW: Auto-discover likely pricing/features pages if none provided
                if (not pages) and url:
                    try:
                        pricing, feats = await discover_pages(url)
                        pages = (pricing + feats)[:6] or [url]
                    except Exception:
                        pages = [url] if url else []

                if not pages:
                    # Nothing to scrape for this competitor; skip gracefully.
                    continue

                res = await scrape_competitor(name, pages)
                results.append(res)
            return results

        results = asyncio.run(run())
        return json.dumps([r.model_dump() for r in results])
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("normalizer")
def normalizer_tool(payload: str) -> str:
    """
    Payload JSON: { "scraped": List[ScrapeResult] }
    Returns: JSON stringified List[NormalizedCompetitor]
    """
    try:
        data = json.loads(payload)
        scraped = [ScrapeResult.model_validate(s) for s in data["scraped"]]
        normd: List[NormalizedCompetitor] = []
        for s in scraped:
            n = normalize_competitor(s.competitor, s.plans, s.features)
            normd.append(n)
        return json.dumps([n.model_dump() for n in normd])
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("feature-tool")
def feature_tool(payload: str) -> str:
    """
    Payload JSON: { "normalized": List[NormalizedCompetitor] }
    Returns: FeatureMatrix JSON string
    """
    try:
        data = json.loads(payload)
        normalized = [NormalizedCompetitor.model_validate(n) for n in data["normalized"]]
        mat = build_feature_matrix(normalized)
        return json.dumps(mat.model_dump())
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("comparison-tool")
def comparison_tool(payload: str) -> str:
    """
    Payload JSON: { "normalized": [...], "matrix": {...} }
    Returns: ComparisonInsights JSON string
    """
    try:
        data = json.loads(payload)
        normalized = [NormalizedCompetitor.model_validate(n) for n in data["normalized"]]
        matrix = FeatureMatrix.model_validate(data["matrix"])
        comp = make_comparison(normalized, matrix)
        return json.dumps(comp.model_dump())
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("strategy-tool")
def strategy_tool(payload: str) -> str:
    """
    Payload JSON: { "normalized": [...], "matrix": {...} }
    Returns: StrategyRecommendations JSON string
    """
    try:
        data = json.loads(payload)
        normalized = [NormalizedCompetitor.model_validate(n) for n in data["normalized"]]
        matrix = FeatureMatrix.model_validate(data["matrix"])
        strat = suggest_strategy(matrix, normalized)
        return json.dumps(strat.model_dump())
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("report-tool")
def report_tool(payload: str) -> str:
    """
    Payload JSON: { "title": str, "normalized": [...], "matrix": {...}, "comparison": {...}, "strategy": {...} }
    Returns: ReportArtifacts JSON string
    """
    try:
        data = json.loads(payload)
        normalized = [NormalizedCompetitor.model_validate(n) for n in data["normalized"]]
        matrix = FeatureMatrix.model_validate(data["matrix"])
        comparison = ComparisonInsights.model_validate(data["comparison"])
        strategy = StrategyRecommendations.model_validate(data["strategy"])

        charts = [
            save_price_vs_features_chart(normalized),
            save_feature_heatmap(matrix)
        ]
        art = export_pdf_and_json(
            title=data.get("title", "AI SaaS Competitor Analyzer Report"),
            normalized=normalized,
            matrix=matrix,
            comparison=comparison,
            strategy=strategy,
            charts=charts
        )
        return json.dumps(art.model_dump())
    except Exception as e:
        return json.dumps({"error": str(e)})

# -----------------------------
# Crew builders
# -----------------------------

def build_crews():
    # Agents
    a_scraper = make_scraper_agent(web_scraper_tool)
    a_normal = make_normalizer_agent(normalizer_tool)
    a_feature = make_feature_extractor_agent(feature_tool)

    a_compare = make_comparison_agent(comparison_tool)
    a_strategy = make_strategy_agent(strategy_tool)
    a_report = make_report_agent(report_tool)

    # Tasks
    t_scrape, t_normalize, t_features, t_compare, t_strategy, t_report = make_tasks()

    # Bind tasks to agents
    t_scrape.agent = a_scraper
    t_normalize.agent = a_normal
    t_features.agent = a_feature
    t_compare.agent = a_compare
    t_strategy.agent = a_strategy
    t_report.agent = a_report

    # Crew 1: Data Acquisition & Prep
    crew1 = Crew(
        agents=[a_scraper, a_normal, a_feature],
        tasks=[t_scrape, t_normalize, t_features],
        process=Process.sequential,
        verbose=True
    )

    # Crew 2: Analysis & Reporting
    crew2 = Crew(
        agents=[a_compare, a_strategy, a_report],
        tasks=[t_compare, t_strategy, t_report],
        process=Process.sequential,
        verbose=True
    )
    return crew1, crew2
