#!/usr/bin/env python3
"""
L.I.F.E Platform Repository Restructuring System
===============================================

GitHub Advisory: Repository Too Large (1,257+ files)
Goal: Split into manageable chunks while maintaining functionality

This system will:
1. Analyze current repository structure
2. Categorize files by purpose and importance
3. Create separate repositories for different components
4. Maintain core functionality in main repo
5. Set up proper cross-repository references

Copyright 2025 - Sergio Paya Borrull
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class RepositoryRestructurer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.analysis_report = {
            "total_files": 0,
            "categories": {},
            "recommended_structure": {},
            "migration_plan": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Define the new repository structure
        self.new_repos = {
            "life-platform-core": {
                "description": "Core L.I.F.E Platform - Essential algorithm and platform",
                "max_files": 50,
                "priority": "CRITICAL",
                "files": []
            },
            "life-azure-infrastructure": {
                "description": "Azure deployment and infrastructure components", 
                "max_files": 100,
                "priority": "HIGH",
                "files": []
            },
            "life-documentation": {
                "description": "Documentation, guides, and reference materials",
                "max_files": 150,
                "priority": "MEDIUM", 
                "files": []
            },
            "life-demos-examples": {
                "description": "Demo applications and example implementations",
                "max_files": 100,
                "priority": "MEDIUM",
                "files": []
            },
            "life-campaigns-marketing": {
                "description": "Marketing campaigns and outreach automation",
                "max_files": 200,
                "priority": "LOW",
                "files": []
            },
            "life-archived-development": {
                "description": "Historical development files and legacy components",
                "max_files": 500,
                "priority": "ARCHIVE",
                "files": []
            }
        }
        
    def analyze_repository(self):
        """Analyze current repository structure and categorize files"""
        print("🔍 Analyzing repository structure...")
        
        # File categorization patterns
        categories = {
            "core_algorithm": ["experimentP2L", "lifetheory.py", "venturi", "quantum"],
            "azure_deployment": ["azure_", "deploy", "function_app", "host.json"],
            "documentation": ["README", ".md", "GUIDE", "INSTRUCTIONS"],
            "demos": ["demo_", "clinical_", "educational_", "interactive_"],
            "campaigns": ["campaign_", "email_", "outreach_", "microsoft_"],
            "configuration": [".json", ".yaml", ".yml", "config", "requirements"],
            "testing": ["test_", "validation_", "benchmark_"],
            "automation": ["automation_", "autonomous_", "monitor"],
            "legacy": ["backup", "old", "deprecated", "archive"],
            "temporary": ["temp_", "tmp_", "quick_", "emergency_"]
        }
        
        all_files = list(self.base_path.rglob("*"))
        self.analysis_report["total_files"] = len([f for f in all_files if f.is_file()])
        
        print(f"📊 Found {self.analysis_report['total_files']} total files")
        
        # Categorize each file
        for file_path in all_files:
            if file_path.is_file():
                relative_path = file_path.relative_to(self.base_path)
                file_str = str(relative_path).lower()
                
                categorized = False
                for category, patterns in categories.items():
                    if any(pattern.lower() in file_str for pattern in patterns):
                        if category not in self.analysis_report["categories"]:
                            self.analysis_report["categories"][category] = []
                        self.analysis_report["categories"][category].append(str(relative_path))
                        categorized = True
                        break
                
                if not categorized:
                    if "uncategorized" not in self.analysis_report["categories"]:
                        self.analysis_report["categories"]["uncategorized"] = []
                    self.analysis_report["categories"]["uncategorized"].append(str(relative_path))
        
        return self.analysis_report
    
    def create_core_repository_structure(self):
        """Identify the essential files for the core repository"""
        print("🎯 Creating core repository structure...")
        
        # Essential files for core repository (must be under 50 files)
        essential_files = [
            # Core Algorithm
            "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "lifetheory.py",
            "venturi_gates_system.py",
            
            # Main Configuration
            "README.md",
            "requirements.txt",
            "azure_config.py",
            
            # Essential Platform Files
            "alternative_deployment.py",
            "life_theory_platform_server.py",
            "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html",
            
            # Critical Azure Components
            "azure_functions_workflow.py",
            "host.json",
            "local.settings.json",
            
            # Essential Documentation
            "QUICK_START.md",
            "DEPLOYMENT_GUIDE.md",
            
            # License and Legal
            "LICENSE",
            ".gitignore"
        ]
        
        # Add to core repo
        for file in essential_files:
            if (self.base_path / file).exists():
                self.new_repos["life-platform-core"]["files"].append(file)
        
        print(f"✅ Core repository: {len(self.new_repos['life-platform-core']['files'])} essential files")
        
    def assign_files_to_repositories(self):
        """Assign remaining files to appropriate repositories"""
        print("📂 Assigning files to repositories...")
        
        # Assignment rules based on file patterns
        assignment_rules = {
            "life-azure-infrastructure": [
                "azure_", "deploy", "function_", "infra/", ".bicep", 
                "cloudshell", "subscription", "marketplace"
            ],
            "life-documentation": [
                "README", ".md", "GUIDE", "INSTRUCTIONS", "MANUAL", 
                "CHECKLIST", "NOTES", "REPORT"
            ],
            "life-demos-examples": [
                "demo_", "clinical_", "educational_", "interactive_", 
                "example_", "tutorial_", "validation_"
            ],
            "life-campaigns-marketing": [
                "campaign_", "email_", "outreach_", "microsoft_", 
                "marketing_", "partnership_", "october_15"
            ]
        }
        
        all_files = [f for f in self.base_path.rglob("*") if f.is_file()]
        
        for file_path in all_files:
            relative_path = str(file_path.relative_to(self.base_path))
            file_lower = relative_path.lower()
            
            # Skip if already in core
            if relative_path in self.new_repos["life-platform-core"]["files"]:
                continue
            
            # Assign based on rules
            assigned = False
            for repo_name, patterns in assignment_rules.items():
                if any(pattern in file_lower for pattern in patterns):
                    self.new_repos[repo_name]["files"].append(relative_path)
                    assigned = True
                    break
            
            # If not assigned, put in archive
            if not assigned:
                self.new_repos["life-archived-development"]["files"].append(relative_path)
        
        # Print summary
        for repo_name, repo_info in self.new_repos.items():
            print(f"📁 {repo_name}: {len(repo_info['files'])} files")
    
    def create_migration_plan(self):
        """Create detailed migration plan"""
        print("📋 Creating migration plan...")
        
        migration_steps = [
            {
                "step": 1,
                "action": "Create life-platform-core repository",
                "description": "Essential L.I.F.E Platform functionality only",
                "files_count": len(self.new_repos["life-platform-core"]["files"]),
                "priority": "IMMEDIATE"
            },
            {
                "step": 2,
                "action": "Create life-azure-infrastructure repository", 
                "description": "All Azure deployment and infrastructure",
                "files_count": len(self.new_repos["life-azure-infrastructure"]["files"]),
                "priority": "HIGH"
            },
            {
                "step": 3,
                "action": "Create life-documentation repository",
                "description": "All documentation and guides", 
                "files_count": len(self.new_repos["life-documentation"]["files"]),
                "priority": "MEDIUM"
            },
            {
                "step": 4,
                "action": "Create life-demos-examples repository",
                "description": "Demo applications and examples",
                "files_count": len(self.new_repos["life-demos-examples"]["files"]),
                "priority": "MEDIUM"
            },
            {
                "step": 5,
                "action": "Create life-campaigns-marketing repository",
                "description": "Marketing and campaign automation",
                "files_count": len(self.new_repos["life-campaigns-marketing"]["files"]),
                "priority": "LOW"
            },
            {
                "step": 6,
                "action": "Create life-archived-development repository",
                "description": "Archive historical and development files",
                "files_count": len(self.new_repos["life-archived-development"]["files"]),
                "priority": "ARCHIVE"
            }
        ]
        
        self.analysis_report["migration_plan"] = migration_steps
        return migration_steps
    
    def generate_new_main_readme(self):
        """Generate a new main README for the core repository"""
        readme_content = """# L.I.F.E Platform - Core System

