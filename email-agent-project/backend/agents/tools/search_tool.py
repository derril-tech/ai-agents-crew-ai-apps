# backend/agents/tools/search_tool.py
"""
Search Tool wrapper for CrewAI
Integrates Tavily and Serper for web searching capabilities
"""

import os
import json
from typing import Dict, Any, List, Optional
from crewai_tools import BaseTool
import httpx
from datetime import datetime


class SearchTool(BaseTool):
    """Unified search tool using Tavily and Serper"""
    
    name: str = "web_search"
    description: str = "Search the web for information using Tavily or Serper APIs"
    
    def __init__(self):
        """Initialize search tool with API keys"""
        super().__init__()
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.client = httpx.Client(timeout=30.0)
    
    def _run(self, query: str, search_type: str = "general", max_results: int = 5) -> str:
        """
        Execute web search
        
        Args:
            query: Search query
            search_type: Type of search (general, news, academic)
            max_results: Maximum number of results
            
        Returns:
            JSON string of search results
        """
        try:
            # Try Tavily first (better for research)
            if self.tavily_api_key:
                results = self._search_tavily(query, search_type, max_results)
                if results:
                    return json.dumps(results)
            
            # Fallback to Serper
            if self.serper_api_key:
                results = self._search_serper(query, search_type, max_results)
                if results:
                    return json.dumps(results)
            
            return json.dumps({
                "error": "No search API keys configured",
                "query": query
            })
            
        except Exception as e:
            return json.dumps({
                "error": f"Search failed: {str(e)}",
                "query": query
            })
    
    def _search_tavily(self, query: str, search_type: str, max_results: int) -> Optional[Dict[str, Any]]:
        """
        Search using Tavily API
        
        Args:
            query: Search query
            search_type: Type of search
            max_results: Maximum results
            
        Returns:
            Search results or None
        """
        try:
            url = "https://api.tavily.com/search"
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced" if search_type == "academic" else "basic",
                "include_answer": True,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [],
                "exclude_domains": []
            }
            
            if search_type == "news":
                payload["topic"] = "news"
            
            response = self.client.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Format results
            results = {
                "source": "tavily",
                "query": query,
                "answer": data.get("answer", ""),
                "results": []
            }
            
            for item in data.get("results", []):
                results["results"].append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0)
                })
            
            print(f"🔍 Tavily search completed: {len(results['results'])} results")
            return results
            
        except Exception as e:
            print(f"⚠️ Tavily search error: {str(e)}")
            return None
    
    def _search_serper(self, query: str, search_type: str, max_results: int) -> Optional[Dict[str, Any]]:
        """
        Search using Serper API
        
        Args:
            query: Search query
            search_type: Type of search
            max_results: Maximum results
            
        Returns:
            Search results or None
        """
        try:
            # Determine endpoint based on search type
            if search_type == "news":
                url = "https://google.serper.dev/news"
            elif search_type == "academic":
                url = "https://google.serper.dev/scholar"
            else:
                url = "https://google.serper.dev/search"
            
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "num": max_results
            }
            
            response = self.client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Format results
            results = {
                "source": "serper",
                "query": query,
                "answer": data.get("answerBox", {}).get("answer", ""),
                "results": []
            }
            
            # Handle different result types
            if "organic" in data:
                for item in data["organic"][:max_results]:
                    results["results"].append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "content": item.get("snippet", ""),
                        "position": item.get("position", 0)
                    })
            elif "news" in data:
                for item in data["news"][:max_results]:
                    results["results"].append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "content": item.get("snippet", ""),
                        "date": item.get("date", "")
                    })
            elif "papers" in data:  # Scholar results
                for item in data["papers"][:max_results]:
                    results["results"].append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "content": item.get("snippet", ""),
                        "authors": item.get("authors", [])
                    })
            
            print(f"🔍 Serper search completed: {len(results['results'])} results")
            return results
            
        except Exception as e:
            print(f"⚠️ Serper search error: {str(e)}")
            return None
    
    def search_context(self, query: str, context_type: str = "company") -> Dict[str, Any]:
        """
        Search for specific context (company info, sender info, etc.)
        
        Args:
            query: Search query
            context_type: Type of context to search
            
        Returns:
            Contextual information
        """
        if context_type == "company":
            # Search for company information
            search_query = f"{query} company information email address contact"
        elif context_type == "person":
            # Search for person information
            search_query = f"{query} LinkedIn profile professional background"
        else:
            search_query = query
        
        results = json.loads(self._run(search_query, "general", 3))
        
        # Extract and summarize key information
        context = {
            "type": context_type,
            "query": query,
            "findings": []
        }
        
        if "results" in results:
            for result in results["results"]:
                context["findings"].append({
                    "source": result.get("url", ""),
                    "info": result.get("content", "")[:200]  # Truncate for summary
                })
        
        return context