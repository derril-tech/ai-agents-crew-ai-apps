

#!/usr/bin/env python3
"""
Progress Dashboard Generator for 60 AI Projects Challenge
Scans projects.json and deliverables/ to create a beautiful progress dashboard
"""

import json
import os
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# Configuration
PROJECTS_FILE = Path("projects.json")
DELIVERABLES_DIR = Path("deliverables")
DASHBOARD_OUTPUT = Path("dashboard/index.html")

# Status definitions
STATUS_COMPLETE = "complete"
STATUS_IN_PROGRESS = "in_progress"
STATUS_NOT_STARTED = "not_started"
STATUS_FAILED = "failed"

class ProjectTracker:
    def __init__(self):
        self.projects = []
        self.deliverables = {}
        self.stats = {
            "total": 0,
            "complete": 0,
            "in_progress": 0,
            "not_started": 0,
            "failed": 0
        }
    
    def load_projects(self):
        """Load projects from projects.json"""
        if not PROJECTS_FILE.exists():
            print(f"❌ {PROJECTS_FILE} not found!")
            return False
        
        try:
            with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                self.projects = json.load(f)
            self.stats["total"] = len(self.projects)
            print(f"✅ Loaded {len(self.projects)} projects")
            return True
        except Exception as e:
            print(f"❌ Error loading projects: {e}")
            return False
    
    def scan_deliverables(self):
        """Scan deliverables directory for completed work"""
        if not DELIVERABLES_DIR.exists():
            print(f"⚠️  {DELIVERABLES_DIR} not found - no deliverables yet")
            return
        
        for project_dir in DELIVERABLES_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            
            project_name = project_dir.name
            deliverables = []
            
            # Check for expected deliverable files
            expected_files = [
                "00_INDEX.md",
                "01_market_brief.md", 
                "02_prompt_pack.md",
                "03_frontend_spec.md",
                "04_backend_spec.md",
                "05_five_prompts_plan.md",
                "06_deploy_checklist.md"
            ]
            
            for file_name in expected_files:
                file_path = project_dir / file_name
                if file_path.exists():
                    deliverables.append(file_name)
            
            self.deliverables[project_name] = deliverables
    
    def get_project_status(self, project_name: str) -> str:
        """Determine status of a project based on deliverables"""
        if project_name not in self.deliverables:
            return STATUS_NOT_STARTED
        
        deliverables = self.deliverables[project_name]
        
        # Check if all expected files are present
        expected_count = 7  # All 6 deliverables + index
        if len(deliverables) == expected_count:
            return STATUS_COMPLETE
        elif len(deliverables) > 0:
            return STATUS_IN_PROGRESS
        else:
            return STATUS_NOT_STARTED
    
    def calculate_stats(self):
        """Calculate overall statistics"""
        for project in self.projects:
            project_name = self._slugify(project.get("project_name", ""))
            status = self.get_project_status(project_name)
            self.stats[status] += 1
    
    def _slugify(self, name: str) -> str:
        """Convert project name to slug format"""
        return "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")
    
    def generate_dashboard(self):
        """Generate the HTML dashboard"""
        self.calculate_stats()
        
        # Create dashboard directory
        DASHBOARD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate HTML content
        html_content = self._generate_html()
        
        # Write to file
        with open(DASHBOARD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard generated: {DASHBOARD_OUTPUT}")
        print(f"📊 Progress: {self.stats['complete']}/{self.stats['total']} complete ({self._get_percentage()}%)")
    
    def _get_percentage(self) -> int:
        """Calculate completion percentage"""
        if self.stats["total"] == 0:
            return 0
        return math.floor((self.stats["complete"] / self.stats["total"]) * 100)
    
    def _generate_html(self) -> str:
        """Generate the complete HTML dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>60 AI Projects Challenge - Progress Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .card-hover {{
            transition: all 0.3s ease;
        }}
        .card-hover:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .status-complete {{ background-color: #10b981; }}
        .status-in-progress {{ background-color: #f59e0b; }}
        .status-not-started {{ background-color: #6b7280; }}
        .status-failed {{ background-color: #ef4444; }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Header -->
    <header class="gradient-bg text-white py-8">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-4xl font-bold mb-2">60 AI Projects Challenge</h1>
                    <p class="text-xl opacity-90">Progress Dashboard</p>
                </div>
                <div class="text-right">
                    <div class="text-3xl font-bold">{self._get_percentage()}%</div>
                    <div class="text-sm opacity-75">Complete</div>
                </div>
            </div>
        </div>
    </header>

    <!-- Stats Cards -->
    <section class="py-8">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-lg shadow-md p-6 card-hover">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-blue-100 text-blue-600">
                            <i data-lucide="target" class="w-6 h-6"></i>
                        </div>
                        <div class="ml-4">
                            <div class="text-2xl font-bold text-gray-900">{self.stats['total']}</div>
                            <div class="text-sm text-gray-500">Total Projects</div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg shadow-md p-6 card-hover">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-green-100 text-green-600">
                            <i data-lucide="check-circle" class="w-6 h-6"></i>
                        </div>
                        <div class="ml-4">
                            <div class="text-2xl font-bold text-gray-900">{self.stats['complete']}</div>
                            <div class="text-sm text-gray-500">Complete</div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg shadow-md p-6 card-hover">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
                            <i data-lucide="clock" class="w-6 h-6"></i>
                        </div>
                        <div class="ml-4">
                            <div class="text-2xl font-bold text-gray-900">{self.stats['in_progress']}</div>
                            <div class="text-sm text-gray-500">In Progress</div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg shadow-md p-6 card-hover">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-gray-100 text-gray-600">
                            <i data-lucide="circle" class="w-6 h-6"></i>
                        </div>
                        <div class="ml-4">
                            <div class="text-2xl font-bold text-gray-900">{self.stats['not_started']}</div>
                            <div class="text-sm text-gray-500">Not Started</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Progress Bar -->
    <section class="py-4">
        <div class="container mx-auto px-4">
            <div class="bg-white rounded-lg shadow-md p-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold text-gray-900">Overall Progress</h2>
                    <span class="text-sm text-gray-500">{self.stats['complete']} of {self.stats['total']} projects</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-4">
                    <div class="bg-gradient-to-r from-blue-500 to-purple-600 h-4 rounded-full transition-all duration-500" 
                         style="width: {self._get_percentage()}%"></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Grid -->
    <section class="py-8">
        <div class="container mx-auto px-4">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Project Status</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {self._generate_project_cards()}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-6 mt-12">
        <div class="container mx-auto px-4 text-center">
            <p class="text-sm opacity-75">
                Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </footer>

    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            // Add click handlers for project cards
            document.querySelectorAll('.project-card').forEach(card => {{
                card.addEventListener('click', function() {{
                    const projectName = this.dataset.project;
                    const deliverablesDir = this.dataset.deliverables;
                    if (deliverablesDir) {{
                        console.log(`Opening deliverables for: ${{projectName}}`);
                        // You could add a modal or navigation here
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    def _generate_project_cards(self) -> str:
        """Generate HTML for project cards"""
        cards = []
        
        for project in self.projects:
            project_name = project.get("project_name", "Untitled")
            project_slug = self._slugify(project_name)
            app_type = project.get("app_type", "AI Application")
            target_users = project.get("target_users", "General users")
            status = self.get_project_status(project_slug)
            
            # Get deliverable count
            deliverable_count = len(self.deliverables.get(project_slug, []))
            total_deliverables = 7
            
            # Status colors and icons
            status_config = {
                STATUS_COMPLETE: {
                    "color": "status-complete",
                    "icon": "check-circle",
                    "text": "Complete"
                },
                STATUS_IN_PROGRESS: {
                    "color": "status-in-progress", 
                    "icon": "clock",
                    "text": "In Progress"
                },
                STATUS_NOT_STARTED: {
                    "color": "status-not-started",
                    "icon": "circle",
                    "text": "Not Started"
                },
                STATUS_FAILED: {
                    "color": "status-failed",
                    "icon": "x-circle",
                    "text": "Failed"
                }
            }
            
            config = status_config[status]
            
            card = f"""
                <div class="bg-white rounded-lg shadow-md p-6 card-hover project-card cursor-pointer" 
                     data-project="{project_slug}" 
                     data-deliverables="{DELIVERABLES_DIR / project_slug if project_slug in self.deliverables else ''}">
                    <div class="flex items-start justify-between mb-4">
                        <div class="flex-1">
                            <h3 class="text-lg font-semibold text-gray-900 mb-2">{project_name}</h3>
                            <p class="text-sm text-gray-600 mb-1">{app_type}</p>
                            <p class="text-xs text-gray-500">{target_users}</p>
                        </div>
                        <div class="flex items-center">
                            <div class="p-2 rounded-full {config['color']} text-white">
                                <i data-lucide="{config['icon']}" class="w-4 h-4"></i>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-4">
                        <div class="flex justify-between text-sm text-gray-600 mb-1">
                            <span>Deliverables</span>
                            <span>{deliverable_count}/{total_deliverables}</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-500 h-2 rounded-full transition-all duration-300" 
                                 style="width: {(deliverable_count/total_deliverables)*100}%"></div>
                        </div>
                    </div>
                    
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-medium text-gray-500 uppercase tracking-wide">{config['text']}</span>
                        {f'<a href="{DELIVERABLES_DIR / project_slug}" class="text-xs text-blue-600 hover:text-blue-800">View Files</a>' if project_slug in self.deliverables else ''}
                    </div>
                </div>
            """
            cards.append(card)
        
        return "\n".join(cards)

def main():
    parser = argparse.ArgumentParser(description="Generate progress dashboard for 60 AI projects")
    parser.add_argument("--output", "-o", default=str(DASHBOARD_OUTPUT), 
                       help="Output path for dashboard HTML")
    args = parser.parse_args()
    
    # Update output path if specified
    global DASHBOARD_OUTPUT
    DASHBOARD_OUTPUT = Path(args.output)
    
    print("🚀 Generating Progress Dashboard...")
    print(f"📁 Projects file: {PROJECTS_FILE}")
    print(f"📁 Deliverables dir: {DELIVERABLES_DIR}")
    print(f"📁 Output: {DASHBOARD_OUTPUT}")
    print()
    
    tracker = ProjectTracker()
    
    if not tracker.load_projects():
        return 1
    
    tracker.scan_deliverables()
    tracker.generate_dashboard()
    
    print()
    print("🎉 Dashboard generation complete!")
    print(f"📊 Open {DASHBOARD_OUTPUT} in your browser to view progress")
    
    return 0

if __name__ == "__main__":
    exit(main())

