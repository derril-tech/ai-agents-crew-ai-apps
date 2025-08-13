# backend/api/middleware/auth.py
"""
Authentication middleware
"""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
import os

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = ["/", "/api/health", "/api/docs", "/api/redoc", "/api/auth/token", "/api/auth/google"]
        
        if any(request.url.path.startswith(path) for path in public_paths):
            response = await call_next(request)
            return response
        
        # Check for WebSocket
        if request.url.path.startswith("/ws/"):
            response = await call_next(request)
            return response
        
        # Verify JWT token for API endpoints
        if request.url.path.startswith("/api/"):
            authorization = request.headers.get("Authorization")
            
            if not authorization or not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing or invalid authorization header"}
                )
            
            token = authorization.split(" ")[1]
            
            try:
                from ..routes.auth import SECRET_KEY, ALGORITHM
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = payload.get("sub")
            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"}
                )
        
        response = await call_next(request)
        return response


# backend/api/middleware/logging.py
"""
Logging middleware
"""

import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Duration: {duration:.3f}s"
        )
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(duration)
        
        return response


# backend/api/middleware/cors.py
"""
CORS middleware configuration
"""

from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    """Setup CORS middleware"""
    import os
    
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"]
    )