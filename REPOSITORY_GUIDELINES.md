# Repository Maintenance Guidelines

## File Naming Conventions
- Do NOT use prefixes like: EMERGENCY, QUICK, IMMEDIATE, COMPREHENSIVE, FINAL
- Use descriptive, lowercase names: `fix-deployment-issue.md`, `setup-guide.md`

## Copilot Best Practices
- Always review Copilot-generated code before committing
- Delete auto-generated analysis files after use
- Use a separate branch for experimental Copilot-assisted work

## Periodic Cleanup
- Weekly: Review and delete unused generated files
- Monthly: Run repository analysis script
- Quarterly: Full repository audit and optimization

## Emergency Procedures
If repository becomes bloated again:
1. Create backup: `git bundle create backup.bundle --all`
2. Run analysis: `python repo-analysis.py`
3. Review quarantine directory before permanent deletion