# 🔄 VS Code Repository Synchronization Tools

**Never recreate your VS Code development environment again!** This toolkit allows you to safely sync VS Code configurations, tools, and utilities from the `.vscode` repository and other sources.

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)
```powershell
# Run the PowerShell setup script
.\sync_vscode_repo.ps1
```

### Option 2: Quick Python Setup
```bash
# Quick setup from SergiLIFE/.vscode repository
python setup_vscode_repo.py --quick-setup

# Or sync from any GitHub repository
python setup_vscode_repo.py --repo "owner/repo"
```

### Option 3: Interactive Setup
```bash
# Full interactive setup with options
python setup_vscode_repo.py
```

## 🛠️ Available Tools

### 1. `sync_vscode_repo.ps1` - PowerShell Quick Setup
- **Purpose**: One-click VS Code environment setup
- **Features**: Prerequisites check, menu-driven setup, automatic workspace opening
- **Best for**: Windows users who want the easiest setup experience

### 2. `setup_vscode_repo.py` - Python Quick Setup
- **Purpose**: Fast repository synchronization with intelligent merging
- **Features**: Backup creation, JSON merging, extension installation
- **Best for**: Quick setup from known repositories

### 3. `vscode_repo_sync.py` - Comprehensive Sync Tool
- **Purpose**: Advanced repository synchronization with conflict resolution
- **Features**: GitHub API integration, selective sync, validation
- **Best for**: Power users who need fine-grained control

## 📋 What Gets Synchronized

### VS Code Configuration Files
- ✅ **settings.json** - Editor and language settings
- ✅ **tasks.json** - Build and automation tasks
- ✅ **launch.json** - Debug configurations
- ✅ **extensions.json** - Recommended extensions
- ✅ **snippets/** - Code snippets
- ✅ **keybindings.json** - Custom keyboard shortcuts

### Development Tools
- ✅ **Performance monitoring scripts**
- ✅ **Testing utilities**
- ✅ **Setup and configuration tools**
- ✅ **Azure integration scripts**
- ✅ **Workspace files**

### Essential Extensions
- 🐍 **Python** (ms-python.python)
- 🔧 **Black Formatter** (ms-python.black-formatter)
- ☁️ **Azure Account** (ms-vscode.azure-account)
- 🤖 **GitHub Copilot** (github.copilot)
- 📝 **YAML** (redhat.vscode-yaml)
- 💻 **PowerShell** (ms-vscode.powershell)

## 🔧 Advanced Usage

### Sync from Specific Repository
```bash
# Sync from the .vscode repository
python setup_vscode_repo.py --repo "SergiLIFE/.vscode"

# Sync from Microsoft samples
python setup_vscode_repo.py --repo "microsoft/vscode-samples"
```

### Install Extensions Only
```bash
python setup_vscode_repo.py --extensions-only
```

### Use the Advanced Sync Tool
```bash
# List suggested repositories
python vscode_repo_sync.py --list-repos

# Sync with GitHub API
python vscode_repo_sync.py --github https://github.com/SergiLIFE/.vscode

# Sync from local repository
python vscode_repo_sync.py --local ../other-project

# Validate current configuration
python vscode_repo_sync.py --validate
```

## 🛡️ Safety Features

### Automatic Backups
- Creates timestamped backups before any changes
- Backup location: `backups/vscode_backup_YYYYMMDD_HHMMSS/`
- Easy restore if something goes wrong

### Intelligent Merging
- **Settings.json**: Merges with conflict resolution prompts
- **Tasks.json**: Adds new tasks without removing existing ones
- **Launch.json**: Combines debug configurations
- **Extensions.json**: Merges recommendation lists

### Validation
- JSON syntax validation
- Configuration completeness checks
- Extension availability verification
- Path and interpreter validation

## 📁 File Structure After Sync

```
your-project/
├── .vscode/
│   ├── settings.json          # 🔧 Editor configuration
│   ├── tasks.json            # 🏃 Build and run tasks
│   ├── launch.json           # 🐛 Debug configurations
│   ├── extensions.json       # 🔌 Extension recommendations
│   └── python.json           # 🐍 Python code snippets
├── backups/                  # 📦 Automatic backups
├── performance_monitor.py    # 📊 System monitoring
├── quick_test.py            # 🧪 Testing utilities
├── setup_vscode_repo.py     # 🚀 Quick setup tool
├── vscode_repo_sync.py      # 🔄 Advanced sync tool
└── sync_vscode_repo.ps1     # 💻 PowerShell launcher
```

## 🎯 Use Cases

### 1. New Project Setup
```powershell
# Set up VS Code environment for a new L.I.F.E. project
.\sync_vscode_repo.ps1
# Choose option 1 for SergiLIFE/.vscode repository
```

### 2. Team Collaboration
```bash
# Share your VS Code config with team
python vscode_repo_sync.py --github https://github.com/your-team/.vscode

# Team members sync from your config
python setup_vscode_repo.py --repo "your-team/.vscode"
```

### 3. Multi-Project Consistency
```bash
# Sync common settings across multiple projects
python vscode_repo_sync.py --local ../template-project
```

### 4. Extension Management
```bash
# Install all recommended extensions for the platform
python setup_vscode_repo.py --extensions-only
```

## 🚨 Troubleshooting

### Common Issues

**Q: Git clone fails**
```bash
# Ensure Git is installed and accessible
git --version

# Check network connectivity
ping github.com
```

**Q: VS Code extensions won't install**
```bash
# Ensure VS Code CLI is available
code --version

# Install VS Code CLI if missing (Windows)
# Open VS Code → Ctrl+Shift+P → "Shell Command: Install 'code' command in PATH"
```

**Q: JSON merge conflicts**
- The tool will prompt you for each conflict
- Choose 'y' to keep new values, 'n' to keep existing, or 'review' for manual selection

**Q: Permission errors**
- Run PowerShell as Administrator if needed
- Ensure write permissions to the project directory

### Recovery

**Restore from backup:**
```bash
# Find your backup
ls backups/

# Restore manually
cp -r backups/vscode_backup_YYYYMMDD_HHMMSS/.vscode ./
```

## 🎉 Success Indicators

After successful sync, you should see:
- ✅ All JSON files are valid
- ✅ VS Code opens without errors
- ✅ Debug configurations are available (F5)
- ✅ Tasks are accessible (Ctrl+Shift+P → "Tasks")
- ✅ Extensions are installed and active
- ✅ Python interpreter is detected
- ✅ Azure account is connected (if configured)

## 🔗 Integration with L.I.F.E. Platform

These tools are specifically designed for the **L.I.F.E. (Learning Individually from Experience)** autonomous optimizer platform:

- **Autonomous Optimizer**: Debug configurations ready
- **Model Optimization**: Performance monitoring integrated
- **SOTA Benchmarks**: Testing utilities included
- **Azure Integration**: Cloud deployment configurations
- **Real-time Monitoring**: System performance tracking

## 📞 Support

If you encounter issues:
1. Check the validation output for specific errors
2. Review the backup directory for recovery options
3. Use the `--validate` flag to diagnose configuration issues
4. Ensure all prerequisites (Python, Git, VS Code) are installed

---

**🎯 Goal**: Zero-setup development environment that works everywhere, every time!

*Last updated: September 9, 2025*
