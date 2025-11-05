# Create New Static Web App via Azure Portal (Reliable Alternative)

## Why Use Portal Instead of CLI
- CLI "No Content" error is common with Static Web Apps
- Portal method is more reliable and provides better error messages
- Visual feedback on configuration

## Step-by-Step Portal Creation

### 1. Open Azure Portal
- Go to https://portal.azure.com
- Navigate to **Create a resource**

### 2. Create Static Web App
- Search for "Static Web App"
- Click **Create**

### 3. Configuration
**Basics:**
- **Subscription**: 5c88cef6-f243-497d-98af-6c6086d575ca
- **Resource Group**: rg-life-platform-static
- **Name**: life-platform-v2
- **Plan Type**: Free
- **Region**: East US 2

**Deployment Details:**
- **Source**: GitHub
- **GitHub Account**: SergiLIFE
- **Organization**: SergiLIFE
- **Repository**: SergiLIFE-life-azure-system
- **Branch**: main

**Build Details:**
- **Build Presets**: Custom
- **App location**: /docs
- **Api location**: (leave empty)
- **Output location**: (leave empty)

### 4. Review and Create
- Review all settings
- Click **Create**
- Wait for deployment to complete

### 5. Update GitHub Secret
After creation:
- Copy the new deployment token from the Overview page
- Go to GitHub repository Settings → Secrets → Actions
- Update or create: AZURE_STATIC_WEB_APPS_API_TOKEN_LIFE_PLATFORM_V2

## Expected Outcome
- New Static Web App at: life-platform-v2.azurestaticapps.net
- Fresh deployment pipeline
- Clean configuration without previous issues

## If Portal Also Fails
Alternative hosting options:
1. **Keep using App Service** (already working at lifecoach-121.com)
2. **GitHub Pages** (free for public repos)
3. **Netlify** (free tier, excellent Static Site hosting)
4. **Vercel** (free tier, optimized for modern frameworks)