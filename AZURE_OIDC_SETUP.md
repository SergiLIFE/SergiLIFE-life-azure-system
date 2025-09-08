# Azure OIDC Authentication Setup for GitHub Actions

This guide will help you set up OpenID Connect (OIDC) authentication between GitHub Actions and Azure, eliminating the need to store long-lived secrets.

## Step 1: Create Azure AD Application (if not exists)

```powershell
# Login to Azure
az login

# Create a new Azure AD application
az ad app create --display-name "GitHub-SergiLIFE-life-azure-system" --sign-in-audience "AzureADMyOrg"

# Note the appId (client-id) from the output
```

## Step 2: Create Service Principal

```powershell
# Create service principal for the app (replace APP_ID with your actual app ID)
az ad sp create --id <APP_ID>

# Assign appropriate role to the service principal (replace SUBSCRIPTION_ID)
az role assignment create --assignee <APP_ID> --role "Contributor" --scope "/subscriptions/<SUBSCRIPTION_ID>"
```

## Step 3: Create Federated Credential for GitHub

```powershell
# Set variables (replace with your values)
$APP_ID = "<YOUR_APP_ID>"
$REPO_OWNER = "SergiLIFE"
$REPO_NAME = "SergiLIFE-life-azure-system"

# Create federated credential for main branch
az ad app federated-credential create --id $APP_ID --parameters @- <<EOF
{
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:$REPO_OWNER/${REPO_NAME}:ref:refs/heads/main",
    "description": "GitHub Actions for main branch",
    "audiences": [
        "api://AzureADTokenExchange"
    ]
}
EOF

# Create federated credential for pull requests (optional)
az ad app federated-credential create --id $APP_ID --parameters @- <<EOF
{
    "name": "github-pr",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:$REPO_OWNER/${REPO_NAME}:pull_request",
    "description": "GitHub Actions for pull requests",
    "audiences": [
        "api://AzureADTokenExchange"
    ]
}
EOF
```

## Step 4: Gather Required Information

You'll need these values for GitHub repository variables:

```powershell
# Get your tenant ID
az account show --query tenantId -o tsv

# Get your subscription ID
az account show --query id -o tsv

# Your client ID is the APP_ID from Step 1
```

## Step 5: Set GitHub Repository Variables

Go to your GitHub repository → Settings → Secrets and variables → Actions → Variables tab:

- `AZURE_CLIENT_ID`: Your application (client) ID
- `AZURE_TENANT_ID`: Your Azure AD tenant ID
- `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID

## Step 6: Update GitHub Actions Workflow

Your workflow should use the `azure/login@v2` action with these inputs:

```yaml
- name: Azure Login
  uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

## Benefits of OIDC

- ✅ No long-lived secrets stored in GitHub
- ✅ Automatic token rotation
- ✅ Fine-grained access control
- ✅ Better security posture
- ✅ Audit trail

## Troubleshooting

1. **Permission denied**: Ensure the service principal has appropriate RBAC roles
2. **Token exchange failed**: Verify federated credential subject matches your repo exactly
3. **Invalid audience**: Ensure audience is set to `api://AzureADTokenExchange`

## Security Best Practices

- Use least privilege principle for RBAC assignments
- Scope permissions to specific resource groups when possible
- Regularly audit federated credentials
- Monitor authentication logs in Azure AD
