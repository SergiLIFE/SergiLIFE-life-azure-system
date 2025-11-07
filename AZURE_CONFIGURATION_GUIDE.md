# L.I.F.E Platform Azure Configuration and Authentication Guide

# Updated: November 7, 2025

# Copyright 2025 - Sergio Paya Benaully

## AZURE SUBSCRIPTION DETAILS

SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
TENANT_ID="e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
SUBSCRIPTION_NAME="Microsoft Azure Sponsorship"
DIRECTORY="Sergio Paya Borrull (lifecoach-121.com)"
ROLE="Account admin"
OFFER="Pay-As-You-Go"
OFFER_ID="MS-AZR-0003P"
CURRENCY="GBP"
STATUS="Active"
SECURE_SCORE="80%"
BILLING_PERIOD="11/1/2025-11/30/2025"

## AZURE CLI INSTALLATION COMMANDS

# Method 1: Windows Package Manager (Recommended)

winget install -e --id Microsoft.AzureCLI

# Method 2: PowerShell Script (Run as Administrator)

# $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri <https://aka.ms/installazurecliwindowsx64> -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; Remove-Item .\AzureCLI.msi

# Method 3: Direct Download

# Download from: <https://aka.ms/installazurecliwindowsx64>

## AZURE LOGIN COMMANDS

# Login to Azure

az login

# Login with specific tenant

az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac

# Login with device code (for restricted environments)

az login --use-device-code

# Set default subscription

az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

# Verify login

az account show

## AZURE RESOURCES FOR L.I.F.E PLATFORM

# Resource Group

RESOURCE_GROUP="life-platform-prod"
LOCATION="eastus2"

# Azure Functions

FUNCTION_APP_NAME="life-functions-app"
FUNCTION_PLAN="life-functions-plan"

# Azure ML Workspace

ML_WORKSPACE_NAME="life-ml-workspace"
ML_COMPUTE_CLUSTER="life-compute-cluster"

# Azure Storage

STORAGE_ACCOUNT="stlifeplatformprod"
CONTAINER_NAME="life-data"

# Azure Key Vault

KEY_VAULT_NAME="kv-life-platform-prod"
KEY_VAULT_URL="<https://kv-life-platform-prod.vault.azure.net/>"

# Azure IoT Hub

IOT_HUB_NAME="life-iot-hub"
IOT_DEVICE_ID="life-eeg-device-01"

# Azure Service Bus

SERVICE_BUS_NAMESPACE="sb-life-platform-prod"

## AZURE RESOURCE CREATION COMMANDS

# Create Resource Group

az group create --name life-platform-prod --location eastus2

# Create Storage Account

az storage account create --name stlifeplatformprod --resource-group life-platform-prod --location eastus2 --sku Standard_LRS

# Create Key Vault

az keyvault create --name kv-life-platform-prod --resource-group life-platform-prod --location eastus2

# Create Azure ML Workspace

az ml workspace create --workspace-name life-ml-workspace --resource-group life-platform-prod

# Create Function App

az functionapp create --name life-functions-app --resource-group life-platform-prod --consumption-plan-location eastus2 --runtime python --runtime-version 3.11 --functions-version 4 --storage-account stlifeplatformprod

# Create IoT Hub

az iot hub create --name life-iot-hub --resource-group life-platform-prod --location eastus2 --sku S1

## AZURE SECRETS MANAGEMENT

# Set secrets in Key Vault

az keyvault secret set --vault-name kv-life-platform-prod --name "EEG-API-KEY" --value "your-eeg-api-key-here"
az keyvault secret set --vault-name kv-life-platform-prod --name "IOT-HUB-CONNECTION-STRING" --value "your-iot-connection-string"
az keyvault secret set --vault-name kv-life-platform-prod --name "STORAGE-CONNECTION-STRING" --value "your-storage-connection"

## AZURE RBAC PERMISSIONS

# Assign contributor role to service principal

az role assignment create --assignee "your-service-principal-id" --role "Contributor" --scope "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca"

# Assign Key Vault access

