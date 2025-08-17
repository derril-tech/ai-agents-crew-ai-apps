"""
AI-Powered Resume Parser & Job Matcher - FastAPI Application
Main application entry point with all endpoints and configurations
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import logging
from contextlib import asynccontextmanager
from typing import List, Optional

# Import our modules
from app.config.settings import Settings
from app.config.database import init_db, get_db
from app.models.resume import Resume, ResumeCreate, ResumeResponse
from app.models.job import Job, JobCreate, JobResponse
from app.models.user import User, UserCreate, UserResponse
from app.services.resume_parser import ResumeParserService
from app.services.job_matcher import JobMatcherService
from app.services.ai_service import AIService
from app.services.auth_service import AuthService
from app.utils.logging import setup_logging
from app.utils.rate_limiter import RateLimiter

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Rate limiter
rate_limiter = RateLimiter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Resume Parser & Job Matcher API...")
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Resume Parser & Job Matcher API...")

# Create FastAPI app
app = FastAPI(
    title="AI Resume Parser & Job Matcher API",
    description="Intelligent resume parsing, skill extraction, job matching algorithm, and interview preparation suggestions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Load settings
settings = Settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Initialize services
resume_parser_service = ResumeParserService()
job_matcher_service = JobMatcherService()
ai_service = AIService()
auth_service = AuthService()

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    try:
        user = await auth_service.verify_token(credentials.credentials)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Resume Parser & Job Matcher API",
        "version": "1.0.0"
    }

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await auth_service.register_user(user_data)
        return user
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
async def login_user(user_data: UserCreate):
    """Login user and return access token"""
    try:
        token = await auth_service.login_user(user_data)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Resume parsing endpoints
@app.post("/resumes/upload", response_model=ResumeResponse)
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload and parse a resume"""
    try:
        # Rate limiting
        await rate_limiter.check_rate_limit(f"upload:{current_user.id}")
        
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and DOC files are allowed")
        
        # Parse resume in background
        background_tasks.add_task(resume_parser_service.parse_resume_async, file, current_user.id)
        
        return {
            "message": "Resume uploaded successfully. Processing in background.",
            "filename": file.filename,
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Resume upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resumes", response_model=List[ResumeResponse])
async def get_user_resumes(current_user: User = Depends(get_current_user)):
    """Get all resumes for the current user"""
    try:
        resumes = await resume_parser_service.get_user_resumes(current_user.id)
        return resumes
    except Exception as e:
        logger.error(f"Get resumes error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, current_user: User = Depends(get_current_user)):
    """Get a specific resume by ID"""
    try:
        resume = await resume_parser_service.get_resume(resume_id, current_user.id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except Exception as e:
        logger.error(f"Get resume error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Job matching endpoints
@app.post("/jobs/match", response_model=List[JobResponse])
async def match_jobs(
    resume_id: int,
    location: Optional[str] = None,
    remote: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """Match jobs based on resume skills and preferences"""
    try:
        # Rate limiting
        await rate_limiter.check_rate_limit(f"match:{current_user.id}")
        
        jobs = await job_matcher_service.match_jobs(
            resume_id=resume_id,
            user_id=current_user.id,
            location=location,
            remote=remote
        )
        return jobs
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/search")
async def search_jobs(
    query: str,
    location: Optional[str] = None,
    remote: Optional[bool] = None,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Search for jobs using external APIs"""
    try:
        # Rate limiting
        await rate_limiter.check_rate_limit(f"search:{current_user.id}")
        
        jobs = await job_matcher_service.search_jobs(
            query=query,
            location=location,
            remote=remote,
            limit=limit
        )
        return jobs
    except Exception as e:
        logger.error(f"Job search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# AI-powered features
@app.post("/ai/analyze-resume")
async def analyze_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered analysis of resume"""
    try:
        analysis = await ai_service.analyze_resume(resume_id, current_user.id)
        return analysis
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/generate-cover-letter")
async def generate_cover_letter(
    resume_id: int,
    job_description: str,
    current_user: User = Depends(get_current_user)
):
    """Generate AI-powered cover letter"""
    try:
        cover_letter = await ai_service.generate_cover_letter(
            resume_id=resume_id,
            job_description=job_description,
            user_id=current_user.id
        )
        return {"cover_letter": cover_letter}
    except Exception as e:
        logger.error(f"Cover letter generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/interview-prep")
async def generate_interview_prep(
    resume_id: int,
    job_id: str,
    current_user: User = Depends(get_current_user)
):
    """Generate interview preparation suggestions"""
    try:
        prep_materials = await ai_service.generate_interview_prep(
            resume_id=resume_id,
            job_id=job_id,
            user_id=current_user.id
        )
        return prep_materials
    except Exception as e:
        logger.error(f"Interview prep generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Skills and insights endpoints
@app.get("/skills/extract")
async def extract_skills(
    resume_id: int,
    current_user: User = Depends(get_current_user)
):
    """Extract skills from resume"""
    try:
        skills = await resume_parser_service.extract_skills(resume_id, current_user.id)
        return {"skills": skills}
    except Exception as e:
        logger.error(f"Skills extraction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights/resume-score")
async def get_resume_score(
    resume_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered resume score and insights"""
    try:
        score = await ai_service.score_resume(resume_id, current_user.id)
        return score
    except Exception as e:
        logger.error(f"Resume scoring error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
