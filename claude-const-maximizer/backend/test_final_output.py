#!/usr/bin/env python3
"""
Test to check what create_perfect_one_page_document actually returns.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crew_app.expert_profiles import create_perfect_one_page_document
    print("✅ Import successful")
    
    project_name = "Ai Meeting Notes And Action Items"
    
    # Sample raw output similar to what CrewAI generates
    sample_raw_output = """
    ---
    
    # **Project Overview: AI Application for Claude-Optimized Content Creation**
    
    **Project Objective**
    Develop an AI-driven application enabling users to effortlessly create Claude-optimized content through a seamless, user-friendly interface.
    
    **Target Audience**
    - **Demographics**: Content creators, digital marketers, and SMEs aged 25-45
    """
    
    print(f"Testing with project: {project_name}")
    print(f"Sample raw output length: {len(sample_raw_output)}")
    
    # Call the function
    result = create_perfect_one_page_document(project_name, sample_raw_output)
    
    print(f"\nResult length: {len(result)}")
    print(f"Result starts with 'You are an expert': {result.startswith('You are an expert')}")
    print(f"\nFirst 500 characters:")
    print("="*50)
    print(result[:500])
    print("="*50)
    
    # Check for role establishment
    if "You are an expert" in result:
        print("✅ Role establishment found!")
    else:
        print("❌ Role establishment NOT found!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
