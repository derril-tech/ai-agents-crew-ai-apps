import requests
import json
import time
from pathlib import Path

def test_project_completion():
    """Test running a project to completion and monitor data flow"""
    
    # Test project
    project_data = {
        "projectName": "AI-Powered Voice-Controlled Smart Home Manager",
        "projectId": "ai-powered-voice-controlled-smart-home-manager"
    }
    
    print("🚀 Starting test project completion...")
    print(f"Project: {project_data['projectName']}")
    print(f"Project ID: {project_data['projectId']}")
    
    # Step 1: Start the project
    print("\n📋 Step 1: Starting project...")
    try:
        response = requests.post(
            "http://localhost:8001/api/run-crewai-project",
            json=project_data,
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Project started successfully!")
            result_text = str(result.get('result', 'No result'))
            print(f"Result: {result_text[:200]}...")
        else:
            print(f"❌ Failed to start project: {response.status_code}")
            print(f"Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error starting project: {e}")
        return
    
    # Step 2: Wait a bit and check status
    print("\n⏳ Step 2: Waiting for completion...")
    time.sleep(10)
    
    # Step 3: Check pipeline status
    print("\n📊 Step 3: Checking pipeline status...")
    try:
        status_response = requests.get("http://localhost:8001/api/pipeline-status")
        if status_response.status_code == 200:
            status_data = status_response.json()
            project_status = status_data.get(project_data['projectId'], {})
            print(f"Project Status: {project_status.get('status', 'unknown')}")
            print(f"Has Result: {'result' in project_status}")
            if 'result' in project_status:
                result_text = str(project_status['result'])
                print(f"Result Preview: {result_text[:200]}...")
        else:
            print(f"❌ Failed to get status: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
    
    # Step 4: Try to get the report
    print("\n📄 Step 4: Getting project report...")
    try:
        report_response = requests.get(f"http://localhost:8001/api/pipeline-complete/{project_data['projectId']}")
        if report_response.status_code == 200:
            report_data = report_response.json()
            print(f"✅ Report generated successfully!")
            print(f"Report Status: {report_data.get('status', 'unknown')}")
            print(f"Has Market Research: {'market_research' in report_data.get('deliverables', {})}")
            print(f"Has Frontend Boilerplate: {'frontend_boilerplate' in report_data.get('deliverables', {})}")
            print(f"Has Backend Boilerplate: {'backend_boilerplate' in report_data.get('deliverables', {})}")
            
            # Check if we have real data or generic data
            market_research = report_data.get('deliverables', {}).get('market_research', {})
            if market_research.get('content') and 'Comprehensive market analysis' not in market_research.get('content', ''):
                print("✅ Real market research data found!")
            else:
                print("⚠️ Generic market research data")
                
        else:
            print(f"❌ Failed to get report: {report_response.status_code}")
            print(f"Error: {report_response.text}")
            
    except Exception as e:
        print(f"❌ Error getting report: {e}")
    
    # Step 5: Check if deliverables directory was created
    print("\n📁 Step 5: Checking deliverables directory...")
    deliverables_path = Path(f"../deliverables/{project_data['projectId']}")
    if deliverables_path.exists():
        print(f"✅ Deliverables directory exists: {deliverables_path}")
        files = list(deliverables_path.rglob("*"))
        print(f"Files found: {len(files)}")
        for file in files[:5]:  # Show first 5 files
            print(f"  - {file.name}")
    else:
        print(f"❌ Deliverables directory not found: {deliverables_path}")
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    test_project_completion()
