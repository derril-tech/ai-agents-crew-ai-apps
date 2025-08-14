# JS-aware fetching + lightweight in-domain discovery for pricing/features pages
import asyncio
import re
from typing import List, Tuple, Optional, Set
from urllib.parse import urlparse, urljoin

from playwright.async_api import async_playwright

PRICING_HINTS = re.compile(r"(pricing|plans?|compare|cost|tariffs?)", re.I)
FEATURE_HINTS = re.compile(r"(feature|capabilit|what.*(you|get)|why.*us|solutions?)", re.I)

async def _rendered_html(url: str, wait_ms: int = 1200) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        try:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            # Allow client-side render
            await page.wait_for_timeout(wait_ms)
            html = await page.content()
            return html
        finally:
            await browser.close()

def _same_domain(start_url: str, candidate: str) -> bool:
    a, b = urlparse(start_url), urlparse(candidate)
    return (b.netloc or a.netloc) == a.netloc

async def discover_pages(start_url: str, max_links: int = 25) -> Tuple[List[str], List[str]]:
    """
    Returns (pricing_pages, feature_pages). Starts from start_url, scrapes and follows internal links.
    Biases links that contain pricing/features hints; caps total.
    """
    visited: Set[str] = set()
    to_visit: List[str] = [start_url]
    pricing, features = [], []

    while to_visit and len(visited) < max_links:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            html = await _rendered_html(url)
        except Exception:
            continue

        # Collect candidate links
        m = re.findall(r'href="([^"#]+)"', html)
        for href in m:
            full = urljoin(url, href)
            if not _same_domain(start_url, full):
                continue
            if full not in visited and len(visited) + len(to_visit) < max_links:
                # prioritize likely pricing/features
                if PRICING_HINTS.search(href):
                    pricing.append(full)
                elif FEATURE_HINTS.search(href):
                    features.append(full)
                # seed crawl queue (light breadth-first)
                to_visit.append(full)

        # Also consider current page itself as pricing/features if path matches
        path = urlparse(url).path.lower()
        if PRICING_HINTS.search(path) and url not in pricing:
            pricing.append(url)
        if FEATURE_HINTS.search(path) and url not in features:
            features.append(url)

    # Deduplicate while preserving order
    def dedupe(seq: List[str]) -> List[str]:
        seen = set(); out = []
        for x in seq:
            if x not in seen:
                seen.add(x); out.append(x)
        return out

    return dedupe(pricing)[:5], dedupe(features)[:5]

async def rendered_fetch(url: str) -> str:
    """Public helper: fetch JS-rendered HTML (Chromium)."""
    return await _rendered_html(url)
