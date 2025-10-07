@description('L.I.F.E. Platform Repository Backup Infrastructure')
@description('Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb')
// Parameters
@description('Environment name')
param environmentName string = 'prod'

@description('Location for resources')
param location string = resourceGroup().location

@description('Admin email for notifications')
param adminEmail string = 'sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com'

@description('Storage account name for backups')
param storageAccountName string = 'stlifeplatformprod'

// Variables
var resourcePrefix = 'life-backup'
var tags = {
  project: 'L.I.F.E. Platform'
  environment: environmentName
  purpose: 'Repository Backup'
  'marketplace-offer-id': '9a600d96-fe1e-420b-902a-a0c42c561adb'
  admin: adminEmail
}

// Storage Account for repository backups
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: 'Standard_ZRS' // Zone-redundant storage for high availability
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    networkAcls: {
      defaultAction: 'Allow' // Restrict as needed
      bypass: 'AzureServices'
    }
  }
}

// Blob containers for organized backup storage
resource backupContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/life-repository-backup'
  properties: {
    publicAccess: 'None'
    metadata: {
      purpose: 'Main repository backups'
      'retention-days': '365'
    }
  }
}

resource versioningContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/life-repository-versions'
  properties: {
    publicAccess: 'None'
    metadata: {
      purpose: 'Individual file versions'
      'retention-days': '90'
    }
  }
}

resource metadataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/life-metadata'
  properties: {
    publicAccess: 'None'
    metadata: {
      purpose: 'Backup metadata and logs'
      'retention-days': '30'
    }
  }
}

// Key Vault for storing backup credentials and secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: 'kv-${resourcePrefix}-${environmentName}'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    accessPolicies: []
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 30
    enablePurgeProtection: true
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Function App for automated backup scheduling
resource hostingPlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${resourcePrefix}-plan-${environmentName}'
  location: location
  tags: tags
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true // Linux
  }
}

resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: '${resourcePrefix}-functions-${environmentName}'
  location: location
  tags: tags
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: hostingPlan.id
    reserved: true
    siteConfig: {
      pythonVersion: '3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: '${resourcePrefix}-functions-${environmentName}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'STORAGE_ACCOUNT_NAME'
          value: storageAccount.name
        }
        {
          name: 'BACKUP_CONTAINER'
          value: 'life-repository-backup'
        }
        {
          name: 'ADMIN_EMAIL'
          value: adminEmail
        }
        {
          name: 'MARKETPLACE_OFFER_ID'
          value: '9a600d96-fe1e-420b-902a-a0c42c561adb'
        }
      ]
    }
    httpsOnly: true
  }
}

// RBAC assignments for Function App to access storage
resource storageContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, functionApp.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    ) // Storage Blob Data Contributor
    principalId: functionApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-insights-${environmentName}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Redfield'
    Request_Source: 'AppServiceEnablementCreate'
  }
}

// Logic App for backup scheduling and notifications
resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: '${resourcePrefix}-scheduler-${environmentName}'
  location: location
  tags: tags
  properties: {
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      contentVersion: '1.0.0.0'
      parameters: {}
      triggers: {
        recurrence: {
          type: 'Recurrence'
          recurrence: {
            frequency: 'Day'
            interval: 1
            startTime: '2025-09-27T02:00:00Z'
          }
        }
      }
      actions: {
        'HTTP-Trigger-Backup': {
          type: 'Http'
          inputs: {
            method: 'POST'
            uri: 'https://${functionApp.properties.defaultHostName}/api/trigger-backup'
            headers: {
              'Content-Type': 'application/json'
            }
            body: {
              admin_email: adminEmail
              storage_account: storageAccount.name
              timestamp: '@{utcNow()}'
            }
          }
        }
      }
    }
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output keyVaultName string = keyVault.name
output functionAppName string = functionApp.name
output backupContainerUrl string = 'https://${storageAccount.name}.blob.core.windows.net/life-repository-backup'
output versioningContainerUrl string = 'https://${storageAccount.name}.blob.core.windows.net/life-repository-versions'
output accessInstructions object = {
  azurePortal: 'https://portal.azure.com'
  storageExplorer: 'https://azure.microsoft.com/features/storage-explorer'
  directAccess: 'https://${storageAccount.name}.blob.core.windows.net'
  subscription: '5c88cef6-f243-497d-98af-6c6086d575ca'
  resourceGroup: resourceGroup().name
}