**Learning Individually from Experience** - Production-Ready Neural Processing Platform

## 🎯 Repository Structure (November 2025 Restructure)

This repository contains only the **essential core components** of the L.I.F.E Platform. The complete system has been restructured into focused repositories for better maintainability.

### 📚 Repository Ecosystem

| Repository | Purpose | Files | Status |
|------------|---------|-------|--------|
| **life-platform-core** | Core algorithm and platform (THIS REPO) | ~50 | 🟢 ACTIVE |
| **life-azure-infrastructure** | Azure deployment & infrastructure | ~100 | 🔄 SETUP |
| **life-documentation** | Documentation & guides | ~150 | 🔄 SETUP |  
| **life-demos-examples** | Demo applications & examples | ~100 | 🔄 SETUP |
| **life-campaigns-marketing** | Marketing & campaigns | ~200 | 🔄 SETUP |
| **life-archived-development** | Historical & legacy files | ~500+ | 📦 ARCHIVE |

## 🚀 Quick Start

```bash
# Clone the core repository
git clone https://github.com/SergiLIFE/life-platform-core.git
cd life-platform-core

# Install dependencies
pip install -r requirements.txt

# Run the platform
python alternative_deployment.py
```

## 🧠 Core Components

- **Algorithm**: `experimentP2L.I.F.E-Learning...py` - Main neural processing algorithm
- **Platform**: `life_theory_platform_server.py` - Core platform server
- **Configuration**: `azure_config.py` - Essential Azure configuration
- **Interface**: `LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html` - Primary clinical interface

