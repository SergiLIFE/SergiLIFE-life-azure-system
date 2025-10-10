# Campaign Trigger PowerShell Script for L.I.F.E. Platform
# Copyright 2025 - Sergio Paya Borrull
# L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("normal", "emergency", "github", "status", "test", "validate")]
    [string]$Action = "normal",
    
    [Parameter(Mandatory=$false)]
    [string]$CampaignType = "marketplace_promotion",
    
    [Parameter(Mandatory=$false)]
    [string]$TargetAudience = "all_segments"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "L.I.F.E. Platform Campaign Trigger" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green
Write-Host "Action: $Action" -ForegroundColor Green
Write-Host ""

switch ($Action) {
    "normal" {
        Write-Host "🔍 Step 1: Validating UI operational status..." -ForegroundColor Blue
        python ui_operational_validator.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ UI validation passed - system operational" -ForegroundColor Green
            Write-Host "🚀 Step 2: Running campaign trigger..." -ForegroundColor Blue
            python campaign_automatic_trigger.py
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Campaign trigger completed successfully" -ForegroundColor Green
            } else {
                Write-Host "❌ Campaign trigger encountered errors" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ UI validation failed - system not ready for triggering" -ForegroundColor Red
            Write-Host "📋 Please check the validation report in logs/ui_validation_report.md" -ForegroundColor Yellow
        }
    }
    
    "emergency" {
        Write-Host "🚨 EMERGENCY CAMPAIGN TRIGGER INITIATED" -ForegroundColor Red
        Write-Host "🔍 Step 1: Quick UI validation..." -ForegroundColor Blue
        python ui_operational_validator.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ UI validation passed" -ForegroundColor Green
            Write-Host "🚨 Step 2: Creating emergency trigger..." -ForegroundColor Red
            python campaign_automatic_trigger.py emergency
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Emergency trigger created" -ForegroundColor Green
                Write-Host "🚀 Step 3: Executing emergency campaign..." -ForegroundColor Blue
                python campaign_automatic_trigger.py
            } else {
                Write-Host "❌ Failed to create emergency trigger" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ UI validation failed - emergency trigger aborted for safety" -ForegroundColor Red
            Write-Host "⚠️ Manual intervention may be required" -ForegroundColor Yellow
        }
    }
    
    "github" {
        Write-Host "🤖 Triggering GitHub Actions workflow..." -ForegroundColor Magenta
        
        # Check if GitHub CLI is installed
        $ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
        if (-not $ghInstalled) {
            Write-Host "❌ GitHub CLI (gh) not found. Please install it first." -ForegroundColor Red
            Write-Host "   Download from: https://cli.github.com/" -ForegroundColor Yellow
            return
        }
        
        # Check if authenticated
        $ghAuth = gh auth status 2>&1
        if ($ghAuth -like "*not logged*" -or $ghAuth -like "*not authenticated*") {
            Write-Host "❌ Not authenticated with GitHub CLI. Please run 'gh auth login' first." -ForegroundColor Red
            return
        }
        
        Write-Host "📋 Campaign Type: $CampaignType" -ForegroundColor Cyan
        Write-Host "🎯 Target Audience: $TargetAudience" -ForegroundColor Cyan
        
        $workflowResult = gh workflow run campaign-launcher.yml --repo SergiLIFE/SergiLIFE-life-azure-system -f campaign_type=$CampaignType -f target_audience=$TargetAudience 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ GitHub Actions workflow triggered successfully!" -ForegroundColor Green
            Write-Host "🔗 View workflow: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions" -ForegroundColor Blue
        } else {
            Write-Host "❌ Failed to trigger GitHub Actions workflow" -ForegroundColor Red
            Write-Host "Error: $workflowResult" -ForegroundColor Red
        }
    }
    
    "status" {
        Write-Host "📊 Checking system status..." -ForegroundColor Blue
        
        # Check Python script availability
        if (Test-Path "campaign_automatic_trigger.py") {
            Write-Host "✅ Campaign trigger script found" -ForegroundColor Green
        } else {
            Write-Host "❌ Campaign trigger script missing" -ForegroundColor Red
        }
        
        # Check GitHub workflow
        if (Test-Path ".github/workflows/campaign-launcher.yml") {
            Write-Host "✅ GitHub Actions workflow found" -ForegroundColor Green
        } else {
            Write-Host "❌ GitHub Actions workflow missing" -ForegroundColor Red
        }
        
        # Check tracking directories
        $trackingDirs = @("tracking_data", "logs", "results")
        foreach ($dir in $trackingDirs) {
            if (Test-Path $dir) {
                Write-Host "✅ Directory exists: $dir" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Directory missing: $dir (will be created automatically)" -ForegroundColor Yellow
            }
        }
        
        # Run status check via Python
        Write-Host ""
        Write-Host "📋 Detailed system status:" -ForegroundColor Blue
        python -c "import asyncio; import campaign_automatic_trigger; asyncio.run(campaign_automatic_trigger.main())"
    }
    
    "test" {
        Write-Host "🧪 Running campaign system test..." -ForegroundColor Magenta
        
        # Test 1: Campaign trigger script
        Write-Host "Test 1: Campaign trigger availability" -ForegroundColor Blue
        if (Test-Path "campaign_automatic_trigger.py") {
            Write-Host "  ✅ Script found" -ForegroundColor Green
            
            # Try importing the module
            $importTest = python -c "import campaign_automatic_trigger; print('Import successful')" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Import successful" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Import failed: $importTest" -ForegroundColor Red
            }
        } else {
            Write-Host "  ❌ Script not found" -ForegroundColor Red
        }
        
        # Test 2: GitHub Actions workflow
        Write-Host "Test 2: GitHub Actions workflow" -ForegroundColor Blue
        if (Test-Path ".github/workflows/campaign-launcher.yml") {
            Write-Host "  ✅ Workflow file exists" -ForegroundColor Green
            
            # Check workflow syntax (basic YAML validation)
            $workflowContent = Get-Content ".github/workflows/campaign-launcher.yml" -Raw
            if ($workflowContent -match "schedule:" -and $workflowContent -match "workflow_dispatch:") {
                Write-Host "  ✅ Automatic and manual triggers configured" -ForegroundColor Green
            } elseif ($workflowContent -match "workflow_dispatch:") {
                Write-Host "  ⚠️  Manual trigger found, automatic trigger may be missing" -ForegroundColor Yellow
            } else {
                Write-Host "  ❌ Triggers not properly configured" -ForegroundColor Red
            }
        } else {
            Write-Host "  ❌ Workflow file missing" -ForegroundColor Red
        }
        
        # Test 3: Dependencies
        Write-Host "Test 3: Python dependencies" -ForegroundColor Blue
        $pythonModules = @("asyncio", "json", "logging", "datetime", "pathlib")
        foreach ($module in $pythonModules) {
            $moduleTest = python -c "import $module; print('OK')" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Module available: $module" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Module missing: $module" -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Host "🏁 Test complete" -ForegroundColor Cyan
    }
    
    "validate" {
        Write-Host "🔍 Running UI Operational Validation..." -ForegroundColor Blue
        python ui_operational_validator.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ UI validation completed successfully" -ForegroundColor Green
            Write-Host "📄 Check logs/ui_validation_report.md for detailed results" -ForegroundColor Blue
        } else {
            Write-Host "❌ UI validation encountered issues" -ForegroundColor Red
            Write-Host "📄 Check logs/ui_validation_report.md for troubleshooting" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Campaign Trigger - Complete" -ForegroundColor Yellow
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Usage examples
Write-Host ""
Write-Host "Usage Examples:" -ForegroundColor Yellow
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action normal" -ForegroundColor Cyan
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action emergency" -ForegroundColor Cyan  
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action github -CampaignType marketplace_promotion" -ForegroundColor Cyan
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action status" -ForegroundColor Cyan
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action test" -ForegroundColor Cyan
Write-Host "  .\TRIGGER_CAMPAIGN.ps1 -Action validate" -ForegroundColor Cyan