# L.I.F.E. Repository Recovery Guide

## 🆘 Emergency Recovery Procedures

### Scenario 1: Repository Corruption Detected
```cmd
cd "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

# Run health check
python simple_repository_protector.py
# Select option 2 for health check

# If corruption found, run auto-repair
python simple_repository_protector.py
# Select option 3 for auto-repair

# Verify repair worked
git fsck --full
```

### Scenario 2: Complete Repository Loss
```cmd
# Navigate to desktop backups
cd "C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups"

# Find latest bundle
dir git_bundles\*.bundle /od

# Clone from latest bundle
git clone "git_bundles\life_repo_YYYYMMDD_HHMMSS.bundle" "recovered_repository"

# Verify recovery
cd recovered_repository
git fsck --full
git log --oneline -5
```

### Scenario 3: Partial File Loss
```cmd
# Navigate to desktop backups
cd "C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups"

# Find latest file backup
dir daily\life_repo_* /ad /od

# Copy missing files from backup
robocopy "daily\life_repo_YYYYMMDD_HHMMSS" "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system" /E /XO
```

## 🛡️ Prevention Best Practices

### Daily Actions
1. **Always check health before major operations:**
   ```cmd
   git health-check
   ```

2. **Use safe-push instead of regular push:**
   ```cmd
   git safe-push
   ```

3. **Create manual backup before risky operations:**
   ```cmd
   backup_life_repository.bat
   ```

### Weekly Actions
1. **Review backup status:**
   ```cmd
   python simple_repository_protector.py
   # Select option 4 for backup status
   ```

2. **Test bundle integrity:**
   ```cmd
   cd "C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups\git_bundles"
   git bundle verify life_repo_YYYYMMDD_HHMMSS.bundle
   ```

### Monthly Actions
1. **Clean up old backups manually if needed**
2. **Review and update protection settings**
3. **Test recovery procedure with old bundle**

## 🚨 Warning Signs to Watch For

### Immediate Action Required
- Git commands returning "object not found" errors
- Zero-byte files appearing in `.git/refs`
- Sudden repository size changes
- Git fsck reporting corruption

### Monitor These Symptoms
- Slow git operations
- Frequent "need to specify how to reconcile" messages
- Unusual merge conflicts
- Commands hanging or timing out

## 📋 Quick Command Reference

### Health & Diagnostics
```cmd
git fsck --full                    # Check repository integrity
git health-check                   # Custom health check alias
git status                         # Check working directory
git remote -v                      # Verify remote connections
```

### Backup & Recovery
```cmd
backup_life_repository.bat         # Full automated backup
python simple_repository_protector.py  # Interactive protection system
git bundle create backup.bundle --all  # Manual bundle creation
```

### Maintenance
```cmd
git gc --prune=now                 # Clean up repository
git fetch --all --prune            # Update from remotes
git backup-refs                    # Backup reference files
```

## 📍 Important File Locations

### Repository Location
```
c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system
```

### Desktop Backup Location
```
C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups\
├── daily\              # Daily file backups
├── git_bundles\        # Git bundle backups
├── health_reports\     # Health check logs
├── checksums\          # File integrity checksums
└── last_backup.json    # Latest backup status
```

### Protection Scripts
- `backup_life_repository.bat` - Automated backup system
- `simple_repository_protector.py` - Interactive protection tool
- `configure_git_safety.bat` - Git safety configuration
- `setup_scheduled_backups.bat` - Windows Task Scheduler setup

## 🔧 Troubleshooting Common Issues

### "Permission Denied" During Backup
- Run command prompt as Administrator
- Check antivirus isn't blocking operations
- Ensure destination folder has write permissions

### "Git Command Not Found"
- Verify Git is installed and in PATH
- Restart command prompt after Git installation
- Use full path to git.exe if needed

### "Bundle Verification Failed"
- Check bundle file isn't corrupted (compare checksum)
- Verify bundle was created successfully (check file size)
- Try older bundle if available

### "Out of Disk Space"
- Clean up old backups in desktop folder
- Move backups to external drive
- Adjust retention settings in protection scripts

## 📞 Emergency Contacts & Resources

### When All Else Fails
1. Check GitHub repository online for latest version
2. Contact repository owner (SergiLIFE)
3. Restore from external backup if available
4. Rebuild from documentation and preserved source files

### Additional Resources
- Git documentation: https://git-scm.com/docs
- Repository protection best practices
- L.I.F.E. platform documentation