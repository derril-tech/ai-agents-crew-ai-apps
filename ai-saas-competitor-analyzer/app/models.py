# Pydantic schemas & types
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional
from datetime import datetime

class CompetitorInput(BaseModel):
    name: str
    url: Optional[HttpUrl] = None
    # Optional seed pages (pricing/features). If absent, scraper will try to discover.
    pages: Optional[List[HttpUrl]] = None

class AnalyzeRequest(BaseModel):
    competitors: List[CompetitorInput] = Field(..., min_items=2)
    industry: Optional[str] = None
    notes: Optional[str] = None

class PlanPrice(BaseModel):
    plan: str
    price: Optional[float] = None
    currency: Optional[str] = None         # e.g., USD, EUR
    billing_period: Optional[str] = None   # monthly, yearly
    price_notes: Optional[str] = None

class FeatureItem(BaseModel):
    name: str
    category: Optional[str] = None
    premium: Optional[bool] = False
    raw: Optional[str] = None
    source_url: Optional[str] = None

class ScrapeResult(BaseModel):
    competitor: str
    source_pages: List[str] = []
    plans: List[PlanPrice] = []
    features: List[FeatureItem] = []
    raw_notes: Optional[str] = None

class NormalizedPlan(BaseModel):
    plan: str
    price_usd_month: Optional[float] = None
    price_basis: Optional[str] = None      # "per seat", "flat"
    notes: Optional[str] = None

class NormalizedCompetitor(BaseModel):
    name: str
    plans: List[NormalizedPlan]
    canonical_features: List[FeatureItem]  # canonicalized names & categories

class FeatureMatrix(BaseModel):
    # rows: competitor, cols: canonical feature; bool for presence
    matrix: Dict[str, Dict[str, bool]]  # { competitor: { feature: True/False }}
    feature_categories: Dict[str, str]  # { feature: category }

class SWOT(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class ComparisonInsights(BaseModel):
    price_efficiency: Dict[str, float]      # competitor: score
    cheapest_for_baseline: Optional[str] = None
    best_for_advanced: Optional[str] = None
    swot: Dict[str, SWOT] = {}              # competitor: SWOT

class StrategyRecommendations(BaseModel):
    gap_features_to_add: List[str]
    pricing_levers: List[str]
    gtms: List[str]        # go-to-market angles
    risks: List[str]

class ReportArtifacts(BaseModel):
    title: str
    created_at: datetime
    charts: List[str]                # paths
    pdf_path: str
    json_export_path: str

class AnalyzeResponse(BaseModel):
    normalized: List[NormalizedCompetitor]
    feature_matrix: FeatureMatrix
    comparison: ComparisonInsights
    strategy: StrategyRecommendations
    report: ReportArtifacts
