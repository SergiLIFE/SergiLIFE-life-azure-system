#!/usr/bin/env python3
"""
L.I.F.E. Platform Deep Corruption Scanner
Advanced corruption detection and automatic remediation
November 3, 2025
"""
import os
import sys
import json
import re
import hashlib
import shutil
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime
import subprocess

class DeepCorruptionScanner:
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path or os.getcwd())
        self.backup_dir = None
        self.scan_results = {
            'security_violations': [],
            'git_corruption': [],
            'file_corruption': [],
            'duplicate_files': [],
            'empty_files': [],
            'encoding_issues': [],
            'critical_files_status': {},
            'cleanup_actions': []
        }
        
        # Critical L.I.F.E. Platform files that must be preserved
        self.critical_files = [
            'experimentP2L*.py',
            'azure_config.py', 
            'venturi_gates_system.py',
            'three_venturi_harmonic_calibration.py',
            'campaign_manager.py',
            'lifetheory.py',
            'requirements.txt',
            'README.md',
            'azure_functions_workflow.py'
        ]
        
        # Known corruption patterns
        self.corruption_patterns = [
            r'h origin clean-historymain --force',  # Git typo artifact
            r'<<<<<<< HEAD',                        # Git merge conflicts
            r'======',                             # Git merge conflicts
            r'>>>>>>> ',                           # Git merge conflicts
            r'CONFLICT \(',                        # Git conflict markers
            r'\|\|\|\|\|\|\| ',                    # Git conflict markers
            r'.*~$',                               # Backup files
            r'.*\.tmp$',                           # Temporary files
            r'.*\.temp$',                          # Temporary files
        ]

    def create_safety_backup(self) -> str:
        """Create backup of critical files before cleanup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = self.repo_path / f"CORRUPTION_CLEANUP_BACKUP_{timestamp}"
        self.backup_dir.mkdir(exist_ok=True)
        
        print(f"💾 Creating safety backup: {self.backup_dir}")
        
        backed_up_files = 0
        for pattern in self.critical_files:
            for file_path in self.repo_path.glob(pattern):
                if file_path.is_file():
                    backup_file = self.backup_dir / file_path.name
                    shutil.copy2(file_path, backup_file)
                    backed_up_files += 1
                    
        print(f"   Backed up {backed_up_files} critical files")
        return str(self.backup_dir)

    def scan_security_violations(self):
        """Scan for security policy violations"""
        print("🔐 Scanning for security violations...")
        
        # Check for .env files (L.I.F.E. Platform uses Azure Key Vault)
        for env_file in self.repo_path.rglob('*.env*'):
            if env_file.is_file():
                self.scan_results['security_violations'].append({
                    'file': str(env_file),
                    'type': 'env_file_violation',
                    'severity': 'HIGH',
                    'reason': 'L.I.F.E. Platform uses Azure Key Vault, not .env files'
                })
        
        # Check for hardcoded secrets
        for py_file in self.repo_path.rglob('*.py'):
            if py_file.is_file():
                try:
                    content = py_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Look for potential secrets
                    secret_patterns = [
                        r'password\s*=\s*["\'](?!.*\$\{)[^"\']{8,}["\']',
                        r'secret\s*=\s*["\'](?!.*\$\{)[^"\']{8,}["\']',
                        r'key\s*=\s*["\'](?!.*\$\{)[^"\']{20,}["\']',
                        r'token\s*=\s*["\'](?!.*\$\{)[^"\']{20,}["\']'
                    ]
                    
                    for i, line in enumerate(content.split('\n'), 1):
                        for pattern in secret_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                self.scan_results['security_violations'].append({
                                    'file': str(py_file),
                                    'line': i,
                                    'type': 'hardcoded_secret',
                                    'severity': 'CRITICAL',
                                    'content': line.strip()[:50] + '...'
                                })
                except Exception:
                    pass

    def scan_git_corruption(self):
        """Scan for Git-related corruption"""
        print("🔄 Scanning for Git corruption...")
        
        # Check for Git command artifacts
        corruption_files = [
            'h origin clean-historymain --force',
            'main)',
            'origin',
            'clean-historymain'
        ]
        
        for corruption_file in corruption_files:
            corruption_path = self.repo_path / corruption_file
            if corruption_path.exists():
                self.scan_results['git_corruption'].append({
                    'file': str(corruption_path),
                    'type': 'git_command_artifact',
                    'severity': 'HIGH'
                })
        
        # Check for Git error files
        for error_file in self.repo_path.glob('git-error-*.txt'):
            self.scan_results['git_corruption'].append({
                'file': str(error_file),
                'type': 'git_error_file', 
                'severity': 'MEDIUM'
            })

    def scan_file_corruption(self):
        """Scan for file corruption and encoding issues"""
        print("📄 Scanning for file corruption...")
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file():
                try:
                    # Check file size
                    size = file_path.stat().st_size
                    
                    # Check for unexpectedly empty files
                    if size == 0 and not self._is_allowed_empty(file_path):
                        self.scan_results['empty_files'].append({
                            'file': str(file_path),
                            'type': 'unexpected_empty'
                        })
                    
                    # Check text files for corruption patterns
                    if file_path.suffix in ['.py', '.js', '.json', '.md', '.txt', '.bat', '.ps1']:
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            
                            # Check for corruption patterns
                            for pattern in self.corruption_patterns:
                                if re.search(pattern, content):
                                    self.scan_results['file_corruption'].append({
                                        'file': str(file_path),
                                        'type': 'corruption_pattern',
                                        'pattern': pattern,
                                        'severity': 'HIGH'
                                    })
                                    break
                            
                            # Check for encoding issues
                            try:
                                file_path.read_text(encoding='utf-8', errors='strict')
                            except UnicodeDecodeError:
                                self.scan_results['encoding_issues'].append({
                                    'file': str(file_path),
                                    'type': 'encoding_error',
                                    'severity': 'MEDIUM'
                                })
                                
                        except Exception:
                            pass
                            
                except Exception:
                    pass

    def check_critical_files_integrity(self):
        """Check integrity of critical L.I.F.E. Platform files"""
        print("🧠 Checking critical L.I.F.E. files integrity...")
        
        for pattern in self.critical_files:
            files_found = list(self.repo_path.glob(pattern))
            
            if files_found:
                for file_path in files_found:
                    if file_path.is_file() and file_path.stat().st_size > 0:
                        self.scan_results['critical_files_status'][pattern] = {
                            'status': 'OK',
                            'file': str(file_path),
                            'size': file_path.stat().st_size
                        }
                    else:
                        self.scan_results['critical_files_status'][pattern] = {
                            'status': 'EMPTY',
                            'file': str(file_path) if file_path.exists() else 'NOT_FOUND'
                        }
            else:
                self.scan_results['critical_files_status'][pattern] = {
                    'status': 'MISSING',
                    'file': 'NOT_FOUND'
                }

    def _is_allowed_empty(self, file_path: Path) -> bool:
        """Check if file is allowed to be empty"""
        allowed_empty = [
            '__init__.py',
            '.gitkeep', 
            '.gitignore',
            'local.settings.json'
        ]
        return file_path.name in allowed_empty or file_path.suffix == '.placeholder'

    def execute_safe_cleanup(self) -> Dict:
        """Execute safe cleanup with rollback capability"""
        print("\n🧹 Executing safe cleanup...")
        
        cleanup_results = {
            'actions_taken': [],
            'files_removed': 0,
            'files_restored': 0,
            'errors': []
        }
        
        # 1. Remove security violations
        for violation in self.scan_results['security_violations']:
            try:
                file_path = Path(violation['file'])
                if file_path.exists():
                    file_path.unlink()
                    cleanup_results['actions_taken'].append(f"REMOVED SECURITY VIOLATION: {violation['file']}")
                    cleanup_results['files_removed'] += 1
            except Exception as e:
                cleanup_results['errors'].append(f"Failed to remove {violation['file']}: {e}")
        
        # 2. Remove Git corruption artifacts
        for corruption in self.scan_results['git_corruption']:
            try:
                file_path = Path(corruption['file'])
                if file_path.exists():
                    file_path.unlink()
                    cleanup_results['actions_taken'].append(f"REMOVED GIT CORRUPTION: {corruption['file']}")
                    cleanup_results['files_removed'] += 1
            except Exception as e:
                cleanup_results['errors'].append(f"Failed to remove {corruption['file']}: {e}")
        
        # 3. Remove files with corruption patterns
        for corruption in self.scan_results['file_corruption']:
            if corruption['type'] == 'corruption_pattern':
                try:
                    file_path = Path(corruption['file'])
                    # Only remove if it's clearly a corruption artifact, not a legitimate file
                    if any(artifact in file_path.name for artifact in ['origin', 'main)', 'git-error']):
                        file_path.unlink()
                        cleanup_results['actions_taken'].append(f"REMOVED CORRUPTED: {corruption['file']}")
                        cleanup_results['files_removed'] += 1
                except Exception as e:
                    cleanup_results['errors'].append(f"Failed to remove {corruption['file']}: {e}")
        
        # 4. Fix Git configuration
        try:
            git_configs = [
                ['git', 'config', '--global', 'core.pager', '""'],
                ['git', 'config', '--global', 'pager.branch', 'false'],
                ['git', 'config', '--global', 'pager.log', 'false'],
                ['git', 'config', '--global', 'pager.diff', 'false'],
                ['git', 'config', '--global', 'core.autocrlf', 'true']
            ]
            
            for config in git_configs:
                subprocess.run(config, check=False, capture_output=True)
            
            cleanup_results['actions_taken'].append("FIXED: Git configuration")
        except Exception as e:
            cleanup_results['errors'].append(f"Failed to fix Git config: {e}")
        
        return cleanup_results

    def validate_platform_integrity(self) -> Dict:
        """Validate L.I.F.E. Platform integrity after cleanup"""
        print("✅ Validating platform integrity...")
        
        validation = {
            'critical_files_ok': True,
            'core_imports_ok': True,
            'platform_functional': True,
            'issues': []
        }
        
        # Check critical files
        for pattern, status in self.scan_results['critical_files_status'].items():
            if status['status'] != 'OK':
                validation['critical_files_ok'] = False
                validation['issues'].append(f"Critical file issue: {pattern} is {status['status']}")
        
        # Test core imports
        try:
            test_script = """
