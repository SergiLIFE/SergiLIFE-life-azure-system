@description('L.I.F.E Platform Section 7 - Ultimate Full-Cycle Deployment')
param environment string = 'prod'
param location string = resourceGroup().location
param uniqueSuffix string = uniqueString(resourceGroup().id)

// Section 7 Configuration
param enableAutomatedRetraining bool = true
param enableGDPRCompliance bool = true
param enableRealTimeAdaptation bool = true
param enableQuantumOptimization bool = true

// Advanced Configuration
param neuralProcessingRate int = 60
param realtimeLatencyTargetMs int = 50
param automatedRetrainingThreshold string = '0.85'
param gdprRetentionDays int = 365

var appName = 'life-section7-${environment}'
var storageAccountName = 'stlifesection7${uniqueSuffix}'
var keyVaultName = 'kv-life-section7-${uniqueSuffix}'
var cosmosAccountName = 'cosmos-life-section7-${uniqueSuffix}'
var eventHubNamespace = 'eh-life-section7-${uniqueSuffix}'
var mlWorkspaceName = 'ml-life-section7-${uniqueSuffix}'
var quantumWorkspaceName = 'quantum-life-section7-${uniqueSuffix}'
var containerAppsEnvironmentName = 'cae-life-section7-${uniqueSuffix}'
var containerRegistryName = 'acrlifesection7${uniqueSuffix}'
var functionAppName = 'func-life-section7-${uniqueSuffix}'

// Container Apps Environment
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerAppsEnvironmentName
  location: location
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

// Storage Account for Section 7
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_ZRS'
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
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
  }
}

// Key Vault for Section 7 Secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    enableRbacAuthorization: true
    enabledForDeployment: false
    enabledForTemplateDeployment: false
    enabledForDiskEncryption: false
    enableSoftDelete: true
    enablePurgeProtection: true
    softDeleteRetentionInDays: 90
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Cosmos DB for GDPR Compliance Records
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = if (enableGDPRCompliance) {
  name: cosmosAccountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
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
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 720
        backupStorageRedundancy: 'Zone'
      }
    }
    isVirtualNetworkFilterEnabled: false
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    disableKeyBasedMetadataWriteAccess: true
  }
}

// Cosmos Database for GDPR
resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-04-15' = if (enableGDPRCompliance) {
  parent: cosmosAccount
  name: 'gdpr_compliance'
  properties: {
    resource: {
      id: 'gdpr_compliance'
    }
  }
}

// Cosmos Container for Compliance Records
resource cosmosContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-04-15' = if (enableGDPRCompliance) {
  parent: cosmosDatabase
  name: 'compliance_records'
  properties: {
    resource: {
      id: 'compliance_records'
      partitionKey: {
        paths: ['/user_id']
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        includedPaths: [
          {
            path: '/*'
          }
        ]
      }
    }
  }
}

// Event Hub Namespace for Real-time Processing
resource eventHubNamespaceResource 'Microsoft.EventHub/namespaces@2023-01-01-preview' = if (enableRealTimeAdaptation) {
  name: eventHubNamespace
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
    capacity: 10
  }
  properties: {
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
    zoneRedundant: true
    isAutoInflateEnabled: true
    maximumThroughputUnits: 20
  }
}

// Event Hub for Neural Data
resource eventHub 'Microsoft.EventHub/namespaces/eventhubs@2023-01-01-preview' = if (enableRealTimeAdaptation) {
  parent: eventHubNamespaceResource
  name: 'neural-data-stream'
  properties: {
    messageRetentionInDays: 1
    partitionCount: 4
    captureDescription: {
      enabled: true
      destination: {
        name: 'EventHubArchive.AzureBlockBlob'
        properties: {
          storageAccountResourceId: storageAccount.id
          blobContainer: 'neural-data-archive'
          archiveNameFormat: '{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}'
        }
      }
      intervalInSeconds: 300
      sizeLimitInBytes: 314572800
    }
  }
}

// Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
    dataEndpointEnabled: false
    encryption: {
      status: 'disabled'
    }
    networkRuleBypassOptions: 'AzureServices'
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: 'disabled'
      }
      retentionPolicy: {
        days: 30
        status: 'enabled'
      }
    }
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
  }
}

