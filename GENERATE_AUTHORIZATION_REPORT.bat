@echo off
echo ========================================
echo 🔍 L.I.F.E PLATFORM - BY-THE-BOOK AUTHORIZATION DIAGNOSTIC
echo ========================================
echo Comprehensive authorization status check for technical support ticket
echo.

echo Generating authorization report: authorization_report.txt
echo. > authorization_report.txt

echo ========================================
echo L.I.F.E PLATFORM AUTHORIZATION DIAGNOSTIC REPORT
echo Generated: %DATE% %TIME%
echo Platform: Learning Individually from Experience (L.I.F.E)
echo Target Revenue: $345K Q4 2025 - $50.7M by 2029
echo Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo ======================================== >> authorization_report.txt

echo.
echo [SECTION 1] AZURE ACCOUNT INFORMATION
echo.

echo SECTION 1: AZURE ACCOUNT INFORMATION >> authorization_report.txt
echo ---------------------------------------- >> authorization_report.txt
az account show --query "{subscriptionName:name, subscriptionId:id, tenantId:tenantId, state:state, userType:user.type, userName:user.name}" --output table
az account show --query "{subscriptionName:name, subscriptionId:id, tenantId:tenantId, state:state, userType:user.type, userName:user.name}" --output table >> authorization_report.txt

echo.
echo [SECTION 2] CURRENT ROLE ASSIGNMENTS
echo.

echo. >> authorization_report.txt
echo SECTION 2: CURRENT ROLE ASSIGNMENTS >> authorization_report.txt
echo ---------------------------------------- >> authorization_report.txt
az role assignment list --assignee $(az account show --query user.name -o tsv) --query "[].{Role:roleDefinitionName, Scope:scope, Principal:principalName}" --output table
az role assignment list --assignee $(az account show --query user.name -o tsv) --query "[].{Role:roleDefinitionName, Scope:scope, Principal:principalName}" --output table >> authorization_report.txt

echo.
echo [SECTION 3] RESOURCE PROVIDER REGISTRATION STATUS
echo.

echo. >> authorization_report.txt
echo SECTION 3: RESOURCE PROVIDER REGISTRATION STATUS >> authorization_report.txt
echo -------------------------------------------------- >> authorization_report.txt
az provider list --query "[?namespace=='Microsoft.Web' || namespace=='Microsoft.Storage' || namespace=='Microsoft.ServiceBus' || namespace=='Microsoft.KeyVault' || namespace=='Microsoft.MarketplaceOrdering'].{Provider:namespace, Status:registrationState}" --output table
az provider list --query "[?namespace=='Microsoft.Web' || namespace=='Microsoft.Storage' || namespace=='Microsoft.ServiceBus' || namespace=='Microsoft.KeyVault' || namespace=='Microsoft.MarketplaceOrdering'].{Provider:namespace, Status:registrationState}" --output table >> authorization_report.txt

echo.
echo [SECTION 4] CURRENT RESOURCE GROUPS
echo.

echo. >> authorization_report.txt
echo SECTION 4: CURRENT RESOURCE GROUPS >> authorization_report.txt
echo ---------------------------------------- >> authorization_report.txt
az group list --query "[].{Name:name, Location:location, ProvisioningState:properties.provisioningState}" --output table
az group list --query "[].{Name:name, Location:location, ProvisioningState:properties.provisioningState}" --output table >> authorization_report.txt

echo.
echo [SECTION 5] SUBSCRIPTION QUOTAS AND LIMITS
echo.

echo. >> authorization_report.txt
echo SECTION 5: SUBSCRIPTION QUOTAS AND LIMITS >> authorization_report.txt
echo --------------------------------------------- >> authorization_report.txt
az vm list-usage --location "East US 2" --query "[?contains(localName, 'App') || contains(localName, 'Web') || contains(localName, 'Function')].{Resource:localName, Current:currentValue, Limit:limit}" --output table 2>nul
az vm list-usage --location "East US 2" --query "[?contains(localName, 'App') || contains(localName, 'Web') || contains(localName, 'Function')].{Resource:localName, Current:currentValue, Limit:limit}" --output table >> authorization_report.txt 2>nul

echo.
echo [SECTION 6] AUTHORIZATION TESTING
echo.

echo. >> authorization_report.txt
echo SECTION 6: AUTHORIZATION TESTING >> authorization_report.txt
echo ----------------------------------- >> authorization_report.txt

echo Testing Resource Group Creation:
az group create --name test-life-authorization --location "East US 2" --dry-run 2>temp_rg_test.txt
if %ERRORLEVEL% EQU 0 (
    echo ✅ Resource Group Creation: AUTHORIZED >> authorization_report.txt
    echo ✅ Resource Group Creation: AUTHORIZED
) else (
    echo ❌ Resource Group Creation: BLOCKED >> authorization_report.txt
    echo ❌ Resource Group Creation: BLOCKED
    echo Error Details: >> authorization_report.txt
    type temp_rg_test.txt >> authorization_report.txt
    type temp_rg_test.txt
)