az keyvault set-policy --name kv-life-platform-prod --object-id "your-object-id" --secret-permissions get list set delete

## AZURE MARKETPLACE INTEGRATION

MARKETPLACE_OFFER_ID="9a600d96-fe1e-420b-902a-a0c42c561adb"
PUBLISHER_ID="sergilifepublisher-1742216063"
OFFER_NAME="L.I.F.E Platform - Neuroadaptive Learning"

## MONITORING AND DIAGNOSTICS

# Enable Application Insights

az monitor app-insights component create --app life-platform-insights --location eastus2 --resource-group life-platform-prod

# Create Log Analytics Workspace

az monitor log-analytics workspace create --workspace-name life-platform-logs --resource-group life-platform-prod --location eastus2

## PRODUCTION DEPLOYMENT COMMANDS

# Deploy Azure Functions

func azure functionapp publish life-functions-app --python

# Deploy Azure ML Model

az ml model deploy --name life-stress-model --model life-neuroadaptive-model:1 --compute-target life-aks-cluster

# Update Function App Settings

az functionapp config appsettings set --name life-functions-app --resource-group life-platform-prod --settings "AZURE_CLIENT_ID=your-client-id" "AZURE_CLIENT_SECRET=your-client-secret" "AZURE_TENANT_ID=e716161a-5e85-4d6d-82f9-96bcdd2e65ac"

## GDPR COMPLIANCE SETTINGS

# Enable soft delete on Key Vault

az keyvault update --name kv-life-platform-prod --enable-soft-delete --enable-purge-protection

# Set data retention policies

az storage account blob-service-properties update --account-name stlifeplatformprod --enable-delete-retention --delete-retention-days 30

## COST OPTIMIZATION

# Set up budget alerts

az consumption budget create --amount 1000 --budget-name "L.I.F.E Platform Budget" --category cost --time-grain monthly --time-period start-date="2025-11-01" end-date="2026-10-31" --resource-group life-platform-prod

# Enable auto-shutdown for development VMs

az vm auto-shutdown --name life-dev-vm --resource-group life-platform-prod --time 1800

## BACKUP AND DISASTER RECOVERY

# Enable backup for storage account

az backup vault create --name life-backup-vault --resource-group life-platform-prod --location eastus2

# Create backup policy

az backup policy create --vault-name life-backup-vault --resource-group life-platform-prod --name "L.I.F.E-Daily-Backup" --backup-management-type AzureStorage --policy backup-policy.json

## SECURITY BEST PRACTICES

# Enable advanced threat protection

az storage account update --name stlifeplatformprod --resource-group life-platform-prod --enable-advanced-threat-protection

# Configure network access rules

az storage account network-rule add --account-name stlifeplatformprod --resource-group life-platform-prod --action Allow --ip-address "your-ip-address"

# Enable Azure Defender

az security auto-provisioning-setting update --name default --auto-provision on

## TROUBLESHOOTING COMMANDS

# Check resource health

az resource show --resource-group life-platform-prod --name life-functions-app --resource-type "Microsoft.Web/sites"

# View activity logs

az monitor activity-log list --resource-group life-platform-prod --start-time 2025-11-07T00:00:00Z

# Test connectivity

az network connectivity test --source-resource /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod/providers/Microsoft.Web/sites/life-functions-app

## ENVIRONMENT VARIABLES FOR LOCAL DEVELOPMENT

export AZURE_SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
export AZURE_TENANT_ID="e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
export AZURE_CLIENT_ID="your-service-principal-client-id"
export AZURE_CLIENT_SECRET="your-service-principal-secret"
export KEY_VAULT_URL="<https://kv-life-platform-prod.vault.azure.net/>"
export STORAGE_CONNECTION_STRING="your-storage-connection-string"
export IOT_HUB_CONNECTION_STRING="your-iot-hub-connection-string"

# Windows PowerShell equivalent

$env:AZURE_SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
$env:AZURE_TENANT_ID="e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
$env:KEY_VAULT_URL="<https://kv-life-platform-prod.vault.azure.net/>"
