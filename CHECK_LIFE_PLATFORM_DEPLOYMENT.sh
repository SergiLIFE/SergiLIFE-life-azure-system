#!/bin/bash
# 🔍 L.I.F.E. PLATFORM DEPLOYMENT CHECKER
# Find where the actual L.I.F.E. Platform application is deployed
# October 11, 2025 - 4 days to demo

echo "🔍 L.I.F.E. PLATFORM DEPLOYMENT STATUS CHECK"
echo "============================================="
echo "Checking all web applications for actual L.I.F.E. Platform deployment..."
echo

# Check the functions app
echo "🚀 CHECKING: life-functions-app.azurewebsites.net"
echo "Command: az functionapp show --name life-functions-app --resource-group life-platform-rg --query '{Name:name, State:state, DefaultHostName:defaultHostName, Kind:kind}' --output table"
az functionapp show --name life-functions-app --resource-group life-platform-rg --query '{Name:name, State:state, DefaultHostName:defaultHostName, Kind:kind}' --output table

echo
echo "🔗 Functions App Details:"
az functionapp list --resource-group life-platform-rg --query '[].{Name:name, DefaultHostName:defaultHostName, State:state, Runtime:siteConfig.linuxFxVersion}' --output table

echo
echo "🌐 CHECKING: Static Web App (life-platform-webapp)"
az staticwebapp show --name life-platform-webapp --resource-group life-platform-rg --query '{Name:name, DefaultHostname:defaultHostname, RepositoryUrl:repositoryUrl}' --output table

echo
echo "📋 ALL WEB APPS IN SUBSCRIPTION:"
echo "Looking for deployed L.I.F.E. Platform applications..."
az webapp list --query '[].{Name:name, ResourceGroup:resourceGroup, DefaultHostName:defaultHostName, State:state, Kind:kind}' --output table

echo
echo "🔍 CHECKING SPECIFIC L.I.F.E. WEB APPS:"
# Check life-theory apps
az webapp show --name life-theory-final --resource-group rg-life-theory-appservice --query '{Name:name, State:state, DefaultHostName:defaultHostName}' --output table 2>/dev/null || echo "life-theory-final: Not found or not accessible"

az webapp show --name life-theory-app-202508292341 --resource-group rg-life-theory-aci --query '{Name:name, State:state, DefaultHostName:defaultHostName}' --output table 2>/dev/null || echo "life-theory-app: Not found or not accessible"

echo
echo "🔍 CHECKING CONTAINER APPS (Modern Deployment):"
az containerapp list --resource-group rg-life-marketplace-prod --query '[].{Name:name, Fqdn:configuration.ingress.fqdn, ProvisioningState:provisioningState}' --output table 2>/dev/null || echo "No container apps found in marketplace prod"

echo
echo "📊 DEPLOYMENT ASSESSMENT:"
echo "========================="
echo "The life-microsoft-demo-app shows default Azure page, which means:"
echo "1. Infrastructure is running ✅"
echo "2. Application code is NOT deployed ❌"
echo "3. Need to identify where L.I.F.E. Platform is actually deployed"
echo
echo "🎯 NEXT STEPS:"
echo "1. Check if L.I.F.E. Platform is in Functions App"  
echo "2. Check Static Web App deployment"
echo "3. Check container apps in marketplace-prod"
echo "4. Deploy to demo app if needed"