## 🔗 Related Repositories

- [Azure Infrastructure](https://github.com/SergiLIFE/life-azure-infrastructure) - Complete deployment setup
- [Documentation](https://github.com/SergiLIFE/life-documentation) - Comprehensive guides  
- [Demo Applications](https://github.com/SergiLIFE/life-demos-examples) - Working examples
- [Marketing Campaigns](https://github.com/SergiLIFE/life-campaigns-marketing) - Automated outreach

## 📊 System Status

- **Core Platform**: ✅ Operational
- **Azure Marketplace**: ✅ Live (Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`)
- **Production Ready**: ✅ September 27, 2025
- **Repository Structure**: 🔄 Restructuring November 2025

## 🎯 Migration Benefits

✅ **Improved Performance**: Faster cloning and navigation  
✅ **Better Organization**: Focused repositories by purpose  
✅ **Easier Maintenance**: Targeted updates and contributions  
✅ **GitHub Compatibility**: No more file truncation warnings  
✅ **Team Collaboration**: Clear ownership and responsibility  

---

**Copyright 2025** - Sergio Paya Borrull | L.I.F.E Platform Production System
"""
        return readme_content
    
    def create_repository_setup_scripts(self):
        """Create scripts to set up the new repository structure"""
        
        # Main setup script
        setup_script = '''#!/bin/bash
# L.I.F.E Platform Repository Restructuring Setup
# Run this script to create the new repository structure

echo "🚀 Setting up L.I.F.E Platform Repository Structure..."

# Create directories for each new repository
mkdir -p ../life-platform-core
mkdir -p ../life-azure-infrastructure  
mkdir -p ../life-documentation
mkdir -p ../life-demos-examples
mkdir -p ../life-campaigns-marketing
mkdir -p ../life-archived-development

echo "✅ Directory structure created"
echo "📋 Next steps:"
echo "1. Run: python REPOSITORY_RESTRUCTURING_PLAN.py"
echo "2. Review the generated migration plan"
echo "3. Execute the migration scripts"
echo "4. Initialize git repositories for each component"

echo "🎯 This will reduce the main repository from 1,257+ files to ~50 core files"
'''
        
        return setup_script
    
    def execute_analysis(self):
        """Execute the complete analysis and generate reports"""
        print("🎯 Starting L.I.F.E Platform Repository Restructuring Analysis...")
        print("=" * 70)
        
        # Run analysis
        self.analyze_repository()
        self.create_core_repository_structure()
        self.assign_files_to_repositories()
        self.create_migration_plan()
        
        # Generate reports
        self.save_analysis_report()
        self.save_file_lists()
        self.generate_setup_instructions()
        
        print("=" * 70)
        print("✅ Analysis complete!")
        print(f"📊 Total files analyzed: {self.analysis_report['total_files']}")
        print("📂 Repository breakdown:")
        
        for repo_name, repo_info in self.new_repos.items():
            file_count = len(repo_info['files'])
            status = "🟢" if file_count <= repo_info['max_files'] else "🔴"
            print(f"   {status} {repo_name}: {file_count} files (max: {repo_info['max_files']})")
        
        print("\n🎯 Recommended Action:")
        print("1. Review the generated reports")
        print("2. Execute the migration plan")  
        print("3. Create focused repositories")
        print("4. Update documentation and references")
        
        return self.analysis_report
    
    def save_analysis_report(self):
        """Save the complete analysis report"""
        report_file = self.base_path / "REPOSITORY_ANALYSIS_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_report, f, indent=2, ensure_ascii=False)
        print(f"📄 Analysis report saved: {report_file}")
    
    def save_file_lists(self):
        """Save detailed file lists for each repository"""
        for repo_name, repo_info in self.new_repos.items():
            list_file = self.base_path / f"{repo_name.upper()}_FILE_LIST.txt"
            with open(list_file, 'w', encoding='utf-8') as f:
                f.write(f"# {repo_name.upper()} - File List\n")
                f.write(f"# {repo_info['description']}\n")
                f.write(f"# Priority: {repo_info['priority']}\n")
                f.write(f"# File Count: {len(repo_info['files'])}\n")
                f.write(f"# Max Files: {repo_info['max_files']}\n\n")
                
                for file_path in sorted(repo_info['files']):
                    f.write(f"{file_path}\n")
            
            print(f"📄 File list saved: {list_file}")
    
    def generate_setup_instructions(self):
        """Generate detailed setup instructions"""
        instructions = """
# L.I.F.E Platform Repository Restructuring Instructions

## Overview
Your repository has grown to 1,257+ files, causing GitHub to truncate listings.
This restructuring plan splits it into 6 focused repositories.

## Quick Start (Recommended)

1. **Create Core Repository First**:
   ```bash
   # Create new core repository with essential files only
   mkdir ../life-platform-core
   # Copy essential files (see LIFE-PLATFORM-CORE_FILE_LIST.txt)
   ```

2. **Test Core Functionality**:
   ```bash
   cd ../life-platform-core
   python alternative_deployment.py
   ```

3. **Create Remaining Repositories**:
   ```bash
   # Follow the migration plan step by step
   # Each repository serves a specific purpose
   ```

## Benefits of Restructuring

✅ **Performance**: Faster GitHub operations  
✅ **Maintainability**: Focused development areas  
✅ **Collaboration**: Clear component ownership  
✅ **Deployment**: Simplified CI/CD pipelines  

## Repository Purposes

- **life-platform-core**: Essential algorithm and platform (~50 files)
- **life-azure-infrastructure**: All Azure deployment components (~100 files)  
- **life-documentation**: Guides, manuals, and documentation (~150 files)
- **life-demos-examples**: Demo applications and examples (~100 files)
- **life-campaigns-marketing**: Marketing and outreach automation (~200 files)
- **life-archived-development**: Historical and legacy files (~500+ files)

## Implementation Timeline

- **Phase 1**: Core repository (IMMEDIATE)
- **Phase 2**: Azure infrastructure (HIGH PRIORITY)  
- **Phase 3**: Documentation (MEDIUM PRIORITY)
- **Phase 4**: Demos and examples (MEDIUM PRIORITY)
- **Phase 5**: Marketing campaigns (LOW PRIORITY)
- **Phase 6**: Archive legacy files (MAINTENANCE)

"""
        
        instructions_file = self.base_path / "RESTRUCTURING_INSTRUCTIONS.md"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📋 Setup instructions saved: {instructions_file}")

def main():
    """Main execution function"""
    base_path = os.getcwd()
    restructurer = RepositoryRestructurer(base_path)
    
    try:
        analysis_report = restructurer.execute_analysis()
        return analysis_report
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return None

if __name__ == "__main__":
    print("🎯 L.I.F.E Platform Repository Restructuring System")
    print("=" * 60)
    
    result = main()
    
    if result:
        print("\n🎉 Repository restructuring analysis completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Review REPOSITORY_ANALYSIS_REPORT.json")
        print("2. Check individual file lists (*_FILE_LIST.txt)")
        print("3. Read RESTRUCTURING_INSTRUCTIONS.md")
        print("4. Begin with creating the core repository")
        
        print(f"\n🎯 This will reduce your main repository from 1,257+ files to ~50 essential files!")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")        print("\n❌ Analysis failed. Please check the error messages above.")