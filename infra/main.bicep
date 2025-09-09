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
