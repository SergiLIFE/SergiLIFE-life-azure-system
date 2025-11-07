#!/bin/bash
# L.I.F.E Platform Section 7 - Ultimate Azure Deployment Script
# Copyright 2025 - Neuroadaptive Learning Platform

set -e

echo "🚀 Starting L.I.F.E Platform Section 7 Ultimate Deployment..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="life-platform-section7-prod"
LOCATION="eastus2"
SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
DEPLOYMENT_NAME="life-section7-deployment-$(date +%Y%m%d-%H%M%S)"

# Section 7 Advanced Configuration
ENABLE_AUTOMATED_RETRAINING=true
ENABLE_GDPR_COMPLIANCE=true
ENABLE_REALTIME_ADAPTATION=true
ENABLE_QUANTUM_OPTIMIZATION=true
NEURAL_PROCESSING_RATE=60
REALTIME_LATENCY_TARGET_MS=50
AUTOMATED_RETRAINING_THRESHOLD="0.85"
GDPR_RETENTION_DAYS=365

echo -e "${BLUE}Configuration:${NC}"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Subscription: $SUBSCRIPTION_ID"
echo "  Deployment Name: $DEPLOYMENT_NAME"
echo ""
echo -e "${BLUE}Section 7 Features:${NC}"
echo "  Automated Retraining: $ENABLE_AUTOMATED_RETRAINING"
echo "  GDPR Compliance: $ENABLE_GDPR_COMPLIANCE"
echo "  Real-time Adaptation: $ENABLE_REALTIME_ADAPTATION"
echo "  Quantum Optimization: $ENABLE_QUANTUM_OPTIMIZATION"
echo "  Neural Processing Rate: ${NEURAL_PROCESSING_RATE}Hz"
echo "  Real-time Latency Target: ${REALTIME_LATENCY_TARGET_MS}ms"
echo ""

# Function to check Azure CLI
check_azure_cli() {
    echo -e "${BLUE}Checking Azure CLI...${NC}"
    if ! command -v az &> /dev/null; then
        echo -e "${RED}Error: Azure CLI is not installed${NC}"
        echo "Please install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Azure CLI found${NC}"
    az version --output table
}

# Function to authenticate and set subscription
authenticate_azure() {
    echo -e "${BLUE}Authenticating with Azure...${NC}"
    
    # Check if already logged in
    if ! az account show &> /dev/null; then
        echo "Please log in to Azure..."
        az login --allow-no-subscriptions
    fi
    
    # Set subscription
    echo "Setting subscription to $SUBSCRIPTION_ID..."
    az account set --subscription "$SUBSCRIPTION_ID"
    
    # Verify subscription
    CURRENT_SUB=$(az account show --query id --output tsv)
    if [ "$CURRENT_SUB" != "$SUBSCRIPTION_ID" ]; then
        echo -e "${RED}Error: Failed to set subscription${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Authenticated with subscription: $CURRENT_SUB${NC}"
}

# Function to create resource group
create_resource_group() {
    echo -e "${BLUE}Creating resource group...${NC}"
    
    if az group show --name "$RESOURCE_GROUP" &> /dev/null; then
        echo -e "${YELLOW}Resource group $RESOURCE_GROUP already exists${NC}"
    else
        az group create \
            --name "$RESOURCE_GROUP" \
            --location "$LOCATION" \
            --tags \
                "Environment=production" \
                "Project=life-platform" \
                "Section=7" \
                "Owner=SergiPaya" \
                "Purpose=neuroadaptive-learning" \
                "Features=automated-retraining,gdpr-compliance,realtime-adaptation,quantum-optimization"
        
        echo -e "${GREEN}✓ Resource group created: $RESOURCE_GROUP${NC}"
    fi
}

# Function to validate Bicep template
validate_bicep() {
    echo -e "${BLUE}Validating Bicep template...${NC}"
    
    # Check if Bicep file exists
    if [ ! -f "infra/section7-deployment.bicep" ]; then
        echo -e "${RED}Error: Bicep template not found at infra/section7-deployment.bicep${NC}"
        exit 1
    fi
    
    # Validate the template
    az deployment group validate \
        --resource-group "$RESOURCE_GROUP" \
        --template-file "infra/section7-deployment.bicep" \
        --parameters \
            environment="prod" \
            location="$LOCATION" \
            enableAutomatedRetraining=$ENABLE_AUTOMATED_RETRAINING \
            enableGDPRCompliance=$ENABLE_GDPR_COMPLIANCE \
            enableRealTimeAdaptation=$ENABLE_REALTIME_ADAPTATION \
            enableQuantumOptimization=$ENABLE_QUANTUM_OPTIMIZATION \
            neuralProcessingRate=$NEURAL_PROCESSING_RATE \
            realtimeLatencyTargetMs=$REALTIME_LATENCY_TARGET_MS \
            automatedRetrainingThreshold="$AUTOMATED_RETRAINING_THRESHOLD" \
            gdprRetentionDays=$GDPR_RETENTION_DAYS
    
    echo -e "${GREEN}✓ Bicep template validation successful${NC}"
}

