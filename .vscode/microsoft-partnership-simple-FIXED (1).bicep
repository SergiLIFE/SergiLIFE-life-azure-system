// L.I.F.E. Platform - Simplified Azure Deployment
// Microsoft Partnership Integration - FIXED VERSION

param environmentName string = 'msftpartnership'
param location string = 'eastus2'
param lifeContainerImage string = 'nginx:latest'

// Simplified naming - avoid special characters and length issues
var uniqueSuffix = take(uniqueString(resourceGroup().id), 6)
var namePrefix = 'life${environmentName}'

// Resource names (keeping simple, alphanumeric only)
var storageAccountName = '${toLower(take(namePrefix, 18))}${uniqueSuffix}'
var logAnalyticsName = '${namePrefix}-logs-${uniqueSuffix}'
var appInsightsName = '${namePrefix}-ai-${uniqueSuffix}'
var containerAppEnvName = '${namePrefix}-env-${uniqueSuffix}'
var containerAppName = '${namePrefix}-app'
var cosmosDbName = '${namePrefix}-cosmos-${uniqueSuffix}'
var eventHubNamespaceName = '${namePrefix}-events-${uniqueSuffix}'
var keyVaultName = '${take(namePrefix, 18)}kv${uniqueSuffix}'
var managedIdentityName = '${namePrefix}-identity'

// ============================================================================
// STORAGE ACCOUNT (ZRS for geo-redundancy)
// ============================================================================
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'  // Sponsorship restriction: must use LRS
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

// Storage container for backups
resource backupContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/backup'
  properties: {
    publicAccess: 'None'
  }
}

// ============================================================================
// LOG ANALYTICS & APP INSIGHTS
// ============================================================================
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'  // Free tier
    }
    retentionInDays: 7  // Minimal retention for sponsorship
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// ============================================================================
// MANAGED IDENTITY
// ============================================================================
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: managedIdentityName
  location: location
}

// ============================================================================
// KEY VAULT (SIMPLE - no purge protection due to sponsorship limits)
// ============================================================================
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'  // Standard only - sponsorship limitation
    }
    tenantId: subscription().tenantId
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: managedIdentity.properties.principalId
        permissions: {
          secrets: ['get', 'list']
          keys: ['get', 'list']
          certificates: ['get', 'list']
        }
      }
    ]
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

// ============================================================================
// COSMOS DB (Serverless - most cost-effective for sponsorship)
// ============================================================================
resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: cosmosDbName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    databaseAccountOfferType: 'Standard'
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
}

// ============================================================================
// EVENT HUB (For EEG data streaming)
// ============================================================================
resource eventHubNamespace 'Microsoft.EventHub/namespaces@2022-10-01-preview' = {
  name: eventHubNamespaceName
  location: location
  sku: {
    name: 'Basic'  // Basic tier for sponsorship
    capacity: 1
  }
  properties: {
    isAutoInflateEnabled: false
  }
}

resource eventHub 'Microsoft.EventHub/namespaces/eventhubs@2022-10-01-preview' = {
  name: 'eeg-data'
  parent: eventHubNamespace
  properties: {
    partitionCount: 2
    messageRetentionInDays: 1
  }
}

// ============================================================================
// CONTAINER APPS ENVIRONMENT (for Container App)
// ============================================================================
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2023-04-01-preview' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ============================================================================
// CONTAINER APP (L.I.F.E. Platform)
// ============================================================================
resource containerApp 'Microsoft.App/containerApps@2023-04-01-preview' = {
  name: containerAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      secrets: []
      registries: []
    }
    template: {
      containers: [
        {
          image: lifeContainerImage
          name: 'life-platform'
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            {
              name: 'ASPNETCORE_ENVIRONMENT'
              value: environmentName
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 2
      }
    }
  }
}

// ============================================================================
// OUTPUTS
// ============================================================================
output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output storageAccountName string = storageAccount.name
output cosmosDbEndpoint string = cosmosDbAccount.properties.documentEndpoint
output keyVaultName string = keyVault.name
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output eventHubConnectionString string = 'Endpoint=sb://${eventHubNamespace.properties.serviceBusEndpoint};'
output managedIdentityId string = managedIdentity.id
output managedIdentityClientId string = managedIdentity.properties.clientId