// Log Analytics Workspace
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-life-section7-${uniqueSuffix}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: 1
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-life-section7-${uniqueSuffix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Machine Learning Workspace
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2023-10-01' = if (enableAutomatedRetraining) {
  name: mlWorkspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'L.I.F.E Section 7 ML Workspace'
    description: 'Machine Learning workspace for automated retraining and optimization'
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    applicationInsights: applicationInsights.id
    publicNetworkAccess: 'Enabled'
    imageBuildCompute: 'cpu-cluster'
    allowPublicAccessWhenBehindVnet: false
    discoveryUrl: 'https://${location}.api.azureml.ms/discovery'
  }
}

// App Service Plan for Functions
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-life-section7-${uniqueSuffix}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
    size: 'Y1'
    family: 'Y'
    capacity: 0
  }
  properties: {
    computeMode: 'Dynamic'
    reserved: false
  }
}

// Function App for Section 7 APIs
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
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
          value: applicationInsights.properties.ConnectionString
        }
        {
          name: 'SECTION7_KEYVAULT_URL'
          value: keyVault.properties.vaultUri
        }
        {
          name: 'SECTION7_COSMOS_ENDPOINT'
          value: enableGDPRCompliance ? cosmosAccount.properties.documentEndpoint : ''
        }
        {
          name: 'SECTION7_EVENTHUB_NAMESPACE'
          value: enableRealTimeAdaptation ? eventHubNamespaceResource.name : ''
        }
        {
          name: 'SECTION7_ML_WORKSPACE_NAME'
          value: enableAutomatedRetraining ? mlWorkspace.name : ''
        }
        {
          name: 'SECTION7_NEURAL_PROCESSING_RATE'
          value: string(neuralProcessingRate)
        }
        {
          name: 'SECTION7_REALTIME_LATENCY_TARGET_MS'
          value: string(realtimeLatencyTargetMs)
        }
        {
          name: 'SECTION7_AUTOMATED_RETRAINING_THRESHOLD'
          value: automatedRetrainingThreshold
        }
        {
          name: 'SECTION7_GDPR_RETENTION_DAYS'
          value: string(gdprRetentionDays)
        }
        {
          name: 'SECTION7_ENABLE_AUTOMATED_RETRAINING'
          value: string(enableAutomatedRetraining)
        }
        {
          name: 'SECTION7_ENABLE_GDPR_COMPLIANCE'
          value: string(enableGDPRCompliance)
        }
        {
          name: 'SECTION7_ENABLE_REALTIME_ADAPTATION'
          value: string(enableRealTimeAdaptation)
        }
        {
          name: 'SECTION7_ENABLE_QUANTUM_OPTIMIZATION'
          value: string(enableQuantumOptimization)
        }
      ]
      pythonVersion: '3.11'
      cors: {
        allowedOrigins: ['https://portal.azure.com', 'https://section7.lifeplatform.ai']
        supportCredentials: false
      }
      use32BitWorkerProcess: false
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
    }
  }
}

