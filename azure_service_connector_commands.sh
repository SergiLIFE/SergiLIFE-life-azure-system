# 🔗 Azure Service Connector Setup Commands
# Execute these commands in Azure Cloud Shell for L.I.F.E. Platform
# Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca

echo "🚀 L.I.F.E. Platform Service Connector Setup"
echo "Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca"

# Set correct subscription
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Verify subscription
echo "✅ Verifying subscription..."
az account show --query "{SubscriptionId:id, Name:name, State:state}" -o table

# Enable managed identity on Function App
echo "🔐 Enabling managed identity on life-functions-app..."
az functionapp identity assign --name "life-functions-app" --resource-group "life-platform-rg"

# Create Service Connector: Function App -> Storage Account
echo "🔗 Creating Service Connector: Function App -> Storage Account..."
az webapp connection create storage-blob \
    --resource-group "life-platform-rg" \
    --name "life-functions-app" \
    --target-resource-group "life-platform-rg" \
    --account "stlifeplatformprod" \
    --system-identity \
    --verbose

# Create Service Connector: Function App -> Key Vault
echo "🔐 Creating Service Connector: Function App -> Key Vault..."
az webapp connection create keyvault \
    --resource-group "life-platform-rg" \
    --name "life-functions-app" \
    --target-resource-group "life-platform-rg" \
    --vault "kv-life-platform-prod" \
    --system-identity \
    --verbose

# Create Service Connector: Function App -> Service Bus
echo "📨 Creating Service Connector: Function App -> Service Bus..."
az webapp connection create servicebus \
    --resource-group "life-platform-rg" \
    --name "life-functions-app" \
    --target-resource-group "life-platform-rg" \
    --namespace "sb-life-platform-prod" \
    --system-identity \
    --verbose

# List all connections to verify
echo "📊 Verifying Service Connector configurations..."
az webapp connection list --resource-group "life-platform-rg" --name "life-functions-app" -o table

# Test the connections
echo "🧪 Testing Service Connector configurations..."
az webapp connection validate --resource-group "life-platform-rg" --name "life-functions-app"

echo "🎉 Service Connector setup complete!"
echo "✅ Function App secured with Managed Identity"
echo "🔒 No more storage authentication errors!"