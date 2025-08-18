#!/usr/bin/env python3
"""
Simple debug test for role establishment.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crew_app.expert_profiles import detect_project_category, get_expert_profile, create_role_establishment
    print("✅ Imports successful")
    
    project_name = "Universal Rag Chatbot"
    print(f"Testing project: {project_name}")
    
    category = detect_project_category(project_name)
    print(f"Category: {category}")
    
    expert_profile = get_expert_profile(project_name)
    print(f"Expert title: {expert_profile['title']}")
    
    role_establishment = create_role_establishment(project_name)
    print(f"Role establishment length: {len(role_establishment)}")
    print(f"First 200 chars: {role_establishment[:200]}")
    
    if "You are an expert" in role_establishment:
        print("✅ Role establishment contains 'You are an expert'")
    else:
        print("❌ Role establishment missing 'You are an expert'")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
