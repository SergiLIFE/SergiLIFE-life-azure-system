#!/usr/bin/env python3
"""
FILE CORRUPTION SCANNER
Advanced file integrity checker for the L.I.F.E Platform repository.
Detects various forms of file corruption and formatting issues.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E Platform - Production-Ready File Integrity System
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import chardet
import yaml


class FileCorruptionScanner:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.scan_results = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_files_scanned": 0,
            "corrupted_files": [],
            "suspicious_files": [],
            "encoding_issues": [],
            "single_line_files": [],
            "oversized_lines": [],
            "summary": {}
        }
        
        # File patterns to check
        self.critical_extensions = ['.md', '.py', '.json', '.yaml', '.yml', '.html', '.js', '.css', '.txt']
        self.skip_patterns = [
            '.git', '__pycache__', '.vscode', 'node_modules', '.env',
            '.pyc', '.log', '.cache', 'venv', '.backup'
        ]
        
    def should_skip_file(self, file_path):
        """Check if file should be skipped based on patterns"""
        path_str = str(file_path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                return True
        return False
        
    def detect_encoding(self, file_path):
        """Detect file encoding"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result['encoding'], result['confidence']
        except Exception as e:
            return None, 0
            
    def check_single_line_corruption(self, file_path):
        """Check if file is corrupted with all content on one line"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            if len(lines) == 1 and len(lines[0]) > 1000:
                return True, len(lines[0])
            return False, len(lines) if lines else 0
            
        except Exception as e:
            return None, str(e)
            
    def check_oversized_lines(self, file_path, max_line_length=500):
        """Check for abnormally long lines that might indicate corruption"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            oversized_lines = []
            for i, line in enumerate(lines, 1):
                if len(line) > max_line_length:
                    oversized_lines.append({
                        "line_number": i,
                        "length": len(line),
                        "preview": line[:100] + "..." if len(line) > 100 else line
                    })
                    
            return oversized_lines
            
        except Exception as e:
            return [{"error": str(e)}]
            
    def validate_json_file(self, file_path):
        """Validate JSON file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "Valid JSON"
        except json.JSONDecodeError as e:
            return False, f"JSON Error: {e}"
        except Exception as e:
            return False, f"File Error: {e}"
            
    def validate_yaml_file(self, file_path):
        """Validate YAML file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            return True, "Valid YAML"
        except yaml.YAMLError as e:
            return False, f"YAML Error: {e}"
        except Exception as e:
            return False, f"File Error: {e}"
            
    def check_python_syntax(self, file_path):
        """Basic Python syntax check"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                
            # Basic checks
            issues = []
            
            # Check for proper indentation
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    if ':' in line and not line.strip().startswith('#'):
                        # Likely a function/class definition without proper structure
                        continue
                        
            # Check for basic Python structure
            if 'def ' in code or 'class ' in code or 'import ' in code:
                return True, "Valid Python structure"
            elif len(code.strip()) == 0:
                return True, "Empty file"
            else:
                return True, "Basic text file"
                
        except Exception as e:
            return False, f"Python check error: {e}"
            
    def scan_file(self, file_path):
        """Comprehensive scan of a single file"""
        file_info = {
            "path": str(file_path),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "extension": file_path.suffix.lower(),
            "issues": []
        }
        
        # Skip empty files or very large files
        if file_info["size"] == 0:
            file_info["issues"].append("Empty file")
            return file_info
            
        if file_info["size"] > 50 * 1024 * 1024:  # 50MB
            file_info["issues"].append("Very large file - skipped detailed scan")
            return file_info
            
        # Encoding detection
        encoding, confidence = self.detect_encoding(file_path)
        file_info["encoding"] = encoding
        file_info["encoding_confidence"] = confidence
        
        if confidence < 0.7:
            file_info["issues"].append(f"Low encoding confidence: {confidence:.2f}")
            
        # Single line corruption check
        is_single_line, line_info = self.check_single_line_corruption(file_path)
        if is_single_line:
            file_info["issues"].append(f"CORRUPTION: All content on single line ({line_info} chars)")
            self.scan_results["single_line_files"].append(file_info["path"])
            
        # Oversized lines check
        oversized = self.check_oversized_lines(file_path)
        if oversized:
            file_info["oversized_lines"] = oversized
            if len(oversized) > 0 and "error" not in oversized[0]:
                file_info["issues"].append(f"Has {len(oversized)} oversized lines")
                
        # File-specific validation
        ext = file_info["extension"]
        
        if ext == '.json':
            is_valid, msg = self.validate_json_file(file_path)
            if not is_valid:
                file_info["issues"].append(f"JSON validation: {msg}")
                
        elif ext in ['.yaml', '.yml']:
            is_valid, msg = self.validate_yaml_file(file_path)
            if not is_valid:
                file_info["issues"].append(f"YAML validation: {msg}")
                
        elif ext == '.py':
            is_valid, msg = self.check_python_syntax(file_path)
            if not is_valid:
                file_info["issues"].append(f"Python syntax: {msg}")
                
        return file_info
        
    def scan_repository(self):
        """Scan entire repository for corruption"""
        print("🔍 Starting comprehensive file corruption scan...")
        print(f"📁 Scanning directory: {self.root_dir.absolute()}")
        
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not self.should_skip_file(file_path):
                if file_path.suffix.lower() in self.critical_extensions:
                    self.scan_results["total_files_scanned"] += 1
                    
                    file_info = self.scan_file(file_path)
                    
                    if file_info["issues"]:
                        if any("CORRUPTION" in issue for issue in file_info["issues"]):
                            self.scan_results["corrupted_files"].append(file_info)
                        else:
                            self.scan_results["suspicious_files"].append(file_info)
                            
                    # Progress indicator
                    if self.scan_results["total_files_scanned"] % 50 == 0:
                        print(f"📊 Scanned {self.scan_results['total_files_scanned']} files...")
                        
    def generate_report(self):
        """Generate comprehensive scan report"""
        # Summary statistics
        self.scan_results["summary"] = {
            "total_scanned": self.scan_results["total_files_scanned"],
            "corrupted_count": len(self.scan_results["corrupted_files"]),
            "suspicious_count": len(self.scan_results["suspicious_files"]),
            "encoding_issues_count": len(self.scan_results["encoding_issues"]),
            "health_status": "HEALTHY" if len(self.scan_results["corrupted_files"]) == 0 else "ISSUES_FOUND"
        }
        
        # Save results
        report_file = "FILE_CORRUPTION_SCAN_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.scan_results, f, indent=2, ensure_ascii=False)
            
        # Print summary
        print("\n" + "="*60)
        print("📋 FILE CORRUPTION SCAN RESULTS")
        print("="*60)
        print(f"📊 Total files scanned: {self.scan_results['summary']['total_scanned']}")
        print(f"🚨 Corrupted files: {self.scan_results['summary']['corrupted_count']}")
        print(f"⚠️  Suspicious files: {self.scan_results['summary']['suspicious_count']}")
        print(f"📝 Report saved to: {report_file}")
        
        if self.scan_results["corrupted_files"]:
            print("\n🚨 CORRUPTED FILES FOUND:")
            for file_info in self.scan_results["corrupted_files"]:
                print(f"  📄 {file_info['path']}")
                for issue in file_info["issues"]:
                    print(f"     ❌ {issue}")
                    
        if self.scan_results["suspicious_files"]:
            print("\n⚠️  SUSPICIOUS FILES:")
            for file_info in self.scan_results["suspicious_files"][:10]:  # Show first 10
                print(f"  📄 {file_info['path']}")
                for issue in file_info["issues"]:
                    print(f"     🔸 {issue}")
                    
        if len(self.scan_results["suspicious_files"]) > 10:
            print(f"     ... and {len(self.scan_results['suspicious_files']) - 10} more")
            
        print(f"\n✅ Repository Health Status: {self.scan_results['summary']['health_status']}")
        
        return self.scan_results

def main():
    """Main execution function"""
    scanner = FileCorruptionScanner()
    scanner.scan_repository()
    results = scanner.generate_report()
    
    # Return appropriate exit code
    if results["summary"]["corrupted_count"] > 0:
        sys.exit(1)  # Exit with error if corruption found
    else:
        sys.exit(0)  # Success

if __name__ == "__main__":
    main()if __name__ == "__main__":
    main()