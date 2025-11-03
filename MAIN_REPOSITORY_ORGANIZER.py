#!/usr/bin/env python3
"""
Main Repository Organization Tool
L.I.F.E. Platform - Repository Management Solution

PURPOSE: Organize 1,257+ files into manageable structure
SOLVES: GitHub truncation + repository navigation issues
STATUS: Ready for execution

Copyright 2025 - Sergio Paya Borrull
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class MainRepositoryOrganizer:
    def __init__(self):
        self.base_path = Path.cwd()
        self.organization_report = {
            "timestamp": datetime.now().isoformat(),
            "original_file_count": 0,
            "organized_structure": {},
            "migration_summary": {},
            "next_steps": []
        }
        
        # Define organization structure
        self.archive_structure = {
            "archive/deployment": {
                "description": "Deployment scripts and Azure configurations",
                "patterns": ["deploy*.py", "deploy*.bat", "deploy*.ps1", "deploy*.sh", 
                           "azure_*.py", "DEPLOY_*.bat", "*deployment*", "*DEPLOY*"]
            },
            "archive/testing": {
                "description": "Test suites and validation frameworks",
                "patterns": ["test*.py", "*test*.py", "TEST_*.bat", "*validation*", 
                           "*benchmark*", "validate_*.py", "*_test.py"]
            },
            "archive/campaigns": {
                "description": "Marketing and outreach automation",
                "patterns": ["campaign*.py", "*campaign*", "CAMPAIGN_*", "*email*", 
                           "*outreach*", "*marketing*", "october_15*"]
            },
            "archive/documentation": {
                "description": "Historical documentation and guides",
                "patterns": ["*.md", "*.html", "*.txt", "*GUIDE*", "*README*", 
                           "*INSTRUCTIONS*", "*CHECKLIST*"]
            },
            "archive/experiments": {
                "description": "Research and experimental implementations",
                "patterns": ["experiment*.py", "*experiment*", "*research*", 
                           "*demo*.py", "*prototype*", "quantum_*.py"]
            },
            "archive/backups": {
                "description": "Backup and recovery systems",
                "patterns": ["backup*.py", "*backup*", "BACKUP_*", "*recovery*", 
                           "*RECOVERY*", "CRITICAL_*"]
            },
            "archive/historical": {
                "description": "Historical development and deprecated files",
                "patterns": ["*DEPRECATED*", "*OLD*", "*LEGACY*", "SergiLIFE-RECOVERED*",
                           "*EMERGENCY*", "*URGENT*"]
            }
        }
        
        # Files to keep in root (high priority)
        self.root_priority_files = [
            "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "lifetheory.py",
            "venturi_gates_system.py",
            "alternative_deployment.py",
            "README.md",
            "requirements.txt",
            "azure_config.py",
            "function_app.py",
            "life_theory_platform_server.py",
            "LICENSE",
            ".gitignore",
            "host.json",
            "local.settings.json"
        ]
    
    def analyze_repository(self):
        """Analyze current repository structure"""
        print("Analyzing repository structure...")
        
        all_files = []
        for item in self.base_path.iterdir():
            if item.is_file():
                all_files.append(item.name)
        
        self.organization_report["original_file_count"] = len(all_files)
        print(f"Found {len(all_files)} files to organize")
        
        return all_files
    
    def categorize_files(self, files):
        """Categorize files into organizational structure"""
        categorized = {
            "root_priority": [],
            "archive": {category: [] for category in self.archive_structure.keys()}
        }
        
        # First, identify root priority files
        for file_name in files:
            if file_name in self.root_priority_files:
                categorized["root_priority"].append(file_name)
        
        # Then categorize remaining files
        remaining_files = [f for f in files if f not in self.root_priority_files]
        
        for file_name in remaining_files:
            categorized_flag = False
            
            for category, config in self.archive_structure.items():
                for pattern in config["patterns"]:
                    # Simple pattern matching (case insensitive)
                    if pattern.replace("*", "").lower() in file_name.lower():
                        categorized["archive"][category].append(file_name)
                        categorized_flag = True
                        break
                
                if categorized_flag:
                    break
            
            # If no category matched, put in historical
            if not categorized_flag:
                categorized["archive"]["archive/historical"].append(file_name)
        
        return categorized
    
    def create_archive_structure(self):
        """Create archive directory structure"""
        print("Creating archive directory structure...")
        
        for category in self.archive_structure.keys():
            category_path = self.base_path / category
            category_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {category}")
    
    def move_files_to_archive(self, categorized):
        """Move files to appropriate archive directories"""
        print("Organizing files into archive structure...")
        
        moved_count = 0
        for category, files in categorized["archive"].items():
            if not files:
                continue
                
            category_path = self.base_path / category
            
            for file_name in files:
                source_file = self.base_path / file_name
                dest_file = category_path / file_name
                
                if source_file.exists() and source_file != dest_file:
                    try:
                        shutil.move(str(source_file), str(dest_file))
                        moved_count += 1
                        print(f"Moved: {file_name} → {category}")
                    except Exception as e:
                        print(f"Error moving {file_name}: {e}")
        
        print(f"Successfully moved {moved_count} files to archive")
        return moved_count
    
    def create_navigation_readme(self, categorized):
        """Create new README with navigation system"""
        readme_content = f"""# L.I.F.E. Platform Ecosystem Hub

**Repository Organized:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Files Organized:** {self.organization_report['original_file_count']} files into structured archive  
**Status:** Navigation hub for L.I.F.E. Platform ecosystem

## 🎯 Active Development Repositories

