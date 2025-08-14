# Agent & task blueprints
from crewai import Agent, Task
from typing import List, Dict, Any
from .models import CompetitorInput, ScrapeResult

# Tool objects will be injected from crews.py to avoid circular imports.
def make_scraper_agent(web_scraper_tool):
    return Agent(
        role="Scraper Agent – Competitive Intel Harvester",
        goal=(
            "Collect pricing tables, plan names, currencies & billing periods, and feature lists "
            "from publicly accessible competitor pages. Output structured JSON per competitor."
        ),
        backstory=(
            "A methodical research spider that respects robots.txt and only uses public pages. "
            "You prefer structured information like tables and bullet lists."
        ),
        tools=[web_scraper_tool],
        verbose=True,
        memory=True
    )

def make_normalizer_agent(normalizer_tool):
    return Agent(
        role="Data Normalizer – Unifier of Messy Inputs",
        goal=(
            "Standardize currencies to USD/month, canonicalize feature names, and tag features "
            "into categories, producing clean normalized competitor objects."
        ),
        backstory="You convert chaos into a consistent schema for clean downstream analysis.",
        tools=[normalizer_tool],
        verbose=True,
        memory=True
    )

def make_feature_extractor_agent(feature_tool):
    return Agent(
        role="Feature Extraction – Signal Finder",
        goal=(
            "Create a feature matrix across competitors, identify common & unique features, "
            "and highlight differentiators."
        ),
        backstory="You reveal what matters most to buyers and what’s unique.",
        tools=[feature_tool],
        verbose=True,
        memory=True
    )

def make_comparison_agent(comparison_tool):
    return Agent(
        role="Comparator – Price & Value Analyst",
        goal=(
            "Compute price-to-feature efficiency, cheapest viable baseline option, "
            "best for advanced users, and SWOT per competitor."
        ),
        backstory="You are objective and numbers-first with crisp takeaways.",
        tools=[comparison_tool],
        verbose=True,
        memory=True
    )

def make_strategy_agent(strategy_tool):
    return Agent(
        role="Strategist – Positioning & Move Planner",
        goal=(
            "Convert comparisons into concrete strategy: features to add, pricing levers, "
            "3 GTM angles, and 2 risk flags."
        ),
        backstory="You deliver practical tactics that execs can act on Monday morning.",
        tools=[strategy_tool],
        verbose=True,
        memory=True
    )

def make_report_agent(report_tool):
    return Agent(
        role="Reporter – Executive-Ready Communications",
        goal=(
            "Produce a polished PDF + JSON bundle with charts, saved under /reports, "
            "and return the file paths."
        ),
        backstory="You communicate clearly with visuals and concise headlines.",
        tools=[report_tool],
        verbose=True,
        memory=False  # keep it stateless
    )

# Tasks: descriptions are short; inputs are provided via Crew.kickoff().
def make_tasks():
    t_scrape = Task(
        description=(
            "Scrape the provided competitor pages for pricing & feature data and return a list of ScrapeResult JSON objects."
        ),
        expected_output="List[ScrapeResult] as JSON string.",
        agent=None  # bind later
    )
    t_normalize = Task(
        description="Normalize scraped results to unified schema (USD/month, canonical features).",
        expected_output="List[NormalizedCompetitor] as JSON string.",
        agent=None
    )
    t_features = Task(
        description="Build feature matrix across normalized competitors and highlight common/unique features.",
        expected_output="FeatureMatrix JSON with highlights.",
        agent=None
    )
    t_compare = Task(
        description="Compute price efficiency, cheapest baseline, best advanced, and SWOT per competitor.",
        expected_output="ComparisonInsights JSON.",
        agent=None
    )
    t_strategy = Task(
        description="Suggest gap features to add, pricing levers, GTM angles, and risks.",
        expected_output="StrategyRecommendations JSON.",
        agent=None
    )
    t_report = Task(
        description="Generate charts and export a PDF + JSON bundle; return file paths.",
        expected_output="ReportArtifacts JSON with paths.",
        agent=None
    )
    return t_scrape, t_normalize, t_features, t_compare, t_strategy, t_report
