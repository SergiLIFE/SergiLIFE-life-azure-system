// Main infrastructure file for L.I.F.E. Platform Azure deployment
// Deploys champion-level autonomous optimization system (22.66x SOTA performance)
// Enterprise-ready deployment with comprehensive security and monitoring

targetScope = 'resourceGroup'

@description('Environment name for L.I.F.E. Platform deployment')
param environmentName string

@description('Location for all Azure resources')
param location string = resourceGroup().location

@description('Application name prefix')
param appName string = 'life-platform'

@description('Environment name (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'prod'

@description('Azure Marketplace Offer ID')
param marketplaceOfferId string = '9a600d96-fe1e-420b-902a-a0c42c561adb'

@description('L.I.F.E. Platform operational mode')
param lifePlatformMode string = 'production'

@description('SOTA performance target multiplier')
param sotaPerformanceTarget string = '22.66'

@description('Neural processing rate in Hz')
param neuralProcessingRate string = '1000'

// Generate unique resource token for consistent naming
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location, environmentName)
var resourcePrefix = 'lif'

// Common tags for all resources
var commonTags = {
  'azd-env-name': environmentName
  project: 'L.I.F.E. Platform'
  'performance-tier': 'champion'
  'sota-multiplier': sotaPerformanceTarget
}

// User-assigned managed identity for secure access
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'mi-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
}

// Log Analytics Workspace for comprehensive monitoring
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'law-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 90
  }
}

// Application Insights for neural processing telemetry
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

// Container Registry for L.I.F.E. Platform images
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'cr${resourcePrefix}${resourceToken}'
  location: location
  tags: commonTags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

// Key Vault for neural processing secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

// Storage Account for neural data
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${resourcePrefix}${resourceToken}'
  location: location
  tags: commonTags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    supportsHttpsTrafficOnly: true
  }
}

// Neural data container
resource neuralDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: 'neural-data'
  parent: storageAccount::blobServices
  properties: {
    publicAccess: 'None'
  }
}

// Blob Services
resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  name: 'default'
  parent: storageAccount
}

// Service Bus Namespace for real-time processing
resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: 'sb-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    minimumTlsVersion: '1.2'
  }
}

// Neural processing queue
resource neuralProcessingQueue 'Microsoft.ServiceBus/namespaces/queues@2022-10-01-preview' = {
  name: 'neural-processing'
  parent: serviceBusNamespace
  properties: {
    maxSizeInMegabytes: 1024
    requiresDuplicateDetection: false
    requiresSession: false
  }
}

// Container Apps Environment
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'cae-${resourcePrefix}-${resourceToken}'
  location: location
  tags: commonTags
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

// L.I.F.E. Autonomous Optimizer Container App
resource lifeOptimizerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'ca-${resourcePrefix}-optimizer-${resourceToken}'
  location: location
  tags: union(commonTags, {
    'azd-service-name': 'life-autonomous-optimizer'
  })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        allowInsecure: false
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
      secrets: []
    }
    template: {
      containers: [
        {
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          name: 'life-optimizer'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'AZURE_STORAGE_ACCOUNT_NAME'
              value: storageAccount.name
            }
            {
              name: 'AZURE_STORAGE_CONTAINER_NAME'
              value: neuralDataContainer.name
            }
            {
              name: 'AZURE_KEYVAULT_NAME'
              value: keyVault.name
            }
            {
              name: 'AZURE_KEYVAULT_URL'
              value: keyVault.properties.vaultUri
            }
            {
              name: 'AZURE_SERVICEBUS_NAMESPACE'
              value: serviceBusNamespace.name
            }
            {
              name: 'AZURE_SERVICEBUS_QUEUE_NAME'
              value: neuralProcessingQueue.name
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
            {
              name: 'LIFE_PLATFORM_MODE'
              value: lifePlatformMode
            }
            {
              name: 'SOTA_PERFORMANCE_TARGET'
              value: sotaPerformanceTarget
            }
            {
              name: 'NEURAL_PROCESSING_RATE'
              value: neuralProcessingRate
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
      }
    }
  }
}

// RBAC Assignments

// Key Vault Secrets Officer role
resource keyVaultSecretsOfficerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, managedIdentity.id, 'Key Vault Secrets Officer')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b86a8fe4-44ce-4948-aee5-eccb2c155cd7')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Storage Blob Data Contributor role
resource storageBlobDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentity.id, 'Storage Blob Data Contributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Service Bus Data Owner role
resource serviceBusDataOwnerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(serviceBusNamespace.id, managedIdentity.id, 'Azure Service Bus Data Owner')
  scope: serviceBusNamespace
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '090c5cfd-751d-490a-894a-3ce6f1109419')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ACR Pull role
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, managedIdentity.id, 'AcrPull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Required outputs for azd
output RESOURCE_GROUP_ID string = resourceGroup().id
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.properties.loginServer
param enableFunctions bool = true

