# Debug script to check project ID mapping
project_name = "AI-Powered Voice-Based Meeting Assistant & Note Taker"
project_id_old = project_name.lower().replace(" ", "-")
project_id_new = project_name.lower().replace(" ", "-").replace("&", "and")
print(f"Project Name: {project_name}")
print(f"Old Project ID: {project_id_old}")
print(f"New Project ID: {project_id_new}")

# Check if this ID exists in pipeline_status.json
import json
with open('pipeline_status.json', 'r') as f:
    data = json.load(f)

print(f"\nAvailable project IDs in pipeline_status.json:")
for key in data.keys():
    print(f"  - {key}")

print(f"\nLooking for old project ID: {project_id_old}")
if project_id_old in data:
    print(f"✅ Found old ID! Status: {data[project_id_old].get('status')}")
    print(f"   Has result: {'result' in data[project_id_old]}")
    if 'result' in data[project_id_old]:
        print(f"   Result preview: {data[project_id_old]['result'][:100]}...")
else:
    print(f"❌ Old ID not found!")

print(f"\nLooking for new project ID: {project_id_new}")
if project_id_new in data:
    print(f"✅ Found new ID! Status: {data[project_id_new].get('status')}")
    print(f"   Has result: {'result' in data[project_id_new]}")
    if 'result' in data[project_id_new]:
        print(f"   Result preview: {data[project_id_new]['result'][:100]}...")
else:
    print(f"❌ New ID not found!")
    
    # Look for similar IDs
    print(f"\nSimilar project IDs:")
    for key in data.keys():
        if "voice" in key.lower() or "meeting" in key.lower() or "assistant" in key.lower():
            print(f"  - {key}")
