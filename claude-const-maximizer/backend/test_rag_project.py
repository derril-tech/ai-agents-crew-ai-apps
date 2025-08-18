#!/usr/bin/env python3
"""
Test to debug the missing role establishment for "Universal Rag Chatbot".
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew_app.expert_profiles import (
    detect_project_category, 
    get_expert_profile, 
    create_role_establishment,
    create_perfect_one_page_document
)

def test_rag_project():
    project_name = "Universal Rag Chatbot"
    
    print(f"🧪 Testing project: {project_name}")
    print("="*80)
    
    # Test category detection
    category = detect_project_category(project_name)
    print(f"Detected category: {category}")
    
    # Test expert profile
    expert_profile = get_expert_profile(project_name)
    print(f"Expert title: {expert_profile['title']}")
    print(f"Psychological approach: {expert_profile.get('psychological_approach', 'NOT FOUND')[:100]}...")
    
    # Test role establishment
    role_establishment = create_role_establishment(project_name)
    print(f"\nRole establishment (first 200 chars):")
    print(f"{role_establishment[:200]}...")
    print(f"Role establishment length: {len(role_establishment)}")
    
    # Test full document creation
    sample_raw_output = """
    # Universal Rag Chatbot
    
    ## Project Overview
    This is a test project overview.
    
    ## Target Audience
    Software developers and tech professionals
    """
    
    full_document = create_perfect_one_page_document(project_name, sample_raw_output)
    print(f"\nFull document (first 500 chars):")
    print(f"{full_document[:500]}...")
    print(f"Full document length: {len(full_document)}")
    
    # Check if role establishment is in the full document
    if "You are an expert" in full_document:
        print("✅ Role establishment found in full document!")
    else:
        print("❌ Role establishment NOT found in full document!")

if __name__ == "__main__":
    test_rag_project()
