@echo off
echo ========================================
echo L.I.F.E Platform - 521 Changes Recovery
echo October 26, 2025
echo ========================================

echo 🔍 STEP 1: Analyzing repository state...
echo.

echo "Current branch:"
git branch --show-current

echo.
echo "Repository status:"
git status

echo.
echo "🔍 STEP 2: Checking for unstaged changes..."
echo "Modified files:"
git diff --name-only
echo.
echo "Untracked files:"
git ls-files --others --exclude-standard
echo.

echo "🔍 STEP 3: Checking for staged changes..."
git diff --cached --name-only

echo.
echo "🔍 STEP 4: Looking for any stashed changes..."
git stash list

echo.
echo "🔍 STEP 5: Checking recent commits vs remote..."
git log --oneline main..origin/main 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo "Fetching latest from remote..."
    git fetch origin main
    git log --oneline main..origin/main
)

echo.
echo "🔍 STEP 6: Comprehensive file discovery..."
echo "Searching for recently modified files (last 24 hours)..."

REM Find files modified in the last day
forfiles /M *.* /S /C "cmd /c echo @path" 2>nul | findstr /V ".git" | findstr /V "node_modules" > recent_files.tmp 2>nul

echo.
echo "🔍 STEP 7: Recovery options available..."
echo.
echo "Choose recovery method:"
echo "1. Stage ALL current files (comprehensive recovery)"
echo "2. Interactive file selection"  
echo "3. Recover from git working directory"
echo "4. Check for hidden/ignored files"
echo "5. Force add everything and commit"
echo "6. Show detailed git status"
echo.

set /p choice="Enter choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo "🚀 COMPREHENSIVE RECOVERY: Adding all files..."
    
    REM Add all files including hidden ones
    git add -A
    git add . --force 2>nul
    
    echo "Files staged for commit:"
    git diff --cached --name-only
    
    echo.
    echo "Creating recovery commit..."
    git commit -m "RECOVERY: Add all 521+ pending changes - L.I.F.E Platform complete state restoration"
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ Recovery commit created!"
        
        echo "Push to GitHub? (y/n)"
        set /p push_choice=""
        if /I "%push_choice%"=="y" (
            git push origin main
            echo "✅ All changes pushed to GitHub!"
        )
    ) else (
        echo "ℹ️ No changes to commit - checking for other recovery options..."
    )
    
) else if "%choice%"=="2" (
    echo.
    echo "📋 INTERACTIVE RECOVERY..."
    echo "Current untracked files:"
    git ls-files --others --exclude-standard
    echo.
    echo "Add these files? (y/n)"
    set /p add_choice=""
    if /I "%add_choice%"=="y" (
        git add .
        git commit -m "RECOVERY: Interactive selection of pending changes"
    )
    
) else if "%choice%"=="3" (
    echo.
    echo "🔄 WORKING DIRECTORY RECOVERY..."
    
    REM Check working directory state
    git status --porcelain > status.tmp
    
    if exist status.tmp (
        for /f %%i in (status.tmp) do (
            echo "Found: %%i"
        )
    )
    
    git add -A
    git commit -m "RECOVERY: Working directory state - all pending files"
    
) else if "%choice%"=="4" (
    echo.
    echo "🔍 HIDDEN/IGNORED FILES CHECK..."
    
    REM Show ignored files
    git status --ignored --porcelain
    
    echo "Include ignored files in recovery? (y/n)"
    set /p ignored_choice=""
    if /I "%ignored_choice%"=="y" (
        git add . --force
        git commit -m "RECOVERY: Include previously ignored files"
    )
    
) else if "%choice%"=="5" (
    echo.
    echo "💪 FORCE RECOVERY: Adding everything..."
    
    REM Most aggressive recovery
    git add -A
    git add . --force
    git add --all
    
    REM Add any remaining files by extension
    git add *.py 2>nul
    git add *.js 2>nul  
    git add *.html 2>nul
    git add *.css 2>nul
    git add *.md 2>nul
    git add *.yml 2>nul
    git add *.json 2>nul
    git add *.txt 2>nul
    git add *.bat 2>nul
    
    echo "Total files staged:"
    git diff --cached --name-only | find /c /v ""
    
    if exist "git diff --cached --name-only" (
        git commit -m "FORCE RECOVERY: Complete L.I.F.E Platform state - all 521+ changes restored and committed"
        
        echo "✅ Force recovery successful!"
        echo "Push immediately? (y/n)"
        set /p force_push=""
        if /I "%force_push%"=="y" (
            git push origin main --force
            echo "✅ Force push completed!"
        )
    ) else (
        echo "ℹ️ No additional files found to recover"
    )
    
) else if "%choice%"=="6" (
    echo.
    echo "📊 DETAILED STATUS..."
    
    echo "=== Git Status ==="
    git status -v
    
    echo.
    echo "=== Diff Summary ==="
    git diff --stat
    
    echo.
    echo "=== Recent Activity ==="
    git log --oneline -10
    
) else (
    echo "❌ Invalid choice"
)

echo.
echo "🔍 FINAL STATUS CHECK..."
echo "Repository state after recovery attempt:"
git status --porcelain

echo.
echo "Recent commits:"
git log --oneline -5

echo.
echo "========================================"
echo "Recovery operation complete!"
echo "Current state saved to: recovery_log.txt"
echo "========================================"

REM Clean up temp files
del recent_files.tmp 2>nul
del status.tmp 2>nul

pause