import requests
import json

def debug_report_structure():
    """Debug the actual report structure"""
    
    project_id = "ai-powered-voice-controlled-smart-home-manager"
    
    print("🔍 Debugging Report Structure...")
    print(f"Project ID: {project_id}")
    
    # Get the report
    try:
        report_response = requests.get(f"http://localhost:8001/api/pipeline-complete/{project_id}")
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"✅ Report generated successfully!")
            
            # Check the structure
            print(f"\n📊 Report Structure:")
            print(f"Project ID: {report.get('projectId')}")
            print(f"Project Name: {report.get('projectName')}")
            print(f"Status: {report.get('status')}")
            
            deliverables = report.get('deliverables', {})
            print(f"\n📦 Deliverables keys: {list(deliverables.keys())}")
            
            # Check market research
            market_research = deliverables.get('market_research', {})
            print(f"\n📈 Market Research:")
            print(f"Keys: {list(market_research.keys())}")
            print(f"Summary: {market_research.get('summary', 'No summary')}")
            
            content = market_research.get('content', '')
            if content:
                print(f"Content length: {len(content)}")
                print(f"Content preview: {content[:200]}...")
                
                # Check if it's real data
                if "Complete Project Package for AI Application Market Research" in content:
                    print("✅ Confirmed: Real CrewAI data!")
                else:
                    print("⚠️ Not the expected CrewAI data")
            else:
                print("❌ No content found")
            
            # Check boilerplates
            print(f"\n🔧 Boilerplates:")
            print(f"Frontend boilerplate: {'frontend_boilerplate' in deliverables}")
            print(f"Backend boilerplate: {'backend_boilerplate' in deliverables}")
            
            if 'backend_boilerplate' in deliverables:
                backend_bp = deliverables['backend_boilerplate']
                print(f"Backend boilerplate keys: {list(backend_bp.keys())}")
                files = backend_bp.get('files', [])
                print(f"Backend files: {len(files)}")
            
        else:
            print(f"❌ Report failed: {report_response.status_code}")
            print(f"Error: {report_response.text}")
            
    except Exception as e:
        print(f"❌ Error getting report: {e}")
    
    print("\n🎯 Debug completed!")

if __name__ == "__main__":
    debug_report_structure()