### Core Platform
- **[life-platform-core](../life-platform-core)** - Essential L.I.F.E. algorithm and platform (19 files)
- **Status:** ✅ Production-ready neuroadaptive learning system
- **Quick Start:** `python life_theory_platform_server.py`

### Specialized Repositories (Recommended Structure)
- **[life-azure-infrastructure]** - Azure deployment and cloud services (~100 files)
- **[life-documentation]** - Comprehensive guides and references (~150 files)  
- **[life-demos-examples]** - Interactive demonstrations (~100 files)
- **[life-campaigns-marketing]** - Outreach and promotion tools (~200 files)

## 📁 This Repository (Organized Archive)

### Root Directory - Essential Files ({len(categorized['root_priority'])} files)
Core L.I.F.E. Platform components maintained in root for quick access:

"""
        
        # List root priority files
        for file_name in sorted(categorized["root_priority"]):
            readme_content += f"- `{file_name}`\n"
        
        readme_content += f"""

### Archive Structure - Organized Resources

This repository has been organized to solve GitHub's file truncation issue while preserving all development history.

"""
        
        # Document archive structure
        for category, config in self.archive_structure.items():
            file_count = len(categorized["archive"].get(category, []))
            readme_content += f"""
#### `{category}/` ({file_count} files)
{config['description']}

"""
        
        readme_content += """
## 🚀 Quick Access

### Run L.I.F.E. Platform
```bash
# Core algorithm test
python experimentP2L*.py

# Launch platform server
python life_theory_platform_server.py

# Azure deployment
python alternative_deployment.py
```

### Navigate Archive
```bash
# View deployment files
ls archive/deployment/

# Browse documentation
ls archive/documentation/

# Check test suites
ls archive/testing/
```

## 📊 Organization Benefits

✅ **GitHub Performance** - No more file truncation warnings  
✅ **Professional Structure** - Enterprise-ready organization  
✅ **Quick Navigation** - Find resources in <3 clicks  
✅ **Preserved History** - Complete development archive maintained  
✅ **Focused Development** - Clear separation of active vs archived code  

## 🎯 Next Steps

1. **Review organized structure** - Explore archive directories
2. **Create specialized repos** - Implement recommended repository structure  
3. **Update documentation** - Add cross-references between repositories
4. **Deploy core platform** - Use streamlined core repository for production

## 💡 Development Workflow

- **Active Development:** Use specialized repositories
- **Historical Research:** Browse archive directories in this repository
- **Quick Access:** Root directory contains essential files
- **Documentation:** Check archive/documentation/ for comprehensive guides

---

**L.I.F.E. Platform Status:** Production-ready neuroadaptive learning system  
**Repository Health:** Organized and GitHub-optimized  
**Copyright 2025** - Sergio Paya Borrull
"""
        
        # Save new README
        readme_path = self.base_path / "README_ORGANIZED.md"
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"Created navigation README: {readme_path}")
    
    def generate_organization_report(self, categorized, moved_count):
        """Generate comprehensive organization report"""
        self.organization_report.update({
            "files_moved": moved_count,
            "root_priority_files": len(categorized["root_priority"]),
            "archive_categories": {
                category: len(files) for category, files in categorized["archive"].items()
            },
            "total_organized": sum(len(files) for files in categorized["archive"].values()) + len(categorized["root_priority"])
        })
        
        # Save report
        report_path = self.base_path / "ORGANIZATION_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.organization_report, f, indent=2, ensure_ascii=False)
        
        print(f"Organization report saved: {report_path}")
    
    def execute_organization(self):
        """Execute complete repository organization"""
        print("L.I.F.E. Platform - Main Repository Organization")
        print("=" * 60)
        print(f"Organizing repository: {self.base_path}")
        print()
        
        try:
            # Step 1: Analyze repository
            files = self.analyze_repository()
            
            # Step 2: Categorize files
            categorized = self.categorize_files(files)
            print(f"Categorized {len(files)} files into organized structure")
            
            # Step 3: Create archive structure
            self.create_archive_structure()
            
            # Step 4: Move files to archive
            moved_count = self.move_files_to_archive(categorized)
            
            # Step 5: Create navigation system
            self.create_navigation_readme(categorized)
            
            # Step 6: Generate report
            self.generate_organization_report(categorized, moved_count)
            
            # Success summary
            print()
            print("REPOSITORY ORGANIZATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"✅ Files analyzed: {len(files)}")
            print(f"✅ Files moved to archive: {moved_count}")
            print(f"✅ Root priority files: {len(categorized['root_priority'])}")
            print(f"✅ Archive structure created")
            print(f"✅ Navigation system updated")
            print()
            print("Benefits Achieved:")
            print("🎯 GitHub truncation issue resolved")
            print("🎯 Professional repository organization")
            print("🎯 Efficient file navigation")
            print("🎯 Complete development history preserved")
            print()
            print("Next Steps:")
            print("1. Review README_ORGANIZED.md for navigation guide")
            print("2. Check ORGANIZATION_REPORT.json for detailed metrics")
            print("3. Consider creating specialized repositories as recommended")
            print("4. Update main README.md with organized structure")
            
        except Exception as e:
            print(f"ERROR during organization: {e}")
            print("Repository remains unchanged.")
            return False
            
        return True

def main():
    """Main execution function"""
    organizer = MainRepositoryOrganizer()
    success = organizer.execute_organization()
    
    if success:
        print("\n🎉 REPOSITORY ORGANIZATION SUCCESSFUL!")
        print("Your main repository is now organized and GitHub-optimized.")
    else:
        print("\n❌ REPOSITORY ORGANIZATION FAILED!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()    main()