@description('L.I.F.E. Platform Backup Infrastructure - AZD Compliant - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb')
// Required AZD parameters
param environmentName string
param location string = resourceGroup().location

@description('Admin email for notifications')
param adminEmail string = 'sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com'

@description('Subscription ID for production deployment')
param subscriptionId string = '5c88cef6-f243-497d-98af-6c6086d575ca'

// Variables
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location, environmentName)
var resourcePrefix = 'life'
var tags = {
  project: 'L.I.F.E. Platform'
  environment: environmentName
  purpose: 'Repository Backup'
  'marketplace-offer-id': '9a600d96-fe1e-420b-902a-a0c42c561adb'
  admin: adminEmail
}

// User-Assigned Managed Identity (MANDATORY for AZD)
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${resourcePrefix}-${resourceToken}'
  location: location
  tags: tags
}

// Storage Account for repository backups
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${resourcePrefix}${resourceToken}'
  location: location
  tags: tags
  sku: {
    name: 'Standard_ZRS' // Zone-redundant storage for high availability
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false // Disable public access (AZD rule)
    allowSharedKeyAccess: false // Disable local auth (AZD rule)
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
      defaultAction: 'Allow'
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
  name: 'kv-${resourcePrefix}-${resourceToken}'
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

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-${resourcePrefix}-${resourceToken}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Redfield'
    Request_Source: 'AppServiceEnablementCreate'
  }
}

// Log Analytics Workspace for Application Insights
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-${resourcePrefix}-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Function App hosting plan
resource hostingPlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-${resourcePrefix}-${resourceToken}'
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

// Function App for automated backup scheduling
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'func-${resourcePrefix}-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'backup-function' // Required AZD tag
  })
  kind: 'functionapp,linux'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    serverFarmId: hostingPlan.id
    reserved: true
    siteConfig: {
      pythonVersion: '3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage__accountName'
          value: storageAccount.name
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: 'func-${resourcePrefix}-${resourceToken}'
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
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
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

// MANDATORY: Storage Blob Data Owner role assignment
resource storageBlobDataOwnerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, userAssignedIdentity.id, 'StorageBlobDataOwner')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'b7e6dc6d-f1e8-4753-8033-0f276bb0955b'
    ) // Storage Blob Data Owner
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// MANDATORY: Storage Blob Data Contributor role assignment
resource storageBlobDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, userAssignedIdentity.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    ) // Storage Blob Data Contributor
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// MANDATORY: Storage Queue Data Contributor role assignment
resource storageQueueDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, userAssignedIdentity.id, 'StorageQueueDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '974c5e8b-45b9-4653-ba55-5f855dd0fb88'
    ) // Storage Queue Data Contributor
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// MANDATORY: Storage Table Data Contributor role assignment
resource storageTableDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, userAssignedIdentity.id, 'StorageTableDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3'
    ) // Storage Table Data Contributor
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// MANDATORY: Monitoring Metrics Publisher role assignment
resource monitoringMetricsPublisherRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(functionApp.id, userAssignedIdentity.id, 'MonitoringMetricsPublisher')
  scope: functionApp
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '3913510d-42f4-4e42-8a64-420c390055eb'
    ) // Monitoring Metrics Publisher
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// MANDATORY: Diagnostic settings for Function App
resource functionAppDiagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-${functionApp.name}'
  scope: functionApp
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'FunctionAppLogs'
        enabled: true
        retentionPolicy: {
          enabled: true
          days: 30
        }
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          enabled: true
          days: 30
        }
      }
    ]
  }
}

// Logic App for backup scheduling and notifications
resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: 'logic-${resourcePrefix}-${resourceToken}'
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

// Required AZD output
output RESOURCE_GROUP_ID string = resourceGroup().id

// Additional outputs for reference
output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output keyVaultName string = keyVault.name
output functionAppName string = functionApp.name
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output userAssignedIdentityId string = userAssignedIdentity.id
output appInsightsName string = appInsights.name
output backupContainerUrl string = 'https://${storageAccount.name}.blob.${environment().suffixes.storage}/life-repository-backup'
output versioningContainerUrl string = 'https://${storageAccount.name}.blob.${environment().suffixes.storage}/life-repository-versions'
output accessInstructions object = {
  azurePortal: 'https://portal.azure.com'
  storageExplorer: 'https://azure.microsoft.com/features/storage-explorer'
  directAccess: 'https://${storageAccount.name}.blob.${environment().suffixes.storage}'
  subscription: subscription().subscriptionId
  resourceGroup: resourceGroup().name
}