# Function to deploy infrastructure
deploy_infrastructure() {
    echo -e "${BLUE}Deploying Section 7 infrastructure...${NC}"
    echo "This may take 10-15 minutes..."
    
    # Start deployment with progress tracking
    az deployment group create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$DEPLOYMENT_NAME" \
        --template-file "infra/section7-deployment.bicep" \
        --parameters \
            environment="prod" \
            location="$LOCATION" \
            enableAutomatedRetraining=$ENABLE_AUTOMATED_RETRAINING \
            enableGDPRCompliance=$ENABLE_GDPR_COMPLIANCE \
            enableRealTimeAdaptation=$ENABLE_REALTIME_ADAPTATION \
            enableQuantumOptimization=$ENABLE_QUANTUM_OPTIMIZATION \
            neuralProcessingRate=$NEURAL_PROCESSING_RATE \
            realtimeLatencyTargetMs=$REALTIME_LATENCY_TARGET_MS \
            automatedRetrainingThreshold="$AUTOMATED_RETRAINING_THRESHOLD" \
            gdprRetentionDays=$GDPR_RETENTION_DAYS \
        --verbose
    
    echo -e "${GREEN}✓ Infrastructure deployment completed${NC}"
}

# Function to get deployment outputs
get_deployment_outputs() {
    echo -e "${BLUE}Retrieving deployment outputs...${NC}"
    
    # Get the deployment outputs
    OUTPUTS=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs \
        --output json)
    
    # Extract key URLs and information
    CONTAINER_APP_URL=$(echo "$OUTPUTS" | jq -r '.containerAppUrl.value')
    FUNCTION_APP_URL=$(echo "$OUTPUTS" | jq -r '.functionAppUrl.value')
    CONTAINER_REGISTRY=$(echo "$OUTPUTS" | jq -r '.containerRegistryName.value')
    KEY_VAULT=$(echo "$OUTPUTS" | jq -r '.keyVaultName.value')
    
    echo -e "${GREEN}✓ Deployment completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}Deployment Summary:${NC}"
    echo "  Container App URL: $CONTAINER_APP_URL"
    echo "  Function App URL: $FUNCTION_APP_URL"
    echo "  Container Registry: $CONTAINER_REGISTRY"
    echo "  Key Vault: $KEY_VAULT"
    echo ""
    
    # Save outputs to file
    echo "$OUTPUTS" > "deployment-outputs.json"
    echo -e "${GREEN}✓ Deployment outputs saved to deployment-outputs.json${NC}"
}

# Function to build and push container image
build_and_push_image() {
    echo -e "${BLUE}Building and pushing container image...${NC}"
    
    # Get container registry name from deployment
    CONTAINER_REGISTRY=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.containerRegistryName.value \
        --output tsv)
    
    # Create Dockerfile if it doesn't exist
    if [ ! -f "Dockerfile" ]; then
        echo "Creating Dockerfile for Section 7..."
        cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs tracking_data/kpis tracking_data/outreach tracking_data/conversions tracking_data/analytics

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Start the application
CMD ["python", "life_algorithm_section7_integration.py"]
EOF
        echo -e "${GREEN}✓ Dockerfile created${NC}"
    fi
    
    # Build and push image
    az acr build \
        --registry "$CONTAINER_REGISTRY" \
        --image "life-section7:latest" \
        --file Dockerfile \
        .
    
    echo -e "${GREEN}✓ Container image built and pushed${NC}"
}

# Function to update container app
update_container_app() {
    echo -e "${BLUE}Updating container app with new image...${NC}"
    
    # Get container app name
    CONTAINER_APP_NAME="life-section7-prod-app"
    
    # Update the container app
    az containerapp update \
        --resource-group "$RESOURCE_GROUP" \
        --name "$CONTAINER_APP_NAME" \
        --image "${CONTAINER_REGISTRY}.azurecr.io/life-section7:latest"
    
    echo -e "${GREEN}✓ Container app updated${NC}"
}

# Function to run deployment tests
run_deployment_tests() {
    echo -e "${BLUE}Running deployment tests...${NC}"
    
    # Get the container app URL
    CONTAINER_APP_URL=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.containerAppUrl.value \
        --output tsv)
    
    echo "Testing health endpoint..."
    if curl -f -s "$CONTAINER_APP_URL/health" > /dev/null; then
        echo -e "${GREEN}✓ Health endpoint responding${NC}"
    else
        echo -e "${YELLOW}⚠ Health endpoint not yet responding (may still be starting)${NC}"
    fi
    
    echo "Testing readiness endpoint..."
    if curl -f -s "$CONTAINER_APP_URL/ready" > /dev/null; then
        echo -e "${GREEN}✓ Readiness endpoint responding${NC}"
    else
        echo -e "${YELLOW}⚠ Readiness endpoint not yet responding (may still be starting)${NC}"
    fi
}

