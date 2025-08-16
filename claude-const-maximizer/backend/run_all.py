# run_all.py
import json
import math
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from crew_app.crew import build_crew

PROJECTS_FILE = Path("../projects.json")
BATCH_SIZE = 5         # run N projects at a time (tune based on API limits & your machine)
MAX_WORKERS = 5        # same as batch, one worker per project
RETRY = 1              # simple retry count if a run fails

def load_projects():
    data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) > 0, "projects.json should be a non-empty list"
    return data

def process_one(brief, attempt=1):
    name = brief.get("project_name", "unnamed")
    print(f"→ Starting: {name} (attempt {attempt})")
    try:
        crew = build_crew()
        result = crew.kickoff(inputs={"project_brief": brief})
        print(f"[EMOJI] Done: {name} → {result['deliverables_dir']}")
        return {"name": name, "ok": True, "dir": result["deliverables_dir"]}
    except Exception as e:
        print(f"[EMOJI] Failed: {name}: {e}")
        if attempt <= RETRY:
            time.sleep(2)
            return process_one(brief, attempt=attempt + 1)
        return {"name": name, "ok": False, "error": str(e)}

def run_batches(projects):
    total = len(projects)
    batches = math.ceil(total / BATCH_SIZE)
    all_results = []

    for i in range(batches):
        start = i * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = projects[start:end]
        print(f"\n=== Batch {i+1}/{batches} | Projects {start+1}–{end} of {total} ===")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = [pool.submit(process_one, brief) for brief in batch]
            for f in as_completed(futures):
                all_results.append(f.result())

    return all_results

def summarize(results):
    success = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]
    print("\n=== SUMMARY ===")
    print(f"Success: {len(success)}")
    for s in success:
        print(f"  - {s['name']} → {s['dir']}")
    if failed:
        print(f"\nFailed: {len(failed)}")
        for f in failed:
            print(f"  - {f['name']}: {f.get('error')}")

if __name__ == "__main__":
    projects = load_projects()
    results = run_batches(projects)
    summarize(results)

