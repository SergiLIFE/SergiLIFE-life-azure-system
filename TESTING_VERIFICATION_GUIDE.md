# 🧪 TESTING YOUR DEPLOYED L.I.F.E PLATFORM

**Date:** October 19, 2025  
**Function App:** life-functions-app  
**Region:** East US 2

---

## 🔍 Quick Health Check

You just ran:
```cmd
curl https://life-functions-app.azurewebsites.net/api/health
```

### Expected Response:

**If deployment succeeded:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-19T...",
  "service": "L.I.F.E Platform",
  "version": "1.0.0",
  "life_core_available": true,
  "offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb"
}
```

**If deployment is still in progress:**
```
Error: 404 Not Found
or
Error: 503 Service Unavailable
```
→ Wait 1-2 more minutes and try again

**If curl doesn't work on Windows:**
Try PowerShell instead:
```cmd
powershell -Command "Invoke-RestMethod -Uri 'https://life-functions-app.azurewebsites.net/api/health'"
```

---

## ✅ Complete Verification Checklist

### Test 1: Health Endpoint (HTTP GET)
```cmd
curl https://life-functions-app.azurewebsites.net/api/health
```
**Expected:** Status 200, JSON with "healthy" status

---

### Test 2: List All Functions
```cmd
az functionapp function list --name life-functions-app --resource-group life-platform-rg --output table
```
**Expected:** Shows health_check, process_eeg, analyze_learning functions

---

### Test 3: Check Function App Status
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --query state
```
**Expected:** `"Running"`

---

### Test 4: View Deployment History
```cmd
az functionapp deployment list --name life-functions-app --resource-group life-platform-rg --output table
```
**Expected:** Shows recent deployment with "Success" status

---

### Test 5: Stream Live Logs
```cmd
az webapp log tail --name life-functions-app --resource-group life-platform-rg
```
**Expected:** Shows function execution logs (hit Ctrl+C to stop)

---

### Test 6: Get Function Keys (for secured endpoints)
```cmd
az functionapp function keys list --name life-functions-app --resource-group life-platform-rg --function-name health_check
```
**Expected:** Shows function keys (if authentication is enabled)

---

## 🧪 Advanced Testing

### Test Process EEG Endpoint (POST)

Using PowerShell:
```powershell
$body = @{
    eeg_data = @(@(0.1, 0.2, 0.3), @(0.4, 0.5, 0.6))
    sampling_rate = 256
    user_id = "test_user"
    session_id = "test_session"
} | ConvertTo-Json

Invoke-RestMethod -Uri 'https://life-functions-app.azurewebsites.net/api/process_eeg' -Method Post -Body $body -ContentType 'application/json'
```

**Expected Response:**
```json
{
  "status": "processed",
  "algorithm": "L.I.F.E Core",
  "message": "EEG data processed successfully",
  "timestamp": "2025-10-19T...",
  "sampling_rate": 256,
  "user_id": "test_user",
  "session_id": "test_session"
}
```

---

### Test Learning Analysis Endpoint (POST)

Using PowerShell:
```powershell
$body = @{
    user_traits = @{
        curiosity = 0.85
        resilience = 0.72
        openness = 0.90
    }
    eeg_metrics = @{
        alpha_power = 0.65
        theta_power = 0.45
        beta_power = 0.55
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri 'https://life-functions-app.azurewebsites.net/api/analyze_learning' -Method Post -Body $body -ContentType 'application/json'
```

**Expected Response:**
```json
{
  "personalization_level": "high",
  "user_profile": {
    "curiosity_driven": true,
    "resilient_learner": true,
    "open_to_experience": true
  },
  "neural_state": {
    "relaxed": true,
    "focused": true,
    "creative": true
  },
  "recommendations": [...]
}
```

---

## 📊 Azure Portal Verification

### View Functions in Portal:
```cmd
start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app/functions
```

**What to check:**
- ✅ Functions list shows: health_check, process_eeg, analyze_learning
- ✅ Each function shows "Enabled" status
- ✅ Can see function URLs and keys

---

### View Application Insights:
```cmd
start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/microsoft.insights/components/life-functions-app
```

**What to check:**
- ✅ Request count > 0
- ✅ Failed requests = 0
- ✅ Avg response time < 1000ms
- ✅ Live metrics showing activity

---

## 🚨 Troubleshooting

### Issue: curl returns "404 Not Found"

