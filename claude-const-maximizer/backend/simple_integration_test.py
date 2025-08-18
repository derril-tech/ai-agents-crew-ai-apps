import requests
import json
import time

def simple_integration_test():
    """Simple test to verify direct pipeline integration"""
    
    print("🧪 Simple Integration Test...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"✅ Server is running: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return
    
    # Test 2: Check direct result file
    import os
    project_id = "ai-powered-voice-controlled-smart-home-manager"
    direct_result_file = f"direct_results/{project_id}_result.json"
    
    if os.path.exists(direct_result_file):
        print(f"✅ Direct result file exists: {direct_result_file}")
        with open(direct_result_file, 'r') as f:
            data = json.load(f)
            result_length = len(data.get('result', ''))
            print(f"✅ Direct result length: {result_length}")
    else:
        print(f"❌ Direct result file not found: {direct_result_file}")
        return
    
    # Test 3: Get report from API
    try:
        print("\n📄 Getting report from API...")
        report_response = requests.get(f"http://localhost:8001/api/pipeline-complete/{project_id}", timeout=10)
        
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"✅ Report API call successful")
            
            # Check market research
            market_research = report.get('deliverables', {}).get('market_research', {})
            content = market_research.get('content', '')
            
            if content:
                print(f"✅ Market research content found: {len(content)} chars")
                if "Complete Project Package for AI Application Market Research" in content:
                    print("🎉 SUCCESS: Real CrewAI data in report!")
                else:
                    print("⚠️ Content doesn't match expected CrewAI result")
            else:
                print("❌ No market research content")
                
        else:
            print(f"❌ Report API failed: {report_response.status_code}")
            print(f"Error: {report_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing report API: {e}")
    
    print("\n🎯 Integration test completed!")

if __name__ == "__main__":
    simple_integration_test()


