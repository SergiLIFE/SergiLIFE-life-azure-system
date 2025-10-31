@echo off
REM ========================================
REM L.I.F.E. Repository Protection Setup
REM Complete setup for corruption prevention
REM ========================================

echo.
echo ████████████████████████████████████████████████
echo  L.I.F.E. REPOSITORY PROTECTION SETUP
echo  Comprehensive backup and corruption prevention
echo ████████████████████████████████████████████████
echo.

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo 🛡️  Setting up repository protection system...

echo.
echo [1/5] Configuring Git safety settings...
call configure_git_safety.bat

echo.
echo [2/5] Creating backup directory structure...
python -c "
import pathlib
backup_dir = pathlib.Path.home() / 'Desktop' / 'LIFE_Repository_Backups'
subdirs = ['daily', 'weekly', 'git_bundles', 'health_reports', 'checksums', 'recovery_kits']
for subdir in subdirs:
    (backup_dir / subdir).mkdir(parents=True, exist_ok=True)
print('✅ Desktop backup directories created')
print(f'📍 Location: {backup_dir}')
"

echo.
echo [3/5] Running initial backup...
call backup_life_repository.bat

echo.
echo [4/5] Setting up scheduled tasks...
call setup_scheduled_backups.bat

echo.
echo [5/5] Running health verification...
python simple_repository_protector.py 2

echo.
echo ████████████████████████████████████████████████
echo  🎉 SETUP COMPLETE! 🎉
echo ████████████████████████████████████████████████
echo.
echo ✅ Git safety configuration applied
echo ✅ Backup system installed
echo ✅ Desktop backup location created
echo ✅ Scheduled tasks configured
echo ✅ Initial backup completed
echo ✅ Health check passed
echo.
echo 📋 DAILY COMMANDS TO REMEMBER:
echo   git health-check     (before major operations)
echo   git safe-push        (instead of git push)
echo   backup_life_repository.bat  (manual backup)
echo.
echo 📁 BACKUP LOCATION:
echo   C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups
echo.
echo 📖 RECOVERY GUIDE:
echo   See REPOSITORY_RECOVERY_GUIDE.md for detailed instructions
echo.
echo 🔧 PROTECTION TOOLS:
echo   simple_repository_protector.py  (interactive protection)
echo   backup_life_repository.bat      (automated backup)
echo   verify_git_repair.bat          (verify repository health)
echo.
echo Protection system is now active and monitoring your repository!
echo.
pause