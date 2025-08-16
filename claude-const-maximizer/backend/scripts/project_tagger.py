# scripts/project_tagger.py
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Archetype mapping rules
ARCHETYPE_RULES = {
    "rag_kb": [
        "knowledge base", "document", "rag", "retrieval", "semantic search", 
        "pdf", "document processing", "intelligent document", "universal rag",
        "contract clause", "legal document", "document analyzer"
    ],
    "agentic": [
        "multi-agent", "autonomous", "crew", "orchestration", "agent system",
        "autonomous research", "multi-agent dev", "e-commerce agent"
    ],
    "dev_tools": [
        "code review", "refactoring", "development", "programming", "code analysis",
        "ai-powered code", "intelligent code"
    ],
    "support_crm": [
        "support", "customer", "chatbot", "crm", "customer service", "help desk",
        "multilingual reply", "email drafting"
    ],
    "finance_trading": [
        "financial", "trading", "portfolio", "investment", "market analysis",
        "financial analysis", "trading bot", "portfolio agent"
    ],
    "healthcare_demo": [
        "medical", "healthcare", "diagnosis", "treatment", "health", "medical assistant",
        "diagnosis assistant", "treatment planner"
    ],
    "legal": [
        "legal", "contract", "law", "compliance", "contract analyzer", "contract negotiator",
        "smart-contract auditor"
    ],
    "media_content": [
        "video", "audio", "content", "generation", "media", "podcast", "script",
        "video generator", "podcast→blog", "script generator"
    ],
    "ops_analytics": [
        "supply chain", "optimization", "analytics", "dashboard", "operations",
        "supply chain optimizer", "real-time moderation"
    ],
    "smart_city_iot": [
        "iot", "smart city", "sensor", "real-time", "moderation", "real-time moderation"
    ],
    "blockchain": [
        "blockchain", "smart contract", "crypto", "web3", "smart-contract auditor"
    ],
    "education": [
        "education", "learning", "tutorial", "course", "student", "academic"
    ],
    "ecommerce": [
        "e-commerce", "ecommerce", "shopping", "product", "recommendation", "store"
    ],
    "hr_recruitment": [
        "hr", "recruitment", "resume", "hiring", "candidate", "job", "resume matcher"
    ],
    "research": [
        "research", "academic", "paper", "study", "analysis", "autonomous research"
    ]
}