echo.
echo Testing Static Web Apps Creation:
az staticwebapp list --output table > temp_swa_test.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Static Web Apps: ACCESSIBLE >> authorization_report.txt
    echo ✅ Static Web Apps: ACCESSIBLE
) else (
    echo ❌ Static Web Apps: NOT ACCESSIBLE >> authorization_report.txt
    echo ❌ Static Web Apps: NOT ACCESSIBLE
    echo Error Details: >> authorization_report.txt
    type temp_swa_test.txt >> authorization_report.txt
)

echo.
echo Testing Function Apps Access:
az functionapp list --output table > temp_func_test.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Function Apps: ACCESSIBLE >> authorization_report.txt
    echo ✅ Function Apps: ACCESSIBLE
) else (
    echo ❌ Function Apps: NOT ACCESSIBLE >> authorization_report.txt
    echo ❌ Function Apps: NOT ACCESSIBLE
    echo Error Details: >> authorization_report.txt
    type temp_func_test.txt >> authorization_report.txt
)

echo.
echo [SECTION 7] L.I.F.E PLATFORM DEPLOYMENT REQUIREMENTS
echo.

echo. >> authorization_report.txt
echo SECTION 7: L.I.F.E PLATFORM DEPLOYMENT REQUIREMENTS >> authorization_report.txt
echo ---------------------------------------------------- >> authorization_report.txt
echo.
echo REQUIRED AZURE SERVICES FOR L.I.F.E PLATFORM: >> authorization_report.txt
echo 1. Azure Static Web Apps (Frontend hosting) >> authorization_report.txt
echo 2. Azure Functions (Backend API processing) >> authorization_report.txt
echo 3. Azure Storage Account (Data persistence) >> authorization_report.txt
echo 4. Azure Service Bus (Message processing) >> authorization_report.txt
echo 5. Azure Key Vault (Secrets management) >> authorization_report.txt
echo 6. Azure Application Insights (Monitoring) >> authorization_report.txt
echo. >> authorization_report.txt
echo BUSINESS JUSTIFICATION: >> authorization_report.txt
echo - Platform Status: Production-ready neuroadaptive learning system >> authorization_report.txt
echo - Target Market: Healthcare, Education, Research institutions >> authorization_report.txt
echo - Revenue Model: Azure Marketplace SaaS subscriptions >> authorization_report.txt
echo - Q4 2025 Target: $345,000 revenue >> authorization_report.txt
echo - 2029 Projection: $50.7M annual revenue >> authorization_report.txt
echo - Global Deployment: Required for worldwide customer base >> authorization_report.txt

echo.
echo [SECTION 8] RECOMMENDATIONS FOR TECHNICAL SUPPORT TICKET
echo.

echo. >> authorization_report.txt
echo SECTION 8: RECOMMENDATIONS FOR TECHNICAL SUPPORT TICKET >> authorization_report.txt
echo -------------------------------------------------------- >> authorization_report.txt

if exist temp_rg_test.txt (
    echo ⚠️  AUTHORIZATION GAPS IDENTIFIED: >> authorization_report.txt
    echo - Resource Group creation permissions needed >> authorization_report.txt
    echo ⚠️  AUTHORIZATION GAPS IDENTIFIED:
    echo - Resource Group creation permissions needed
)

if exist temp_swa_test.txt (
    echo - Static Web Apps access permissions needed >> authorization_report.txt
    echo - Static Web Apps access permissions needed
)

if exist temp_func_test.txt (
    echo - Function Apps access permissions needed >> authorization_report.txt  
    echo - Function Apps access permissions needed
)

echo. >> authorization_report.txt
echo IMMEDIATE ACTIONS REQUIRED: >> authorization_report.txt
echo 1. Submit technical support ticket with this report >> authorization_report.txt
echo 2. Request comprehensive Azure services authorization >> authorization_report.txt
echo 3. Accelerate Azure Marketplace publisher verification >> authorization_report.txt
echo 4. Schedule technical consultation for L.I.F.E Platform deployment >> authorization_report.txt
echo. >> authorization_report.txt
echo BUSINESS IMPACT OF DELAYS: >> authorization_report.txt
echo - Each week of delay impacts Q4 2025 revenue target >> authorization_report.txt
echo - Platform is complete and market-ready >> authorization_report.txt
echo - Only authorization blocks revenue generation >> authorization_report.txt

echo.
echo ========================================
echo DIAGNOSTIC COMPLETE
echo ========================================
echo.
echo 📄 Full report saved to: authorization_report.txt
echo 📧 Attach this report to your technical support ticket
echo.
echo NEXT STEPS:
echo 1. Review authorization_report.txt
echo 2. Submit technical support ticket with report attached
echo 3. Include business justification for L.I.F.E Platform
echo 4. Request priority handling due to revenue impact
echo.

echo 💡 KEY MESSAGE FOR TECHNICAL SUPPORT:
echo "L.I.F.E Platform is production-ready with $345K Q4 revenue target."
echo "Only Azure authorization blocks deployment and revenue generation."
echo.

REM Clean up temporary files
if exist temp_rg_test.txt del temp_rg_test.txt
if exist temp_swa_test.txt del temp_swa_test.txt  
if exist temp_func_test.txt del temp_func_test.txt

echo 📊 Authorization diagnostic complete!
echo Report ready for technical support submission.
echo.
pause