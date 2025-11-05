# L.I.F.E Platform Repository Restructuring Plan
# =============================================
# Problem: Repository too large (1,257+ files) - GitHub truncating listings
# Solution: Split into 6 focused repositories

## 📊 Current Repository Analysis

**Total Files**: 1,257+ (causing GitHub truncation)
**GitHub Advice**: "Sorry, we had to truncate this directory to 1,000 files. 257 entries were omitted from the list."

## 🎯 Recommended Repository Structure

### 1. life-platform-core (MAIN) - ~50 files
**Purpose**: Essential L.I.F.E Platform functionality only
**Priority**: IMMEDIATE - Create this first

Essential files to keep:
- experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py
- lifetheory.py  
- venturi_gates_system.py
- README.md
- requirements.txt
- azure_config.py
- alternative_deployment.py
- life_theory_platform_server.py
- LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
- azure_functions_workflow.py
- host.json
- local.settings.json
- LICENSE
- .gitignore

### 2. life-azure-infrastructure - ~100 files
**Purpose**: All Azure deployment and infrastructure components
**Priority**: HIGH

Move these files:
- All files starting with "azure_", "deploy_", "AZURE_"
- Infrastructure files (infra/, *.bicep, *.json configs)
- CloudShell scripts and deployment automation
- Marketplace and subscription management

### 3. life-documentation - ~150 files  
**Purpose**: Documentation, guides, and reference materials
**Priority**: MEDIUM

Move these files:
- All .md files (except core README.md)
- All GUIDE, MANUAL, INSTRUCTIONS files
- All documentation and reference materials
- Setup and troubleshooting guides

### 4. life-demos-examples - ~100 files
**Purpose**: Demo applications and example implementations  
**Priority**: MEDIUM

Move these files:
- All demo_, clinical_, educational_ files
- Example implementations and tutorials
- Interactive tools and validation scripts
- Testing and benchmark applications

### 5. life-campaigns-marketing - ~200 files
**Purpose**: Marketing campaigns and outreach automation
**Priority**: LOW

Move these files:
- All campaign_, email_, outreach_ files  
- Microsoft partnership and ISV materials
- Marketing automation and templates
- October 15 demo materials

### 6. life-archived-development - ~500+ files
**Purpose**: Historical development files and legacy components
**Priority**: ARCHIVE

Move these files:
- Backup and recovery files
- Legacy/deprecated implementations
- Temporary and emergency fixes
- Development history and archives

## 🚀 Quick Implementation Steps

### Step 1: Create Core Repository (IMMEDIATE)
```bash
# Create new directory for core files
mkdir ../life-platform-core

# Copy essential files (list above)
# Test that core functionality works
cd ../life-platform-core
python alternative_deployment.py
```

### Step 2: Update Main Repository References
```bash
# Add README linking to other repositories
# Update documentation with new structure
# Create repository overview
```

### Step 3: Create Additional Repositories (As Needed)
```bash
# Create focused repositories for each component
# Migrate files according to categories above
# Set up cross-repository references
```

## ✅ Benefits of This Structure

1. **GitHub Compatibility**: No more file truncation warnings
2. **Improved Performance**: Faster cloning and operations  
3. **Better Organization**: Clear separation of concerns
4. **Easier Maintenance**: Focused development areas
5. **Team Collaboration**: Clear component ownership
6. **Simplified Deployment**: Targeted CI/CD pipelines

## 🎯 Immediate Action Plan

1. **TODAY**: Create life-platform-core with ~50 essential files
2. **THIS WEEK**: Move Azure infrastructure to separate repository
3. **ONGOING**: Gradually migrate other components as needed

This approach will immediately solve the GitHub truncation issue while maintaining all functionality.

---

**Goal**: Reduce main repository from 1,257+ files to ~50 core files
**Timeline**: Core repository can be created immediately  
**Impact**: Solves GitHub advisory while improving maintainability