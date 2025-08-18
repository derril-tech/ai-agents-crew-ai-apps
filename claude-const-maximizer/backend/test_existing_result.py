import requests
import json

def test_existing_result():
    """Test the integrated system with existing direct result"""
    
    project_id = "ai-powered-voice-controlled-smart-home-manager"
    
    print("🧪 Testing Integrated System with Existing Direct Result...")
    print(f"Project ID: {project_id}")
    
    # Check if direct result exists
    import os
    direct_result_file = f"direct_results/{project_id}_result.json"
    if not os.path.exists(direct_result_file):
        print(f"❌ Direct result file not found: {direct_result_file}")
        return
    
    print(f"✅ Direct result file exists: {direct_result_file}")
    
    # Get the report from the integrated system
    print("\n📄 Getting integrated report...")
    try:
        report_response = requests.get(f"http://localhost:8001/api/pipeline-complete/{project_id}")
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
                    
                    # Check if it's the real content we expect
                    if "Complete Project Package for AI Application Market Research" in content:
                        print("✅ Confirmed: This is the real CrewAI result!")
                    else:
                        print("⚠️ Content doesn't match expected CrewAI result")
            else:
                print("❌ No market research content")
                
            # Check for custom boilerplates
            has_frontend_boilerplate = 'frontend_boilerplate' in report.get('deliverables', {})
            has_backend_boilerplate = 'backend_boilerplate' in report.get('deliverables', {})
            print(f"Has frontend boilerplate: {has_frontend_boilerplate}")
            print(f"Has backend boilerplate: {has_backend_boilerplate}")
            
            if has_backend_boilerplate:
                backend_files = report.get('deliverables', {}).get('backend_boilerplate', {}).get('files', [])
                print(f"Backend boilerplate files: {len(backend_files)}")
            
        else:
            print(f"❌ Report failed: {report_response.status_code}")
            print(f"Error: {report_response.text}")
            
    except Exception as e:
        print(f"❌ Error getting report: {e}")
    
    print("\n🎯 Existing result test completed!")

if __name__ == "__main__":
    test_existing_result()


