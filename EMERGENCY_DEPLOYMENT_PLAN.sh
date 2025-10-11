#!/bin/bash
# 🚀 L.I.F.E. PLATFORM EMERGENCY DEPLOYMENT - OCTOBER 15 DEMO
# Deploy actual L.I.F.E. Platform code to Azure services
# 4 days remaining until demo!

echo "🚨 L.I.F.E. PLATFORM EMERGENCY DEPLOYMENT"
echo "========================================"
echo "Issue: Infrastructure running but no application code deployed"
echo "Solution: Deploy L.I.F.E. Platform from GitHub repository"
echo "Target: October 15, 2025 demos (4 days remaining)"
echo

# Check current deployment status
echo "📊 CURRENT DEPLOYMENT STATUS:"
echo "✅ Static Web App: green-ground-0c65efe0f.1.azurestaticapps.net - Shows default page"
echo "✅ Demo App: life-microsoft-demo-app.azurewebsites.net - Shows default page"  
echo "✅ Theory App: life-theory-app-202508292341.azurewebsites.net - Shows default page"
echo "❌ Authentication: AADSTS50011 error (redirect URI mismatch)"
echo

# Check GitHub connection for static web app
echo "🔍 CHECKING GITHUB CONNECTION:"
az staticwebapp show --name life-platform-webapp --resource-group life-platform-rg --query '{Name:name, RepositoryUrl:repositoryUrl, Branch:repositoryBranch}' --output table

echo
echo "📂 CHECKING STATIC WEB APP DEPLOYMENT:"
az staticwebapp deployment list --name life-platform-webapp --resource-group life-platform-rg --query '[0].{Status:status, CreatedTime:createdTimeUtc, Source:source}' --output table

echo
echo "🔧 CHECKING FUNCTION APP DEPLOYMENT:"
az functionapp deployment source show --name life-functions-app --resource-group life-platform-rg --query '{RepoUrl:repoUrl, Branch:branch, IsManualIntegration:isManualIntegration}' --output table

echo
echo "⚙️ WEBAPP DEPLOYMENT SOURCE:"
az webapp deployment source show --name life-microsoft-demo-app --resource-group rg-microsoft-demo-env --query '{RepoUrl:repoUrl, Branch:branch, IsManualIntegration:isManualIntegration}' --output table

echo
echo "🎯 SOLUTION OPTIONS FOR OCTOBER 15:"
echo "=================================="
echo "OPTION 1: GitHub Auto-Deploy (Recommended)"
echo "- Configure GitHub Actions deployment"
echo "- Automatic deployment from main branch"
echo "- Takes 5-10 minutes"
echo
echo "OPTION 2: Manual ZIP Deploy"  
echo "- Upload L.I.F.E. Platform files directly"
echo "- Immediate deployment"
echo "- Takes 2-3 minutes"
echo
echo "OPTION 3: Local Development Demo"
echo "- Run L.I.F.E. Platform locally"
echo "- Screen share during demos"
echo "- Zero deployment time"
echo

echo "🚀 IMMEDIATE ACTIONS NEEDED:"
echo "1. Check if GitHub repository has deployable code"
echo "2. Configure deployment source for web apps"
echo "3. Test deployment with simple index.html"
echo "4. Deploy full L.I.F.E. Platform application"
echo "5. Update demo URLs for October 15"