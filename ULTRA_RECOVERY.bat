@echo off
echo ULTRA-URGENT: FILES DELETED AGAIN!
echo.
echo Checking current state...
dir /b | head -10

echo.
echo Quick recovery attempts...
git checkout HEAD~1 -- . 2>nul
git checkout HEAD~2 -- . 2>nul
git stash pop 2>nul

echo.
echo Restore from any backups...
if exist "BACKUP_BEFORE_NUCLEAR" xcopy "BACKUP_BEFORE_NUCLEAR\*" . /s /e /h /y 2>nul

echo.
echo Current files after recovery:
dir /b | head -10

echo.
echo Add whatever we recovered...
git add -A
git commit -m "ULTRA RECOVERY: Restore files deleted during commit"
git push origin main

echo.
echo Check if files are back...
for /f %%i in ('dir /b ^| find /c /v ""') do echo Files now: %%i

pause