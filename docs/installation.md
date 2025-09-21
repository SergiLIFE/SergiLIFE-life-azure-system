# L.I.F.E Platform Installation Guide

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.11 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended for EEG processing)
- **Storage**: 10GB available space
- **Network**: Internet connection for Azure services

### Azure Requirements
- **Azure Subscription**: Active Azure subscription with billing enabled
- **Resource Quota**: Sufficient quota for App Services, Functions, and Container Apps
- **Permissions**: Contributor role or higher in target resource group
- **Azure CLI**: Version 2.50.0 or higher

### Development Tools (Optional)
- **Visual Studio Code**: Latest version with Python and Azure extensions
- **Git**: For version control and repository management
- **Docker**: For container-based development and testing

## Installation Methods

### 1. Azure Marketplace Deployment (Recommended)

#### Quick Deploy
1. **Navigate to Azure Marketplace**
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "L.I.F.E Platform" or use Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`

2. **Select Your Plan**
   - **Basic Plan**: $15/user/month - Core features
   - **Professional Plan**: $30/user/month - Advanced analytics
   - **Enterprise Plan**: $50/user/month - Full platform + support

3. **Configure Deployment**
   ```bash
   # Basic configuration
   Resource Group: life-platform-rg
   Region: East US (or preferred)
   App Name: your-life-platform
   Pricing Tier: B2 (or higher)
   ```

4. **Complete Installation**
   - Review and accept terms
   - Click "Create" to deploy
   - Wait 10-15 minutes for deployment completion

#### Custom Deployment
```bash
# Download deployment template
az deployment group create \
  --resource-group life-platform-rg \
  --template-uri https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main/infra/main.bicep \
  --parameters @infra/main.parameters.json
```

### 2. Manual Azure Deployment

#### Step 1: Clone Repository
```bash
git clone https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git
cd SergiLIFE-life-azure-system
```

#### Step 2: Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Azure CLI (if not already installed)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

#### Step 3: Azure Login and Setup
```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Create resource group
az group create --name life-platform-rg --location eastus
```

#### Step 4: Deploy Infrastructure
```bash
# Deploy using Azure CLI
az deployment group create \
  --resource-group life-platform-rg \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json
```

#### Step 5: Deploy Application Code
```bash
# Build and deploy to App Service
az webapp up \
  --name your-life-platform-app \
  --resource-group life-platform-rg \
  --plan your-life-platform-plan \
  --runtime "PYTHON:3.11" \
  --sku B2
```

### 3. Local Development Setup

#### Step 1: Environment Setup
```bash
# Create virtual environment
python -m venv life-platform-env
source life-platform-env/bin/activate  # On Windows: life-platform-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

#### Step 2: Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
# Add your Azure credentials and settings
```

#### Step 3: Run Locally
```bash
# Start the application
python lifetheory.py

# Run tests
python -m pytest tests/

# Start with monitoring
python life_platform_demo.py
```

## Configuration

### Environment Variables
```bash
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=life-platform-rg
AZURE_MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb

# Application Settings
LIFE_PLATFORM_ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Database (if using custom storage)
DATABASE_URL=your-database-connection-string

# EEG Processing
EEG_SAMPLING_RATE=256
EEG_CHANNEL_COUNT=64
PROCESSING_BUFFER_SIZE=1024

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

### Azure Application Settings
Configure in Azure Portal under App Service > Configuration:

```json
{
  "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=...",
  "AZURE_MARKETPLACE_OFFER_ID": "9a600d96-fe1e-420b-902a-a0c42c561adb",
  "LIFE_PLATFORM_ENVIRONMENT": "production",
  "SCM_DO_BUILD_DURING_DEPLOYMENT": "true",
  "ENABLE_ORYX_BUILD": "true",
  "PRE_BUILD_COMMAND": "pip install -r requirements.txt"
}
```

## Verification

### Health Check
```bash
# Check application health
curl https://your-app-name.azurewebsites.net/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "life_algorithm": "operational",
    "eeg_processor": "operational",
    "venturi_gates": "operational",
    "quantum_processor": "operational"
  }
}
```

### Performance Test
```bash
# Run performance validation
python comprehensive_life_test.py

# Expected output:
✅ L.I.F.E Algorithm: 95.8% accuracy
✅ EEG Processing: 176,721 samples/sec
✅ Venturi Gates: 97.4% efficiency
✅ Quantum Coherence: 95.7%
```

### Monitoring Setup
```bash
# Verify Application Insights
az monitor app-insights component show \
  --app your-life-platform-insights \
  --resource-group life-platform-rg

# Check logs
az webapp log tail --name your-life-platform-app --resource-group life-platform-rg
```

## Troubleshooting

### Common Issues

#### Deployment Failures
```bash
# Check deployment status
az deployment group show \
  --resource-group life-platform-rg \
  --name main

# View deployment logs
az webapp log download --name your-app-name --resource-group life-platform-rg
```

#### Performance Issues
```bash
# Check resource usage
az monitor metrics list \
  --resource /subscriptions/{subscription}/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/your-app-name \
  --metric "CpuPercentage,MemoryPercentage"

# Scale if needed
az appservice plan update \
  --name your-life-platform-plan \
  --resource-group life-platform-rg \
  --sku P1v2
```

#### EEG Processing Issues
```bash
# Validate EEG configuration
python -c "from eeg_processor import EEGProcessor; EEGProcessor().validate_setup()"

# Check sample rate compatibility
python -c "import numpy as np; print(f'NumPy version: {np.__version__}')"
```

### Support Resources
- **Documentation**: [GitHub Repository](https://github.com/SergiLIFE/SergiLIFE-life-azure-system)
- **Azure Support**: Available through Azure Portal
- **Community**: Azure Marketplace Q&A section
- **Enterprise Support**: Included with Enterprise plan

## Security Considerations

### Network Security
```bash
# Configure application gateway (optional)
az network application-gateway create \
  --name life-platform-agw \
  --resource-group life-platform-rg \
  --sku Standard_v2 \
  --public-ip-address life-platform-pip
```

### SSL/TLS Configuration
- **Automatic HTTPS**: Enabled by default in Azure App Service
- **Custom Domains**: Configure through Azure Portal
- **SSL Certificates**: Free certificates available through App Service

### Data Encryption
- **At Rest**: Azure Storage encryption enabled by default
- **In Transit**: HTTPS enforced for all communications
- **Application Level**: Custom encryption for sensitive EEG data

## Scaling and Performance

### Horizontal Scaling
```bash
# Configure autoscaling
az monitor autoscale create \
  --resource-group life-platform-rg \
  --resource /subscriptions/{subscription}/resourceGroups/life-platform-rg/providers/Microsoft.Web/serverFarms/your-plan \
  --min-count 1 \
  --max-count 10 \
  --count 2
```

### Performance Optimization
- **Application Insights**: Monitor performance metrics
- **CDN**: Configure Azure CDN for static content
- **Caching**: Implement Redis caching for frequently accessed data

## Next Steps

1. **Complete Setup**: Follow [User Guide](user-guide.md) for initial configuration
2. **API Integration**: Review [API Reference](api-reference.md) for development
3. **Security Review**: Implement recommendations from [Security Policy](../SECURITY.md)
4. **Monitoring**: Configure alerts and dashboards in Azure Portal
5. **Backup Strategy**: Implement data backup and disaster recovery

---

**Need Help?**
- 📧 Technical Support: Available through Azure Marketplace
- 📚 Documentation: [Complete documentation](user-guide.md)
- 🎯 Enterprise Support: Dedicated support for Enterprise customers
