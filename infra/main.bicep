targetScope = 'resourceGroup'

// Parameters
@description('Application name prefix')
param appName string = 'life-platform'

@description('Environment name (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'prod'

@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Resource token for unique naming')
param resourceToken string = uniqueString(resourceGroup().id)

@description('Azure Marketplace Offer ID')
param marketplaceOfferId string = '9a600d96-fe1e-420b-902a-a0c42c561adb'

@description('Pricing tier for App Service')
@allowed(['B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'P1v2', 'P2v2', 'P3v2'])
param appServicePlanSku string = 'B2'

@description('Enable Application Insights')
param enableApplicationInsights bool = true

@description('Enable Container Apps')
param enableContainerApps bool = true

@description('Enable Azure Functions')
param enableFunctions bool = true

@description('Enable Event Hub for EEG streaming')
param enableEventHub bool = true

@description('Enable Azure Quantum')
param enableQuantum bool = true

@description('Enable Azure Machine Learning')
param enableML bool = true

@description('Enable Cosmos DB')
param enableCosmosDB bool = true

@description('Enable Key Vault')
param enableKeyVault bool = true

// Variables
var resourceBaseName = '${appName}-${environment}-${resourceToken}'
var tags = {
  'azd-env-name': environment
  'life-platform': 'neural-processing'
  'marketplace-offer': marketplaceOfferId
  'cost-center': 'life-platform'
  'architecture-layer': 'quantum-neuroadaptive'
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
          value: enableApplicationInsights ? 'placeholder-connection-string' : ''
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

// App Service Plan for Functions (Premium Plan for Layer 2)
resource functionAppServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = if (enableFunctions) {
  name: '${resourceBaseName}-functions-plan'
  location: location
  tags: tags
  sku: {
    name: 'EP3'
    tier: 'PremiumV3'
    size: 'EP3'
    capacity: 2
  }
  kind: 'functionapp'
  properties: {
    maximumElasticWorkerCount: 100
    reserved: true
  }
}

// Azure Functions (Layer 2: Preprocessing)
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
    serverFarmId: functionAppServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      functionAppScaleLimit: 100
      minimumElasticInstanceCount: 2
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'UseDevelopmentStorage=true'
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
          value: enableApplicationInsights ? 'placeholder-connection-string' : ''
        }
        {
          name: 'AZURE_MARKETPLACE_OFFER_ID'
          value: marketplaceOfferId
        }
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'FUNCTIONS_WORKER_PROCESS_COUNT'
          value: '1'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME_VERSION'
          value: '3.11'
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

// Event Hub Namespace and Hub (Layer 1: Data Ingestion)
resource eventHubNamespace 'Microsoft.EventHub/namespaces@2022-10-01-preview' = if (enableEventHub) {
  name: '${resourceBaseName}-events'
  location: location
  sku: {
    name: 'Premium'
    tier: 'Premium'
    capacity: 1
  }
  tags: tags
  properties: {
    isAutoInflateEnabled: true
    maximumThroughputUnits: 20
    kafkaEnabled: true
    zoneRedundant: true
  }
}

resource eventHub 'Microsoft.EventHub/namespaces/eventhubs@2022-10-01-preview' = if (enableEventHub) {
  parent: eventHubNamespace
  name: 'eeg-stream'
  properties: {
    messageRetentionInDays: 7
    partitionCount: 32
    status: 'Active'
    captureDescription: {
      enabled: true
      encoding: 'Avro'
      intervalInSeconds: 300
      sizeLimitInBytes: 314572800
      destination: {
        name: 'EventHubArchive.AzureBlockBlob'
        properties: {
          storageAccountResourceId: storageAccount.id
          blobContainer: 'eeg-archive'
        }
      }
    }
  }
}

// Azure Quantum Workspace (Layer 3: Quantum Processing)
resource quantumWorkspace 'Microsoft.Quantum/Workspaces@2023-11-13-preview' = if (enableQuantum) {
  name: '${resourceBaseName}-quantum'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    providers: [
      {
        providerId: 'microsoft'
        providerSku: 'QDK'
      }
      {
        providerId: 'd-wave'
        providerSku: 'Advantage_system4.1'
      }
    ]
    storageAccount: storageAccount.id
  }
}

// Azure Machine Learning Workspace (Layer 4: ML Processing)
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2023-10-01' = if (enableML) {
  name: '${resourceBaseName}-ml'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'L.I.F.E. Neural Processing ML'
    description: 'Machine Learning workspace for neuroadaptive learning algorithms'
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    applicationInsights: enableApplicationInsights ? applicationInsights.id : ''
    hbiWorkspace: false
    publicNetworkAccess: 'Enabled'
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
}

// Cosmos DB Account (Layer 5: Data Storage)
resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = if (enableCosmosDB) {
  name: '${resourceBaseName}-cosmos'
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
      maxStalenessPrefix: 100
      maxIntervalInSeconds: 5
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: true
      }
      {
        locationName: 'East US 2'
        failoverPriority: 1
        isZoneRedundant: true
      }
      {
        locationName: 'West Europe'
        failoverPriority: 2
        isZoneRedundant: true
      }
    ]
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: true
    enableMultipleWriteLocations: true
    publicNetworkAccess: 'Enabled'
    networkAclBypass: 'AzureServices'
    disableKeyBasedMetadataWriteAccess: false
    enableFreeTier: false
    enableAnalyticalStorage: true
    backupPolicy: {
      type: 'Continuous'
    }
  }
}

// Key Vault (Layer 6: Security)
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = if (enableKeyVault) {
  name: '${resourceBaseName}-vault'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'premium'
    }
    tenantId: subscription().tenantId
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: userAssignedIdentity.properties.principalId
        permissions: {
          keys: ['Get', 'List', 'Update', 'Create', 'Import', 'Delete', 'Recover', 'Backup', 'Restore']
          secrets: ['Get', 'List', 'Set', 'Delete', 'Recover', 'Backup', 'Restore']
          certificates: ['Get', 'List', 'Update', 'Create', 'Import', 'Delete', 'Recover', 'Backup', 'Restore']
        }
      }
    ]
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
    enableRbacAuthorization: false
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
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
output functionAppUrl string = enableFunctions ? 'https://placeholder-functions-url' : ''

@description('The name of the Container App')
output containerAppName string = enableContainerApps ? containerApp.name : ''

@description('The URL of the Container App')
output containerAppUrl string = enableContainerApps ? 'https://placeholder-url' : ''

@description('Application Insights Connection String')
output applicationInsightsConnectionString string = enableApplicationInsights ? 'placeholder-connection-string' : ''

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

@description('Event Hub Namespace Name')
output eventHubNamespaceName string = enableEventHub ? eventHubNamespace.name : ''

@description('Event Hub Name')
output eventHubName string = enableEventHub ? eventHub.name : ''

@description('Quantum Workspace Name')
output quantumWorkspaceName string = enableQuantum ? quantumWorkspace.name : ''

@description('ML Workspace Name')
output mlWorkspaceName string = enableML ? mlWorkspace.name : ''

@description('Cosmos DB Account Name')
output cosmosDBAccountName string = enableCosmosDB ? cosmosDBAccount.name : ''

@description('Key Vault Name')
output keyVaultName string = enableKeyVault ? keyVault.name : ''
