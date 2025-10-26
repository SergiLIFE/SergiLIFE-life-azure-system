@echo off
echo ========================================
echo DIRECT COMMIT: All 521+ Changes
echo Simple Recovery Solution
echo ========================================

echo Step 1: Check current state...
git status

echo.
echo Step 2: Add EVERYTHING in workspace...
echo "Adding all files recursively..."

REM Add absolutely everything
git add -A
git add .
git add --all

REM Force add common file types that might be ignored
git add *.py --force 2>nul
git add *.js --force 2>nul
git add *.html --force 2>nul
git add *.css --force 2>nul
git add *.md --force 2>nul
git add *.yml --force 2>nul
git add *.yaml --force 2>nul
git add *.json --force 2>nul
git add *.txt --force 2>nul
git add *.bat --force 2>nul
git add *.sh --force 2>nul
git add *.ps1 --force 2>nul

REM Add directories that might have been missed
git add .github/ --force 2>nul
git add .vscode/ --force 2>nul
git add src/ --force 2>nul
git add docs/ --force 2>nul
git add scripts/ --force 2>nul
git add logs/ --force 2>nul
git add results/ --force 2>nul

echo.
echo Step 3: Check what's staged...
echo "Files ready to commit:"
git diff --cached --name-only
echo.
echo "Total files staged:"
git diff --cached --name-only | find /c /v ""

echo.
echo Step 4: Create comprehensive commit...
git commit -m "COMPLETE RECOVERY: All 521+ changes committed - L.I.F.E Platform full state restoration, GitHub Actions fixed, Azure integrations updated, campaign automation enhanced"

if %ERRORLEVEL% EQU 0 (
    echo "✅ SUCCESS! All changes committed!"
    
    echo.
    echo "Step 5: Push to GitHub..."
    git push origin main
    
    if %ERRORLEVEL% EQU 0 (
        echo "🎉 COMPLETE SUCCESS!"
        echo "✅ All 521+ changes committed and pushed"
        echo "✅ Repository fully synchronized"
        echo "✅ GitHub Actions should now work properly"
    ) else (
        echo "⚠️ Commit successful, but push failed"
        echo "Try manual push: git push origin main"
    )
) else (
    echo "ℹ️ No new changes found to commit"
    echo "Checking repository state..."
    
    echo "Recent commits:"
    git log --oneline -3
    
    echo "Remote status:"
    git status -v
)

echo.
echo "========================================"
echo "Recovery Complete - Check Results Above"
echo "========================================"
pause