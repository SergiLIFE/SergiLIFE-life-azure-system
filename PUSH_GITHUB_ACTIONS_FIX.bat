@echo off
echo ========================================
echo GitHub Actions Fix - Commit and Push
echo October 26, 2025
echo ========================================

echo Step 1: Abort any rebase operations...
git rebase --abort 2>nul

echo Step 2: Add all fixes...
git add -A

echo Step 3: Check what we're committing...
echo "Files to be committed:"
git diff --cached --name-only

echo.
echo Step 4: Create commit...
git commit -m "Fix: Resolve Azure Static Web Apps deployment failures - disable auto-deploy until tokens configured"

if %ERRORLEVEL% EQU 0 (
    echo "✅ Commit created successfully"
    
    echo.
    echo Step 5: Push to GitHub...
    git push origin main
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ Push successful - GitHub Actions should now work!"
        echo.
        echo "🎯 Summary of fixes:"
        echo "- Azure Static Web Apps: Disabled auto-deploy (manual trigger only)"
        echo "- Added skip_deploy_on_missing_secrets to prevent failures"
        echo "- All deployment workflows now safe from token issues"
        echo.
        echo "📋 Next: Monitor GitHub Actions to confirm no more failures"
    ) else (
        echo "❌ Push failed - check git status"
    )
) else (
    echo "ℹ️ No changes to commit (fixes may already be applied)"
)

echo.
echo Step 6: Final status...
git status --porcelain
git log --oneline -2

echo.
echo "========================================"
echo "GitHub Actions Fix Complete!"
echo "========================================"
pause