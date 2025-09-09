# 🚀 VS Code Repository Sync PowerShell Script
# =============================================
# 
# Quickly sync VS Code configurations from the .vscode repository
# and other common sources to set up your development environment.

Write-Host ""
Write-Host "🚀 VS Code Repository Sync" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git not found. Please install Git first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Menu
Write-Host "📋 Quick Setup Options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Sync from SergiLIFE/.vscode repository (Recommended)" -ForegroundColor White
Write-Host "2. Sync from custom GitHub repository" -ForegroundColor White
Write-Host "3. Create minimal VS Code configuration" -ForegroundColor White
Write-Host "4. Install VS Code extensions only" -ForegroundColor White
Write-Host "5. Run full interactive setup" -ForegroundColor White
Write-Host "6. Run comprehensive sync tool" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Select option (1-6)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🔄 Syncing from SergiLIFE/.vscode repository..." -ForegroundColor Cyan
        python setup_vscode_repo.py --quick-setup
    }
    "2" {
        Write-Host ""
        $repo = Read-Host "Enter GitHub repository (owner/repo)"
        Write-Host "🔄 Syncing from $repo..." -ForegroundColor Cyan
        python setup_vscode_repo.py --repo $repo
    }
    "3" {
        Write-Host ""
        Write-Host "🔧 Creating minimal VS Code configuration..." -ForegroundColor Cyan
        python -c "from setup_vscode_repo import QuickVSCodeSetup; s=QuickVSCodeSetup(); s.create_backup(); s.create_essential_configs(); s.validate_setup()"
    }
    "4" {
        Write-Host ""
        Write-Host "🔌 Installing VS Code extensions..." -ForegroundColor Cyan
        python setup_vscode_repo.py --extensions-only
    }
    "5" {
        Write-Host ""
        Write-Host "🚀 Running interactive setup..." -ForegroundColor Cyan
        python setup_vscode_repo.py
    }
    "6" {
        Write-Host ""
        Write-Host "🔄 Running comprehensive sync tool..." -ForegroundColor Cyan
        python vscode_repo_sync.py --list-repos
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Restart VS Code to apply changes" -ForegroundColor White
Write-Host "   2. Open your workspace file: life-autonomous-optimizer.code-workspace" -ForegroundColor White
Write-Host "   3. Press F5 to start debugging your autonomous optimizer" -ForegroundColor White
Write-Host "   4. Use Ctrl+Shift+P → 'Tasks: Run Task' for automation" -ForegroundColor White
Write-Host ""

# Check if VS Code is installed
try {
    $codeVersion = code --version 2>&1
    Write-Host "🔧 VS Code detected: Ready to open workspace" -ForegroundColor Green
    
    $openWorkspace = Read-Host "Open VS Code workspace now? (y/n)"
    if ($openWorkspace -eq "y" -or $openWorkspace -eq "Y") {
        if (Test-Path "life-autonomous-optimizer.code-workspace") {
            code life-autonomous-optimizer.code-workspace
        }
        else {
            code .
        }
    }
}
catch {
    Write-Host "⚠️  VS Code CLI not found. You can open VS Code manually." -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"
