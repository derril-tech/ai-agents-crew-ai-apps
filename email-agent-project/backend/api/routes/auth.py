# backend/api/routes/auth.py
"""
Authentication routes for Gmail OAuth and API authentication
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

router = APIRouter()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Google OAuth settings
GOOGLE_CLIENT_SECRETS = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SCOPES = os.getenv("GMAIL_SCOPES", "").split(",")
REDIRECT_URI = f"http://localhost:{os.getenv('API_PORT', 8000)}/api/auth/google/callback"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_email: str


class GoogleAuthRequest(BaseModel):
    return_url: Optional[str] = "/"


class ConfigureKeysRequest(BaseModel):
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email, "user_id": payload.get("user_id")}
    except JWTError:
        raise credentials_exception


@router.post("/google", response_model=Dict[str, str])
async def google_auth(request: GoogleAuthRequest):
    """
    Initiate Google OAuth flow for Gmail access
    """
    try:
        # Create flow instance
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS,
            scopes=GOOGLE_SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session (in production, use proper session storage)
        # For now, we'll pass it through the URL
        return {
            "authorization_url": authorization_url,
            "state": state,
            "message": "Redirect user to authorization_url"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth initialization failed: {str(e)}")


@router.get("/google/callback")
async def google_callback(code: str, state: str, request: Request):
    """
    Handle Google OAuth callback
    """
    try:
        # Create flow instance
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS,
            scopes=GOOGLE_SCOPES,
            redirect_uri=REDIRECT_URI,
            state=state
        )
        
        # Exchange authorization code for tokens
        flow.fetch_token(code=code)
        
        # Get credentials
        credentials = flow.credentials
        
        # Save credentials to file
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        with open('token.json', 'w') as token_file:
            json.dump(token_data, token_file)
        
        # Get user email
        service = build('gmail', 'v1', credentials=credentials)
        profile = service.users().getProfile(userId='me').execute()
        user_email = profile['emailAddress']
        
        # Create JWT token for our app
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_email, "user_id": user_email},
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        redirect_url = f"http://localhost:3000/dashboard?token={access_token}&email={user_email}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint for API access (simplified for development)
    """
    # In production, verify against database
    # For now, check if email matches configured email
    if form_data.username != os.getenv("MY_EMAIL"):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "user_id": form_data.username},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_email=form_data.username
    )


@router.get("/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "email": current_user["email"],
        "authenticated": True,
        "gmail_connected": os.path.exists("token.json")
    }


@router.post("/logout")
async def logout(response: Response):
    """Logout endpoint"""
    # In production, invalidate token in database
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.post("/config/keys")
async def configure_api_keys(
    config: ConfigureKeysRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Configure API keys (stored securely in production)
    """
    updated = []
    
    # In production, encrypt and store in database
    # For development, update environment variables
    
    if config.openai_api_key:
        os.environ["OPENAI_API_KEY"] = config.openai_api_key
        updated.append("OpenAI")
    
    if config.google_api_key:
        os.environ["GOOGLE_API_KEY"] = config.google_api_key
        updated.append("Google")
    
    if config.serper_api_key:
        os.environ["SERPER_API_KEY"] = config.serper_api_key
        updated.append("Serper")
    
    if config.tavily_api_key:
        os.environ["TAVILY_API_KEY"] = config.tavily_api_key
        updated.append("Tavily")
    
    return {
        "message": f"API keys updated for: {', '.join(updated)}",
        "updated": updated
    }


@router.get("/config/status")
async def get_config_status(current_user: Dict = Depends(get_current_user)):
    """Check configuration status"""
    return {
        "gmail_connected": os.path.exists("token.json"),
        "api_keys": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY")),
            "serper": bool(os.getenv("SERPER_API_KEY")),
            "tavily": bool(os.getenv("TAVILY_API_KEY"))
        },
        "user_email": os.getenv("MY_EMAIL")
    }


@router.post("/refresh-gmail-token")
async def refresh_gmail_token(current_user: Dict = Depends(get_current_user)):
    """Refresh Gmail OAuth token"""
    try:
        if not os.path.exists('token.json'):
            raise HTTPException(status_code=400, detail="No Gmail token found")
        
        creds = Credentials.from_authorized_user_file('token.json', GOOGLE_SCOPES)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            
            # Save refreshed token
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            
            return {"message": "Gmail token refreshed successfully"}
        else:
            return {"message": "Token is still valid"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")