#!/usr/bin/env python3
"""
L.I.F.E. Platform Repository Health Scanner
Identifies and resolves corruption issues while preserving critical data
"""
import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Set
import re
import hashlib
import shutil
from datetime import datetime

class RepositoryHealthScanner:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.scan_results = {
            'corruption_issues': [],
            'security_violations': [],
            'duplicate_files': [],
            'empty_files': [],
            'invalid_files': [],
            'recommendations': []
        }
        
    def scan_repository(self) -> Dict:
        """Comprehensive repository health scan"""
        print("🔍 L.I.F.E. Platform Repository Health Scanner")
        print("=" * 60)
        
        # 1. Check for security violations (.env files, secrets)
        self._check_security_violations()
        
        # 2. Find duplicate files
        self._find_duplicate_files()
        
        # 3. Identify empty or corrupted files
        self._check_file_integrity()
        
        # 4. Check for invalid file patterns
        self._check_invalid_patterns()
        
        # 5. Generate recommendations
        self._generate_recommendations()
        
        return self.scan_results
    
    def _check_security_violations(self):
        """Check for security violations like .env files"""
        print("🔐 Checking for security violations...")
        
        security_patterns = [
            '*.env*',
            '*secret*',
            '*password*', 
            '*key.txt',
            '*credentials*'
        ]
        
        for pattern in security_patterns:
            for file_path in self.repo_path.rglob(pattern):
                if file_path.is_file():
                    self.scan_results['security_violations'].append({
                        'file': str(file_path),
                        'type': 'sensitive_file',
                        'pattern': pattern,
                        'size': file_path.stat().st_size
                    })
                    
        print(f"   Found {len(self.scan_results['security_violations'])} security violations")
    
    def _find_duplicate_files(self):
        """Find duplicate files by content hash"""
        print("📄 Checking for duplicate files...")
        
        file_hashes = {}
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and file_path.stat().st_size > 0:
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in file_hashes:
                        self.scan_results['duplicate_files'].append({
                            'original': file_hashes[file_hash],
                            'duplicate': str(file_path),
                            'hash': file_hash,
                            'size': file_path.stat().st_size
                        })
                    else:
                        file_hashes[file_hash] = str(file_path)
                        
                except (PermissionError, OSError):
                    pass
                    
        print(f"   Found {len(self.scan_results['duplicate_files'])} duplicate files")
    
    def _check_file_integrity(self):
        """Check for empty or potentially corrupted files"""
        print("🔧 Checking file integrity...")
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    
                    # Check for empty files (except known empty files)
                    if size == 0 and not self._is_allowed_empty_file(file_path):
                        self.scan_results['empty_files'].append({
                            'file': str(file_path),
                            'type': 'empty_file'
                        })
                    
                    # Check for files with invalid content
                    if file_path.suffix in ['.py', '.js', '.json', '.md', '.txt']:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if self._has_corruption_markers(content):
                                    self.scan_results['corruption_issues'].append({
                                        'file': str(file_path),
                                        'type': 'corruption_markers',
                                        'size': size
                                    })
                        except (UnicodeDecodeError, PermissionError):
                            pass
                            
                except (PermissionError, OSError):
                    self.scan_results['invalid_files'].append({
                        'file': str(file_path),
                        'type': 'access_error'
                    })
                    
        print(f"   Found {len(self.scan_results['empty_files'])} empty files")
        print(f"   Found {len(self.scan_results['corruption_issues'])} corruption issues")
    
    def _check_invalid_patterns(self):
        """Check for files with invalid naming patterns"""
        print("📝 Checking file naming patterns...")
        
        invalid_patterns = [
            r'.*\s+origin\s+.*',  # Git conflict markers
            r'.*<<<<<<.*',        # Merge conflict markers
            r'.*======.*',        # Merge conflict markers  
            r'.*>>>>>>.*',        # Merge conflict markers
            r'.*~.*',             # Backup files
            r'.*\.tmp$',          # Temporary files
        ]
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file():
                file_name = file_path.name
                for pattern in invalid_patterns:
                    if re.match(pattern, file_name):
                        self.scan_results['invalid_files'].append({
                            'file': str(file_path),
                            'type': 'invalid_pattern',
                            'pattern': pattern
                        })
                        break
    
    def _is_allowed_empty_file(self, file_path: Path) -> bool:
        """Check if empty file is allowed"""
        allowed_empty = [
            '__init__.py',
            '.gitkeep',
            '.gitignore',
            'requirements.txt'
        ]
        return file_path.name in allowed_empty
    
    def _has_corruption_markers(self, content: str) -> bool:
        """Check for corruption markers in file content"""
        corruption_markers = [
            '<<<<<<< HEAD',
            '======',
            '>>>>>>> ',
            'CONFLICT (',
            '|||||||| ',
            'h origin clean-historymain --force'  # Specific corruption seen in your repo
        ]
        
        for marker in corruption_markers:
            if marker in content:
                return True
        return False
    
    def _generate_recommendations(self):
        """Generate cleanup recommendations"""
        print("💡 Generating recommendations...")
        
        # Security recommendations
        if self.scan_results['security_violations']:
            self.scan_results['recommendations'].append({
                'priority': 'HIGH',
                'action': 'REMOVE_SECURITY_FILES',
                'description': 'Remove .env and credential files (use Azure Key Vault)',
                'files': len(self.scan_results['security_violations'])
            })
        
        # Duplicate file recommendations
        if self.scan_results['duplicate_files']:
            self.scan_results['recommendations'].append({
                'priority': 'MEDIUM',
                'action': 'REMOVE_DUPLICATES',
                'description': 'Remove duplicate files to reduce repository size',
                'files': len(self.scan_results['duplicate_files'])
            })
        
        # Corruption recommendations
        if self.scan_results['corruption_issues']:
            self.scan_results['recommendations'].append({
                'priority': 'HIGH',
                'action': 'FIX_CORRUPTION',
                'description': 'Fix files with corruption markers',
                'files': len(self.scan_results['corruption_issues'])
            })
        
        # Empty file recommendations
        if self.scan_results['empty_files']:
            self.scan_results['recommendations'].append({
                'priority': 'LOW',
                'action': 'REMOVE_EMPTY_FILES',
                'description': 'Remove unnecessary empty files',
                'files': len(self.scan_results['empty_files'])
            })

    def create_backup(self) -> str:
        """Create backup before cleanup"""
        backup_dir = self.repo_path / f"BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"💾 Creating backup: {backup_dir}")
        
        # Backup critical files
        critical_files = [
            'experimentP2L*.py',
            'azure_config.py',
            'venturi_gates_system.py',
            'campaign_manager.py',
            'requirements.txt',
            'README.md',
            '.github/workflows/*'
        ]
        
        backup_dir.mkdir(exist_ok=True)
        
        for pattern in critical_files:
            for file_path in self.repo_path.glob(pattern):
                if file_path.is_file():
                    backup_file = backup_dir / file_path.name
                    shutil.copy2(file_path, backup_file)
        
        return str(backup_dir)
    
    def execute_cleanup(self, backup: bool = True) -> Dict:
        """Execute safe cleanup based on scan results"""
        cleanup_results = {
            'backup_location': None,
            'actions_taken': [],
            'files_removed': 0,
            'errors': []
        }
        
        if backup:
            cleanup_results['backup_location'] = self.create_backup()
        
        print("🧹 Executing cleanup...")
        
        # 1. Remove security violations (HIGH PRIORITY)
        for violation in self.scan_results['security_violations']:
            try:
                file_path = Path(violation['file'])
                if file_path.exists():
                    file_path.unlink()
                    cleanup_results['actions_taken'].append(f"REMOVED: {violation['file']}")
                    cleanup_results['files_removed'] += 1
            except Exception as e:
                cleanup_results['errors'].append(f"Error removing {violation['file']}: {e}")
        
        # 2. Remove duplicate files (keep first occurrence)
        for duplicate in self.scan_results['duplicate_files']:
            try:
                file_path = Path(duplicate['duplicate'])
                if file_path.exists():
                    file_path.unlink()
                    cleanup_results['actions_taken'].append(f"REMOVED DUPLICATE: {duplicate['duplicate']}")
                    cleanup_results['files_removed'] += 1
            except Exception as e:
                cleanup_results['errors'].append(f"Error removing duplicate {duplicate['duplicate']}: {e}")
        
        # 3. Remove empty files
        for empty_file in self.scan_results['empty_files']:
            try:
                file_path = Path(empty_file['file'])
                if file_path.exists():
                    file_path.unlink()
                    cleanup_results['actions_taken'].append(f"REMOVED EMPTY: {empty_file['file']}")
                    cleanup_results['files_removed'] += 1
            except Exception as e:
                cleanup_results['errors'].append(f"Error removing empty file {empty_file['file']}: {e}")
        
        return cleanup_results

