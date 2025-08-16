"""
Market Researcher Agent
Responsible for Step 1 of Phase 3: Comprehensive market research and analysis
"""

import asyncio
from typing import Dict, Any, List
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.tools import TavilySearchResults
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

class MarketResearcher:
    """World-class market research agent for comprehensive project analysis"""
    
    def __init__(self):
        # Primary LLM (DeepSeek - cost-effective for research)
        self.primary_llm = ChatOpenAI(
            model="deepseek-chat",
            temperature=0.2,  # Lower temperature for consistent research
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
        
        # Backup LLMs
        self.backup_llms = []
        
        # Add Gemini if API key is available
        if os.getenv("GOOGLE_API_KEY"):
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                gemini_llm = ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    temperature=0.2,
                    google_api_key=os.getenv("GOOGLE_API_KEY")
                )
                self.backup_llms.append(gemini_llm)
                print("  ✅ Gemini Pro backup LLM configured for Market Researcher")
            except Exception as e:
                print(f"  ⚠️ Failed to configure Gemini Pro for Market Researcher: {e}")
        
        # Add GPT-3.5 as backup
        self.backup_llms.append(
            ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.2,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        )
        print("  ✅ GPT-3.5 Turbo backup LLM configured for Market Researcher")
        
        print("  ✅ Market Researcher: DeepSeek → Gemini Pro → GPT-3.5 Turbo")
        
        # Enhanced search tool
        self.search_tool = TavilySearchResults(
            api_key=os.getenv("TAVILY_API_KEY"),
            max_results=8  # Increased for comprehensive research
        )
        
        # Research categories for comprehensive coverage
        self.research_categories = {
            "market_analysis": [
                "market size", "market trends", "market growth", "market opportunity",
                "total addressable market", "serviceable market", "market share"
            ],
            "competitive_analysis": [
                "competitors", "competitive landscape", "market leaders", "direct competitors",
                "indirect competitors", "competitive advantages", "market positioning"
            ],
            "target_audience": [
                "target audience", "user personas", "demographics", "psychographics",
                "user needs", "pain points", "user behavior", "customer segments"
            ],
            "technology_trends": [
                "technology trends", "AI trends", "tech stack", "emerging technologies",
                "industry standards", "best practices", "technology adoption"
            ],
            "business_model": [
                "business model", "revenue model", "pricing strategy", "go-to-market",
                "monetization", "business strategy", "market entry"
            ],
            "regulatory_compliance": [
                "regulations", "compliance", "legal requirements", "data privacy",
                "security requirements", "industry standards", "regulatory framework"
            ]
        }
    
    async def research_project(self, project_name: str, description: str, tech_stack: str) -> Dict[str, Any]:
        """Conduct comprehensive market research for a project"""
        
        print(f"🔍 Starting comprehensive market research for: {project_name}")
        
        # Phase 1: Initial Research
        print("  📊 Phase 1: Conducting initial market research...")
        research_data = await self._conduct_comprehensive_research(project_name, description, tech_stack)
        
        # Phase 2: Deep Analysis
        print("  🔬 Phase 2: Performing deep market analysis...")
        analysis = await self._perform_deep_analysis(project_name, description, tech_stack, research_data)
        
        # Phase 3: Validation and Enhancement
        print("  ✅ Phase 3: Validating and enhancing research...")
        enhanced_analysis = await self._validate_and_enhance_analysis(project_name, description, analysis, research_data)
        
        # Compile final research report
        final_report = {
            "project_name": project_name,
            "description": description,
            "tech_stack": tech_stack,
            "research_date": asyncio.get_event_loop().time(),
            "research_data": research_data,
            "market_research": enhanced_analysis,
            "target_audience": enhanced_analysis.get("target_audience", ""),
            "competitors": enhanced_analysis.get("competitors", ""),
            "market_size": enhanced_analysis.get("market_size", ""),
            "key_features": enhanced_analysis.get("key_features", ""),
            "api_sources": enhanced_analysis.get("api_sources", ""),
            "data_sources": enhanced_analysis.get("data_sources", ""),
            "market_opportunity": enhanced_analysis.get("market_opportunity", ""),
            "risks": enhanced_analysis.get("risks", ""),
            "recommendations": enhanced_analysis.get("recommendations", ""),
            "business_model": enhanced_analysis.get("business_model", ""),
            "go_to_market": enhanced_analysis.get("go_to_market", ""),
            "success_metrics": enhanced_analysis.get("success_metrics", ""),
            "research_quality_score": self._calculate_research_quality_score(enhanced_analysis)
        }
        
        print(f"  🎯 Research completed with quality score: {final_report['research_quality_score']}/100")
        return final_report
    
    async def _conduct_comprehensive_research(self, project_name: str, description: str, tech_stack: str) -> List[Dict[str, Any]]:
        """Conduct comprehensive web research across multiple categories"""
        
        all_research_results = []
        
        # Generate search queries for each research category
        for category, keywords in self.research_categories.items():
            print(f"    🔍 Researching {category}...")
            
            # Create category-specific search queries
            category_queries = self._generate_category_queries(project_name, description, tech_stack, category, keywords)
            
            for query in category_queries:
                try:
                    results = await self.search_tool.ainvoke({"query": query})
                    
                    # Add category metadata to results
                    for result in results:
                        result["research_category"] = category
                        result["search_query"] = query
                    
                    all_research_results.extend(results)
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ⚠️ Search error for query '{query}': {e}")
                    continue
        
        # Remove duplicates and limit results
        unique_results = self._deduplicate_results(all_research_results)
        return unique_results[:50]  # Limit to top 50 results
    
    def _generate_category_queries(self, project_name: str, description: str, tech_stack: str, category: str, keywords: List[str]) -> List[str]:
        """Generate category-specific search queries"""
        queries = []
        
        # Base queries for each category
        base_queries = [
            f'"{project_name}" {category}',
            f'"{description}" {category}',
            f'"{tech_stack}" {category}'
        ]
        
        # Add keyword-specific queries
        for keyword in keywords[:3]:  # Use top 3 keywords per category
            queries.extend([
                f'"{project_name}" {keyword}',
                f'"{description}" {keyword}',
                f'AI {keyword} {category}',
                f'{tech_stack} {keyword} market'
            ])
        
        # Add category-specific queries
        queries.extend(base_queries)
        
        return list(set(queries))  # Remove duplicates
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate search results"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    async def _perform_deep_analysis(self, project_name: str, description: str, tech_stack: str, research_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform deep market analysis using LLM"""
        
        # Prepare comprehensive research summary
        research_summary = self._create_comprehensive_summary(research_data)
        
        analysis_prompt = f"""
You are a senior market research analyst with expertise in AI applications and technology markets. Conduct a comprehensive market analysis for the following project:

## PROJECT DETAILS
**Project Name:** {project_name}
**Description:** {description}
**Tech Stack:** {tech_stack}

## RESEARCH DATA
{research_summary}

## ANALYSIS REQUIREMENTS
Provide a comprehensive, structured analysis covering all aspects of the market opportunity. Your analysis should be:

1. **Data-Driven**: Base conclusions on the research data provided
2. **Actionable**: Provide specific, implementable insights
3. **Comprehensive**: Cover all critical market aspects
4. **Realistic**: Provide balanced, achievable assessments

## REQUIRED ANALYSIS SECTIONS

### 1. TARGET AUDIENCE
- Primary user personas (detailed demographics, psychographics)
- Secondary user segments
- User needs and pain points
- User behavior patterns
- Market segmentation strategy

### 2. COMPETITIVE LANDSCAPE
- Direct competitors (list with brief analysis)
- Indirect competitors
- Competitive advantages and disadvantages
- Market positioning opportunities
- Competitive differentiation strategy

### 3. MARKET SIZE & OPPORTUNITY
- Total Addressable Market (TAM) estimate
- Serviceable Addressable Market (SAM) estimate
- Serviceable Obtainable Market (SOM) estimate
- Market growth potential and trends
- Market timing considerations

### 4. KEY FEATURES & DIFFERENTIATION
- Must-have features (core functionality)
- Nice-to-have features (enhancement features)
- Unique selling propositions (USPs)
- Feature prioritization matrix
- Technical differentiators

### 5. API & DATA SOURCES
- Required third-party APIs and services
- Data sources and databases needed
- Integration requirements
- Data dependencies and costs
- Alternative data sources

### 6. BUSINESS MODEL & MONETIZATION
- Recommended business model
- Pricing strategy and tiers
- Revenue streams
- Cost structure considerations
- Profitability analysis

### 7. GO-TO-MARKET STRATEGY
- Market entry strategy
- Customer acquisition channels
- Marketing approach
- Partnership opportunities
- Launch timeline

### 8. MARKET OPPORTUNITY & TIMING
- Current market gaps and opportunities
- Emerging trends and technologies
- Market timing assessment
- Success factors and critical success factors
- Market validation approach

### 9. RISKS & CHALLENGES
- Market risks and uncertainties
- Technical challenges and limitations
- Competitive threats
- Regulatory and compliance risks
- Resource and execution risks

### 10. RECOMMENDATIONS & NEXT STEPS
- Strategic recommendations
- Feature roadmap priorities
- Development timeline
- Success metrics and KPIs
- Risk mitigation strategies

## OUTPUT FORMAT
Return your analysis as a JSON object with the following structure:
{{
    "target_audience": "Detailed target audience analysis...",
    "competitors": "Comprehensive competitive analysis...",
    "market_size": "Market size estimates and opportunity...",
    "key_features": "Feature analysis and prioritization...",
    "api_sources": "API and data source requirements...",
    "data_sources": "Data dependencies and sources...",
    "business_model": "Business model recommendations...",
    "go_to_market": "Go-to-market strategy...",
    "market_opportunity": "Market opportunity assessment...",
    "risks": "Risk analysis and challenges...",
    "recommendations": "Strategic recommendations...",
    "success_metrics": "Success metrics and KPIs..."
}}

Ensure all sections are comprehensive, actionable, and based on the research data provided.
"""
        
        return await self._generate_analysis_with_fallback(analysis_prompt)
    
    async def _validate_and_enhance_analysis(self, project_name: str, description: str, analysis: Dict[str, Any], research_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate and enhance the analysis with additional insights"""
        
        validation_prompt = f"""
You are a senior market research director reviewing a market analysis report. Validate and enhance the following analysis:

## PROJECT CONTEXT
**Project Name:** {project_name}
**Description:** {description}

## CURRENT ANALYSIS
{json.dumps(analysis, indent=2)}

## VALIDATION TASK
1. **Validate Completeness**: Ensure all required sections are present and comprehensive
2. **Validate Accuracy**: Check if analysis aligns with current market realities
3. **Enhance Insights**: Add missing insights and improve existing ones
4. **Improve Actionability**: Make recommendations more specific and implementable
5. **Add Market Intelligence**: Include additional market intelligence and trends

## ENHANCEMENT FOCUS AREAS
- Market timing and opportunity windows
- Competitive positioning strategies
- Technical differentiation opportunities
- Customer acquisition strategies
- Risk mitigation approaches
- Success probability factors

## OUTPUT FORMAT
Return the enhanced analysis as a JSON object with the same structure as the input, but with improved content, additional insights, and more actionable recommendations.

Focus on making the analysis more comprehensive, accurate, and actionable for product development and go-to-market planning.
"""
        
        enhanced_analysis = await self._generate_analysis_with_fallback(validation_prompt)
        
        # Merge with original analysis, preferring enhanced content
        final_analysis = analysis.copy()
        for key, value in enhanced_analysis.items():
            if value and value != "Analysis failed":
                final_analysis[key] = value
        
        return final_analysis
    
    async def _generate_analysis_with_fallback(self, prompt: str) -> Dict[str, Any]:
        """Generate analysis with multi-LLM fallback"""
        
        messages = [
            SystemMessage(content="You are a senior market research analyst. Provide comprehensive, actionable market insights in JSON format."),
            HumanMessage(content=prompt)
        ]
        
        # Try primary LLM first
        try:
            print(f"    🔄 Generating analysis with DeepSeek...")
            response = await self.primary_llm.agenerate([messages])
            
            if response.generations and response.generations[0]:
                analysis_text = response.generations[0][0].text
                analysis = self._parse_analysis_response(analysis_text)
                if analysis and not self._is_fallback_response(analysis):
                    print(f"    ✅ Analysis generated successfully with DeepSeek")
                    return analysis
            
        except Exception as e:
            print(f"    ⚠️ DeepSeek analysis failed: {e}")
        
        # Try backup LLMs
        for i, backup_llm in enumerate(self.backup_llms):
            try:
                llm_name = "Gemini Pro" if i == 0 else "GPT-3.5 Turbo"
                print(f"    🔄 Trying {llm_name} for analysis...")
                
                response = await backup_llm.agenerate([messages])
                
                if response.generations and response.generations[0]:
                    analysis_text = response.generations[0][0].text
                    analysis = self._parse_analysis_response(analysis_text)
                    if analysis and not self._is_fallback_response(analysis):
                        print(f"    ✅ Analysis generated successfully with {llm_name}")
                        return analysis
                        
            except Exception as e:
                print(f"    ⚠️ {llm_name} analysis failed: {e}")
        
        # Return fallback analysis
        print(f"    ⚠️ All LLMs failed, using fallback analysis")
        return self._create_fallback_analysis()
    
    def _parse_analysis_response(self, analysis_text: str) -> Dict[str, Any]:
        """Parse analysis response, handling various formats"""
        
        # Try to extract JSON
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Try to parse as JSON directly
        try:
            return json.loads(analysis_text)
        except json.JSONDecodeError:
            pass
        
        # Extract sections manually
        return self._extract_sections_manually(analysis_text)
    
    def _extract_sections_manually(self, text: str) -> Dict[str, str]:
        """Extract analysis sections manually from text"""
        sections = {
            "target_audience": "",
            "competitors": "",
            "market_size": "",
            "key_features": "",
            "api_sources": "",
            "data_sources": "",
            "business_model": "",
            "go_to_market": "",
            "market_opportunity": "",
            "risks": "",
            "recommendations": "",
            "success_metrics": ""
        }
        
        # Section patterns to look for
        section_patterns = {
            "target_audience": r"(?:target audience|user personas?|demographics?)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "competitors": r"(?:competitors?|competitive landscape|competition)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "market_size": r"(?:market size|TAM|SAM|SOM|market opportunity)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "key_features": r"(?:key features?|features?|differentiation)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "api_sources": r"(?:API|apis?|data sources?|integrations?)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "data_sources": r"(?:data sources?|data dependencies?|databases?)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "business_model": r"(?:business model|monetization|pricing|revenue)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "go_to_market": r"(?:go.?to.?market|GTM|marketing|acquisition)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "market_opportunity": r"(?:market opportunity|opportunity|timing)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "risks": r"(?:risks?|challenges?|threats?)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "recommendations": r"(?:recommendations?|next steps?|strategy)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))",
            "success_metrics": r"(?:success metrics?|KPIs?|metrics?)(?:\s*:|\s*\n)(.*?)(?=\n\s*(?:[A-Z][A-Z\s]+:|\Z))"
        }
        
        for section, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section] = match.group(1).strip()
        
        return sections
    
    def _create_comprehensive_summary(self, research_data: List[Dict[str, Any]]) -> str:
        """Create comprehensive summary of research data"""
        summary_parts = []
        
        # Group by research category
        by_category = {}
        for result in research_data:
            category = result.get("research_category", "general")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(result)
        
        # Create summary for each category
        for category, results in by_category.items():
            summary_parts.append(f"\n## {category.upper().replace('_', ' ')} RESEARCH")
            
            for i, result in enumerate(results[:5], 1):  # Top 5 per category
                title = result.get("title", "No title")
                content = result.get("content", "No content")
                url = result.get("url", "No URL")
                
                summary_parts.append(f"\n### Source {i}: {title}")
                summary_parts.append(f"**URL:** {url}")
                summary_parts.append(f"**Content:** {content[:300]}...")
        
        return "\n".join(summary_parts)
    
    def _is_fallback_response(self, analysis: Dict[str, Any]) -> bool:
        """Check if the analysis is a fallback/error response"""
        if not analysis:
            return True
        
        # Check for fallback indicators
        fallback_indicators = [
            "analysis failed", "error", "unable to", "cannot", "failed to",
            "not available", "insufficient data", "no information"
        ]
        
        for value in analysis.values():
            if isinstance(value, str):
                value_lower = value.lower()
                if any(indicator in value_lower for indicator in fallback_indicators):
                    return True
        
        return False
    
    def _create_fallback_analysis(self) -> Dict[str, str]:
        """Create a basic fallback analysis"""
        return {
            "target_audience": "Primary: Tech-savvy professionals and businesses seeking AI solutions. Secondary: General users interested in productivity tools.",
            "competitors": "Direct competitors include established AI platforms and similar productivity tools. Indirect competitors include traditional software solutions.",
            "market_size": "The AI market is growing rapidly with significant opportunities in productivity and automation sectors.",
            "key_features": "Core functionality should focus on user experience, AI integration, and productivity enhancement features.",
            "api_sources": "Requires AI/ML APIs, authentication services, and data processing capabilities.",
            "data_sources": "User data, analytics data, and potentially third-party data sources for enhanced functionality.",
            "business_model": "SaaS subscription model with freemium tier and premium features.",
            "go_to_market": "Digital-first approach with content marketing, partnerships, and direct sales for enterprise.",
            "market_opportunity": "Strong market opportunity with growing demand for AI-powered productivity tools.",
            "risks": "Competitive pressure, technical challenges, and market adoption risks.",
            "recommendations": "Focus on unique value proposition, rapid iteration, and strong user experience.",
            "success_metrics": "User acquisition, retention rates, revenue growth, and market share."
        }
    
    def _calculate_research_quality_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate research quality score (0-100)"""
        score = 0
        max_score = 100
        
        # Check completeness (60 points)
        required_sections = [
            "target_audience", "competitors", "market_size", "key_features",
            "api_sources", "data_sources", "business_model", "go_to_market",
            "market_opportunity", "risks", "recommendations", "success_metrics"
        ]
        
        for section in required_sections:
            content = analysis.get(section, "")
            if content and content != "Analysis failed" and len(content) > 50:
                score += 5  # 5 points per complete section
        
        # Check quality indicators (40 points)
        quality_indicators = [
            "detailed", "comprehensive", "specific", "actionable",
            "market", "competitive", "strategy", "recommendations"
        ]
        
        for value in analysis.values():
            if isinstance(value, str):
                value_lower = value.lower()
                for indicator in quality_indicators:
                    if indicator in value_lower:
                        score += 1
        
        return min(score, max_score)
