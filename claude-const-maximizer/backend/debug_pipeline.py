#!/usr/bin/env python3
"""
Debug script to identify why the pipeline is hanging
"""

import sys
import os
from pathlib import Path

def check_imports():
    """Check if all required modules can be imported"""
    print("[INVESTIGATE] Checking imports...")
    
    try:
        print("  [EMOJI] Basic imports work")
        
        # Check if we can import the orchestrator
        try:
            from phase3_research_prompt_code import Phase3Orchestrator
            print("  [EMOJI] Phase3Orchestrator imported successfully")
        except ImportError as e:
            print(f"  [ERROR] Failed to import Phase3Orchestrator: {e}")
            return False
        
        # Check agent imports
        try:
            from crew_app.agents.market_researcher import MarketResearcher
            print("  [EMOJI] MarketResearcher imported successfully")
        except ImportError as e:
            print(f"  [ERROR] Failed to import MarketResearcher: {e}")
            return False
            
        try:
            from crew_app.agents.prompt_engineer import PromptEngineer
            print("  [EMOJI] PromptEngineer imported successfully")
        except ImportError as e:
            print(f"  [ERROR] Failed to import PromptEngineer: {e}")
            return False
            
        try:
            from crew_app.agents.claude_coder import ClaudeCoder
            print("  [EMOJI] ClaudeCoder imported successfully")
        except ImportError as e:
            print(f"  [ERROR] Failed to import ClaudeCoder: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Import check failed: {e}")
        return False

def check_files():
    """Check if required files exist"""
    print("\n[EMOJI] Checking required files...")
    
    required_files = [
        "../projects.json",
        "crew_app/agents/market_researcher.py",
        "crew_app/agents/prompt_engineer.py", 
        "crew_app/agents/claude_coder.py",
        "templates/project_brief_template.py",
        "templates/prompt_templates.py",
        "validation/pre_code_validator.py",
        "validation/dependency_verifier.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  [EMOJI] {file_path}")
        else:
            print(f"  [ERROR] {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def check_env_vars():
    """Check if required environment variables are set"""
    print("\n[EMOJI] Checking environment variables...")
    
    required_vars = [
        "OPENAI_API_KEY",
        "TAVILY_API_KEY", 
        "SERPER_API_KEY"
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  [EMOJI] {var} = {value[:10]}...")
        else:
            print(f"  [ERROR] {var} - NOT SET")
            all_set = False
    
    return all_set

def test_basic_orchestrator():
    """Test if we can create the orchestrator"""
    print("\n[EMOJI] Testing orchestrator creation...")
    
    try:
        from phase3_research_prompt_code import Phase3Orchestrator
        
        # Try to create the orchestrator
        orchestrator = Phase3Orchestrator()
        print("  [EMOJI] Orchestrator created successfully")
        
        # Check if projects loaded
        if hasattr(orchestrator, 'projects') and orchestrator.projects:
            print(f"  [EMOJI] Loaded {len(orchestrator.projects)} projects")
        else:
            print("  [ERROR] No projects loaded")
            return False
            
        return True
        
    except Exception as e:
        print(f"  [ERROR] Orchestrator creation failed: {e}")
        return False

def main():
    print("[LAUNCH] Pipeline Debug Diagnostic")
    print("=" * 50)
    
    # Check imports
    imports_ok = check_imports()
    
    # Check files
    files_ok = check_files()
    
    # Check environment variables
    env_ok = check_env_vars()
    
    # Test orchestrator
    orchestrator_ok = test_basic_orchestrator()
    
    print("\n" + "=" * 50)
    print("[METRICS] DIAGNOSTIC RESULTS:")
    print(f"  Imports: {'[OK] OK' if imports_ok else '[ERROR] FAILED'}")
    print(f"  Files: {'[OK] OK' if files_ok else '[ERROR] FAILED'}")
    print(f"  Environment: {'[OK] OK' if env_ok else '[ERROR] FAILED'}")
    print(f"  Orchestrator: {'[OK] OK' if orchestrator_ok else '[ERROR] FAILED'}")
    
    if all([imports_ok, files_ok, env_ok, orchestrator_ok]):
        print("\n[SUCCESS] All checks passed! The pipeline should work.")
    else:
        print("\n[WARN]  Some checks failed. Fix the issues above before running the pipeline.")

if __name__ == "__main__":
    main()
