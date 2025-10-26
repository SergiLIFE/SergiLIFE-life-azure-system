# GitHub Personal Access Token Setup Guide

## Quick Setup (2 minutes)

### 1. Create Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: `L.I.F.E Platform - Git Operations`
4. Select expiration: `90 days` (or custom)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

### 2. Use Token for Git Push
When Git asks for password, paste your token instead.

**Example:**
```
Username: SergiLIFE
Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Save Token in Git (Optional - Stores Securely)
After successful push, Git will remember the token:
```cmd
git config --global credential.helper wincred
```

## Alternative: Use SSH Instead (No tokens needed)

If you prefer SSH keys, let me know and I'll guide you through that setup.

## Troubleshooting

**Error: "Authentication failed"**
- Make sure you copied the full token
- Check that `repo` scope is selected
- Try generating a new token

**Token Already Expired?**
- Go back to https://github.com/settings/tokens
- Delete old token
- Generate new one with same scopes

## Current Push Command Waiting
```cmd
git push origin clean-history:main --force
Username: [Enter SergiLIFE]
Password: [Paste your PAT token]
```

This will push your GitHub Pages fix and all recovery work!
