from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from .database import get_db, engine
from .models import Base
from .schemas import UserCreate, User, Token, TokenData
from .auth import create_access_token, get_current_user, verify_password
from .crud import get_user_by_email, create_user
from .routers import auth, users, chat

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI SaaS Backend",
    description="Modern FastAPI backend with authentication and AI integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "FastAPI SaaS Backend is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user_id": current_user.id,
        "email": current_user.email
    }
