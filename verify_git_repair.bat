@echo off
echo ===== GIT REPAIR VERIFICATION =====
cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo.
echo Testing git repository status...
git status --porcelain
echo Git status exit code: %ERRORLEVEL%

echo.
echo Testing git fsck...
git fsck --full
echo Git fsck exit code: %ERRORLEVEL%

echo.
echo Testing git branch info...
git branch --show-current
echo Current branch exit code: %ERRORLEVEL%

echo.
echo Testing git remotes...
git remote -v
echo Remotes exit code: %ERRORLEVEL%

echo.
echo Testing git log (last 3 commits)...
git log --oneline -3
echo Log exit code: %ERRORLEVEL%

echo.
echo ===== VERIFICATION COMPLETE =====
echo If all exit codes are 0, the repository is healthy.
pause