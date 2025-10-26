@echo off
echo ========================================
echo QUICK FIX - Git Rebase Resolution
echo ========================================

echo Step 1: Abort any ongoing rebase...
git rebase --abort 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Rebase aborted successfully
) else (
    echo ℹ️ No rebase to abort
)

echo.
echo Step 2: Check current status...
git status --porcelain

echo.
echo Step 3: Add any remaining files...
git add -A

echo.
echo Step 4: Check if commit is needed...
git diff --cached --quiet
if %ERRORLEVEL% NEQ 0 (
    echo "📝 Creating commit for remaining changes..."
    git commit -m "Fix: Final resolution of git state and remaining changes"
    echo "✅ Commit created"
) else (
    echo "✅ No changes to commit"
)

echo.
echo Step 5: Force push to ensure sync...
git push origin main --force
if %ERRORLEVEL% EQU 0 (
    echo "✅ Push successful"
) else (
    echo "❌ Push failed"
)

echo.
echo Step 6: Final status check...
git status
git log --oneline -3

echo.
echo "========================================"
echo "✅ Git state should now be resolved!"
echo "========================================"
pause