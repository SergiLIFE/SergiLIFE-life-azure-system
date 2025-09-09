#!/usr/bin/env python3
"""
Azure Marketplace Documentation Compliance Checker
Validates all required documents for marketplace submission
"""

import os
import json
from pathlib import Path
from datetime import datetime

class MarketplaceDocumentationChecker:
    def __init__(self):
        self.base_path = Path('.')
        self.required_docs = {
            # Critical marketplace documents
            'README.md': {'required': True, 'description': 'Main product documentation', 'min_size': 1000},
            'LICENSE': {'required': True, 'description': 'Software license', 'min_size': 100},
            'azure.yaml': {'required': True, 'description': 'Azure deployment config', 'min_size': 200},
            'requirements.txt': {'required': True, 'description': 'Python dependencies', 'min_size': 50},
            
            # Infrastructure documents
            'infra/main.bicep': {'required': True, 'description': 'Infrastructure as Code', 'min_size': 500},
            'infra/main.parameters.json': {'required': True, 'description': 'Deployment parameters', 'min_size': 100},
            
            # CI/CD and automation
            '.github/workflows/azure-deploy.yml': {'required': False, 'description': 'CI/CD pipeline', 'min_size': 200},
            
            # Documentation
            'docs/installation.md': {'required': False, 'description': 'Installation guide', 'min_size': 500},
            'docs/user-guide.md': {'required': False, 'description': 'User documentation', 'min_size': 1000},
            'docs/api-reference.md': {'required': False, 'description': 'API documentation', 'min_size': 500},
            'CHANGELOG.md': {'required': False, 'description': 'Version history', 'min_size': 200},
            'SECURITY.md': {'required': False, 'description': 'Security policy', 'min_size': 300},
            'CONTRIBUTING.md': {'required': False, 'description': 'Contribution guidelines', 'min_size': 200},
        }
        
        self.marketplace_content_requirements = {
            'README.md': [
                'Azure Marketplace',
                'Installation',
                'Features',
                'Pricing',
                'Support',
                'License',
                'Getting Started',
                'Prerequisites'
            ]
        }
        
        self.offer_id = "9a600d96-fe1e-420b-902a-a0c42c561adb"
        
    def check_file_exists(self, file_path: str) -> dict:
        """Check if a file exists and get its details"""
        path = self.base_path / file_path
        
        if not path.exists():
            return {'exists': False, 'size': 0, 'type': 'missing'}
        
        if path.is_file():
            size = path.stat().st_size
            return {'exists': True, 'size': size, 'type': 'file', 'path': str(path)}
        elif path.is_dir():
            files = list(path.glob('*'))
            return {'exists': True, 'size': len(files), 'type': 'directory', 'files': len(files)}
        
        return {'exists': False, 'size': 0, 'type': 'unknown'}
    
    def check_content_requirements(self, file_path: str, requirements: list) -> dict:
        """Check if file contains required content markers"""
        path = self.base_path / file_path
        if not path.exists() or not path.is_file():
            return {'checked': False, 'found': [], 'missing': requirements}
        
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            found = []
            missing = []
            
            for req in requirements:
                if req.lower() in content.lower():
                    found.append(req)
                else:
                    missing.append(req)
            
            return {'checked': True, 'found': found, 'missing': missing, 'content_length': len(content)}
        except Exception as e:
            return {'checked': False, 'error': str(e), 'found': [], 'missing': requirements}
    
    def run_comprehensive_check(self) -> dict:
        """Run complete marketplace documentation validation"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'offer_id': self.offer_id,
            'files': {},
            'summary': {
                'total_files': len(self.required_docs),
                'required_files': len([k for k, v in self.required_docs.items() if v['required']]),
                'optional_files': len([k for k, v in self.required_docs.items() if not v['required']]),
                'found_files': 0,
                'missing_required': 0,
                'missing_optional': 0,
                'content_compliance': {}
            }
        }
        
        # Check each file
        for file_path, requirements in self.required_docs.items():
            file_info = self.check_file_exists(file_path)
            file_info.update(requirements)
            
            # Check content requirements if applicable
            if file_path in self.marketplace_content_requirements:
                content_check = self.check_content_requirements(
                    file_path, 
                    self.marketplace_content_requirements[file_path]
                )
                file_info['content_check'] = content_check
                results['summary']['content_compliance'][file_path] = content_check
            
            results['files'][file_path] = file_info
            
            # Update summary
            if file_info['exists']:
                results['summary']['found_files'] += 1
            else:
                if requirements['required']:
                    results['summary']['missing_required'] += 1
                else:
                    results['summary']['missing_optional'] += 1
        
        # Calculate readiness score
        required_found = results['summary']['required_files'] - results['summary']['missing_required']
        optional_found = results['summary']['found_files'] - required_found
        
        # Weighted scoring: required files 80%, optional files 20%
        required_score = (required_found / results['summary']['required_files']) * 80
        optional_score = (optional_found / results['summary']['optional_files']) * 20 if results['summary']['optional_files'] > 0 else 0
        
        results['summary']['readiness_score'] = required_score + optional_score
        results['summary']['marketplace_ready'] = results['summary']['readiness_score'] >= 75
        
        return results
    
    def print_detailed_report(self, results: dict):
        """Print a detailed validation report"""
        print("🎯 AZURE MARKETPLACE DOCUMENTATION VALIDATION")
        print("=" * 70)
        print(f"📅 Validation Date: {results['timestamp'][:19]}")
        print(f"🆔 Offer ID: {results['offer_id']}")
        print(f"📊 Readiness Score: {results['summary']['readiness_score']:.1f}%")
        
        if results['summary']['marketplace_ready']:
            print("✅ MARKETPLACE READY")
        else:
            print("⚠️ MARKETPLACE NOT READY - Action Required")
        
        print("\n" + "=" * 70)
        print("📋 DOCUMENT VALIDATION RESULTS")
        print("-" * 70)
        
        # Group by required/optional
        required_files = {k: v for k, v in results['files'].items() if v['required']}
        optional_files = {k: v for k, v in results['files'].items() if not v['required']}
        
        print("\n🔴 REQUIRED DOCUMENTS:")
        for file_path, info in required_files.items():
            status = self._get_file_status(info)
            print(f"  {status} {file_path:<35} {info['description']}")
            if 'content_check' in info:
                self._print_content_status(info['content_check'])
        
        print("\n🟡 OPTIONAL DOCUMENTS:")
        for file_path, info in optional_files.items():
            status = self._get_file_status(info)
            print(f"  {status} {file_path:<35} {info['description']}")
        
        print("\n" + "=" * 70)
        print("📊 SUMMARY STATISTICS")
        print("-" * 70)
        summary = results['summary']
        print(f"📁 Total Files Checked: {summary['total_files']}")
        print(f"✅ Files Found: {summary['found_files']}")
        print(f"🔴 Required Missing: {summary['missing_required']}")
        print(f"🟡 Optional Missing: {summary['missing_optional']}")
        
        if summary['missing_required'] > 0:
            print("\n❌ CRITICAL ACTIONS REQUIRED:")
            for file_path, info in results['files'].items():
                if info['required'] and not info['exists']:
                    print(f"  - Create: {file_path} ({info['description']})")
        
        if summary['readiness_score'] < 75:
            print("\n⚠️ RECOMMENDATIONS:")
            print("  - Complete all required documents")
            print("  - Enhance README.md with marketplace content")
            print("  - Add missing infrastructure files")
            print("  - Include proper licensing")
        
        print(f"\n🚀 NEXT STEPS:")
        if results['summary']['marketplace_ready']:
            print("  ✅ Documentation is marketplace ready!")
            print("  📋 Review content quality and completeness")
            print("  🎯 Proceed with Azure Marketplace submission")
        else:
            print("  📝 Complete missing required documents")
            print("  🔍 Review and enhance existing content")
            print("  ✅ Re-run validation after updates")
    
    def _get_file_status(self, info: dict) -> str:
        """Get status emoji for file"""
        if not info['exists']:
            return "❌"
        elif info['type'] == 'file':
            if info['size'] >= info['min_size']:
                return "✅"
            else:
                return "⚠️"
        elif info['type'] == 'directory':
            if info['size'] > 0:
                return "📁"
            else:
                return "📂"
        return "❓"
    
    def _print_content_status(self, content_check: dict):
        """Print content validation status"""
        if not content_check['checked']:
            return
        
        if content_check['found']:
            print(f"     ✅ Content found: {', '.join(content_check['found'])}")
        if content_check['missing']:
            print(f"     ⚠️ Missing content: {', '.join(content_check['missing'])}")

def main():
    """Main execution function"""
    checker = MarketplaceDocumentationChecker()
    results = checker.run_comprehensive_check()
    checker.print_detailed_report(results)
    
    # Save results to file
    with open('marketplace_validation_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed report saved to: marketplace_validation_report.json")

if __name__ == "__main__":
    main()
