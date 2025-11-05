import os
import json
from pathlib import Path
from collections import defaultdict

def analyze_repository(repo_path):
    analysis = {
        "total_files": 0,
        "file_types": defaultdict(int),
        "suspicious_files": [],
        "duplicate_names": defaultdict(list),
        "large_files": [],
        "auto_generated_patterns": []
    }
    
    # Define suspicious patterns
    suspicious_patterns = [
        "COMPREHENSIVE", "EMERGENCY", "DEPLOY", "FIX", "QUICK",
        "IMMEDIATE", "CRITICAL", "CORRECTED", "CORRECTED", "CREDENTIAL",
        "SECRET", "DIAGNOSTIC", "RECOVERY", "VALIDATION", "TEST"
    ]
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            analysis["total_files"] += 1
            filepath = os.path.join(root, file)
            
            # Track file extensions
            _, ext = os.path.splitext(file)
            analysis["file_types"][ext] += 1
            
            # Identify suspicious files
            if any(pattern in file.upper() for pattern in suspicious_patterns):
                analysis["suspicious_files"].append(file)
            
            # Track duplicates
            analysis["duplicate_names"][file].append(filepath)
            
            # Flag large files
            try:
                size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                if size > 5:
                    analysis["large_files"].append({
                        "file": file,
                        "size_mb": round(size, 2)
                    })
            except:
                pass
    
    return analysis

# Run analysis
results = analyze_repository(".")
with open("repo_analysis.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"Total files: {results['total_files']}")
print(f"Suspicious files: {len(results['suspicious_files'])}")
print(f"Large files: {len(results['large_files'])}")