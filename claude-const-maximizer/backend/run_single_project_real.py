#!/usr/bin/env python3
"""
Real CrewAI Pipeline Runner for Single Project
This script runs the actual CrewAI agents for a single project.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crew_app.crew import crew

# Load environment variables
load_dotenv()

def run_single_project(project_name: str):
    """
    Run the real CrewAI pipeline for a single project
    """
    print(f"🚀 Starting REAL CrewAI pipeline for: {project_name}")
    
    try:
        # Run the crew for this specific project
        result = crew.kickoff({
            "project_name": project_name,
            "description": f"Create a comprehensive AI application for: {project_name}",
            "requirements": "Full-stack application with frontend, backend, and AI integration"
        })
        
        print(f"✅ CrewAI pipeline completed for: {project_name}")
        print(f"📊 Result: {result}")
        
        return {
            "success": True,
            "project_name": project_name,
            "result": result
        }
        
    except Exception as e:
        print(f"❌ CrewAI pipeline failed for {project_name}: {e}")
        return {
            "success": False,
            "project_name": project_name,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_single_project_real.py 'Project Name'")
        sys.exit(1)
    
    project_name = sys.argv[1]
    result = run_single_project(project_name)
    print(json.dumps(result, indent=2))


