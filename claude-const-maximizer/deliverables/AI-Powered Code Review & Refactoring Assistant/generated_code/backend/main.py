from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Code Review API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Code Review API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}