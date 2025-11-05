#!/usr/bin/env python3
"""
L.I.F.E Platform Core Repository Creator
======================================
Automatically creates the core repository with essential files only
Solves GitHub's "too many files" truncation issue
"""

import os
import shutil
from pathlib import Path

def create_core_repository():
    """Create the core repository with essential files only"""
    
    # Essential files for the core repository (keep under 50 files)
    essential_files = [
        # Core Algorithm Files
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
        "lifetheory.py", 
        "venturi_gates_system.py",
        
        # Main Platform Files
        "alternative_deployment.py",
        "life_theory_platform_server.py", 
        "life_theory_platform.html",
        "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html",
        
        # Configuration Files
        "README.md",
        "requirements.txt", 
        "azure_config.py",
        "host.json",
        "local.settings.json",
        "azure.yaml",
        
        # Azure Integration  
        "azure_functions_workflow.py",
        "function_app.py",
        
        # Core Styles
        "life_theory_platform_styles.css",
        "styles.css",
        "index.html",
        
        # Testing
        "core_life_validation.py",
        "simple_life_testing_suite.py",
        
        # Essential Documentation
        "LICENSE",
        ".gitignore"
    ]
    
    current_dir = Path.cwd()
    core_dir = current_dir.parent / "life-platform-core"
    
    print("🎯 L.I.F.E Platform Core Repository Creator")
    print("=" * 50)
    print(f"Source: {current_dir}")
    print(f"Target: {core_dir}")
    print()
    
    # Create core directory
    if not core_dir.exists():
        core_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {core_dir}")
    else:
        print(f"📁 Using existing directory: {core_dir}")
    
    # Copy essential files
    copied_files = 0
    missing_files = []
    
    print("\n📋 Copying essential files...")
    
    for file_name in essential_files:
        source_file = current_dir / file_name
        target_file = core_dir / file_name
        
        if source_file.exists():
            try:
                # Create target directory if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(source_file, target_file)
                print(f"✅ Copied: {file_name}")
                copied_files += 1
            except Exception as e:
                print(f"❌ Error copying {file_name}: {e}")
        else:
            missing_files.append(file_name)
            print(f"⚠️  Missing: {file_name}")
    
    # Create new README for core repository
    core_readme = """# L.I.F.E Platform - Core System

**Learning Individually from Experience** - Essential Core Components

## 🎯 Repository Focus

This repository contains **only the essential core components** of the L.I.F.E Platform. The complete system has been restructured into focused repositories for better maintainability and to solve GitHub's file limit issues.

### 🧠 Core Components

- **experimentP2L Algorithm** - Main neural processing algorithm  
- **Platform Server** - Core platform functionality
- **Clinical Interface** - Primary clinical dashboard
- **Azure Configuration** - Essential cloud integration

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the platform
python alternative_deployment.py

# Or start the theory platform
python life_theory_platform_server.py
```

### 🔗 Complete L.I.F.E Platform Ecosystem

| Repository | Purpose | Status |
|------------|---------|--------|
| **life-platform-core** | Essential algorithm & platform (THIS REPO) | 🟢 ACTIVE |
| **life-azure-infrastructure** | Deployment & infrastructure | 🔄 PLANNED |
| **life-documentation** | Guides & documentation | 🔄 PLANNED |
| **life-demos-examples** | Demo applications | 🔄 PLANNED |
| **life-campaigns-marketing** | Marketing automation | 🔄 PLANNED |

### 📊 System Status

- **Core Platform**: ✅ Operational
- **Azure Marketplace**: ✅ Live (Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`)  
- **Production Ready**: ✅ September 27, 2025
- **File Count**: ~{file_count} essential files (vs 1,257+ in original repo)

---

**Copyright 2025** - Sergio Paya Borrull | L.I.F.E Platform Core System
""".replace("{file_count}", str(copied_files))
    
    # Write new README
    core_readme_file = core_dir / "README.md"
    with open(core_readme_file, 'w', encoding='utf-8') as f:
        f.write(core_readme)
    
    print(f"\n📄 Created core README: {core_readme_file}")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ Core Repository Creation Complete!")
    print(f"📊 Files copied: {copied_files}")
    if missing_files:
        print(f"⚠️  Missing files: {len(missing_files)}")
        print("   (These may be optional or in different locations)")
    
    print(f"\n📁 Core repository created at: {core_dir}")
    print(f"🎯 Reduced from 1,257+ files to {copied_files} essential files")
    
    print("\n🚀 Next Steps:")
    print("1. Test the core repository:")
    print(f"   cd {core_dir}")
    print("   python alternative_deployment.py")
    print("\n2. Initialize git repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial L.I.F.E Platform core repository'")
    print("\n3. Create GitHub repository and push")
    print("4. Create additional focused repositories as needed")
    
    return core_dir, copied_files, missing_files

if __name__ == "__main__":
    try:
        core_dir, copied_files, missing_files = create_core_repository()
        
        if copied_files > 0:
            print(f"\n🎉 Success! Core repository created with {copied_files} files")
        else:
            print("\n❌ No files were copied. Please check the file paths.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the script and try again.")