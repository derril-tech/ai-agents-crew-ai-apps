# scripts/progress_dashboard.py
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# HTML template for the dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>60 AI Apps Pipeline - Progress Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'dark': '#0f172a',
                        'darker': '#020617'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .card-hover {{
            transition: all 0.3s ease;
        }}
        .card-hover:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        .status-complete {{ background: linear-gradient(135deg, #10b981, #059669); }}
        .status-in-progress {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
        .status-not-started {{ background: linear-gradient(135deg, #6b7280, #4b5563); }}
        .status-failed {{ background: linear-gradient(135deg, #ef4444, #dc2626); }}
    </style>
</head>
<body class="bg-dark text-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-5xl font-bold mb-4 gradient-bg bg-clip-text text-transparent">
                60 AI Apps Pipeline
            </h1>
            <p class="text-xl text-gray-300 mb-2">Progress Dashboard</p>
            <p class="text-sm text-gray-400">Last updated: {timestamp}</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <div class="bg-darker rounded-lg p-6 card-hover">
                <div class="text-3xl font-bold text-blue-400">{total_projects}</div>
                <div class="text-gray-400">Total Projects</div>
            </div>
            <div class="bg-darker rounded-lg p-6 card-hover">
                <div class="text-3xl font-bold text-green-400">{completed}</div>
                <div class="text-gray-400">Completed</div>
            </div>
            <div class="bg-darker rounded-lg p-6 card-hover">
                <div class="text-3xl font-bold text-yellow-400">{in_progress}</div>
                <div class="text-gray-400">In Progress</div>
            </div>
            <div class="bg-darker rounded-lg p-6 card-hover">
                <div class="text-3xl font-bold text-red-400">{failed}</div>
                <div class="text-gray-400">Failed</div>
            </div>
        </div>

        <!-- Progress Bar -->
        <div class="bg-darker rounded-lg p-6 mb-12">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Overall Progress</h3>
                <span class="text-2xl font-bold text-blue-400">{progress_percent}%</span>
            </div>
            <div class="w-full bg-gray-700 rounded-full h-4">
                <div class="gradient-bg h-4 rounded-full transition-all duration-500" 
                     style="width: {progress_percent}%"></div>
            </div>
        </div>

        <!-- Projects Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {project_cards}
        </div>

        <!-- Legend -->
        <div class="mt-12 bg-darker rounded-lg p-6">
            <h3 class="text-lg font-semibold mb-4">Status Legend</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full status-complete mr-2"></div>
                    <span class="text-sm">Complete</span>
                </div>
                <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full status-in-progress mr-2"></div>
                    <span class="text-sm">In Progress</span>
                </div>
                <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full status-not-started mr-2"></div>
                    <span class="text-sm">Not Started</span>
                </div>
                <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full status-failed mr-2"></div>
                    <span class="text-sm">Failed</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            window.location.reload();
        }}, 30000);
    </script>
</body>
</html>
"""

def get_project_status(project_dir: Path) -> Dict:
    """Determine the status of a project based on its deliverables."""
    required_files = [
        "00_INDEX.md",
        "01_market_brief.md", 
        "02_prompt_pack.md",
        "03_frontend_spec.md",
        "04_backend_spec.md",
        "05_five_prompts_plan.md",
        "06_deploy_checklist.md"
    ]
    
    if not project_dir.exists():
        return {"status": "not_started", "files": [], "progress": 0}
    
    existing_files = []
    for file in required_files:
        if (project_dir / file).exists():
            existing_files.append(file)
    
    if len(existing_files) == len(required_files):
        return {"status": "complete", "files": existing_files, "progress": 100}
    elif len(existing_files) > 0:
        progress = int((len(existing_files) / len(required_files)) * 100)
        return {"status": "in_progress", "files": existing_files, "progress": progress}
    else:
        return {"status": "not_started", "files": [], "progress": 0}

def generate_project_card(project_name: str, project_slug: str, status_info: Dict) -> str:
    """Generate HTML for a single project card."""
    status = status_info["status"]
    progress = status_info["progress"]
    files = status_info["files"]
    
    status_classes = {
        "complete": "status-complete",
        "in_progress": "status-in-progress", 
        "not_started": "status-not-started",
        "failed": "status-failed"
    }
    
    status_text = {
        "complete": "Complete",
        "in_progress": "In Progress",
        "not_started": "Not Started", 
        "failed": "Failed"
    }
    
    # Create file list HTML
    file_list = ""
    if files:
        file_list = "<div class='text-xs text-gray-400 mt-2'>"
        for file in files:
            file_list += f"<div>✓ {file}</div>"
        file_list += "</div>"
    
    return f"""
    <div class="bg-darker rounded-lg p-6 card-hover">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-blue-300">{project_name}</h3>
            <div class="w-3 h-3 rounded-full {status_classes[status]}"></div>
        </div>
        <div class="text-sm text-gray-400 mb-2">{status_text[status]}</div>
        <div class="w-full bg-gray-700 rounded-full h-2 mb-4">
            <div class="gradient-bg h-2 rounded-full transition-all duration-500" 
                 style="width: {progress}%"></div>
        </div>
        <div class="text-xs text-gray-500 mb-2">{progress}% complete</div>
        {file_list}
        <div class="mt-4">
            <a href="deliverables/{project_slug}/" 
               class="text-blue-400 hover:text-blue-300 text-sm">
                View Details →
            </a>
        </div>
    </div>
    """

def load_projects() -> List[Dict]:
    """Load projects from projects.json."""
    projects_file = Path("projects.json")
    if not projects_file.exists():
        print("❌ projects.json not found!")
        return []
    
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading projects.json: {e}")
        return []

def generate_dashboard():
    """Generate the progress dashboard."""
    print("🔍 Scanning projects...")
    
    # Load projects from root directory
    projects_file = Path("../../projects.json")
    if not projects_file.exists():
        print("❌ projects.json not found!")
        return
    
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    except Exception as e:
        print(f"❌ Error loading projects.json: {e}")
        return
    
    if not projects:
        print("❌ No projects found!")
        return
    
    # Create deliverables directory if it doesn't exist
    deliverables_dir = Path("../../deliverables")
    deliverables_dir.mkdir(exist_ok=True)
    
    # Analyze each project
    project_cards = []
    stats = {"complete": 0, "in_progress": 0, "not_started": 0, "failed": 0}
    
    for project in projects:
        project_name = project.get("project_name", "Unknown Project")
        project_slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in project_name).strip("-")
        
        project_dir = deliverables_dir / project_slug
        status_info = get_project_status(project_dir)
        
        # Update stats
        stats[status_info["status"]] += 1
        
        # Generate card
        card_html = generate_project_card(project_name, project_slug, status_info)
        project_cards.append(card_html)
    
    # Calculate overall progress
    total_projects = len(projects)
    completed = stats["complete"]
    progress_percent = int((completed / total_projects) * 100) if total_projects > 0 else 0
    
    # Generate dashboard HTML
    dashboard_html = DASHBOARD_TEMPLATE.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_projects=total_projects,
        completed=completed,
        in_progress=stats["in_progress"],
        failed=stats["failed"],
        progress_percent=progress_percent,
        project_cards="\n".join(project_cards)
    )
    
    # Write dashboard
    dashboard_dir = Path("../../frontend/dashboard-html")
    dashboard_dir.mkdir(exist_ok=True)
    
    dashboard_file = dashboard_dir / "index.html"
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"✅ Dashboard generated: {dashboard_file}")
    print(f"📊 Stats: {completed}/{total_projects} complete ({progress_percent}%)")

if __name__ == "__main__":
    generate_dashboard()

