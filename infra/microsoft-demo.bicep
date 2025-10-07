// microsoft-demo.bicep - L.I.F.E. Theory Platform Microsoft Partnership Demo Infrastructure
// Copyright 2025 - Sergio Paya Borrull
// Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

// Generate unique token for resource naming
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location, environmentName)

// Resource names (max 32 characters)
var containerRegistryName = 'acr${resourceToken}'
var containerAppName = 'ca${resourceToken}'
var functionAppName = 'func${resourceToken}'
var storageAccountName = 'st${resourceToken}'
// Key Vault removed for simplified demo deployment
var openAIServiceName = 'oai${resourceToken}'
var logAnalyticsName = 'log${resourceToken}'
var appInsightsName = 'ai${resourceToken}'
var managedIdentityName = 'id${resourceToken}'
var containerAppEnvironmentName = 'cae-${environmentName}'

// Create User-Assigned Managed Identity (required by AZD rules)
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: managedIdentityName
  location: location
}

// Create Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Create Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// Create Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

// MANDATORY: AcrPull role assignment for managed identity on container registry
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(containerRegistry.id, managedIdentity.id, '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '7f951dda-4ed3-4680-a7ca-43fe172d538d'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Create Storage Account for function app and demo data
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    defaultToOAuthAuthentication: true
  }
}

// MANDATORY: Storage role assignments for function app managed identity
resource storageBlobDataOwnerRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'b7e6dc6d-f1e8-4753-8033-0f276bb0955b'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageBlobDataContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageQueueDataContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, '974c5e8b-45b9-4653-ba55-5f855dd0fb88')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '974c5e8b-45b9-4653-ba55-5f855dd0fb88'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageTableDataContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource monitoringMetricsPublisherRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, '3913510d-42f4-4e42-8a64-420c390055eb')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '3913510d-42f4-4e42-8a64-420c390055eb'
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Create Azure OpenAI Service for GPT-4 integration
resource openAIService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAIServiceName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: openAIServiceName
    publicNetworkAccess: 'Enabled'
  }
}

// Create Container App Environment
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerAppEnvironmentName
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

// Create Container App for L.I.F.E. Demo Platform
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  tags: {
    'azd-service-name': 'web'
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'life-demo-app'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            {
              name: 'LIFE_THEORY_VERSION'
              value: '2025.1.0-PRODUCTION'
            }
            {
              name: 'AZURE_SUBSCRIPTION_ID'
              value: '5c88cef6-f243-497d-98af-6c6086d575ca'
            }
            {
              name: 'MICROSOFT_DEMO_MODE'
              value: 'true'
            }
            {
              name: 'PERFORMANCE_TARGET'
              value: '880x'
            }
            {
              name: 'MARKETPLACE_OFFER_ID'
              value: '9a600d96-fe1e-420b-902a-a0c42c561adb'
            }
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: openAIService.properties.endpoint
            }
            {
              name: 'AZURE_STORAGE_ACCOUNT_NAME'
              value: storageAccount.name
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
  dependsOn: [
    acrPullRoleAssignment
  ]
}

// Create Azure Function App for executive outreach automation
resource functionAppServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: 'plan-${functionAppName}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  tags: {
    'azd-service-name': 'api'
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    serverFarmId: functionAppServicePlan.id
    reserved: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage__accountName'
          value: storageAccount.name
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
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'MICROSOFT_EXECUTIVES_CONFIG'
          value: 'Satya Nadella,Scott Guthrie,Sam Altman,Kevin Scott'
        }
        {
          name: 'LINKEDIN_API_SETTINGS'
          value: 'enabled'
        }
        {
          name: 'EMAIL_AUTOMATION_CONFIG'
          value: 'professional'
        }
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: openAIService.properties.endpoint
        }
      ]
    }
  }
}

// Diagnostic settings for function app
resource functionAppDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: functionApp
  name: 'diagnostics'
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'FunctionAppLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// AZD Required Outputs
output RESOURCE_GROUP_ID string = resourceGroup().id
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = 'https://${containerRegistry.properties.loginServer}'

// Additional outputs for demo environment
output AZURE_CONTAINER_APP_URL string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output AZURE_FUNCTION_APP_URL string = 'https://${functionApp.properties.defaultHostName}'
output AZURE_OPENAI_ENDPOINT string = openAIService.properties.endpoint
output AZURE_STORAGE_ACCOUNT_NAME string = storageAccount.name
