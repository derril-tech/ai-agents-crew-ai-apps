import os
import re
import json
import pathlib
from typing import List, Dict, Optional, Tuple
from datetime import datetime

import httpx
import trafilatura
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process as rf_process
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .models import (
    ScrapeResult, PlanPrice, FeatureItem, NormalizedCompetitor,
    NormalizedPlan, FeatureMatrix, ComparisonInsights, SWOT,
    StrategyRecommendations, ReportArtifacts
)

# ⬇️ NEW: JS-rendering & discovery helpers
from .tools_playwright import discover_pages, rendered_fetch

# -----------------------------
# Utilities / constants
# -----------------------------
REPORTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

CANONICAL_FEATURES = [
    # extend as needed
    "Single Sign-On (SSO)", "Audit Logs", "Role-Based Access Control",
    "API Access", "Webhooks", "Custom Branding",
    "Integrations", "Slack Integration", "Zapier Integration",
    "Analytics Dashboard", "A/B Testing", "Custom Reports",
    "24/7 Support", "Priority Support", "Onboarding Assistance",
    "Data Export", "CSV Import", "Security Certifications",
    "EU Data Residency", "Two-Factor Authentication",
    "Auto-Scaling", "Rate Limits", "Usage Quotas"
]

FEATURE_SYNONYMS = {
    "Single Sign-On (SSO)": ["sso", "single sign on", "oauth", "saml"],
    "Role-Based Access Control": ["rbac", "role based access control", "roles & permissions", "permissions"],
    "24/7 Support": ["round-the-clock support", "24x7 support", "always-on support"],
    "Analytics Dashboard": ["analytics", "insights dashboard", "reporting dashboard"],
    "Two-Factor Authentication": ["2fa", "two factor", "mfa", "multi-factor authentication"],
    "API Access": ["public api", "developer api", "rest api", "graphql api"],
}

FEATURE_CATEGORY_OVERRIDES = {
    "Single Sign-On (SSO)": "Security",
    "Role-Based Access Control": "Security",
    "Two-Factor Authentication": "Security",
    "Audit Logs": "Security",
    "API Access": "Integrations",
    "Webhooks": "Integrations",
    "Slack Integration": "Integrations",
    "Zapier Integration": "Integrations",
    "Analytics Dashboard": "Analytics",
    "Custom Reports": "Analytics",
    "A/B Testing": "Analytics",
    "24/7 Support": "Support",
    "Priority Support": "Support",
    "Onboarding Assistance": "Support",
    "Custom Branding": "Customization",
    "EU Data Residency": "Compliance",
    "Auto-Scaling": "Performance",
    "Rate Limits": "Performance",
    "Usage Quotas": "Performance",
    "CSV Import": "Data",
    "Data Export": "Data",
}

CURRENCY_TO_USD = {
    # Very rough static rates for demo. Replace with live FX in production.
    "USD": 1.0, "EUR": 1.10, "GBP": 1.27, "SEK": 0.095
}

# -----------------------------
# Scraping helpers
# -----------------------------

# ⬇️ REPLACED: JS-aware fallback using Playwright when needed
async def fetch_page(url: str) -> str:
    """
    Try fast HTTP fetch; fall back to JS-rendered fetch for dynamic pages.
    """
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            # Heuristic: if page is suspiciously small or hints at JS, render it
            if len(r.text) < 1000 or "enable javascript" in r.text.lower() or "javascript" in r.text.lower():
                return await rendered_fetch(url)
            return r.text
    except Exception:
        # Network issues or script-heavy sites → render with Playwright
        return await rendered_fetch(url)

