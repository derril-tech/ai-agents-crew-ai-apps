#!/usr/bin/env python3
"""
Script to remove all emoji characters from Python files in the backend
"""

import os
import re
from pathlib import Path

# Emoji to text mapping
EMOJI_REPLACEMENTS = {
    '[OK]': '[OK]',
    '[ERROR]': '[ERROR]',
    '[WARN]': '[WARN]',
    '[PROCESS]': '[PROCESS]',
    '[LAUNCH]': '[START]',
    '[METRICS]': '[STATS]',
    '[INVESTIGATE]': '[SEARCH]',
    '[CHECKLIST]': '[INFO]',
    '[SUCCESS]': '[SUCCESS]',
    '[CONFIG]': '[DEBUG]',
    '[SCIENCE]': '[ANALYSIS]',
    '[DOC]': '[DOC]',
    '[FAST]': '[FAST]',
    '[GOAL]': '[TARGET]',
    '[IDEA]': '[IDEA]',
    '[TOOL]': '[FIX]',
    '[PROGRESS]': '[GROWTH]',
    '[PROTECT]': '[SECURITY]',
    '[NETWORK]': '[WEB]',
    '[APP]': '[MOBILE]',
    '[CODE]': '[TECH]',
    '[UI]': '[DESIGN]',
    '[KNOWLEDGE]': '[LEARN]',
    '[CONNECT]': '[LINK]',
    '[WRITE]': '[NOTE]',
    '[ENTERTAIN]': '[FUN]',
    '[MEDICAL]': '[HEALTH]',
    '[LAW]': '[LEGAL]',
    '[PLAY]': '[GAME]',
    '[STUDY]': '[EDU]',
    '[SCIENCE]': '[RESEARCH]',
    '[TALK]': '[CHAT]',
    '[READ]': '[RAG]',
    '[MONEY]': '[FINANCE]',
    '[CORP]': '[BUSINESS]',
    '[GOAL]': '[FOCUS]',
    '[LAUNCH]': '[LAUNCH]',
    '[METRICS]': '[METRICS]',
    '[INVESTIGATE]': '[INVESTIGATE]',
    '[CHECKLIST]': '[CHECKLIST]',
    '[CONFIG]': '[CONFIG]',
    '[TOOL]': '[TOOL]',
    '[PROGRESS]': '[PROGRESS]',
    '[PROTECT]': '[PROTECT]',
    '[NETWORK]': '[NETWORK]',
    '[APP]': '[APP]',
    '[CODE]': '[CODE]',
    '[UI]': '[UI]',
    '[KNOWLEDGE]': '[KNOWLEDGE]',
    '[CONNECT]': '[CONNECT]',
    '[WRITE]': '[WRITE]',
    '[ENTERTAIN]': '[ENTERTAIN]',
    '[MEDICAL]': '[MEDICAL]',
    '[LAW]': '[LAW]',
    '[PLAY]': '[PLAY]',
    '[STUDY]': '[STUDY]',
    '[SCIENCE]': '[SCIENCE]',
    '[TALK]': '[TALK]',
    '[READ]': '[READ]',
    '[MONEY]': '[MONEY]',
    '[CORP]': '[CORP]',
    '[GOAL]': '[GOAL]'
}

def clean_file(file_path):
    """Clean emoji characters from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all emoji characters
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)
        
        # Also replace any remaining Unicode emoji characters with a generic replacement
        # This regex matches most emoji characters
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF\U0001F900-\U0001F9FF\U0001F018-\U0001F270]')
        content = emoji_pattern.sub('[EMOJI]', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [CLEANED] {file_path}")
            return True
        else:
            print(f"  [SKIP] {file_path} (no emojis found)")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Failed to clean {file_path}: {e}")
        return False

def main():
    """Main cleanup function"""
    print("[CLEANUP] Starting emoji cleanup of all backend Python files...")
    
    backend_dir = Path(__file__).parent
    cleaned_count = 0
    total_count = 0
    
    # Find all Python files in backend directory
    for py_file in backend_dir.rglob("*.py"):
        total_count += 1
        if clean_file(py_file):
            cleaned_count += 1
    
    print(f"\n[CLEANUP] Complete!")
    print(f"  [STATS] Processed {total_count} files")
    print(f"  [STATS] Cleaned {cleaned_count} files")
    print(f"  [STATS] Skipped {total_count - cleaned_count} files")

if __name__ == "__main__":
    main()
