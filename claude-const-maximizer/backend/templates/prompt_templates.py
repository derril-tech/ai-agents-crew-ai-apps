"""
Prompt Templates for Phase 3 Pipeline
"""

import json
from pathlib import Path

# Load the JSON file
template_file = Path(__file__).parent / "prompt_templates.json"

with open(template_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Export the app types as PROMPT_TEMPLATES
PROMPT_TEMPLATES = data.get("app_types", {})

# Export Claude Constitution if available
CLAUDE_CONSTITUTION = data.get("claude_constitution", {
    "rules": [
        "Write clean, production-ready code",
        "Follow best practices and design patterns",
        "Include proper error handling and validation",
        "Add comprehensive documentation",
        "Ensure security best practices",
        "Optimize for performance and scalability",
        "Use modern development practices",
        "Include proper testing structure"
    ]
})
