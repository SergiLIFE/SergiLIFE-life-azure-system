// Microsoft Partnership Demo - L.I.F.E. Platform Infrastructure (Simplified)
// Removes Functions (requires paid plan) - Uses Container Apps only

@description('Environment name (dev, staging, prod)')
param environmentName string = 'demo'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Unique identifier for resource naming')
param uniqueId string = uniqueString(resourceGroup().id)

@description('L.I.F.E. Platform container image')
param lifeContainerImage string = 'nginx:latest'

@description('Existing Container Apps Environment name (optional - if provided, will use existing instead of creating new)')
param existingContainerAppsEnvName string = ''

@description('Existing Container Apps Environment resource group (defaults to current)')
param existingContainerAppsEnvResourceGroup string = resourceGroup().name

@description('Existing Container Registry name (optional - if provided, will use existing instead of creating new)')
param existingContainerRegistryName string = ''

@description('Existing Container Registry resource group (required if using existing ACR)')
param existingContainerRegistryResourceGroup string = resourceGroup().name

var useExistingContainerAppsEnv = existingContainerAppsEnvName != ''
var useExistingContainerRegistry = existingContainerRegistryName != ''

// Simplified - no high availability (requires paid features)
var resourcePrefix = 'life${environmentName}'
var storagePrefix = 'life${take(environmentName, 4)}' // Shorter prefix for storage (max 8 chars)
var kvPrefix = 'kv${take(environmentName, 4)}' // Shorter prefix for Key Vault (max 8 chars)
var tags = {
  Environment: environmentName
  Project: 'L.I.F.E. Platform'
  Partnership: 'Microsoft Demo'
  Owner: 'SergiLIFE'
  CostCenter: 'L.I.F.E-Platform'
}

// Managed Identity for secure authentication
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${resourcePrefix}-identity'
  location: location
  tags: tags
}

// Key Vault for secrets management
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${kvPrefix}${uniqueId}' // Shorter naming: kv + 4 chars env + uniqueId = ~17 chars
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    // enablePurgeProtection: false  // REMOVED - cannot be set to false once enabled in subscription
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
    accessPolicies: [
      {
        tenantId: tenant().tenantId
        objectId: managedIdentity.properties.principalId
        permissions: {
          secrets: ['get', 'list']
          keys: ['get', 'list']
          certificates: ['get', 'list']
        }
      }
    ]
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-logs-${uniqueId}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: 10
    }
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-ai-${uniqueId}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Container Registry (create new when no existing provided)
resource newContainerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = if (!useExistingContainerRegistry) {
  name: '${resourcePrefix}acr${uniqueId}'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    anonymousPullEnabled: false
    networkRuleSet: {
      defaultAction: 'Allow'
    }
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
    }
  }
}

var containerRegistryId = useExistingContainerRegistry
  ? resourceId(
      existingContainerRegistryResourceGroup,
      'Microsoft.ContainerRegistry/registries',
      existingContainerRegistryName
    )
  : newContainerRegistry.id

var containerRegistryLoginServer = reference(containerRegistryId, '2023-11-01-preview').loginServer
var containerRegistryCredentials = listCredentials(containerRegistryId, '2023-11-01-preview')

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: '${storagePrefix}${uniqueId}' // Shorter naming: life + 4 chars env + uniqueId = ~17 chars
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    defaultToOAuthAuthentication: true
    allowCrossTenantReplication: false
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      requireInfrastructureEncryption: false
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
}

// Container Apps Environment (create new or use existing)
var containerAppsEnvironmentId = useExistingContainerAppsEnv
  ? resourceId(existingContainerAppsEnvResourceGroup, 'Microsoft.App/managedEnvironments', existingContainerAppsEnvName)
  : ''

resource newContainerAppsEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = if (existingContainerAppsEnvName == '') {
  name: '${resourcePrefix}-env-${uniqueId}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: false
  }
}

var resolvedContainerAppsEnvironmentId = useExistingContainerAppsEnv
  ? containerAppsEnvironmentId
  : newContainerAppsEnvironment.id

// Container App
resource lifeContainerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${resourcePrefix}-app'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: resolvedContainerAppsEnvironmentId
    configuration: {
      secrets: [
        {
          name: 'registry-password'
          value: containerRegistryCredentials.passwords[0].value
        }
      ]
      registries: [
        {
          server: containerRegistryLoginServer
          username: containerRegistryCredentials.username
          passwordSecretRef: 'registry-password'
        }
      ]
      ingress: {
        external: true
        targetPort: 80
        allowInsecure: false
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
      }
    }
    template: {
      containers: [
        {
          image: lifeContainerImage
          name: 'life-platform'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'ENVIRONMENT'
              value: environmentName
            }
            {
              name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
              value: appInsights.properties.InstrumentationKey
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: managedIdentity.properties.clientId
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

// Cosmos DB
resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: '${resourcePrefix}-cosmos-${uniqueId}'
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    enableFreeTier: false
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
}

// Event Hub
resource eventHubNamespace 'Microsoft.EventHub/namespaces@2024-01-01' = {
  name: '${resourcePrefix}-events-${uniqueId}'
  location: location
  tags: tags
  sku: {
    name: 'Standard'
    tier: 'Standard'
    capacity: 1
  }
  properties: {
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
    zoneRedundant: false
  }
}

resource eegDataEventHub 'Microsoft.EventHub/namespaces/eventhubs@2024-01-01' = {
  parent: eventHubNamespace
  name: 'eeg-data'
  properties: {
    messageRetentionInDays: 1
    partitionCount: 2
  }
}

// Role Assignments
// Note: ACR role assignment skipped - ACR is in different resource group (rg-life-marketplace-prod)
// Grant permission manually if needed: az role assignment create --assignee <principalId> --role AcrPull --scope <acrId>

resource storageBlobRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentity.id, 'blobcontributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output resourceGroupName string = resourceGroup().name
output containerAppUrl string = 'https://${lifeContainerApp.properties.configuration.ingress.fqdn}'
output containerRegistryName string = useExistingContainerRegistry
  ? existingContainerRegistryName
  : newContainerRegistry.name
output cosmosDbEndpoint string = cosmosDbAccount.properties.documentEndpoint
output storageAccountName string = storageAccount.name
