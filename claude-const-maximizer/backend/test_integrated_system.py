import requests
import json
import time

def test_integrated_system():
    """Test the integrated system with direct pipeline"""
    
    project_data = {
        "projectName": "AI-Powered Financial Analysis & Trading Bot",
        "projectId": "ai-powered-financial-analysis-and-trading-bot"
    }
    
    print("🧪 Testing Integrated System with Direct Pipeline...")
    print(f"Project: {project_data['projectName']}")
    print(f"Project ID: {project_data['projectId']}")
    
    # Step 1: Run the project
    print("\n📋 Step 1: Running project...")
    try:
        response = requests.post(
            "http://localhost:8001/api/run-crewai-project",
            json=project_data,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Project completed successfully!")
            result_text = str(result.get('result', ''))
            print(f"Result length: {len(result_text)}")
        else:
            print(f"❌ Failed to run project: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error running project: {e}")
        return
    
    # Step 2: Wait a moment
    print("\n⏳ Step 2: Waiting for processing...")
    time.sleep(5)
    
    # Step 3: Check if direct result was saved
    print("\n📁 Step 3: Checking direct result file...")
    import os
    direct_result_file = f"direct_results/{project_data['projectId']}_result.json"
    if os.path.exists(direct_result_file):
        print(f"✅ Direct result file exists: {direct_result_file}")
        with open(direct_result_file, 'r') as f:
            direct_data = json.load(f)
            print(f"Direct result length: {len(direct_data.get('result', ''))}")
    else:
        print(f"❌ Direct result file not found: {direct_result_file}")
    
    # Step 4: Get the report from the integrated system
    print("\n📄 Step 4: Getting integrated report...")
    try:
        report_response = requests.get(f"http://localhost:8001/api/pipeline-complete/{project_data['projectId']}")
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"✅ Report generated successfully!")
            print(f"Report status: {report.get('status')}")
            
            # Check if we have real data
            market_research = report.get('deliverables', {}).get('market_research', {})
            if market_research.get('content'):
                content = market_research['content']
                if 'Comprehensive market analysis' in content:
                    print("⚠️ Still showing generic market research")
                else:
                    print("🎉 SUCCESS: Real CrewAI data in integrated report!")
                    print(f"Content preview: {content[:200]}...")
            else:
                print("❌ No market research content")
                
            # Check for custom boilerplates
            has_frontend_boilerplate = 'frontend_boilerplate' in report.get('deliverables', {})
            has_backend_boilerplate = 'backend_boilerplate' in report.get('deliverables', {})
            print(f"Has frontend boilerplate: {has_frontend_boilerplate}")
            print(f"Has backend boilerplate: {has_backend_boilerplate}")
            
        else:
            print(f"❌ Report failed: {report_response.status_code}")
            print(f"Error: {report_response.text}")
            
    except Exception as e:
        print(f"❌ Error getting report: {e}")
    
    print("\n🎯 Integrated system test completed!")

if __name__ == "__main__":
    test_integrated_system()


