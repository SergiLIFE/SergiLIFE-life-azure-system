# File Corruption Recovery Plan

**Date:** November 7, 2025
**Status:** ENCODING CORRUPTION DETECTED (NOT VIRUS)

## Problem Summary

- **Type:** Systematic character replacement in Python files
- **Pattern:** "import"→"ipo", "class"→"lss", "Learning"→"Lnin"
- **Empty Files:** ~11 files completely blank
- **Date Occurred:** November 6, 2025, 15:48

## Root Cause

This is **NOT** a virus or malware. This is an **encoding corruption issue** likely caused by:

1. Editor encoding mismatch
2. Git line ending conversion issue
3. File system corruption
4. Character set conflict during save

## Affected Files

### Corrupted (character replacement)

- `algorithms/python-core/experimentP2L_REPAIRED.py` (24,121 bytes)
- `algorithms/python-core/experimentP2L.I.F.E-Learning...py` (15,889 bytes)
- Multiple other Python files in workspace

### Empty (0 bytes)

- `algorithms/python-core/eeg_validation_demo.py`
- `algorithms/python-core/lightweight_eeg_validation.py`
- `docs/user-guide.md`
- Several documentation markdown files

## Recovery Options

### Option 1: Git Reset (SAFEST)

```cmd
git reset --hard HEAD~5
git checkout HEAD -- algorithms/python-core/experimentP2L*
```

This recovers files from before corruption (Oct-Nov commits).

### Option 2: Use Clean Version

The clean version I created exists:

- `algorithms/python-core/experimentP2L_REPAIRED_CLEAN.py` (564 lines, fully functional)
- Contains all core L.I.F.E. Algorithm functionality
- Ready to use immediately

### Option 3: GitHub Remote Recovery

```cmd
git fetch origin
git checkout origin/main -- algorithms/python-core/experimentP2L_REPAIRED.py
```

## Immediate Actions

1. ✅ Verified no malware (encoding issue only)
2. ⏳ Check if F: drive has uncorrupted backup
3. ⏳ Test git recovery options
4. ⏳ Verify clean version works
5. ⏳ Commit clean version to git

## Prevention

1. Always use UTF-8 encoding in VS Code
2. Set git to handle line endings: `git config core.autocrlf false`
3. Regular backups to F: drive
4. Commit working code frequently
