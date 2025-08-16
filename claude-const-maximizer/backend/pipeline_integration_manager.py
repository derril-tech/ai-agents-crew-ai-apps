"""
Pipeline Integration Manager
Connects backend pipeline progress with frontend to-do list updates
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import asyncio

class PipelineIntegrationManager:
    """Manages integration between backend pipeline and frontend to-do list"""
    
    def __init__(self, frontend_dir: str = "../frontend/dashboard"):
        self.frontend_dir = Path(frontend_dir)
        self.todo_file = self.frontend_dir / "lib" / "pipeline-todos.json"
        self.todo_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Pipeline step mappings
        self.step_mappings = {
            "market_research": {
                "todo_id": "market-research",
                "agent": "MarketResearcher",
                "description": "🔍 Market Research & Analysis"
            },
            "project_brief": {
                "todo_id": "project-brief", 
                "agent": "PromptEngineer",
                "description": "📋 Create Project Brief"
            },
            "prompt_template": {
                "todo_id": "prompt-template",
                "agent": "PromptEngineer", 
                "description": "🎯 Select & Customize Prompt Template"
            },
            "backend_code": {
                "todo_id": "backend-code",
                "agent": "ClaudeCoder",
                "description": "⚙️ Generate Backend Code"
            },
            "frontend_code": {
                "todo_id": "frontend-code",
                "agent": "ClaudeCoder",
                "description": "🎨 Generate Frontend Code"
            },
            "integration": {
                "todo_id": "integration",
                "agent": "ClaudeCoder",
                "description": "🔗 Integration & API Connections"
            },
            "deployment": {
                "todo_id": "deployment",
                "agent": "ClaudeCoder",
                "description": "🚀 Deployment Configuration"
            },
            "validation": {
                "todo_id": "validation",
                "agent": "PreCodeValidator",
                "description": "✅ Validation & Testing"
            }
        }
    
    def initialize_project_todos(self, project_name: str, project_id: str = None) -> Dict[str, Any]:
        """Initialize to-do list for a new project"""
        if not project_id:
            project_id = project_name.lower().replace(" ", "-").replace("&", "and")
        
        todos = {
            "projectId": project_id,
            "projectName": project_name,
            "items": [],
            "progress": 0,
            "activeAgents": [],
            "lastUpdated": datetime.now().isoformat()
        }
        
        # Add pipeline milestones
        for step_key, step_info in self.step_mappings.items():
            todos["items"].append({
                "id": step_info["todo_id"],
                "text": step_info["description"],
                "completed": False,
                "agent": step_info["agent"],
                "status": "pending",
                "timestamp": None
            })
        
        self._save_project_todos(project_id, todos)
        print(f"📋 Initialized to-do list for project: {project_name}")
        return todos
    
    def start_agent_work(self, project_id: str, step_name: str) -> None:
        """Mark that an agent has started working on a step"""
        todos = self._load_project_todos(project_id)
        if not todos:
            return
        
        step_info = self.step_mappings.get(step_name)
        if not step_info:
            return
        
        # Update the specific todo item
        for item in todos["items"]:
            if item["id"] == step_info["todo_id"]:
                item["status"] = "in_progress"
                item["timestamp"] = datetime.now().isoformat()
                break
        
        # Add agent to active agents if not already there
        if step_info["agent"] not in todos["activeAgents"]:
            todos["activeAgents"].append(step_info["agent"])
        
        todos["lastUpdated"] = datetime.now().isoformat()
        self._save_project_todos(project_id, todos)
        
        print(f"🚀 Agent {step_info['agent']} started working on {step_info['description']}")
    
    def complete_step(self, project_id: str, step_name: str, success: bool = True) -> None:
        """Mark a pipeline step as completed"""
        todos = self._load_project_todos(project_id)
        if not todos:
            return
        
        step_info = self.step_mappings.get(step_name)
        if not step_info:
            return
        
        # Update the specific todo item
        for item in todos["items"]:
            if item["id"] == step_info["todo_id"]:
                item["completed"] = success
                item["status"] = "completed" if success else "error"
                item["timestamp"] = datetime.now().isoformat()
                break
        
        # Remove agent from active agents
        if step_info["agent"] in todos["activeAgents"]:
            todos["activeAgents"].remove(step_info["agent"])
        
        # Update progress
        completed_count = sum(1 for item in todos["items"] if item["completed"])
        todos["progress"] = int((completed_count / len(todos["items"])) * 100)
        
        todos["lastUpdated"] = datetime.now().isoformat()
        self._save_project_todos(project_id, todos)
        
        status = "✅ completed" if success else "❌ failed"
        print(f"{status} {step_info['description']} for project {project_id}")
    
    def update_project_status(self, project_id: str, status: str) -> None:
        """Update overall project status"""
        todos = self._load_project_todos(project_id)
        if not todos:
            return
        
        todos["status"] = status
        todos["lastUpdated"] = datetime.now().isoformat()
        self._save_project_todos(project_id, todos)
        
        print(f"📊 Updated project {project_id} status to: {status}")
    
    def get_project_todos(self, project_id: str) -> Dict[str, Any]:
        """Get current to-do list for a project"""
        return self._load_project_todos(project_id)
    
    def get_all_project_todos(self) -> List[Dict[str, Any]]:
        """Get all project to-do lists"""
        all_todos = []
        if self.todo_file.exists():
            try:
                with open(self.todo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        all_todos = list(data.values())
                    elif isinstance(data, list):
                        all_todos = data
            except Exception as e:
                print(f"⚠️ Error loading to-do lists: {e}")
        
        return all_todos
    
    def _load_project_todos(self, project_id: str) -> Dict[str, Any]:
        """Load to-do list for a specific project"""
        if not self.todo_file.exists():
            return None
        
        try:
            with open(self.todo_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data.get(project_id)
                elif isinstance(data, list):
                    for project in data:
                        if project.get("projectId") == project_id:
                            return project
        except Exception as e:
            print(f"⚠️ Error loading to-do list for {project_id}: {e}")
        
        return None
    
    def _save_project_todos(self, project_id: str, todos: Dict[str, Any]) -> None:
        """Save to-do list for a specific project"""
        try:
            # Load existing data
            existing_data = {}
            if self.todo_file.exists():
                with open(self.todo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        existing_data = data
                    elif isinstance(data, list):
                        existing_data = {p["projectId"]: p for p in data}
            
            # Update with new data
            existing_data[project_id] = todos
            
            # Save back to file
            with open(self.todo_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Error saving to-do list for {project_id}: {e}")
    
    def clear_project_todos(self, project_id: str) -> None:
        """Clear to-do list for a specific project"""
        try:
            if self.todo_file.exists():
                with open(self.todo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        if project_id in data:
                            del data[project_id]
                    elif isinstance(data, list):
                        data = [p for p in data if p.get("projectId") != project_id]
                
                with open(self.todo_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
                print(f"🗑️ Cleared to-do list for project: {project_id}")
        except Exception as e:
            print(f"⚠️ Error clearing to-do list for {project_id}: {e}")
