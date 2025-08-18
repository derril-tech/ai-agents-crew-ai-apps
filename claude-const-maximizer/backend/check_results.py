import json

# Load the pipeline status
with open('pipeline_status.json', 'r') as f:
    data = json.load(f)

print("=== PROJECTS WITH RESULTS ===")
projects_with_results = 0
for project_id, project_data in data.items():
    if 'result' in project_data and project_data['result']:
        projects_with_results += 1
        print(f"✅ {project_id}")
        print(f"   Result: {project_data['result'][:200]}...")
        print(f"   Status: {project_data.get('status', 'unknown')}")
        print()

print(f"\n=== SUMMARY ===")
print(f"Total projects: {len(data)}")
print(f"Projects with results: {projects_with_results}")
print(f"Projects without results: {len(data) - projects_with_results}")

if projects_with_results == 0:
    print("\n❌ NO PROJECTS HAVE COMPLETED SUCCESSFULLY!")
    print("This is why the reports show generic content.")
    print("You need to run a project to completion first.")