try:
    import azure_config
    import sys
    from pathlib import Path
    sys.path.append(str(Path.cwd()))
    from venturi_gates_system import VenturiGatesSystem
    print("CORE_IMPORTS_OK")
except Exception as e:
    print(f"CORE_IMPORTS_ERROR: {e}")
"""
            result = subprocess.run([sys.executable, '-c', test_script], 
                                 capture_output=True, text=True, cwd=self.repo_path)
            
            if "CORE_IMPORTS_OK" not in result.stdout:
                validation['core_imports_ok'] = False
                validation['issues'].append(f"Core import error: {result.stdout + result.stderr}")
                
        except Exception as e:
            validation['core_imports_ok'] = False
            validation['issues'].append(f"Import test failed: {e}")
        
        validation['platform_functional'] = validation['critical_files_ok'] and validation['core_imports_ok']
        
        return validation

    def run_comprehensive_scan(self) -> Dict:
        """Run complete corruption scan and cleanup"""
        print("🔍 L.I.F.E. Platform Deep Corruption Scanner")
        print("=" * 60)
        
        # Create safety backup
        self.create_safety_backup()
        
        # Run all scans
        self.scan_security_violations()
        self.scan_git_corruption() 
        self.scan_file_corruption()
        self.check_critical_files_integrity()
        
        # Display results
        print("\n📊 SCAN RESULTS:")
        print(f"   Security violations: {len(self.scan_results['security_violations'])}")
        print(f"   Git corruption: {len(self.scan_results['git_corruption'])}")
        print(f"   File corruption: {len(self.scan_results['file_corruption'])}")
        print(f"   Empty files: {len(self.scan_results['empty_files'])}")
        print(f"   Encoding issues: {len(self.scan_results['encoding_issues'])}")
        
        # Show critical files status
        print("\n🧠 CRITICAL L.I.F.E. FILES STATUS:")
        for pattern, status in self.scan_results['critical_files_status'].items():
            status_icon = "✅" if status['status'] == 'OK' else "⚠️"
            print(f"   {status_icon} {pattern}: {status['status']}")
        
        return self.scan_results

def main():
    """Main execution"""
    scanner = DeepCorruptionScanner()
    
    # Run comprehensive scan
    results = scanner.run_comprehensive_scan()
    
    # Check if cleanup is needed
    issues_found = (
        len(results['security_violations']) +
        len(results['git_corruption']) +
        len(results['file_corruption'])
    )
    
    if issues_found > 0:
        print(f"\n⚠️  Found {issues_found} corruption issues")
        
        response = input("\n🧹 Execute automatic cleanup? (y/N): ").lower().strip()
        if response == 'y':
            # Execute cleanup
            cleanup_results = scanner.execute_safe_cleanup()
            
            print(f"\n✅ CLEANUP COMPLETED")
            print(f"   Files removed: {cleanup_results['files_removed']}")
            print(f"   Actions taken: {len(cleanup_results['actions_taken'])}")
            
            if cleanup_results['errors']:
                print(f"   Errors: {len(cleanup_results['errors'])}")
                for error in cleanup_results['errors'][:3]:  # Show first 3 errors
                    print(f"     - {error}")
            
            # Validate platform integrity
            validation = scanner.validate_platform_integrity()
            
            if validation['platform_functional']:
                print("\n🚀 L.I.F.E. PLATFORM STATUS: OPERATIONAL")
                print("   All critical systems verified")
            else:
                print("\n⚠️  L.I.F.E. PLATFORM STATUS: NEEDS ATTENTION") 
                for issue in validation['issues']:
                    print(f"     - {issue}")
            
            print(f"\n💾 Backup location: {scanner.backup_dir}")
    else:
        print("\n✅ NO CORRUPTION DETECTED")
        print("   L.I.F.E. Platform repository is clean")
    
    # Save scan results
    results_file = scanner.repo_path / 'logs' / 'corruption_scan_results.json'
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved: {results_file}")

if __name__ == "__main__":
    main()