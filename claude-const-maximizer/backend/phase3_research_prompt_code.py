"""
Phase 3: Research → Prompt → Code Workflow
Orchestrates the complete pipeline for building each of the 60 projects
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

from crew_app.agents.market_researcher import MarketResearcher
from crew_app.agents.prompt_engineer import PromptEngineer
from crew_app.agents.claude_coder import ClaudeCoder
from templates.project_brief_template import PROJECT_BRIEF_TEMPLATE
from templates.prompt_templates import PROMPT_TEMPLATES
from validation.pre_code_validator import PreCodeValidator
from validation.dependency_verifier import DependencyVerifier

@dataclass
class ProjectSpecification:
    project_name: str
    description: str
    tech_stack: str
    archetype: str
    market_research: Optional[Dict[str, Any]] = None
    project_brief: Optional[str] = None
    prompt_template: Optional[Dict[str, Any]] = None
    generated_code: Optional[Dict[str, Any]] = None
    validation_report: Optional[Dict[str, Any]] = None
    status: str = "pending"

class Phase3Orchestrator:
    """Orchestrates the complete Phase 3 workflow"""
    
    def __init__(self, projects_file: str = "../projects.json"):
        self.projects_file = Path(projects_file)
        self.deliverables_dir = Path("../deliverables")
        self.deliverables_dir.mkdir(exist_ok=True)
        
        # Initialize agents
        self.market_researcher = MarketResearcher()
        self.prompt_engineer = PromptEngineer()
        self.claude_coder = ClaudeCoder()
        
        # Load projects
        self.projects = self.load_projects()
        
    def load_projects(self) -> List[Dict[str, Any]]:
        """Load projects from JSON file"""
        if not self.projects_file.exists():
            raise FileNotFoundError(f"Projects file not found: {self.projects_file}")
        
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_project_specification(self, project: Dict[str, Any]) -> ProjectSpecification:
        """Create project specification from project data"""
        return ProjectSpecification(
            project_name=project["project_name"],
            description=project["description"],
            tech_stack=project["tech_stack"],
            archetype=project.get("archetype", "CRUD")
        )
    
    async def step1_market_research(self, spec: ProjectSpecification) -> ProjectSpecification:
        """Step 1: Market research and analysis"""
        print(f"🔍 Step 1: Market Research for {spec.project_name}")
        
        research_result = await self.market_researcher.research_project(
            project_name=spec.project_name,
            description=spec.description,
            tech_stack=spec.tech_stack
        )
        
        spec.market_research = research_result
        spec.status = "research_complete"
        
        # Save research results
        research_file = self.deliverables_dir / f"{spec.project_name}/market_research.json"
        research_file.parent.mkdir(exist_ok=True)
        
        with open(research_file, 'w', encoding='utf-8') as f:
            json.dump(research_result, f, indent=2)
        
        print(f"✅ Market research complete: {research_file}")
        return spec
    
    def step2_create_project_brief(self, spec: ProjectSpecification) -> ProjectSpecification:
        """Step 2: Create comprehensive project brief"""
        print(f"📋 Step 2: Creating Project Brief for {spec.project_name}")
        
        if not spec.market_research:
            raise ValueError("Market research must be completed first")
        
        # Extract analysis data from market research
        analysis = spec.market_research.get("analysis", {})
        
        # Helper function to format nested data
        def format_nested_data(data):
            if isinstance(data, dict):
                return "; ".join([f"{k}: {v}" for k, v in data.items()])
            elif isinstance(data, list):
                return "; ".join(data)
            else:
                return str(data) if data else ""
        
        # Generate project brief using template
        brief_content = PROJECT_BRIEF_TEMPLATE.format(
            project_name=spec.project_name,
            description=spec.description,
            tech_stack=spec.tech_stack,
            archetype=spec.archetype,
            target_audience=format_nested_data(analysis.get("TARGET AUDIENCE", "")),
            competitors=format_nested_data(analysis.get("COMPETITORS", "")),
            market_size=format_nested_data(analysis.get("MARKET SIZE", "")),
            key_features=format_nested_data(analysis.get("KEY FEATURES", "")),
            api_sources=format_nested_data(analysis.get("API SOURCES", "")),
            data_sources=format_nested_data(analysis.get("DATA SOURCES", "")),
            research_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        spec.project_brief = brief_content
        spec.status = "brief_complete"
        
        # Save project brief
        brief_file = self.deliverables_dir / f"{spec.project_name}/project_brief.md"
        brief_file.parent.mkdir(exist_ok=True)
        
        with open(brief_file, 'w', encoding='utf-8') as f:
            f.write(brief_content)
        
        print(f"✅ Project brief complete: {brief_file}")
        return spec
    
    def step3_select_prompt_template(self, spec: ProjectSpecification) -> ProjectSpecification:
        """Step 3: Select and customize prompt template"""
        print(f"🎯 Step 3: Selecting Prompt Template for {spec.project_name}")
        
        # Determine app type based on archetype
        app_type = self.map_archetype_to_app_type(spec.archetype)
        
        if app_type not in PROMPT_TEMPLATES:
            raise ValueError(f"Unknown app type: {app_type}")
        
        template = PROMPT_TEMPLATES[app_type].copy()
        
        # Customize template with project-specific details
        template["project_name"] = spec.project_name
        template["description"] = spec.description
        template["tech_stack"] = spec.tech_stack
        template["app_type"] = app_type  # Add the missing app_type field
        
        spec.prompt_template = template
        spec.status = "template_selected"
        
        # Save prompt template
        template_file = self.deliverables_dir / f"{spec.project_name}/prompt_template.json"
        template_file.parent.mkdir(exist_ok=True)
        
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2)
        
        print(f"✅ Prompt template selected: {template_file}")
        return spec
    
    async def step4_generate_code(self, spec: ProjectSpecification) -> ProjectSpecification:
        """Step 4: Generate code using Claude"""
        print(f"💻 Step 4: Generating Code for {spec.project_name}")
        
        if not spec.prompt_template:
            raise ValueError("Prompt template must be selected first")
        
        # Generate code using 5-prompt development plan
        generated_code = await self.claude_coder.generate_project_code(
            project_name=spec.project_name,
            project_brief=spec.project_brief,
            prompt_template=spec.prompt_template,
            market_research=spec.market_research
        )
        
        spec.generated_code = generated_code
        spec.status = "code_generated"
        
        # Save generated code
        code_dir = self.deliverables_dir / f"{spec.project_name}/generated_code"
        code_dir.mkdir(exist_ok=True)
        
        # Save each component
        for component, content in generated_code.items():
            if component == "backend":
                backend_dir = code_dir / "backend"
                backend_dir.mkdir(exist_ok=True)
                for file_path, file_content in content.items():
                    full_path = backend_dir / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(file_content)
            elif component == "frontend":
                frontend_dir = code_dir / "frontend"
                frontend_dir.mkdir(exist_ok=True)
                for file_path, file_content in content.items():
                    full_path = frontend_dir / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(file_content)
            else:
                # Save other components as JSON
                component_file = code_dir / f"{component}.json"
                with open(component_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
        
        print(f"✅ Code generation complete: {code_dir}")
        return spec
    
    def step5_validate_and_verify(self, spec: ProjectSpecification) -> ProjectSpecification:
        """Step 5: Validate specifications and verify dependencies"""
        print(f"✅ Step 5: Validation and Verification for {spec.project_name}")
        
        project_dir = self.deliverables_dir / spec.project_name
        
        # Pre-code validation
        validator = PreCodeValidator(str(project_dir))
        validation_report = validator.run_full_validation()
        
        # Dependency verification
        verifier = DependencyVerifier()
        verification_report = verifier.run_full_verification()
        
        spec.validation_report = {
            "pre_code_validation": validation_report,
            "dependency_verification": verification_report,
            "timestamp": datetime.now().isoformat()
        }
        
        # Determine overall status
        if validation_report["overall_status"] == "failed":
            spec.status = "validation_failed"
        elif verification_report["overall_status"] == "failed":
            spec.status = "verification_failed"
        else:
            spec.status = "ready_for_development"
        
        # Save validation reports
        validation_file = project_dir / "validation_report.json"
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(spec.validation_report, f, indent=2)
        
        print(f"✅ Validation complete: {validation_file}")
        return spec
    
    def map_archetype_to_app_type(self, archetype: str) -> str:
        """Map project archetype to app type for prompt templates"""
        mapping = {
            "CRUD": "CRUD",
            "CHATBOT": "CHATBOT", 
            "RAG": "RAG",
            "DASHBOARD": "DASHBOARD",
            "GENERATOR": "GENERATOR",
            "ANALYTICS": "ANALYTICS"
        }
        return mapping.get(archetype.upper(), "CRUD")
    
    async def process_project(self, project: Dict[str, Any]) -> ProjectSpecification:
        """Process a single project through all phases"""
        print(f"\n🚀 Processing Project: {project['project_name']}")
        print("=" * 60)
        
        spec = self.get_project_specification(project)
        
        try:
            # Step 1: Market Research
            spec = await self.step1_market_research(spec)
            
            # Step 2: Create Project Brief
            spec = self.step2_create_project_brief(spec)
            
            # Step 3: Select Prompt Template
            spec = self.step3_select_prompt_template(spec)
            
            # Step 4: Generate Code
            spec = await self.step4_generate_code(spec)
            
            # Step 5: Validate and Verify
            spec = self.step5_validate_and_verify(spec)
            
            print(f"\n🎉 Project Complete: {spec.project_name}")
            print(f"Status: {spec.status}")
            
        except Exception as e:
            print(f"❌ Error processing {spec.project_name}: {str(e)}")
            spec.status = "error"
            spec.validation_report = {"error": str(e)}
        
        return spec
    
    async def process_all_projects(self, start_index: int = 0, end_index: Optional[int] = None) -> List[ProjectSpecification]:
        """Process all projects through the pipeline"""
        print(f"🚀 Starting Phase 3: Research → Prompt → Code")
        print(f"Total projects: {len(self.projects)}")
        
        if end_index is None:
            end_index = len(self.projects)
        
        projects_to_process = self.projects[start_index:end_index]
        results = []
        
        for i, project in enumerate(projects_to_process, start=start_index + 1):
            print(f"\n📊 Progress: {i}/{len(self.projects)}")
            
            result = await self.process_project(project)
            results.append(result)
            
            # Save progress
            self.save_progress(results)
        
        print(f"\n🎉 Phase 3 Complete!")
        print(f"Processed: {len(results)} projects")
        
        return results
    
    def save_progress(self, results: List[ProjectSpecification]):
        """Save progress to file"""
        progress_file = self.deliverables_dir / "phase3_progress.json"
        
        progress_data = {
            "timestamp": datetime.now().isoformat(),
            "total_projects": len(self.projects),
            "completed_projects": len(results),
            "results": [
                {
                    "project_name": r.project_name,
                    "status": r.status,
                    "archetype": r.archetype
                }
                for r in results
            ]
        }
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2)

def main():
    """Main entry point for Phase 3"""
    import sys
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Phase 3: Research → Prompt → Code Workflow')
    parser.add_argument('--test', action='store_true', help='Run in test mode (process first project only)')
    parser.add_argument('--start', type=int, help='Start index for processing projects')
    parser.add_argument('--end', type=int, help='End index for processing projects')
    parser.add_argument('--step5-only', action='store_true', help='Run only Step 5 (validation) without LLM calls')
    
    args = parser.parse_args()
    
    orchestrator = Phase3Orchestrator()
    
    if args.step5_only:
        # Test only Step 5 (validation) without expensive LLM calls
        print("🧪 Running STEP 5 ONLY - Testing validation without LLM calls")
        test_project = orchestrator.projects[0]
        spec = orchestrator.get_project_specification(test_project)
        
        # Simulate completed steps 1-4
        spec.market_research = {"analysis": {"TARGET AUDIENCE": "Developers", "COMPETITORS": "SonarQube, CodeClimate"}}
        spec.project_brief = "Test project brief content"
        spec.prompt_template = {"app_type": "CRUD", "prompt_template": "Test template"}
        spec.generated_code = {"backend": {"main.py": "test code"}, "frontend": {"app/page.tsx": "test code"}}
        
        # Run only Step 5
        spec = orchestrator.step5_validate_and_verify(spec)
        print(f"✅ Step 5 Complete: {spec.project_name}")
        print(f"Status: {spec.status}")
        return
    
    if args.test:
        print("🧪 Running in TEST MODE - Processing first project only")
        # Run the pipeline on first project only
        asyncio.run(orchestrator.process_all_projects(0, 1))
    else:
        # Run the pipeline
        asyncio.run(orchestrator.process_all_projects(args.start, args.end))

if __name__ == "__main__":
    main()
