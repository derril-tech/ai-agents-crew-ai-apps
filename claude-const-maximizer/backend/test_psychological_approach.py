#!/usr/bin/env python3
"""
Quick test to see the psychological approach in action.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew_app.expert_profiles import create_role_establishment, get_expert_profile

def test_psychological_approach():
    print("🧠 Testing Psychological Approach Integration...")
    
    # Test with a few different project types
    test_projects = [
        "AI-Powered Personal Voice Assistant & Calendar Manager",
        "Multi-Agent Content Creation & Marketing System", 
        "Intelligent Document Processing & Knowledge Base",
        "AI-Powered Video Content Generator",
        "AI-Powered Medical Diagnosis Assistant",
        "Intelligent E-commerce Management System",
        "AI-Powered Code Review & Refactoring Assistant",
        "Web Scraping & Data Aggregation Platform"
    ]
    
    for project in test_projects:
        print(f"\n{'='*80}")
        print(f"PROJECT: {project}")
        print(f"{'='*80}")
        
        # Get the expert profile
        expert_profile = get_expert_profile(project)
        print(f"Expert Title: {expert_profile['title']}")
        print(f"Psychological Approach: {expert_profile.get('psychological_approach', 'NOT FOUND')[:100]}...")
        
        # Generate the role establishment
        role_establishment = create_role_establishment(project)
        print(f"\nROLE ESTABLISHMENT (First 300 chars):")
        print(f"{role_establishment[:300]}...")
        
        # Check if psychological elements are present
        psychological_keywords = ["revolutionary", "prestige", "competitive advantage", "legacy", "validation", "urgency", "masterpiece", "300%"]
        found_keywords = [kw for kw in psychological_keywords if kw.lower() in role_establishment.lower()]
        
        print(f"\nPsychological Keywords Found: {found_keywords}")
        print(f"Total Length: {len(role_establishment)} characters")

if __name__ == "__main__":
    test_psychological_approach()
