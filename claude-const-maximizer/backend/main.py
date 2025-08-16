from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio
import subprocess
from pathlib import Path
from functools import partial

app = FastAPI(title="60 AI Apps Pipeline API", version="1.0.0")

# Add CORS middleware to allow frontend requests
DEV_ORIGINS = [
    "http://localhost:3000", "http://localhost:3001",
    "http://127.0.0.1:3000", "http://127.0.0.1:3001",
    "http://localhost:5173", "http://0.0.0.0:3000", "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use __file__ to get absolute paths that work regardless of working directory
BASE_DIR = Path(__file__).parent.parent
PIPELINE_TODOS_PATH = BASE_DIR / "frontend" / "dashboard" / "lib" / "pipeline-todos.json"
PROJECTS_PATH = BASE_DIR / "projects.json"

async def read_json_file_safe(file_path: Path, default_value):
    """Safely read JSON file with async I/O and graceful error handling"""
    try:
        if not file_path.exists():
            return default_value
        
        # Run file read in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file_path.read_text, "utf-8")
        
        if not content.strip():
            return default_value
            
        data = await loop.run_in_executor(None, json.loads, content)
        return data
        
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Warning: Invalid JSON in {file_path}: {e}")
        return default_value
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}")
        return default_value

async def run_pipeline_command():
    """Run the pipeline command asynchronously"""
    try:
        # Run the pipeline command in a thread pool
        loop = asyncio.get_event_loop()
        
        def run_subprocess():
            return subprocess.run(
                ["python", "phase3_research_prompt_code.py", "--test", "--step5-only"],
                cwd=Path(__file__).parent,  # Run from backend directory where the file is
                capture_output=True,
                text=True
            )
        
        result = await loop.run_in_executor(None, run_subprocess)
        
        print(f"Pipeline command completed with return code: {result.returncode}")
        print(f"Pipeline output: {result.stdout}")
        if result.stderr:
            print(f"Pipeline errors: {result.stderr}")
            
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.stderr else None
        }
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

@app.get("/")
async def root():
    return {"message": "60 AI Apps Pipeline API", "status": "running"}

@app.post("/api/run-pipeline")
async def run_pipeline():
    """Run the pipeline command"""
    print("[START] Starting pipeline execution...")
    result = await run_pipeline_command()
    print(f"[COMPLETE] Pipeline execution completed: {result['success']}")
    return result

@app.post("/api/stop-pipeline")
async def stop_pipeline():
    """Stop the pipeline and clear active agents"""
    print("[STOP] Stopping pipeline and clearing active agents...")
    
    try:
        # Clear the pipeline todos file
        if PIPELINE_TODOS_PATH.exists():
            # Read current data and clear activeAgents
            data = await read_json_file_safe(PIPELINE_TODOS_PATH, {})
            
            # Clear activeAgents from all projects
            for project_id in data:
                if isinstance(data[project_id], dict) and 'activeAgents' in data[project_id]:
                    data[project_id]['activeAgents'] = []
            
            # Write back the cleared data
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: PIPELINE_TODOS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8"))
            
            print("[STOP] Pipeline data cleared successfully")
            return {"success": True, "message": "Pipeline stopped and active agents cleared"}
        else:
            return {"success": True, "message": "No pipeline data to clear"}
            
    except Exception as e:
        print(f"[ERROR] Failed to stop pipeline: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/pipeline")
async def get_pipeline_data():
    """Get the current pipeline todos data"""
    try:
        data = await read_json_file_safe(PIPELINE_TODOS_PATH, {})
        return {"items": data} if data else {"items": {}}
    except Exception as e:
        print(f"Error in pipeline endpoint: {e}")
        return {"items": {}}

@app.get("/api/projects")
async def get_projects():
    """Get the projects list"""
    try:
        projects = await read_json_file_safe(PROJECTS_PATH, [])
        
        if not projects:
            # Return sample data if projects.json doesn't exist or is empty
            return [
                {
                    "project_name": "AI-Powered Code Review & Refactoring Assistant",
                    "description": "Automated code analysis, security vulnerability detection, performance optimization suggestions",
                    "tech_stack": "Python, FastAPI, React, OpenAI/Claude API",
                    "why_impressive": "Shows full-stack development, AI integration, and understanding of software engineering best practices"
                },
                {
                    "project_name": "Intelligent Document Processing & Knowledge Base",
                    "description": "Multi-format document ingestion, semantic search, automated summarization, Q&A system",
                    "tech_stack": "Python, LangChain, Vector DB, React, FastAPI",
                    "why_impressive": "Demonstrates RAG architecture, vector embeddings, and enterprise-level document management"
                }
            ]
        
        return projects
        
    except Exception as e:
        print(f"Error in projects endpoint: {e}")
        return []

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "pipeline_file_exists": PIPELINE_TODOS_PATH.exists(),
        "projects_file_exists": PROJECTS_PATH.exists(),
        "pipeline_file_size": PIPELINE_TODOS_PATH.stat().st_size if PIPELINE_TODOS_PATH.exists() else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
