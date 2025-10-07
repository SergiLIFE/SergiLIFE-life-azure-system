#!/usr/bin/env python3
"""
L.I.F.E. Platform Empty File Detector
Scan workspace for empty files and create remediation report

Copyright 2025 - Sergio Paya Borrull
"""
import json
import os
from datetime import datetime
from pathlib import Path


def detect_empty_files():
    """Detect and report empty files in L.I.F.E. Platform"""
    
    print("🔍 L.I.F.E. Platform Empty File Detection System")
    print("=" * 60)
    
    workspace_root = os.getcwd()
    empty_files = []
    large_files = []
    all_files = []
    
    # Directories to skip
    skip_dirs = {'.git', '__pycache__', '.mypy_cache', 'node_modules', '.venv', '.env'}
    
    for root, dirs, files in os.walk(workspace_root):
        # Filter out skip directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            try:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, workspace_root)
                file_size = os.path.getsize(file_path)
                
                file_info = {
                    'name': file,
                    'path': relative_path,
                    'size': file_size,
                    'extension': os.path.splitext(file)[1].lower()
                }
                
                all_files.append(file_info)
                
                # Detect empty files
                if file_size == 0:
                    empty_files.append(file_info)
                    
                # Track large files for reference
                elif file_size > 100000:  # > 100KB
                    large_files.append(file_info)
                    
            except (OSError, PermissionError):
                continue
    
    # Generate report
    report = {
        "audit_info": {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(all_files),
            "empty_files_count": len(empty_files),
            "large_files_count": len(large_files)
        },
        "empty_files": empty_files[:50],  # First 50 empty files
        "large_files": large_files[:20],   # First 20 large files
        "recommendations": []
    }
    
    # Print results
    print(f"📊 SCAN RESULTS:")
    print(f"├─ Total files scanned: {len(all_files):,}")
    print(f"├─ Empty files found: {len(empty_files)}")
    print(f"└─ Large files (>100KB): {len(large_files)}")
    
    if empty_files:
        print(f"\n⚠️  EMPTY FILES DETECTED:")
        for i, file in enumerate(empty_files[:10], 1):
            print(f"{i:2}. {file['path']}")
        
        if len(empty_files) > 10:
            print(f"    ... and {len(empty_files) - 10} more empty files")
        
        # Generate recommendations
        for file in empty_files:
            if file['extension'] in ['.env', '.txt', '.bat']:
                report['recommendations'].append({
                    'file': file['path'],
                    'priority': 'HIGH',
                    'action': 'Requires content - critical for functionality'
                })
            elif file['extension'] in ['.json', '.yaml', '.yml']:
                report['recommendations'].append({
                    'file': file['path'],
                    'priority': 'MEDIUM',
                    'action': 'Configuration file - may need default values'
                })
            else:
                report['recommendations'].append({
                    'file': file['path'],
                    'priority': 'LOW',
                    'action': 'Review if file is needed or can be removed'
                })
    else:
        print("✅ No empty files found! System is clean.")
    
    # Save detailed report
    report_file = f"EMPTY_FILES_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📁 Detailed report saved: {report_file}")
    
    # Summary for October 7th launch
    if len(empty_files) <= 5:
        print(f"\n🎯 LAUNCH STATUS: ✅ READY")
        print(f"Few or no empty files detected - system is launch-ready!")
    else:
        print(f"\n⚠️  LAUNCH ATTENTION NEEDED:")
        print(f"Review {len(empty_files)} empty files before October 7th launch")
    
    return report

if __name__ == "__main__":
    try:
        report = detect_empty_files()
        print("\n🎉 Empty file detection completed successfully!")
    except Exception as e:
        print(f"❌ Error during scan: {str(e)}")        print(f"❌ Error during scan: {str(e)}")