**Possible causes:**
1. Deployment not complete yet → Wait 1-2 more minutes
2. Functions not synced → Restart Function App
3. Wrong URL → Verify endpoint path

**Solutions:**
```cmd
REM Check if functions are listed
az functionapp function list --name life-functions-app --resource-group life-platform-rg

REM Restart Function App
az functionapp restart --name life-functions-app --resource-group life-platform-rg

REM Wait 30 seconds, then test again
timeout /t 30
curl https://life-functions-app.azurewebsites.net/api/health
```

---

### Issue: curl returns "503 Service Unavailable"

**Possible causes:**
1. Function App is starting up
2. Application error in code
3. Dependencies failed to install

**Solutions:**
```cmd
REM Check Function App status
az functionapp show --name life-functions-app --resource-group life-platform-rg --query state

REM View application logs
az webapp log tail --name life-functions-app --resource-group life-platform-rg

REM Check for errors in deployment
az webapp log download --name life-functions-app --resource-group life-platform-rg --log-file logs.zip
```

---

### Issue: "ModuleNotFoundError" in logs

**Cause:** Dependency not installed during remote build

**Solution:**
```cmd
REM Redeploy with remote build
func azure functionapp publish life-functions-app --python --build remote

REM Or check requirements.txt is correct
type requirements.txt
```

---

### Issue: curl command not recognized on Windows

**Solution:** Use PowerShell instead:
```cmd
powershell -Command "Invoke-RestMethod -Uri 'https://life-functions-app.azurewebsites.net/api/health'"
```

Or install curl:
```cmd
winget install curl
```

---

## ✅ Success Criteria

Your deployment is successful if:

- ✅ Health endpoint returns 200 OK with JSON
- ✅ All functions appear in `az functionapp function list`
- ✅ Function App state is "Running"
- ✅ Application Insights shows requests
- ✅ No errors in live logs
- ✅ Can POST to process_eeg and analyze_learning

---

## 📈 Performance Benchmarks

**Expected response times:**
- Health check: < 200ms
- Process EEG: < 1000ms (depends on data size)
- Analyze learning: < 500ms

**If slower:**
- Cold start (first request after idle): 5-10 seconds (normal)
- Warm start (subsequent requests): < 1 second

---

## 🎯 Next Steps After Verification

Once all tests pass:

1. ✅ **Configure Application Settings**
   ```cmd
   az functionapp config appsettings set --name life-functions-app --resource-group life-platform-rg --settings LIFE_ENV=production
   ```

2. ✅ **Set Up Custom Domain** (optional)
   ```cmd
   az functionapp config hostname add --name life-functions-app --resource-group life-platform-rg --hostname api.coach121life.com
   ```

3. ✅ **Enable Authentication** (optional)
   ```cmd
   az functionapp auth update --name life-functions-app --resource-group life-platform-rg --enabled true
   ```

4. ✅ **Configure Monitoring Alerts**
   - Set up alerts for failed requests
   - Configure availability tests
   - Set up performance monitoring

5. ✅ **Update GitHub Actions** (optional)
   - Set up CI/CD pipeline
   - Auto-deploy on push to main

---

## 📞 Quick Reference Commands

```cmd
REM Test health
curl https://life-functions-app.azurewebsites.net/api/health

REM List functions
az functionapp function list --name life-functions-app --resource-group life-platform-rg --output table

REM Check status
az functionapp show --name life-functions-app --resource-group life-platform-rg --query state

REM View logs
az webapp log tail --name life-functions-app --resource-group life-platform-rg

REM Restart if needed
az functionapp restart --name life-functions-app --resource-group life-platform-rg

REM Open in browser
start https://life-functions-app.azurewebsites.net/api/health
```

---

## 🎉 If All Tests Pass:

**CONGRATULATIONS! Your L.I.F.E Platform is LIVE on Azure!** 🚀

✅ Infrastructure deployed (15+ resources)  
✅ Function App configured and running  
✅ Code deployed with Python 3.11  
✅ Health endpoint responding  
✅ Ready for production traffic!

---

**Generated:** October 19, 2025  
**L.I.F.E Platform Offer ID:** 9a600d96-fe1e-420b-902a-a0c42c561adb  
**Deployment Target:** $345K Q4 2025 → $50.7M by 2029

🧠 **"No two brains learn the same way" - Your platform is ready to prove it!**
