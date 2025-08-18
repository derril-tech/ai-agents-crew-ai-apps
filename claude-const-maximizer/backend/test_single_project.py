# test_single_project.py
import json
from pathlib import Path
from crew_app.crew import build_crew

PROJECTS_FILE = Path("../projects.json")

def test_single_project():
    """Test the pipeline with just 1 project to save tokens."""
    
    # Load projects
    data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) > 0, "projects.json should be a non-empty list"
    
    # Take only the first project
    test_project = data[0]
    name = test_project.get("project_name", "unnamed")
    
    print(f"🧪 Testing pipeline with 1 project: {name}")
    print(f"📋 Project brief: {test_project.get('description', 'No description')[:100]}...")
    
    try:
        # Build and run crew
        crew = build_crew()
        result = crew.kickoff(inputs={"project_brief": test_project})
        
        print(f"✅ SUCCESS: {name}")
        print(f"📁 Output directory: {result['deliverables_dir']}")
        
        # Check what was generated
        output_dir = Path(result['deliverables_dir'])
        if output_dir.exists():
            files = list(output_dir.rglob("*"))
            print(f"📄 Generated {len(files)} files:")
            for file in files[:10]:  # Show first 10 files
                print(f"   - {file.relative_to(output_dir)}")
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {name}")
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    success = test_single_project()
    if success:
        print("\n🎉 Pipeline test successful! Ready to run full pipeline.")
    else:
        print("\n⚠️  Pipeline test failed. Check configuration before running full pipeline.")
