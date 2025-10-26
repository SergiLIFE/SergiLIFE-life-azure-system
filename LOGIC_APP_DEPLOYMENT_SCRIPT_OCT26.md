# 🚀 Logic App Deployment Script - October 26, 2025

**Purpose:** Deploy missing Logic App to fix system references  
**Status:** Safe deployment using Azure CLI  
**Target:** life-platform-prod resource group  

---

## 📋 **LOGIC APP CONFIGURATION**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2016-06-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "logicAppName": {
      "type": "string",
      "defaultValue": "life-platform-campaign-launcher"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Logic/workflows",
      "apiVersion": "2017-07-01",
      "name": "[parameters('logicAppName')]",
      "location": "eastus2",
      "properties": {
        "definition": {
          "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
          "contentVersion": "1.0.0.0",
          "triggers": {
            "Recurrence": {
              "recurrence": {
                "frequency": "Day",
                "interval": 1,
                "startTime": "2025-10-07T00:01:00Z",
                "timeZone": "UTC"
              },
              "type": "Recurrence"
            }
          },
          "actions": {
            "HTTP_Trigger_Functions": {
              "type": "Http",
              "inputs": {
                "method": "POST",
                "uri": "https://life-functions-app-prod.azurewebsites.net/api/CampaignLauncher",
                "headers": {
                  "Content-Type": "application/json"
                },
                "body": {
                  "triggerType": "scheduled",
                  "timestamp": "@{utcnow()}"
                }
              }
            }
          }
        },
        "state": "Enabled"
      }
    }
  ]
}
```

---

## 🔧 **DEPLOYMENT COMMANDS**

### **Step 1: Create Logic App**
```bash
az logic workflow create \
  --resource-group life-platform-prod \
  --location eastus2 \
  --name life-platform-campaign-launcher \
  --definition @logic-app-definition.json
```

### **Step 2: Verify Deployment**
```bash
az logic workflow show \
  --resource-group life-platform-prod \
  --name life-platform-campaign-launcher \
  --query "{name:name,state:state,location:location}"
```

### **Step 3: Test Logic App**
```bash
az logic workflow run trigger \
  --resource-group life-platform-prod \
  --name life-platform-campaign-launcher \
  --trigger-name Recurrence
```

---

## ✅ **POST-DEPLOYMENT VALIDATION**

1. Check Logic App appears in Azure Portal
2. Verify trigger configuration
3. Test connection to Azure Functions
4. Update system references
5. Monitor for errors

---

**Ready to deploy? This will fix the Logic App references safely.**