// Container App for L.I.F.E Section 7 Platform
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${appName}-app'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
        corsPolicy: {
          allowedOrigins: ['https://section7.lifeplatform.ai', 'https://portal.azure.com']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: containerApp.identity.principalId
        }
      ]
      secrets: [
        {
          name: 'cosmos-connection-string'
          value: enableGDPRCompliance ? cosmosAccount.listConnectionStrings().connectionStrings[0].connectionString : ''
        }
        {
          name: 'eventhub-connection-string'
          value: enableRealTimeAdaptation ? eventHubNamespaceResource.listKeys().keys[0].primaryConnectionString : ''
        }
        {
          name: 'storage-connection-string'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'life-section7-app'
          image: '${containerRegistry.properties.loginServer}/life-section7:latest'
          env: [
            {
              name: 'SECTION7_KEYVAULT_URL'
              value: keyVault.properties.vaultUri
            }
            {
              name: 'SECTION7_COSMOS_ENDPOINT'
              value: enableGDPRCompliance ? cosmosAccount.properties.documentEndpoint : ''
            }
            {
              name: 'SECTION7_COSMOS_CONNECTION_STRING'
              secretRef: 'cosmos-connection-string'
            }
            {
              name: 'SECTION7_EVENTHUB_CONNECTION_STRING'
              secretRef: 'eventhub-connection-string'
            }
            {
              name: 'SECTION7_STORAGE_CONNECTION_STRING'
              secretRef: 'storage-connection-string'
            }
            {
              name: 'SECTION7_ML_WORKSPACE_NAME'
              value: enableAutomatedRetraining ? mlWorkspace.name : ''
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
            {
              name: 'SECTION7_NEURAL_PROCESSING_RATE'
              value: string(neuralProcessingRate)
            }
            {
              name: 'SECTION7_REALTIME_LATENCY_TARGET_MS'
              value: string(realtimeLatencyTargetMs)
            }
            {
              name: 'SECTION7_AUTOMATED_RETRAINING_THRESHOLD'
              value: automatedRetrainingThreshold
            }
            {
              name: 'SECTION7_GDPR_RETENTION_DAYS'
              value: string(gdprRetentionDays)
            }
          ]
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: 8000
              }
              initialDelaySeconds: 30
              periodSeconds: 10
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/ready'
                port: 8000
              }
              initialDelaySeconds: 10
              periodSeconds: 5
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
          {
            name: 'cpu-scaling'
            custom: {
              type: 'cpu'
              metadata: {
                type: 'Utilization'
                value: '70'
              }
            }
          }
        ]
      }
    }
  }
}

// RBAC Assignments
resource keyVaultSecretsUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, functionApp.identity.principalId, 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: functionApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource containerAppKeyVaultAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, containerApp.identity.principalId, 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, containerApp.identity.principalId, 'AcrPull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource cosmosDataContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableGDPRCompliance) {
  name: guid(cosmosAccount.id, containerApp.identity.principalId, 'Cosmos DB Data Contributor')
  scope: cosmosAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '00000000-0000-0000-0000-000000000002')
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource eventHubDataSender 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableRealTimeAdaptation) {
  name: guid(eventHubNamespaceResource.id, containerApp.identity.principalId, 'Azure Event Hubs Data Sender')
  scope: eventHubNamespaceResource
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2b629674-e913-4c01-ae53-ef4638d8f975')
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource mlWorkspaceContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableAutomatedRetraining) {
  name: guid(mlWorkspace.id, containerApp.identity.principalId, 'Azure ML Workspace Contributor')
  scope: mlWorkspace
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'f6c7c914-8db3-469d-8ca1-694a8f32e121')
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output storageAccountName string = storageAccount.name
output keyVaultName string = keyVault.name
output cosmosAccountName string = enableGDPRCompliance ? cosmosAccount.name : ''
output eventHubNamespace string = enableRealTimeAdaptation ? eventHubNamespaceResource.name : ''
output mlWorkspaceName string = enableAutomatedRetraining ? mlWorkspace.name : ''
output containerRegistryName string = containerRegistry.name
output applicationInsightsName string = applicationInsights.name
output logAnalyticsWorkspaceName string = logAnalyticsWorkspace.name

// Section 7 Specific Outputs
output section7Configuration object = {
  neuralProcessingRate: neuralProcessingRate
  realtimeLatencyTargetMs: realtimeLatencyTargetMs
  automatedRetrainingThreshold: automatedRetrainingThreshold
  gdprRetentionDays: gdprRetentionDays
  enabledFeatures: {
    automatedRetraining: enableAutomatedRetraining
    gdprCompliance: enableGDPRCompliance
    realtimeAdaptation: enableRealTimeAdaptation
    quantumOptimization: enableQuantumOptimization
  }
}

output deploymentSummary object = {
  appName: appName
  environment: environment
  location: location
  containerAppUrl: 'https://${containerApp.properties.configuration.ingress.fqdn}'
  functionAppUrl: 'https://${functionApp.properties.defaultHostName}'
  section7Status: 'fully_deployed'
  featuresEnabled: {
    automatedRetraining: enableAutomatedRetraining
    gdprCompliance: enableGDPRCompliance
    realtimeAdaptation: enableRealTimeAdaptation
    quantumOptimization: enableQuantumOptimization
  }
}