def main():
    """Main execution function"""
    repo_path = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize scanner
    scanner = RepositoryHealthScanner(repo_path)
    
    # Run scan
    results = scanner.scan_repository()
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 SCAN RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"🔐 Security Violations: {len(results['security_violations'])}")
    print(f"📄 Duplicate Files: {len(results['duplicate_files'])}")
    print(f"🔧 Corruption Issues: {len(results['corruption_issues'])}")
    print(f"📝 Empty Files: {len(results['empty_files'])}")
    print(f"⚠️  Invalid Files: {len(results['invalid_files'])}")
    
    print("\n💡 RECOMMENDATIONS:")
    for rec in results['recommendations']:
        print(f"   {rec['priority']}: {rec['description']} ({rec['files']} files)")
    
    # Ask for cleanup confirmation
    print("\n" + "=" * 60)
    response = input("🧹 Execute automatic cleanup? (y/N): ").lower().strip()
    
    if response == 'y':
        cleanup_results = scanner.execute_cleanup(backup=True)
        
        print(f"\n✅ CLEANUP COMPLETE")
        print(f"   Files removed: {cleanup_results['files_removed']}")
        print(f"   Backup location: {cleanup_results['backup_location']}")
        
        if cleanup_results['errors']:
            print(f"   Errors: {len(cleanup_results['errors'])}")
            for error in cleanup_results['errors']:
                print(f"     - {error}")
    
    # Save detailed results
    results_file = os.path.join(repo_path, 'logs', 'repository_health_scan.json')
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()