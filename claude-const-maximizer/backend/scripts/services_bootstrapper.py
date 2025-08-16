# scripts/services_bootstrapper.py
import json
import os
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin

class VercelBootstrapper:
    def __init__(self, token: str, team_id: Optional[str] = None):
        self.token = token
        self.team_id = team_id
        self.base_url = "https://api.vercel.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def create_project(self, name: str, slug: str) -> Dict:
        """Create a new Vercel project."""
        url = urljoin(self.base_url, "/projects")
        
        data = {
            "name": name,
            "framework": "nextjs",
            "buildCommand": "npm run build",
            "outputDirectory": ".next",
            "installCommand": "npm install",
            "devCommand": "npm run dev"
        }
        
        if self.team_id:
            data["teamId"] = self.team_id
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create Vercel project: {response.text}")
    
    def set_env_vars(self, project_id: str, env_vars: Dict[str, str]) -> bool:
        """Set environment variables for a project."""
        url = urljoin(self.base_url, f"/projects/{project_id}/env")
        
        for key, value in env_vars.items():
            data = {
                "key": key,
                "value": value,
                "target": ["production", "preview", "development"],
                "type": "encrypted"
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code != 200:
                print(f"Warning: Failed to set env var {key}: {response.text}")
                return False
        
        return True

class RenderBootstrapper:
    def __init__(self, api_key: str, owner_id: str):
        self.api_key = api_key
        self.owner_id = owner_id
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_web_service(self, name: str, slug: str, repo_url: str = None) -> Dict:
        """Create a new Render web service."""
        url = urljoin(self.base_url, "/services")
        
        data = {
            "name": name,
            "type": "web_service",
            "ownerId": self.owner_id,
            "env": "node",  # Default, can be overridden
            "buildCommand": "npm install && npm run build",
            "startCommand": "npm start",
            "plan": "starter"  # Free tier
        }
        
        if repo_url:
            data["repo"] = repo_url
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create Render service: {response.text}")
    
    def create_postgres_db(self, name: str, slug: str) -> Dict:
        """Create a new PostgreSQL database."""
        url = urljoin(self.base_url, "/databases")
        
        data = {
            "name": name,
            "databaseName": slug.replace("-", "_"),
            "ownerId": self.owner_id,
            "plan": "starter"  # Free tier
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create PostgreSQL database: {response.text}")
    
    def set_env_vars(self, service_id: str, env_vars: Dict[str, str]) -> bool:
        """Set environment variables for a service."""
        url = urljoin(self.base_url, f"/services/{service_id}/env-vars")
        
        for key, value in env_vars.items():
            data = {
                "key": key,
                "value": value
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code != 201:
                print(f"Warning: Failed to set env var {key}: {response.text}")
                return False
        
        return True

def load_projects() -> List[Dict]:
    """Load projects from projects.json."""
    projects_file = Path("../projects.json")
    if not projects_file.exists():
        raise FileNotFoundError("projects.json not found!")
    
    with open(projects_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_envs() -> Dict:
    """Load environment variables from envs.json."""
    envs_file = Path("../envs.json")
    if not envs_file.exists():
        print("[WARN]  envs.json not found, using empty env vars")
        return {}
    
    with open(envs_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def slugify(name: str) -> str:
    """Convert project name to URL-friendly slug."""
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")

def bootstrap_services(dry_run: bool = True):
    """Bootstrap all services for the projects."""
    print("[LAUNCH] Starting services bootstrap...")
    
    # Load configuration
    projects = load_projects()
    envs = load_envs()
    
    # Initialize bootstrappers
    vercel_token = os.getenv("VERCEL_TOKEN")
    vercel_team_id = os.getenv("VERCEL_TEAM_ID")
    render_api_key = os.getenv("RENDER_API_KEY")
    render_owner_id = os.getenv("RENDER_OWNER_ID")
    
    if not dry_run:
        if not vercel_token:
            raise ValueError("VERCEL_TOKEN environment variable required")
        if not render_api_key:
            raise ValueError("RENDER_API_KEY environment variable required")
        if not render_owner_id:
            raise ValueError("RENDER_OWNER_ID environment variable required")
    
    vercel = VercelBootstrapper(vercel_token or "fake-token", vercel_team_id) if not dry_run else None
    render = RenderBootstrapper(render_api_key or "fake-key", render_owner_id or "fake-owner") if not dry_run else None
    
    results = {
        "vercel_projects": [],
        "render_services": [],
        "render_databases": [],
        "errors": []
    }
    
    print(f"[CHECKLIST] Processing {len(projects)} projects...")
    
    for i, project in enumerate(projects, 1):
        project_name = project.get("project_name", f"Project {i}")
        project_slug = slugify(project_name)
        
        print(f"\n[{i}/{len(projects)}] Processing: {project_name}")
        
        # Get environment variables for this project
        project_envs = envs.get(project_slug, {})
        
        try:
            # Create Vercel project (frontend)
            if dry_run:
                print(f"  [EMOJI] Would create Vercel project: {project_name}")
                print(f"     Slug: {project_slug}")
                print(f"     Env vars: {list(project_envs.keys())}")
                results["vercel_projects"].append({
                    "name": project_name,
                    "slug": project_slug,
                    "status": "would_create"
                })
            else:
                print(f"  [UI] Creating Vercel project: {project_name}")
                vercel_project = vercel.create_project(project_name, project_slug)
                vercel.set_env_vars(vercel_project["id"], project_envs)
                results["vercel_projects"].append({
                    "name": project_name,
                    "id": vercel_project["id"],
                    "url": vercel_project.get("url"),
                    "status": "created"
                })
                print(f"     [OK] Created: {vercel_project.get('url')}")
            
            # Create Render web service (backend)
            if dry_run:
                print(f"  [EMOJI] Would create Render service: {project_name}-api")
                results["render_services"].append({
                    "name": f"{project_name}-api",
                    "slug": f"{project_slug}-api",
                    "status": "would_create"
                })
            else:
                print(f"  [TOOL] Creating Render service: {project_name}-api")
                render_service = render.create_web_service(
                    f"{project_name}-api", 
                    f"{project_slug}-api"
                )
                render.set_env_vars(render_service["id"], project_envs)
                results["render_services"].append({
                    "name": f"{project_name}-api",
                    "id": render_service["id"],
                    "url": render_service.get("serviceUrl"),
                    "status": "created"
                })
                print(f"     [OK] Created: {render_service.get('serviceUrl')}")
            
            # Create Render PostgreSQL database
            if dry_run:
                print(f"  [EMOJI] Would create PostgreSQL database: {project_name}-db")
                results["render_databases"].append({
                    "name": f"{project_name}-db",
                    "slug": f"{project_slug}-db",
                    "status": "would_create"
                })
            else:
                print(f"  [EMOJI]️  Creating PostgreSQL database: {project_name}-db")
                render_db = render.create_postgres_db(
                    f"{project_name}-db", 
                    f"{project_slug}-db"
                )
                results["render_databases"].append({
                    "name": f"{project_name}-db",
                    "id": render_db["id"],
                    "connection_string": render_db.get("connectionString"),
                    "status": "created"
                })
                print(f"     [OK] Created database")
        
        except Exception as e:
            error_msg = f"Failed to process {project_name}: {str(e)}"
            print(f"     [ERROR] {error_msg}")
            results["errors"].append({
                "project": project_name,
                "error": str(e)
            })
    
    # Save results
    results_file = Path("bootstrap_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[METRICS] Bootstrap Summary:")
    print(f"  Vercel projects: {len(results['vercel_projects'])}")
    print(f"  Render services: {len(results['render_services'])}")
    print(f"  Render databases: {len(results['render_databases'])}")
    print(f"  Errors: {len(results['errors'])}")
    print(f"  Results saved to: {results_file}")
    
    if dry_run:
        print(f"\n[EMOJI] This was a dry run. To actually create services, run:")
        print(f"   python scripts/services_bootstrapper.py")
    else:
        print(f"\n[OK] Services bootstrap completed!")

def main():
    parser = argparse.ArgumentParser(description="Bootstrap Vercel and Render services for all projects")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="Show what would be created without actually creating (default)")
    parser.add_argument("--execute", action="store_true",
                       help="Actually create the services (requires API keys)")
    
    args = parser.parse_args()
    
    # If --execute is passed, override dry_run
    dry_run = not args.execute
    
    try:
        bootstrap_services(dry_run=dry_run)
    except Exception as e:
        print(f"[ERROR] Bootstrap failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()

