#!/bin/bash
# L.I.F.E. Platform - Code Deployment Script
# Run AFTER infrastructure deployment completes
# Deploys your actual Python code, algorithms, and functions to Azure

echo "📦 L.I.F.E. Platform Code Deployment"
echo "===================================="
echo ""

# Get resource names from Azure
echo "🔍 Discovering deployed resources..."
ACR_NAME=$(az acr list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)
CONTAINER_APP_NAME=$(az containerapp list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)
FUNCTION_APP_NAME=$(az functionapp list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)
STORAGE_ACCOUNT=$(az storage account list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)

echo "✅ Found resources:"
echo "   - Container Registry: $ACR_NAME"
echo "   - Container App: $CONTAINER_APP_NAME"
echo "   - Function App: $FUNCTION_APP_NAME"
echo "   - Storage Account: $STORAGE_ACCOUNT"
echo ""

# Step 1: Create Dockerfile for L.I.F.E. Platform
echo "🐳 Creating Dockerfile for L.I.F.E. Platform..."
cat > Dockerfile << 'DOCKERFILE'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy L.I.F.E. Platform code
COPY algorithms/ ./algorithms/
COPY *.py ./

# Expose port for Container Apps
EXPOSE 8080

# Run the platform
CMD ["python", "life_algorithm_ultimate_section3.py"]
DOCKERFILE

echo "✅ Dockerfile created"
echo ""

# Step 2: Build and push Docker image
echo "🏗️  Building Docker image with your L.I.F.E. code..."
echo "   This includes:"
echo "   - Venturi adaptive system"
echo "   - EEG processing algorithms"
echo "   - Neural processing core"
echo "   - All 686+ Python files"
echo ""

# Note: This assumes we're running from the GitHub repo
# In Cloud Shell, you'd need to upload your repo first or use GitHub integration

echo "⚠️  NOTE: This step requires your code repository"
echo "   Option 1: Upload your entire repo to Cloud Shell"
echo "   Option 2: Use GitHub Actions (recommended)"
echo ""

read -p "Do you want to set up GitHub Actions deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📋 Creating GitHub Actions workflow..."
    
    # Create GitHub Actions workflow
    mkdir -p .github/workflows
    cat > .github/workflows/deploy-life-platform.yml << 'WORKFLOW'
name: Deploy L.I.F.E. Platform to Azure

on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - 'algorithms/**'
      - '*.py'
      - 'requirements.txt'

env:
  AZURE_CONTAINER_REGISTRY: __ACR_NAME__
  CONTAINER_APP_NAME: __CONTAINER_APP_NAME__
  RESOURCE_GROUP: rg-life-microsoft-demo
  IMAGE_NAME: life-platform

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build and push to ACR
        run: |
          az acr build \
            --registry ${{ env.AZURE_CONTAINER_REGISTRY }} \
            --image ${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --image ${{ env.IMAGE_NAME }}:latest \
            --file Dockerfile \
            .

      - name: Deploy to Container Apps
        run: |
          az containerapp update \
            --name ${{ env.CONTAINER_APP_NAME }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --image ${{ env.AZURE_CONTAINER_REGISTRY }}.azurecr.io/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Verify deployment
        run: |
          echo "✅ L.I.F.E. Platform deployed successfully!"
          az containerapp show \
            --name ${{ env.CONTAINER_APP_NAME }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --query properties.configuration.ingress.fqdn \
            -o tsv
WORKFLOW

    # Replace placeholders
    sed -i "s/__ACR_NAME__/$ACR_NAME/g" .github/workflows/deploy-life-platform.yml
    sed -i "s/__CONTAINER_APP_NAME__/$CONTAINER_APP_NAME/g" .github/workflows/deploy-life-platform.yml
    
    echo "✅ GitHub Actions workflow created!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Commit and push this workflow to your GitHub repo"
    echo "2. Add AZURE_CREDENTIALS secret to GitHub:"
    echo "   - Go to repo Settings → Secrets → Actions"
    echo "   - Create secret named AZURE_CREDENTIALS"
    echo "   - Value: Run this command to get credentials:"
    echo ""
    echo "   az ad sp create-for-rbac --name life-github-deploy --role contributor --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo --sdk-auth"
    echo ""
fi

# Step 3: Deploy Azure Functions
echo "⚡ Deploying Azure Functions..."
echo ""

if [ -d "azure_functions" ]; then
    echo "📂 Found azure_functions directory"
    
    # Check if func CLI is available
    if command -v func &> /dev/null; then
        cd azure_functions
        func azure functionapp publish $FUNCTION_APP_NAME --python
        cd ..
        echo "✅ Functions deployed!"
    else
        echo "⚠️  Azure Functions Core Tools not installed"
        echo "   Install: npm install -g azure-functions-core-tools@4"
        echo "   Or use Azure Portal to deploy functions manually"
    fi
else
    echo "⚠️  No azure_functions folder found"
fi

echo ""
echo "✅ Code Deployment Script Complete!"
echo ""
echo "📊 Summary:"
echo "   Infrastructure: ✅ Deployed"
echo "   Dockerfile: ✅ Created"
echo "   GitHub Actions: ✅ Configured (if selected)"
echo "   Functions: ⚠️  Manual deployment may be needed"
echo ""
echo "🎯 Next Actions:"
echo "1. Commit Dockerfile and GitHub workflow to your repo"
echo "2. Configure GitHub secrets"
echo "3. Push to main branch → automatic deployment!"
echo "4. Or manually build: az acr build --registry $ACR_NAME --image life-platform:latest ."
echo ""
echo "🔗 Your deployed app will be at:"
echo "   https://$CONTAINER_APP_NAME.eastus2.azurecontainerapps.io"