def extract_text_and_tables(html: str, base_url: str) -> Tuple[List[PlanPrice], List[FeatureItem]]:
    """Very simple extractor: parse pricing hints & features from tables/lists."""
    soup = BeautifulSoup(html, "lxml")

    # Plans & prices from table-like structures
    plans: List[PlanPrice] = []
    for table in soup.find_all(["table"]):
        rows = table.find_all("tr")
        headers = [th.get_text(" ", strip=True) for th in rows[0].find_all(["th","td"])] if rows else []
        for row in rows[1:]:
            cols = [td.get_text(" ", strip=True) for td in row.find_all(["td","th"])]
            if not cols:
                continue
            # Heuristic: plan name first col, price somewhere
            plan_name = cols[0]
            price = None
            currency = None
            period = None
            joined = " ".join(cols)
            m = re.search(r'([€$£]|SEK)\s?(\d+[.,]?\d*)', joined)
            if m:
                symbol, amount = m.group(1), m.group(2).replace(",", "")
                price = float(amount)
                currency = {"$":"USD","€":"EUR","£":"GBP","SEK":"SEK"}.get(symbol, "USD")
            if "month" in joined.lower():
                period = "monthly"
            elif "year" in joined.lower() or "/yr" in joined.lower():
                period = "yearly"
            plans.append(PlanPrice(plan=plan_name, price=price, currency=currency, billing_period=period, price_notes=joined))

    # Features from bullet lists and feature grids
    features: List[FeatureItem] = []
    for ul in soup.find_all(["ul", "ol"]):
        for li in ul.find_all("li"):
            text = li.get_text(" ", strip=True)
            if len(text) < 3:
                continue
            features.append(FeatureItem(name=text, raw=text, source_url=base_url))

    # Also attempt trafilatura main text for stray feature mentions
    extracted = trafilatura.extract(html, include_tables=True, include_images=False)
    if extracted:
        for line in extracted.splitlines():
            line = line.strip()
            if len(line) > 8 and any(k in line.lower() for k in ["support", "integration", "api", "report", "dashboard", "sso", "security"]):
                features.append(FeatureItem(name=line[:140], raw=line, source_url=base_url))
    return plans, features

async def scrape_competitor(name: str, pages: List[str]) -> ScrapeResult:
    src_pages = []
    all_plans: List[PlanPrice] = []
    all_features: List[FeatureItem] = []
    for url in pages:
        try:
            html = await fetch_page(url)
            plans, feats = extract_text_and_tables(html, url)
            all_plans.extend(plans)
            all_features.extend(feats)
            src_pages.append(url)
        except Exception as e:
            all_features.append(FeatureItem(name=f"[Scrape error: {e}]", raw=str(e), source_url=url))
    return ScrapeResult(competitor=name, source_pages=src_pages, plans=all_plans, features=all_features)

# -----------------------------
# Normalization & feature ops
# -----------------------------

def normalize_currency_to_usd_month(price: Optional[float], currency: Optional[str], period: Optional[str]) -> Optional[float]:
    if price is None:
        return None
    cur = (currency or "USD").upper()
    fx = CURRENCY_TO_USD.get(cur, 1.0)
    usd = price * fx
    if (period or "monthly").lower().startswith("year"):
        usd = usd / 12.0
    return round(usd, 2)

def canonicalize_feature_name(raw_name: str) -> Tuple[str, str]:
    """Map raw feature → canonical feature via synonyms + fuzzy match."""
    low = raw_name.lower()
    for canon, syns in FEATURE_SYNONYMS.items():
        if any(s in low for s in syns):
            return canon, FEATURE_CATEGORY_OVERRIDES.get(canon, "General")
    # Fuzzy match against list for everything else
    match, score, _ = rf_process.extractOne(raw_name, CANONICAL_FEATURES, scorer=fuzz.WRatio)
    if score >= 85:
        return match, FEATURE_CATEGORY_OVERRIDES.get(match, "General")
    # Fall back to the raw string (treated as canonical for now)
    return raw_name, "General"

def normalize_competitor(name: str, plans: List[PlanPrice], features: List[FeatureItem]) -> NormalizedCompetitor:
    nplans: List[NormalizedPlan] = []
    for p in plans:
        nplans.append(NormalizedPlan(
            plan=p.plan,
            price_usd_month=normalize_currency_to_usd_month(p.price, p.currency, p.billing_period),
            price_basis="flat",  # could detect per-seat, etc., later
            notes=p.price_notes
        ))
    canon_feats: List[FeatureItem] = []
    seen = set()
    for f in features:
        canon, cat = canonicalize_feature_name(f.name)
        key = (canon, cat)
        if key in seen:
            continue
        seen.add(key)
        canon_feats.append(FeatureItem(name=canon, category=cat, premium=("enterprise" in (f.raw or "").lower()), raw=f.raw, source_url=f.source_url))
    return NormalizedCompetitor(name=name, plans=nplans, canonical_features=canon_feats)

def build_feature_matrix(normalized: List[NormalizedCompetitor]) -> FeatureMatrix:
    # Determine columns
    all_features = {}
    for c in normalized:
        for f in c.canonical_features:
            all_features[f.name] = f.category or "General"
    # Build matrix
    matrix: Dict[str, Dict[str, bool]] = {}
    for c in normalized:
        row: Dict[str, bool] = {feat: False for feat in all_features.keys()}
        for f in c.canonical_features:
            row[f.name] = True
        matrix[c.name] = row
    return FeatureMatrix(matrix=matrix, feature_categories=all_features)

# -----------------------------
# Comparison & strategy
# -----------------------------

