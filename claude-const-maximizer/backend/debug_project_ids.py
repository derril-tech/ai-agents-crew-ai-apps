import json

# Load the pipeline status
with open('pipeline_status.json', 'r') as f:
    data = json.load(f)

print("=== ALL PROJECT IDs IN PIPELINE_STATUS.JSON ===")
for i, project_id in enumerate(data.keys(), 1):
    project_data = data[project_id]
    status = project_data.get('status', 'unknown')
    has_result = 'result' in project_data
    result_preview = ""
    if has_result:
        result_text = str(project_data['result'])
        result_preview = result_text[:100] + "..." if len(result_text) > 100 else result_text
    
    print(f"{i:2d}. {project_id}")
    print(f"    Status: {status}")
    print(f"    Has Result: {has_result}")
    if has_result:
        print(f"    Result Preview: {result_preview}")
    print()

# Check for the specific project we're testing
test_project_id = "ai-powered-voice-controlled-smart-home-manager"
print(f"\n=== LOOKING FOR TEST PROJECT ===")
print(f"Test Project ID: {test_project_id}")
if test_project_id in data:
    print(f"✅ Found! Status: {data[test_project_id].get('status')}")
    print(f"   Has Result: {'result' in data[test_project_id]}")
else:
    print(f"❌ Not found!")
    
    # Look for similar IDs
    print(f"\nSimilar project IDs:")
    for key in data.keys():
        if "voice" in key.lower() or "smart" in key.lower() or "home" in key.lower():
            print(f"  - {key}")


