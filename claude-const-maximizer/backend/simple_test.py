import requests
import json
import time

def simple_test():
    """Simple test to check result saving"""
    
    project_data = {
        "projectName": "Test Project",
        "projectId": "test-project"
    }
    
    print("🚀 Starting simple test...")
    
    # Step 1: Start project
    print("📋 Starting project...")
    response = requests.post(
        "http://localhost:8001/api/run-crewai-project",
        json=project_data,
        timeout=300
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Project completed!")
        print(f"Result type: {type(result.get('result'))}")
        print(f"Result preview: {str(result.get('result'))[:200]}...")
    else:
        print(f"❌ Failed: {response.status_code}")
        return
    
    # Step 2: Wait a moment
    print("⏳ Waiting...")
    time.sleep(5)
    
    # Step 3: Check pipeline status directly
    print("📊 Checking pipeline status...")
    try:
        with open('pipeline_status.json', 'r') as f:
            data = json.load(f)
        
        if 'test-project' in data:
            project = data['test-project']
            print(f"✅ Project found in pipeline_status.json")
            print(f"Status: {project.get('status')}")
            print(f"Has result: {'result' in project}")
            if 'result' in project:
                print(f"Result length: {len(str(project['result']))}")
                print(f"Result preview: {str(project['result'])[:200]}...")
            else:
                print("❌ No result found!")
        else:
            print("❌ Project not found in pipeline_status.json")
            
    except Exception as e:
        print(f"❌ Error reading pipeline_status.json: {e}")
    
    # Step 4: Check report
    print("📄 Checking report...")
    report_response = requests.get("http://localhost:8001/api/pipeline-complete/test-project")
    if report_response.status_code == 200:
        report = report_response.json()
        print(f"✅ Report generated")
        print(f"Report status: {report.get('status')}")
        print(f"Has market research: {'market_research' in report.get('deliverables', {})}")
        
        market_research = report.get('deliverables', {}).get('market_research', {})
        if market_research.get('content'):
            content = market_research['content']
            if 'Comprehensive market analysis' in content:
                print("⚠️ Still showing generic market research")
            else:
                print("✅ Real market research data!")
        else:
            print("❌ No market research content")
    else:
        print(f"❌ Report failed: {report_response.status_code}")

if __name__ == "__main__":
    simple_test()


