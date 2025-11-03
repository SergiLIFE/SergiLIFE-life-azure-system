import os
import re
from pathlib import Path

def categorize_files(repo_path, quarantine_path):
    
    # File patterns to quarantine
    patterns = {
        "auto_generated": [
            r"^COMPREHENSIVE.*\.(md|html|txt)$",
            r"^EMERGENCY.*\.(bat|ps1|py|md)$",
            r"^DEPLOY.*\.(bat|ps1|sh)$",
            r"^QUICK.*\.(bat|ps1|md)$",
            r"^IMMEDIATE.*\.(py|md|txt)$",
            r"^FINAL.*\.(bat|ps1|md)$",
            r".*REPORT\.(md|html|txt)$",
            r".*SUMMARY\.(md|html|txt)$"
        ],
        "duplicates": [
            r".*CORRECTED.*",
            r".*FIXED.*",
            r".*VERIFIED.*",
            r".*UPDATED.*"
        ],
        "scripts": [
            r".*\.(bat|ps1|sh)$"
        ]
    }
    
    categorized = {cat: [] for cat in patterns}
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories and known safe paths
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_path)
            
            for category, pattern_list in patterns.items():
                if any(re.match(pattern, file, re.IGNORECASE) for pattern in pattern_list):
                    categorized[category].append(rel_path)
                    break
    
    return categorized

# Categorize files
categorized = categorize_files(".", ".cleanup/quarantine")

# Log results
for category, files in categorized.items():
    print(f"\n{category}: {len(files)} files")
    with open(f".cleanup/logs/{category}.txt", "w") as f:
        for file in files:
            f.write(file + "\n")