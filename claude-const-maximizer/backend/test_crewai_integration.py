#!/usr/bin/env python3
"""
Test to check if the expert profile system works in the actual CrewAI environment.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crew_app.crew import kickoff_with_retries
    print("✅ CrewAI integration import successful")
    
    # Test with a simple project name
    project_name = "Universal Rag Chatbot"
    print(f"Testing kickoff_with_retries with project: {project_name}")
    
    # This should call the expert profile system
    result = kickoff_with_retries(max_retries=1, project_name=project_name)
    
    print(f"Result length: {len(result)}")
    print(f"Result starts with 'You are an expert': {result.startswith('You are an expert')}")
    print(f"First 300 chars: {result[:300]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
