from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import asyncio
from dotenv import load_dotenv

# Import our custom modules
from services.code_analyzer import CodeAnalyzer
from services.security_scanner import SecurityScanner
from services.ai_insights import AIInsightsService
from services.performance_analyzer import PerformanceAnalyzer
from models.database import get_db, init_db
from models.schemas import (
    CodeAnalysisRequest,
    CodeAnalysisResponse,
    SecurityScanRequest,
    SecurityScanResponse,
    PerformanceAnalysisRequest,
    PerformanceAnalysisResponse,
    AIInsightsRequest,
    AIInsightsResponse
)

load_dotenv()

app = FastAPI(
    title="AI Code Review Assistant API",
    description="Automated code analysis, security vulnerability detection, and performance optimization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
code_analyzer = CodeAnalyzer()
security_scanner = SecurityScanner()
ai_insights = AIInsightsService()
performance_analyzer = PerformanceAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    await init_db()
    print("🚀 AI Code Review Assistant API started")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Code Review Assistant API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/analyze/code", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code for quality, complexity, and best practices
    """
    try:
        analysis = await code_analyzer.analyze(
            code=request.code,
            language=request.language,
            file_path=request.file_path
        )
        
        return CodeAnalysisResponse(
            success=True,
            analysis=analysis,
            message="Code analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/scan/security", response_model=SecurityScanResponse)
async def scan_security(request: SecurityScanRequest):
    """
    Scan code for security vulnerabilities
    """
    try:
        vulnerabilities = await security_scanner.scan(
            code=request.code,
            language=request.language,
            scan_type=request.scan_type
        )
        
        return SecurityScanResponse(
            success=True,
            vulnerabilities=vulnerabilities,
            risk_score=security_scanner.calculate_risk_score(vulnerabilities),
            message="Security scan completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security scan failed: {str(e)}")

@app.post("/analyze/performance", response_model=PerformanceAnalysisResponse)
async def analyze_performance(request: PerformanceAnalysisRequest):
    """
    Analyze code for performance issues and optimization opportunities
    """
    try:
        performance_issues = await performance_analyzer.analyze(
            code=request.code,
            language=request.language,
            context=request.context
        )
        
        return PerformanceAnalysisResponse(
            success=True,
            issues=performance_issues,
            optimization_score=performance_analyzer.calculate_optimization_score(performance_issues),
            message="Performance analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance analysis failed: {str(e)}")

@app.post("/insights/ai", response_model=AIInsightsResponse)
async def get_ai_insights(request: AIInsightsRequest):
    """
    Get AI-powered insights and suggestions for code improvement
    """
    try:
        insights = await ai_insights.generate_insights(
            code=request.code,
            analysis_results=request.analysis_results,
            focus_areas=request.focus_areas
        )
        
        return AIInsightsResponse(
            success=True,
            insights=insights,
            message="AI insights generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI insights generation failed: {str(e)}")

@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a code file for analysis
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs')):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Read file content
        content = await file.read()
        code = content.decode('utf-8')
        
        # Determine language from file extension
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust'
        }
        
        language = language_map.get(os.path.splitext(file.filename)[1], 'unknown')
        
        # Perform comprehensive analysis
        analysis_tasks = [
            code_analyzer.analyze(code, language, file.filename),
            security_scanner.scan(code, language, 'comprehensive'),
            performance_analyzer.analyze(code, language, {}),
        ]
        
        results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        return {
            "success": True,
            "filename": file.filename,
            "language": language,
            "file_size": len(content),
            "analysis": {
                "code_quality": results[0] if not isinstance(results[0], Exception) else None,
                "security": results[1] if not isinstance(results[1], Exception) else None,
                "performance": results[2] if not isinstance(results[2], Exception) else None,
            },
            "message": "File analysis completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@app.get("/languages/supported")
async def get_supported_languages():
    """
    Get list of supported programming languages
    """
    return {
        "languages": [
            {"name": "Python", "extension": ".py", "features": ["security", "performance", "quality"]},
            {"name": "JavaScript", "extension": ".js", "features": ["security", "performance", "quality"]},
            {"name": "TypeScript", "extension": ".ts", "features": ["security", "performance", "quality"]},
            {"name": "Java", "extension": ".java", "features": ["security", "performance", "quality"]},
            {"name": "C++", "extension": ".cpp", "features": ["security", "performance", "quality"]},
            {"name": "C", "extension": ".c", "features": ["security", "performance", "quality"]},
            {"name": "Go", "extension": ".go", "features": ["security", "performance", "quality"]},
            {"name": "Rust", "extension": ".rs", "features": ["security", "performance", "quality"]},
        ]
    }

@app.get("/health")
async def health_check():
    """
    Comprehensive health check
    """
    health_status = {
        "status": "healthy",
        "services": {
            "code_analyzer": "operational",
            "security_scanner": "operational", 
            "ai_insights": "operational",
            "performance_analyzer": "operational"
        },
        "environment": {
            "openai_key": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
            "anthropic_key": "configured" if os.getenv("ANTHROPIC_API_KEY") else "missing",
            "database": "connected"
        }
    }
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
