#!/usr/bin/env python3
"""
Comprehensive test script to verify the expert profile system works with all 60 projects.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew_app.expert_profiles import (
    detect_project_category, 
    get_expert_profile, 
    get_all_60_projects,
    get_project_count_by_category,
    validate_project_name,
    create_role_establishment
)

def test_all_60_projects():
    print("🧪 Testing Expert Profile System with All 60 Projects...")
    
    # Get all projects and counts
    all_projects = get_all_60_projects()
    project_counts = get_project_count_by_category()
    
    print("\n" + "="*80)
    print("PROJECT DISTRIBUTION:")
    print("="*80)
    
    total_projects = 0
    for category, count in project_counts.items():
        print(f"{category.upper()}: {count} projects")
        total_projects += count
    
    print(f"\nTOTAL: {total_projects} projects")
    
    print("\n" + "="*80)
    print("PROJECT CATEGORY DETECTION TEST:")
    print("="*80)
    
    success_count = 0
    total_tests = 0
    
    for category, projects in all_projects.items():
        print(f"\n--- {category.upper()} PROJECTS ---")
        for project in projects:
            detected_category = detect_project_category(project)
            expert_profile = get_expert_profile(project)
            is_valid = validate_project_name(project)
            
            status = "✅" if detected_category == category else "❌"
            print(f"{status} {project}")
            print(f"   Detected: {detected_category} | Expert: {expert_profile['title']} | Valid: {is_valid}")
            
            if detected_category == category:
                success_count += 1
            total_tests += 1
    
    print(f"\n" + "="*80)
    print("TEST RESULTS:")
    print("="*80)
    print(f"Success Rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    
    if success_count == total_tests:
        print("🎉 ALL PROJECTS CORRECTLY CATEGORIZED!")
    else:
        print(f"⚠️ {total_tests - success_count} projects need attention")
    
    print("\n" + "="*80)
    print("ROLE ESTABLISHMENT SAMPLE:")
    print("="*80)
    
    # Test role establishment for one project from each category
    sample_projects = {
        "voice": "AI-Powered Personal Voice Assistant & Calendar Manager",
        "crewai": "Multi-Agent Content Creation & Marketing System",
        "rag": "Intelligent Document Processing & Knowledge Base",
        "content": "AI-Powered Video Content Generator",
        "healthcare": "AI-Powered Medical Diagnosis Assistant",
        "ecommerce": "Intelligent E-commerce Management System",
        "developer": "AI-Powered Code Review & Refactoring Assistant",
        "api": "Web Scraping & Data Aggregation Platform"
    }
    
    for category, project in sample_projects.items():
        print(f"\n--- {category.upper()} ---")
        role_establishment = create_role_establishment(project)
        print(f"Project: {project}")
        print("Role Establishment Preview:")
        print(role_establishment[:200] + "..." if len(role_establishment) > 200 else role_establishment)
        
        # Check for required elements
        has_role = "You are an expert" in role_establishment
        has_psychological = any(elem in role_establishment for elem in ["time-sensitive", "high-priority", "legendary", "masterpiece", "300%"])
        
        print(f"✅ Role establishment: {has_role}")
        print(f"✅ Psychological elements: {has_psychological}")
    
    print(f"\n🎉 Expert Profile System Test Complete!")
    print(f"📊 Total Projects: {total_projects}")
    print(f"🎯 Success Rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")

if __name__ == "__main__":
    test_all_60_projects()
