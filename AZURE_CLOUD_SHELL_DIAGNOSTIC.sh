#!/bin/bash
# 🔍 AZURE ACCOUNT DIAGNOSTIC COMMANDS
# L.I.F.E. Platform - October 15, 2025 Demo Assessment
# Run these commands in Azure Cloud Shell to identify account and resources

echo "🔍 AZURE ACCOUNT DIAGNOSTIC - OCTOBER 15 DEMO PREPARATION"
echo "=========================================================="
echo "Current Date: October 11, 2025 (4 days to demo)"
echo "=========================================================="
echo

echo "📊 STEP 1: Current Account Information"
echo "--------------------------------------"
echo "Command: az account show"
echo "This shows which account you're logged in with:"
az account show --output table
echo
az account show --query '{subscriptionId:id, tenantId:tenantId, user:user.name, subscriptionName:name}' --output table
echo

echo "📋 STEP 2: All Available Subscriptions"
echo "---------------------------------------"
echo "Command: az account list"
echo "This shows all subscriptions you have access to:"
az account list --query '[].{Name:name, SubscriptionId:id, TenantId:tenantId, State:state}' --output table
echo

echo "🎯 STEP 3: Looking for L.I.F.E. Platform Target Subscription"
echo "-------------------------------------------------------------"
echo "Target Subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca"
echo "Target Tenant ID: e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
echo "Target Account: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"
echo

# Check if target subscription exists
TARGET_SUB="5c88cef6-f243-497d-98af-6c6086d575ca"
echo "Checking for L.I.F.E. Platform subscription..."
az account list --query "[?id=='$TARGET_SUB'].{Found:'✅ L.I.F.E. Subscription Found', Name:name, State:state}" --output table

echo
echo "🏗️ STEP 4: Resource Groups in Current Subscription"
echo "--------------------------------------------------"
echo "Command: az group list"
az group list --query '[].{Name:name, Location:location, ProvisioningState:properties.provisioningState}' --output table
echo

echo "🔍 Looking for L.I.F.E. Platform resources..."
az group list --query "[?contains(name, 'life')].{Name:name, Location:location}" --output table
az group list --query "[?contains(name, 'platform')].{Name:name, Location:location}" --output table

echo
echo "🚀 STEP 5: Azure Functions and Web Apps"
echo "----------------------------------------"
echo "Command: az functionapp list"
az functionapp list --query '[].{Name:name, ResourceGroup:resourceGroup, Location:location, State:state}' --output table 2>/dev/null || echo "No Function Apps found in current subscription"
echo

echo "Command: az webapp list"
az webapp list --query '[].{Name:name, ResourceGroup:resourceGroup, Location:location, State:state}' --output table 2>/dev/null || echo "No Web Apps found in current subscription"

echo
echo "💾 STEP 6: Storage Accounts"
echo "----------------------------"
echo "Command: az storage account list"
az storage account list --query '[].{Name:name, ResourceGroup:resourceGroup, Location:location, Tier:sku.tier}' --output table 2>/dev/null || echo "No Storage Accounts found in current subscription"

echo
echo "🔐 STEP 7: Key Vaults"
echo "----------------------"
echo "Command: az keyvault list"
az keyvault list --query '[].{Name:name, ResourceGroup:resourceGroup, Location:location}' --output table 2>/dev/null || echo "No Key Vaults found in current subscription"

echo
echo "🎯 STEP 8: L.I.F.E. Platform Specific Resources"
echo "-----------------------------------------------"
echo "Looking for specific L.I.F.E. Platform resources..."

# Look for L.I.F.E. specific resources
az resource list --query "[?contains(name, 'life')].{Name:name, Type:type, ResourceGroup:resourceGroup, Location:location}" --output table 2>/dev/null || echo "No 'life' named resources found"

az resource list --query "[?contains(name, 'platform')].{Name:name, Type:type, ResourceGroup:resourceGroup, Location:location}" --output table 2>/dev/null || echo "No 'platform' named resources found"

echo
echo "📍 STEP 9: Check East US 2 Resources (L.I.F.E. Platform Location)"
echo "------------------------------------------------------------------"
az resource list --query "[?location=='eastus2'].{Name:name, Type:type, ResourceGroup:resourceGroup}" --output table 2>/dev/null || echo "No resources found in East US 2"

echo
echo "🔍 STEP 10: Account Assessment Summary"
echo "======================================="

# Get current subscription info
CURRENT_SUB=$(az account show --query 'id' -o tsv)
CURRENT_USER=$(az account show --query 'user.name' -o tsv)
CURRENT_TENANT=$(az account show --query 'tenantId' -o tsv)

echo "Current Account: $CURRENT_USER"
echo "Current Subscription: $CURRENT_SUB"
echo "Current Tenant: $CURRENT_TENANT"
echo
echo "L.I.F.E. Platform Targets:"
echo "Target Account: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"
echo "Target Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca"
echo "Target Tenant: e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
echo

if [ "$CURRENT_SUB" = "5c88cef6-f243-497d-98af-6c6086d575ca" ]; then
    echo "✅ SUCCESS: You are in the CORRECT L.I.F.E. Platform subscription!"
    echo "🎉 This account has access to your October 15 demo resources!"
else
    echo "⚠️  ATTENTION: This is NOT the target L.I.F.E. Platform subscription"
    echo "💡 But we can still work with this account or switch subscriptions"
fi

echo
echo "🎯 NEXT STEPS:"
echo "1. Review the resources found above"
echo "2. Determine if this account can access L.I.F.E. Platform"
echo "3. Switch subscription if needed: az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca"
echo "4. Prepare for October 15 demo with available resources"
echo
echo "📊 Diagnostic complete! Share these results for next steps."