def compute_price_efficiency(normalized: List[NormalizedCompetitor], matrix: FeatureMatrix) -> Dict[str, float]:
    scores = {}
    for c in normalized:
        # pick cheapest non-null plan
        prices = [p.price_usd_month for p in c.plans if p.price_usd_month is not None]
        cheapest = min(prices) if prices else None
        features_count = sum(1 for f in c.canonical_features)
        if cheapest and features_count:
            # simple features per $ metric
            scores[c.name] = round(features_count / cheapest, 2)
        else:
            scores[c.name] = 0.0
    return scores

def cheapest_for_baseline(normalized: List[NormalizedCompetitor]) -> Optional[str]:
    best_name, best_price = None, None
    for c in normalized:
        prices = [p.price_usd_month for p in c.plans if p.price_usd_month is not None]
        if not prices:
            continue
        cheapest = min(prices)
        if best_price is None or cheapest < best_price:
            best_price, best_name = cheapest, c.name
    return best_name

def best_for_advanced(normalized: List[NormalizedCompetitor]) -> Optional[str]:
    # naive: most features overall
    best_name, best_feats = None, -1
    for c in normalized:
        count = len(c.canonical_features)
        if count > best_feats:
            best_feats, best_name = count, c.name
    return best_name

def swot_for_competitor(c: NormalizedCompetitor, avg_price: float) -> SWOT:
    strengths, weaknesses, opportunities, threats = [], [], [], []
    prices = [p.price_usd_month for p in c.plans if p.price_usd_month is not None]
    min_price = min(prices) if prices else None
    if min_price and min_price <= avg_price * 0.9:
        strengths.append(f"Competitive entry price (${min_price}/mo).")
    elif min_price and min_price >= avg_price * 1.2:
        weaknesses.append(f"Higher entry price (${min_price}/mo) than market average (${avg_price:.2f}).")

    # Feature-based heuristics
    feat_names = {f.name for f in c.canonical_features}
    if "Analytics Dashboard" in feat_names:
        strengths.append("Strong analytics for decision-makers.")
    if "Single Sign-On (SSO)" not in feat_names:
        weaknesses.append("Missing SSO may hinder enterprise deals.")

    opportunities.append("Bundle premium features into mid-tier to improve adoption.")
    threats.append("Rivals may undercut on pricing with similar feature sets.")
    return SWOT(strengths=strengths, weaknesses=weaknesses, opportunities=opportunities, threats=threats)

def make_comparison(normalized: List[NormalizedCompetitor], matrix: FeatureMatrix) -> ComparisonInsights:
    scores = compute_price_efficiency(normalized, matrix)
    base = cheapest_for_baseline(normalized)
    adv = best_for_advanced(normalized)
    # Average price for SWOT reference
    all_prices = []
    for c in normalized:
        all_prices += [p.price_usd_month for p in c.plans if p.price_usd_month is not None]
    avg_price = sum(all_prices) / len(all_prices) if all_prices else 0.0
    swot = {c.name: swot_for_competitor(c, avg_price) for c in normalized}
    return ComparisonInsights(price_efficiency=scores, cheapest_for_baseline=base, best_for_advanced=adv, swot=swot)

def suggest_strategy(matrix: FeatureMatrix, normalized: List[NormalizedCompetitor]) -> StrategyRecommendations:
    # Gap = features common among most competitors but missing in some
    feature_counts = {f: 0 for f in matrix.feature_categories.keys()}
    for comp, row in matrix.matrix.items():
        for feat, has in row.items():
            if has:
                feature_counts[feat] += 1
    total = len(matrix.matrix)
    common = [f for f, cnt in feature_counts.items() if cnt >= max(2, int(0.6 * total))]  # common in ≥60% or at least 2
    # Assume "you" are a new product: recommend adding common features first
    gap_features_to_add = common[:8]

    pricing_levers = [
        "Introduce longer trial (21-30 days) to reduce adoption friction.",
        "Offer annual discount (15-20%) to lock in revenue.",
        "Bundle premium features as add-ons to protect ARPU."
    ]
    gtms = [
        "Position as 'Best Value for Analytics‑heavy Teams'.",
        "Differentiate with enterprise‑grade security ramp at mid‑tier.",
        "Publish transparent, developer‑first pricing with generous API limits."
    ]
    risks = [
        "Feature parity race can erode margins; protect moats (ecosystem & data).",
        "Underpricing with premium support leads to unscalable costs."
    ]
    return StrategyRecommendations(
        gap_features_to_add=gap_features_to_add,
        pricing_levers=pricing_levers,
        gtms=gtms,
        risks=risks
    )