def load_archetypes() -> Dict:
    """Load archetype configurations."""
    archetypes_file = Path("../archetypes.json")
    if not archetypes_file.exists():
        raise FileNotFoundError("archetypes.json not found!")
    
    with open(archetypes_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_projects() -> List[Dict]:
    """Load projects from projects.json."""
    projects_file = Path("../projects.json")
    if not projects_file.exists():
        raise FileNotFoundError("projects.json not found!")
    
    with open(projects_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def determine_archetype(project_name: str, app_type: str, core_features: List[str]) -> str:
    """Determine the best archetype for a project based on its description."""
    # Combine all text for matching
    text = f"{project_name} {app_type} {' '.join(core_features)}".lower()
    
    # Score each archetype
    scores = {}
    for archetype, keywords in ARCHETYPE_RULES.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        scores[archetype] = score
    
    # Find the best match
    best_archetype = max(scores.items(), key=lambda x: x[1])
    
    # If no clear match, default to rag_kb
    if best_archetype[1] == 0:
        return "rag_kb"
    
    return best_archetype[0]

def slugify(name: str) -> str:
    """Convert project name to URL-friendly slug."""
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")

def generate_env_vars(archetype_config: Dict, project_slug: str) -> Dict[str, str]:
    """Generate environment variables for a project based on its archetype."""
    env_vars = {}
    
    for env_var in archetype_config.get("env", []):
        if env_var == "DATABASE_URL":
            env_vars[env_var] = "${DATABASE_URL}"
        elif env_var == "R2_BUCKET":
            env_vars[env_var] = f"{project_slug}-assets"
        elif env_var == "POSTHOG_API_KEY":
            env_vars[env_var] = "${POSTHOG_API_KEY}"
        elif env_var == "PUSHER_APP_ID":
            env_vars[env_var] = "${PUSHER_APP_ID}"
        elif env_var == "PUSHER_KEY":
            env_vars[env_var] = "${PUSHER_KEY}"
        else:
            # For API keys, use placeholder
            env_vars[env_var] = f"${{{env_var}}}"
    
    return env_vars

def tag_projects():
    """Tag all projects with archetypes and generate environment variables."""
    print("[EMOJI]️  Starting project tagging...")
    
    # Load configurations
    archetypes = load_archetypes()
    projects = load_projects()
    
    tagged_projects = []
    envs = {}
    
    print(f"[CHECKLIST] Processing {len(projects)} projects...")
    
    for i, project in enumerate(projects, 1):
        project_name = project.get("project_name", f"Project {i}")
        app_type = project.get("app_type", "")
        core_features = project.get("core_features", [])
        
        print(f"\n[{i}/{len(projects)}] Processing: {project_name}")
        
        # Determine archetype
        archetype = determine_archetype(project_name, app_type, core_features)
        archetype_config = archetypes[archetype]
        
        # Generate slug
        project_slug = slugify(project_name)
        
        # Generate environment variables
        project_envs = generate_env_vars(archetype_config, project_slug)
        
        # Add to results
        tagged_project = {
            **project,
            "archetype": archetype,
            "backend": archetype_config["backend"],
            "services": archetype_config["services"],
            "project_slug": project_slug
        }
        
        if "vector" in archetype_config:
            tagged_project["vector"] = archetype_config["vector"]
        
        tagged_projects.append(tagged_project)
        envs[project_slug] = project_envs
        
        print(f"  [EMOJI]️  Archetype: {archetype}")
        print(f"  [TOOL] Backend: {archetype_config['backend']}")
        print(f"  [CONNECT] Services: {', '.join(archetype_config['services'])}")
        print(f"  [EMOJI] Env vars: {list(project_envs.keys())}")
    
    # Save tagged projects
    tagged_projects_file = Path("../tagged_projects.json")
    with open(tagged_projects_file, 'w', encoding='utf-8') as f:
        json.dump(tagged_projects, f, indent=2)
    
    # Save environment variables
    envs_file = Path("../envs.json")
    with open(envs_file, 'w', encoding='utf-8') as f:
        json.dump(envs, f, indent=2)
    
    # Generate summary
    archetype_counts = {}
    backend_counts = {}
    
    for project in tagged_projects:
        archetype = project["archetype"]
        backend = project["backend"]
        
        archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1
        backend_counts[backend] = backend_counts.get(backend, 0) + 1
    
    print(f"\n[METRICS] Tagging Summary:")
    print(f"  Total projects: {len(tagged_projects)}")
    print(f"  Archetypes used: {len(archetype_counts)}")
    print(f"  Backends used: {len(backend_counts)}")
    
    print(f"\n[EMOJI]️  Archetype Distribution:")
    for archetype, count in sorted(archetype_counts.items()):
        percentage = (count / len(tagged_projects)) * 100
        print(f"  {archetype}: {count} ({percentage:.1f}%)")
    
    print(f"\n[TOOL] Backend Distribution:")
    for backend, count in sorted(backend_counts.items()):
        percentage = (count / len(tagged_projects)) * 100
        print(f"  {backend}: {count} ({percentage:.1f}%)")
    
    print(f"\n[OK] Files generated:")
    print(f"  [DOC] Tagged projects: {tagged_projects_file}")
    print(f"  [EMOJI] Environment vars: {envs_file}")
    
    # Generate stack choice documentation
    generate_stack_choices(tagged_projects, archetypes)

def generate_stack_choices(tagged_projects: List[Dict], archetypes: Dict):
    """Generate stack choice documentation for each project."""
    print(f"\n[WRITE] Generating stack choice documentation...")
    
    deliverables_dir = Path("../deliverables")
    deliverables_dir.mkdir(exist_ok=True)
    
    for project in tagged_projects:
        project_slug = project["project_slug"]
        archetype = project["archetype"]
        archetype_config = archetypes[archetype]
        
        project_dir = deliverables_dir / project_slug
        project_dir.mkdir(exist_ok=True)
        
        stack_choice_content = f"""# Stack Choice: {project['project_name']}

## Archetype: {archetype}
{archetype_config['description']}

## Backend Choice: {archetype_config['backend']}
- **Framework**: {archetype_config['backend'].upper()}
- **Rationale**: Optimized for {archetype_config['description'].lower()}

## Services Required
{chr(10).join(f"- {service}" for service in archetype_config['services'])}

## Environment Variables
{chr(10).join(f"- {env_var}" for env_var in archetype_config.get('env', []))}

## Vector Database
{f"- **Vector DB**: {archetype_config['vector']}" if 'vector' in archetype_config else "- **Vector DB**: None required"}

## Deployment Profile
- **Frontend**: Vercel (Next.js 14 + React + Tailwind)
- **Backend**: Render ({archetype_config['backend']})
- **Database**: Render PostgreSQL
- **File Storage**: Cloudflare R2 (if required)

## Next Steps
1. Review the market brief in `01_market_brief.md`
2. Check the prompt pack in `02_prompt_pack.md`
3. Follow the 5-prompts plan in `05_five_prompts_plan.md`
4. Use the deployment checklist in `06_deploy_checklist.md`
"""
        
        stack_choice_file = project_dir / "00_STACK_CHOICE.md"
        with open(stack_choice_file, 'w', encoding='utf-8') as f:
            f.write(stack_choice_content)

if __name__ == "__main__":
    try:
        tag_projects()
    except Exception as e:
        print(f"[ERROR] Project tagging failed: {e}")
        exit(1)

