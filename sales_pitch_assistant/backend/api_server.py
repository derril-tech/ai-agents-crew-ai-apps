#!/usr/bin/env python
import json
import warnings
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import the crew after loading environment variables
from sales_meeting_preparation.crew import SalesMeetingPreparation

app = FastAPI(title="AI Sales Pitch Assistant API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SalesPitchRequest(BaseModel):
    person: str
    company: str

@app.get("/")
async def root():
    return {"message": "AI Sales Pitch Assistant API is running"}

@app.post("/api/generate-sales-pitch")
async def generate_sales_pitch(request: SalesPitchRequest):
    """
    Generate a sales pitch report for the given person and company.
    """
    try:
        print(f"🔧 Generating sales pitch for {request.person} at {request.company}")
        
        inputs = {
            'person': request.person,
            'company': request.company,
            'meeting_date': datetime.now().strftime('%Y-%m-%d'),
            'product_service': 'AI Development Platform'
        }
        
        print("🔧 Initializing SalesMeetingPreparation...")
        sales_crew = SalesMeetingPreparation()
        print("🔧 Creating crew...")
        crew = sales_crew.crew()
        print("🔧 Starting crew execution...")
        result = crew.kickoff(inputs=inputs)
        
        # Try to extract final output from known CrewAI formats
        final_output = None
        if hasattr(result, "final_output"):
            final_output = result.final_output
        elif hasattr(result, "output"):
            final_output = result.output
        elif isinstance(result, str):
            final_output = result
        else:
            final_output = str(result)
        
        if final_output:
            # Create outputs directory if it doesn't exist
            Path("outputs").mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"sales_meeting_prep_{inputs['company'].lower().replace(' ', '_')}_{timestamp}.md"
            filepath = f"outputs/{filename}"
            
            # Save to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_output)
            
            print(f"✅ Report saved to {filepath}")
            
            # Return response for frontend
            response = {
                "success": True,
                "report": final_output,
                "filename": filename,
                "filepath": filepath,
                "person": request.person,
                "company": request.company,
                "timestamp": timestamp
            }
            
            return response
        else:
            raise HTTPException(status_code=500, detail="No output content returned.")
            
    except Exception as e:
        print(f"❌ Error generating sales pitch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Starting AI Sales Pitch Assistant API server...")
    print("📡 Server will be available at http://localhost:3001")
    print("🌐 Frontend should be running at http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=3001, reload=False)