# -----------------------------
# Charts & reporting
# -----------------------------

def save_price_vs_features_chart(normalized: List[NormalizedCompetitor]) -> str:
    names, cheapest_prices, feature_counts = [], [], []
    for c in normalized:
        prices = [p.price_usd_month for p in c.plans if p.price_usd_month is not None]
        cheapest = min(prices) if prices else None
        if cheapest is None:  # skip if no price
            continue
        names.append(c.name)
        cheapest_prices.append(cheapest)
        feature_counts.append(len(c.canonical_features))

    plt.figure()
    plt.scatter(cheapest_prices, feature_counts)
    for i, name in enumerate(names):
        plt.annotate(name, (cheapest_prices[i], feature_counts[i]))
    plt.xlabel("Cheapest plan (USD/month)")
    plt.ylabel("# Canonical Features")
    out = REPORTS_DIR / f"chart_price_vs_features_{datetime.utcnow().timestamp():.0f}.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return str(out)

def save_feature_heatmap(matrix: FeatureMatrix) -> str:
    # Simple table-like PNG using matplotlib text plot.
    comps = list(matrix.matrix.keys())
    feats = list(matrix.feature_categories.keys())[:20]  # cap for readability
    data = [[1 if matrix.matrix[c][f] else 0 for f in feats] for c in comps]

    fig, ax = plt.subplots()
    cax = ax.imshow(data, aspect="auto")
    ax.set_xticks(range(len(feats)))
    ax.set_xticklabels([f[:18] for f in feats], rotation=90)
    ax.set_yticks(range(len(comps)))
    ax.set_yticklabels(comps)
    fig.colorbar(cax, ax=ax)
    plt.tight_layout()
    out = REPORTS_DIR / f"heatmap_features_{datetime.utcnow().timestamp():.0f}.png"
    plt.savefig(out)
    plt.close()
    return str(out)

def export_pdf_and_json(title: str,
                        normalized: List[NormalizedCompetitor],
                        matrix: FeatureMatrix,
                        comparison: ComparisonInsights,
                        strategy: StrategyRecommendations,
                        charts: List[str]) -> ReportArtifacts:
    ts = datetime.utcnow()
    json_path = REPORTS_DIR / f"export_{int(ts.timestamp())}.json"
    pdf_path = REPORTS_DIR / f"report_{int(ts.timestamp())}.pdf"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": title,
            "created_at": ts.isoformat(),
            "normalized": [n.model_dump() for n in normalized],
            "matrix": matrix.model_dump(),
            "comparison": comparison.model_dump(),
            "strategy": strategy.model_dump(),
            "charts": charts
        }, f, indent=2)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(pdf_path))
    flow = [Paragraph(title, styles["Title"]), Spacer(1, 12)]
    flow.append(Paragraph(f"Created at (UTC): {ts.isoformat()}", styles["Normal"]))
    flow.append(Spacer(1, 12))

    # Summary table: price efficiency
    pe = comparison.price_efficiency
    table_data = [["Competitor", "Price Efficiency (features per $)"]]
    for k, v in sorted(pe.items(), key=lambda x: x[1], reverse=True):
        table_data.append([k, str(v)])
    table = Table(table_data, colWidths=[220, 220])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("ALIGN", (1,1), (-1,-1), "RIGHT")
    ]))
    flow.append(table)
    flow.append(Spacer(1, 12))

    flow.append(Paragraph(f"Cheapest for baseline: <b>{comparison.cheapest_for_baseline}</b>", styles["Normal"]))
    flow.append(Paragraph(f"Best for advanced users: <b>{comparison.best_for_advanced}</b>", styles["Normal"]))
    flow.append(Spacer(1, 12))

    for ch in charts:
        flow.append(Image(ch, width=460, height=260))
        flow.append(Spacer(1, 12))

    flow.append(Paragraph("<b>Strategy Recommendations</b>", styles["Heading2"]))
    flow.append(Paragraph("Gap features to add: " + ", ".join(strategy.gap_features_to_add), styles["Normal"]))
    flow.append(Paragraph("Pricing levers: " + "; ".join(strategy.pricing_levers), styles["Normal"]))
    flow.append(Paragraph("GTM angles: " + "; ".join(strategy.gtms), styles["Normal"]))
    flow.append(Paragraph("Risks: " + "; ".join(strategy.risks), styles["Normal"]))

    doc.build(flow)

    return ReportArtifacts(
        title=title,
        created_at=ts,
        charts=charts,
        pdf_path=str(pdf_path),
        json_export_path=str(json_path)
    )
