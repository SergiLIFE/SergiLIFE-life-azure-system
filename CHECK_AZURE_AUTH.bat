@echo off
echo ========================================
echo AZURE AUTHORIZATION STATUS CHECK
echo ========================================
echo Date/Time: %DATE% %TIME%
echo.

echo [1] Checking current Azure login status...
az account show --query "{name:name, id:id, tenantId:tenantId, state:state}" --output table
echo.

echo [2] Checking subscription details...
az account show --query "{subscriptionName:name, subscriptionId:id, tenantId:tenantId, state:state, isDefault:isDefault}" --output json
echo.

echo [3] Checking available resource groups...
az group list --query "[].{Name:name, Location:location, ProvisioningState:properties.provisioningState}" --output table
echo.

echo [4] Checking Function App permissions...
echo Checking if we can list Function Apps in subscription...
az functionapp list --query "length(@)"
if %ERRORLEVEL% EQU 0 (
    echo ✅ Function App permissions: GRANTED
    az functionapp list --query "[].{Name:name, ResourceGroup:resourceGroup, State:state, Location:location}" --output table
) else (
    echo ❌ Function App permissions: DENIED or LIMITED
)
echo.

echo [5] Checking Azure CLI permissions...
echo Testing resource creation permissions...
az provider list --query "[?namespace=='Microsoft.Web'].{Namespace:namespace, RegistrationState:registrationState}" --output table
echo.

echo [6] Checking subscription limits...
az vm list-usage --location "East US 2" --query "[?localName=='Standard DSv3 Family vCPUs'].{Name:localName, CurrentValue:currentValue, Limit:limit}" --output table 2>nul
echo.

echo ========================================
echo AUTHORIZATION SUMMARY
echo ========================================
echo.
echo If you see errors above, it means:
echo 1. Azure subscription may not have Function App creation permissions
echo 2. Your account may need additional roles (Contributor, Owner)
echo 3. The subscription may require approval for Function App deployments
echo 4. Corporate/Enterprise policies may be blocking deployments
echo.
echo ALTERNATIVE APPROACH:
echo - We can create a LOCAL version of the L.I.F.E Platform
echo - Test all functionality locally using Flask/FastAPI
echo - Deploy to Azure when authorization is approved
echo.
pause