# Function to setup monitoring and alerts
setup_monitoring() {
    echo -e "${BLUE}Setting up monitoring and alerts...${NC}"
    
    # Get Application Insights name
    APP_INSIGHTS=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.applicationInsightsName.value \
        --output tsv)
    
    # Create action group for alerts
    az monitor action-group create \
        --resource-group "$RESOURCE_GROUP" \
        --name "life-section7-alerts" \
        --short-name "LifeS7" \
        --email-receivers \
            name="admin" \
            email="admin@lifeplatform.ai" \
        --webhook-receivers \
            name="webhook" \
            service-uri="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    
    # Create availability alert
    az monitor metrics alert create \
        --resource-group "$RESOURCE_GROUP" \
        --name "life-section7-availability" \
        --description "Alert when Section 7 availability drops below 99%" \
        --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Insights/components/$APP_INSIGHTS" \
        --condition "avg availabilityResults/availabilityPercentage < 99" \
        --action "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Insights/actionGroups/life-section7-alerts" \
        --evaluation-frequency 5m \
        --window-size 15m \
        --severity 2
    
    echo -e "${GREEN}✓ Monitoring and alerts configured${NC}"
}

# Function to create deployment documentation
create_documentation() {
    echo -e "${BLUE}Creating deployment documentation...${NC}"
    
    cat > "SECTION7_DEPLOYMENT_GUIDE.md" << EOF
# L.I.F.E Platform Section 7 - Deployment Guide

## Deployment Information
- **Deployment Date**: $(date)
- **Resource Group**: $RESOURCE_GROUP
- **Location**: $LOCATION
- **Deployment Name**: $DEPLOYMENT_NAME

## Section 7 Features Enabled
- **Automated Retraining**: $ENABLE_AUTOMATED_RETRAINING
- **GDPR Compliance**: $ENABLE_GDPR_COMPLIANCE
- **Real-time Adaptation**: $ENABLE_REALTIME_ADAPTATION
- **Quantum Optimization**: $ENABLE_QUANTUM_OPTIMIZATION

## Configuration
- **Neural Processing Rate**: ${NEURAL_PROCESSING_RATE}Hz
- **Real-time Latency Target**: ${REALTIME_LATENCY_TARGET_MS}ms
- **Automated Retraining Threshold**: $AUTOMATED_RETRAINING_THRESHOLD
- **GDPR Retention Days**: $GDPR_RETENTION_DAYS

## Deployed Resources
$(az resource list --resource-group "$RESOURCE_GROUP" --output table)

## URLs
- **Container App**: $CONTAINER_APP_URL
- **Function App**: $FUNCTION_APP_URL

## Management Commands
\`\`\`bash
# View resource group
az group show --name "$RESOURCE_GROUP"

# View deployment status
az deployment group show --resource-group "$RESOURCE_GROUP" --name "$DEPLOYMENT_NAME"

# View container app logs
az containerapp logs show --resource-group "$RESOURCE_GROUP" --name "life-section7-prod-app"

# Scale container app
az containerapp update --resource-group "$RESOURCE_GROUP" --name "life-section7-prod-app" --min-replicas 2 --max-replicas 20
\`\`\`

## Monitoring
- **Application Insights**: Monitor performance and errors
- **Log Analytics**: Centralized logging
- **Alerts**: Configured for availability and performance

## Support
For support and troubleshooting, refer to the L.I.F.E Platform documentation or contact the development team.
EOF
    
    echo -e "${GREEN}✓ Deployment documentation created: SECTION7_DEPLOYMENT_GUIDE.md${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}Starting L.I.F.E Platform Section 7 Ultimate Deployment${NC}"
    echo "======================================================"
    
    check_azure_cli
    authenticate_azure
    create_resource_group
    validate_bicep
    deploy_infrastructure
    get_deployment_outputs
    build_and_push_image
    update_container_app
    run_deployment_tests
    setup_monitoring
    create_documentation
    
    echo ""
    echo -e "${GREEN}🎉 L.I.F.E Platform Section 7 Ultimate Deployment Complete! 🎉${NC}"
    echo "================================================================="
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Visit the Container App URL to verify the deployment"
    echo "2. Configure DNS and SSL certificates for production"
    echo "3. Set up continuous deployment pipelines"
    echo "4. Monitor the application through Application Insights"
    echo "5. Review and test all Section 7 features"
    echo ""
    echo -e "${GREEN}Happy Learning! 🧠✨${NC}"
}

# Run the deployment
main "$@"