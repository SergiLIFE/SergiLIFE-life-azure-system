#!/usr/bin/env python3
"""
Repository Analysis Script for Automated Maintenance
Supports the GitHub Actions workflow for weekly repository health checks
"""

import os
import json
import glob
import subprocess
from datetime import datetime
from pathlib import Path

class RepositoryAnalyzer:
    def __init__(self):
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "file_counts": {},
            "problematic_files": [],
            "large_files": [],
            "repository_health": {},
            "recommendations": []
        }
    
    def analyze_file_patterns(self):
        """Check for problematic file naming patterns"""
        problematic_patterns = [
            "*EMERGENCY*", "*QUICK*", "*IMMEDIATE*", 
            "*COMPREHENSIVE*", "*FINAL*", "*CORRECTED*",
            "*DEPLOY*", "*AUTO*", "*GENERATED*"
        ]
        
        for pattern in problematic_patterns:
            matches = glob.glob(pattern, recursive=True)
            if matches:
                self.analysis_results["problematic_files"].extend(matches)
        
        print(f"Found {len(self.analysis_results['problematic_files'])} problematic files")
    
    def count_file_types(self):
        """Count files by extension"""
        extensions = ['.py', '.md', '.bat', '.html', '.js', '.json', '.yml', '.yaml']
        
        for ext in extensions:
            count = len(glob.glob(f"**/*{ext}", recursive=True))
            self.analysis_results["file_counts"][ext] = count
        
        print(f"File type analysis completed")
    
    def check_large_files(self):
        """Find files larger than 1MB"""
        large_files = []
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size > 1024 * 1024:  # 1MB
                        large_files.append({
                            "file": file_path,
                            "size_mb": round(size / (1024 * 1024), 2)
                        })
                except OSError:
                    pass
        
        self.analysis_results["large_files"] = large_files
        print(f"Found {len(large_files)} large files")
    
    def check_repository_health(self):
        """Check git repository health"""
        try:
            # Check if it's a git repository
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode == 0:
                self.analysis_results["repository_health"]["is_git_repo"] = True
                
                # Get repository statistics
                count_result = subprocess.run(['git', 'count-objects', '-v'], capture_output=True, text=True)
                if count_result.returncode == 0:
                    self.analysis_results["repository_health"]["git_stats"] = count_result.stdout
                
                # Check for uncommitted changes
                status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
                uncommitted_count = len(status_result.stdout.strip().split('\n')) if status_result.stdout.strip() else 0
                self.analysis_results["repository_health"]["uncommitted_files"] = uncommitted_count
                
            else:
                self.analysis_results["repository_health"]["is_git_repo"] = False
        except FileNotFoundError:
            self.analysis_results["repository_health"]["git_available"] = False
    
    def generate_recommendations(self):
        """Generate cleanup and maintenance recommendations"""
        recommendations = []
        
        if len(self.analysis_results["problematic_files"]) > 0:
            recommendations.append(f"Remove {len(self.analysis_results['problematic_files'])} files with problematic naming patterns")
        
        if len(self.analysis_results["large_files"]) > 5:
            recommendations.append(f"Review {len(self.analysis_results['large_files'])} large files for optimization")
        
        if self.analysis_results["repository_health"].get("uncommitted_files", 0) > 10:
            recommendations.append("Consider committing or cleaning up uncommitted changes")
        
        total_files = sum(self.analysis_results["file_counts"].values())
        if total_files > 1000:
            recommendations.append("Repository has grown large - consider archiving old files")
        
        if not recommendations:
            recommendations.append("Repository appears healthy - no immediate action required")
        
        self.analysis_results["recommendations"] = recommendations
    
    def save_results(self):
        """Save analysis results to JSON file"""
        with open('repo_analysis.json', 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print("Analysis results saved to repo_analysis.json")
    
    def run_analysis(self):
        """Run complete repository analysis"""
        print("Starting repository analysis...")
        
        self.analyze_file_patterns()
        self.count_file_types()
        self.check_large_files()
        self.check_repository_health()
        self.generate_recommendations()
        self.save_results()
        
        print("Repository analysis completed!")
        
        # Print summary
        print("\n=== ANALYSIS SUMMARY ===")
        print(f"Problematic files: {len(self.analysis_results['problematic_files'])}")
        print(f"Large files: {len(self.analysis_results['large_files'])}")
        print(f"Total file types analyzed: {len(self.analysis_results['file_counts'])}")
        print(f"Recommendations: {len(self.analysis_results['recommendations'])}")
        
        for rec in self.analysis_results['recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    analyzer = RepositoryAnalyzer()
    analyzer.run_analysis()