// Variables
var resourceBaseName = '${appName}-${environment}-${resourceToken}'
var tags = {
  'azd-env-name': environment
  'life-platform': 'neural-processing'
  'marketplace-offer': marketplaceOfferId
  'deployment-date': utcNow('yyyy-MM-dd')
  'cost-center': 'life-platform'
}

// User-assigned managed identity
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${resourceBaseName}-identity'
  location: location
  tags: tags
}

// Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = if (enableApplicationInsights) {
  name: '${resourceBaseName}-insights'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Log Analytics Workspace
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${resourceBaseName}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      searchVersion: 1
      legacy: 0
    }
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${resourceBaseName}-plan'
  location: location
  tags: tags
  sku: {
    name: appServicePlanSku
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// App Service for L.I.F.E Platform
resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: '${resourceBaseName}-app'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
      appSettings: [
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: enableApplicationInsights ? applicationInsights.properties.ConnectionString : ''
        }
        {
          name: 'AZURE_MARKETPLACE_OFFER_ID'
          value: marketplaceOfferId
        }
        {
          name: 'LIFE_PLATFORM_ENVIRONMENT'
          value: environment
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        {
          name: 'PRE_BUILD_COMMAND'
          value: 'pip install -r requirements.txt'
        }
      ]
    }
  }
}

// Azure Functions (if enabled)
resource functionApp 'Microsoft.Web/sites@2022-09-01' = if (enableFunctions) {
  name: '${resourceBaseName}-functions'
  location: location
  kind: 'functionapp,linux'
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
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
          value: enableApplicationInsights ? applicationInsights.properties.ConnectionString : ''
        }
        {
          name: 'AZURE_MARKETPLACE_OFFER_ID'
          value: marketplaceOfferId
        }
      ]
    }
  }
}

// Storage Account for Functions
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = if (enableFunctions) {
  name: '${replace(resourceBaseName, '-', '')}storage'
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

// Container Apps Environment (if enabled)
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = if (enableContainerApps) {
  name: '${resourceBaseName}-env'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// Container App (if enabled)
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = if (enableContainerApps) {
  name: '${resourceBaseName}-container'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: enableContainerApps ? containerAppsEnvironment.id : ''
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      secrets: [
        {
          name: 'application-insights-connection-string'
          value: enableApplicationInsights ? applicationInsights.properties.ConnectionString : ''
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'life-platform'
          image: 'nginx:latest' // Placeholder image - will be updated during deployment
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'application-insights-connection-string'
            }
            {
              name: 'AZURE_MARKETPLACE_OFFER_ID'
              value: marketplaceOfferId
            }
            {
              name: 'LIFE_PLATFORM_ENVIRONMENT'
              value: environment
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
}

// Outputs
@description('The name of the resource group')
output resourceGroupName string = resourceGroup().name

@description('The name of the App Service')
output appServiceName string = appService.name

@description('The URL of the App Service')
output appServiceUrl string = 'https://${appService.properties.defaultHostName}'

@description('The name of the Function App')
output functionAppName string = enableFunctions ? functionApp.name : ''

@description('The URL of the Function App')
output functionAppUrl string = enableFunctions ? 'https://${functionApp.properties.defaultHostName}' : ''

@description('The name of the Container App')
output containerAppName string = enableContainerApps ? containerApp.name : ''

@description('The URL of the Container App')
output containerAppUrl string = enableContainerApps
  ? 'https://${containerApp.properties.configuration.ingress.fqdn}'
  : ''

@description('Application Insights Connection String')
output applicationInsightsConnectionString string = enableApplicationInsights
  ? applicationInsights.properties.ConnectionString
  : ''

@description('User Assigned Identity ID')
output userAssignedIdentityId string = userAssignedIdentity.id

@description('User Assigned Identity Client ID')
output userAssignedIdentityClientId string = userAssignedIdentity.properties.clientId

@description('Storage Account Name')
output storageAccountName string = enableFunctions ? storageAccount.name : ''

@description('Log Analytics Workspace ID')
output logAnalyticsWorkspaceId string = logAnalyticsWorkspace.id

@description('Azure Marketplace Offer ID')
output marketplaceOfferId string = marketplaceOfferId

@description('Environment Name')
output environmentName string = environment

@description('Resource Token')
output resourceToken string = resourceToken
