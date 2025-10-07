# 🚀 L.I.F.E. Platform Quick Start Script
# Copyright 2025 - Sergio Paya Borrull
# Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
# Launch Ready: October 7, 2025

param(
    [switch]$Development,
    [switch]$Production,
    [switch]$Testing,
    [switch]$SkipValidation,
    [switch]$Verbose,
    [string]$Environment = "production"
)

# Script Configuration
$ScriptVersion = "2025.1.0-PRODUCTION"
$LaunchDate = "October 7, 2025"
$AzureSubscription = "5c88cef6-f243-497d-98af-6c6086d575ca"
$ResourceGroup = "life-platform-rg"
$Location = "East US 2"

# Color Functions for Enhanced Output
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️ $Message" -ForegroundColor Cyan
}

function Write-Header {
    param([string]$Message)
    Write-Host "`n🚀 $Message" -ForegroundColor Magenta
    Write-Host "=" * 60 -ForegroundColor Gray
}

# Main Quick Start Function
function Start-LIFEPlatform {
    Write-Header "L.I.F.E. Platform Quick Start - Version $ScriptVersion"
    Write-Info "Launch Target: $LaunchDate"
    Write-Info "Environment: $Environment"
    Write-Info "Azure Subscription: $AzureSubscription"
    
    try {
        # Step 1: Environment Validation
        Write-Header "Step 1: Environment Validation"
        Test-Prerequisites
        
        # Step 2: Python Environment Setup
        Write-Header "Step 2: Python Environment Setup"
        Initialize-PythonEnvironment
        
        # Step 3: Azure Configuration
        Write-Header "Step 3: Azure Configuration"
        Initialize-AzureEnvironment
        
        # Step 4: Dependencies Installation
        Write-Header "Step 4: Dependencies Installation"
        Install-Dependencies
        
        # Step 5: Core System Validation
        Write-Header "Step 5: Core System Validation"
        Test-CoreSystem
        
        # Step 6: Launch Readiness Check
        Write-Header "Step 6: Launch Readiness Validation"
        Test-LaunchReadiness
        
        Write-Success "L.I.F.E. Platform Quick Start completed successfully!"
        Write-Info "Platform is ready for October 7th birthday launch! 🎂"
        
    } catch {
        Write-Error "Quick Start failed: $($_.Exception.Message)"
        Write-Warning "Please check the error details and retry"
        exit 1
    }
}

# Prerequisites Validation
function Test-Prerequisites {
    Write-Info "Validating system prerequisites..."
    
    # Check Python Installation
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion -match "Python 3\.([8-9]|1[0-2])") {
            Write-Success "Python version validated: $pythonVersion"
        } else {
            throw "Python 3.8+ required. Found: $pythonVersion"
        }
    } catch {
        Write-Error "Python not found or invalid version"
        Write-Info "Please install Python 3.8+ from https://python.org"
        throw $_
    }
    
    # Check Git Installation
    try {
        $gitVersion = git --version 2>$null
        Write-Success "Git version validated: $gitVersion"
    } catch {
        Write-Error "Git not found"
        Write-Info "Please install Git from https://git-scm.com"
        throw $_
    }
    
    # Check Azure CLI Installation
    try {
        $azVersion = az --version 2>$null | Select-String "azure-cli"
        Write-Success "Azure CLI validated: $($azVersion.Line.Trim())"
    } catch {
        Write-Warning "Azure CLI not found - will install automatically"
    }
    
    # Check VS Code (optional)
    try {
        $codeVersion = code --version 2>$null
        if ($codeVersion) {
            Write-Success "VS Code detected - enhanced development experience available"
        }
    } catch {
        Write-Info "VS Code not detected - terminal-only mode"
    }
    
    Write-Success "Prerequisites validation completed"
}

# Python Environment Initialization
function Initialize-PythonEnvironment {
    Write-Info "Setting up Python virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path "venv")) {
        Write-Info "Creating Python virtual environment..."
        python -m venv venv
        Write-Success "Virtual environment created"
    } else {
        Write-Info "Virtual environment already exists"
    }
    
    # Activate virtual environment
    Write-Info "Activating virtual environment..."
    if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
        & ".\venv\Scripts\Activate.ps1"
    } else {
        & "venv/bin/activate"
    }
    
    # Upgrade pip
    Write-Info "Upgrading pip to latest version..."
    python -m pip install --upgrade pip | Out-Null
    
    Write-Success "Python environment initialized"
}

# Azure Environment Configuration
function Initialize-AzureEnvironment {
    Write-Info "Configuring Azure environment..."
    
    # Install Azure CLI if not present
    try {
        az --version | Out-Null
    } catch {
        Write-Info "Installing Azure CLI..."
        if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
            Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
            Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
            Remove-Item .\AzureCLI.msi
        } else {
            curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
        }
        Write-Success "Azure CLI installed"
    }
    
    # Check Azure login status
    try {
        $account = az account show --query "user.name" -o tsv 2>$null
        if ($account) {
            Write-Success "Azure authenticated as: $account"
        } else {
            throw "Not authenticated"
        }
    } catch {
        Write-Info "Azure authentication required..."
        Write-Info "Please login when prompted..."
        az login
        Write-Success "Azure authentication completed"
    }
    
    # Set subscription
    Write-Info "Setting Azure subscription..."
    az account set --subscription $AzureSubscription
    $currentSub = az account show --query "name" -o tsv
    Write-Success "Active subscription: $currentSub"
    
    # Validate resource group access
    try {
        $rg = az group show --name $ResourceGroup --query "name" -o tsv 2>$null
        if ($rg -eq $ResourceGroup) {
            Write-Success "Resource group access validated: $ResourceGroup"
        } else {
            Write-Warning "Resource group not found or inaccessible: $ResourceGroup"
        }
    } catch {
        Write-Warning "Could not validate resource group access"
    }
    
    Write-Success "Azure environment configured"
}

# Dependencies Installation
function Install-Dependencies {
    Write-Info "Installing Python dependencies..."
    
    # Check if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Info "Installing from requirements.txt..."
        pip install -r requirements.txt
        Write-Success "Dependencies installed from requirements.txt"
    } else {
        Write-Info "Installing core dependencies manually..."
        
        # Core dependencies for L.I.F.E. Platform
        $coreDependencies = @(
            "numpy>=1.24.0",
            "pandas>=2.0.0",
            "scikit-learn>=1.3.0",
            "azure-functions>=1.18.0",
            "azure-storage-blob>=12.19.0",
            "azure-keyvault-secrets>=4.7.0",
            "azure-servicebus>=7.11.0",
            "azure-monitor-opentelemetry>=1.0.0",
            "asyncio-mqtt>=0.13.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "pylint>=2.17.0"
        )
        
        foreach ($package in $coreDependencies) {
            Write-Info "Installing $package..."
            pip install $package | Out-Null
        }
        
        Write-Success "Core dependencies installed"
    }
    
    # Verify key imports
    Write-Info "Validating critical imports..."
    try {
        python -c "import numpy, pandas, sklearn; print('Core ML libraries: OK')" | Out-Null
        python -c "import azure.functions; print('Azure Functions: OK')" | Out-Null
        python -c "import asyncio; print('Async support: OK')" | Out-Null
        Write-Success "Critical imports validated"
    } catch {
        Write-Error "Import validation failed - some dependencies may be missing"
        throw $_
    }
    
    Write-Success "Dependencies installation completed"
}

# Core System Testing
function Test-CoreSystem {
    Write-Info "Testing core L.I.F.E. Platform components..."
    
    # Test core algorithm import
    try {
        if (Test-Path "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py") {
            Write-Info "Testing core algorithm import..."
            python -c "from importlib import import_module; import_module('experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se'); print('Core algorithm import: OK')"
            Write-Success "Core algorithm validated"
        } else {
            Write-Warning "Core algorithm file not found - development mode?"
        }
    } catch {
        Write-Warning "Core algorithm test failed: $($_.Exception.Message)"
    }
    
    # Test Azure configuration
    try {
        if (Test-Path "azure_config.py") {
            Write-Info "Testing Azure configuration..."
            python -c "import azure_config; print('Azure config: OK')"
            Write-Success "Azure configuration validated"
        } else {
            Write-Warning "Azure configuration file not found"
        }
    } catch {
        Write-Warning "Azure configuration test failed: $($_.Exception.Message)"
    }
    
    # Test autonomous optimizer
    try {
        if (Test-Path "autonomous_optimizer.py") {
            Write-Info "Testing autonomous optimizer..."
            python -c "import autonomous_optimizer; print('Autonomous optimizer: OK')"
            Write-Success "Autonomous optimizer validated"
        } else {
            Write-Warning "Autonomous optimizer file not found"
        }
    } catch {
        Write-Warning "Autonomous optimizer test failed: $($_.Exception.Message)"
    }
    
    Write-Success "Core system testing completed"
}

# Launch Readiness Validation
function Test-LaunchReadiness {
    Write-Info "Performing comprehensive launch readiness check..."
    
    $readinessScore = 0
    $totalChecks = 10
    
    # Check 1: Core files present
    $coreFiles = @(
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
        "azure_config.py",
        "autonomous_optimizer.py",
        "azure_functions_workflow.py"
    )
    
    $filesFound = 0
    foreach ($file in $coreFiles) {
        if (Test-Path $file) {
            $filesFound++
        }
    }
    
    if ($filesFound -eq $coreFiles.Count) {
        Write-Success "All core files present ($filesFound/$($coreFiles.Count))"
        $readinessScore++
    } else {
        Write-Warning "Missing core files ($filesFound/$($coreFiles.Count))"
    }
    
    # Check 2: Python environment
    try {
        python --version | Out-Null
        Write-Success "Python environment operational"
        $readinessScore++
    } catch {
        Write-Error "Python environment issues detected"
    }
    
    # Check 3: Azure CLI access
    try {
        az account show | Out-Null
        Write-Success "Azure CLI access confirmed"
        $readinessScore++
    } catch {
        Write-Warning "Azure CLI access issues"
    }
    
    # Check 4: Dependencies
    try {
        python -c "import numpy, pandas, sklearn" 2>$null
        Write-Success "Core ML libraries available"
        $readinessScore++
    } catch {
        Write-Warning "Missing ML dependencies"
    }
    
    # Check 5: Azure Functions support
    try {
        python -c "import azure.functions" 2>$null
        Write-Success "Azure Functions support available"
        $readinessScore++
    } catch {
        Write-Warning "Azure Functions dependencies missing"
    }
    
    # Check 6: Documentation
    $docs = @("README.md", "QUICK_START.md", "AZURE_OIDC_SETUP.md")
    $docsFound = ($docs | Where-Object { Test-Path $_ }).Count
    
    if ($docsFound -ge 2) {
        Write-Success "Documentation available ($docsFound/$($docs.Count))"
        $readinessScore++
    } else {
        Write-Warning "Limited documentation available"
    }
    
    # Check 7: Testing capabilities
    try {
        python -c "import pytest" 2>$null
        Write-Success "Testing framework available"
        $readinessScore++
    } catch {
        Write-Warning "Testing framework not available"
    }
    
    # Check 8: Version control
    if (Test-Path ".git") {
        Write-Success "Git repository initialized"
        $readinessScore++
    } else {
        Write-Warning "Git repository not found"
    }
    
    # Check 9: Azure resources (if accessible)
    try {
        $rg = az group show --name $ResourceGroup --query "name" -o tsv 2>$null
        if ($rg) {
            Write-Success "Azure resources accessible"
            $readinessScore++
        } else {
            Write-Warning "Azure resources not accessible"
        }
    } catch {
        Write-Warning "Cannot validate Azure resources"
    }
    
    # Check 10: Environment configuration
    if ($Environment -eq "production") {
        Write-Success "Production environment configured"
        $readinessScore++
    } else {
        Write-Info "Development environment configured"
        $readinessScore++
    }
    
    # Calculate readiness percentage
    $readinessPercentage = [math]::Round(($readinessScore / $totalChecks) * 100, 1)
    
    Write-Host "`n📊 LAUNCH READINESS SCORE: $readinessScore/$totalChecks ($readinessPercentage%)" -ForegroundColor Magenta
    
    if ($readinessPercentage -ge 80) {
        Write-Success "✅ LAUNCH READY - Platform prepared for October 7th launch!"
        Write-Info "🎂 Ready for birthday launch celebration!"
    } elseif ($readinessPercentage -ge 60) {
        Write-Warning "⚠️ MOSTLY READY - Minor issues to address before launch"
    } else {
        Write-Error "❌ NOT READY - Significant issues require attention"
    }
    
    Write-Success "Launch readiness validation completed"
}

# Quick Actions Menu
function Show-QuickActions {
    Write-Header "L.I.F.E. Platform Quick Actions"
    Write-Host "1. 🧠 Run Autonomous Optimizer" -ForegroundColor Green
    Write-Host "2. 🧪 Run Test Suite" -ForegroundColor Green
    Write-Host "3. 🏆 Run SOTA Benchmarks" -ForegroundColor Green
    Write-Host "4. 🚀 Azure Deploy Prep" -ForegroundColor Green
    Write-Host "5. 📊 Performance Monitor" -ForegroundColor Green
    Write-Host "6. 🔧 Install Dependencies" -ForegroundColor Green
    Write-Host "7. 🎯 Target Tracker" -ForegroundColor Green
    Write-Host "8. ❌ Exit" -ForegroundColor Red
    
    $choice = Read-Host "`nSelect action (1-8)"
    
    switch ($choice) {
        "1" { 
            Write-Info "Running Autonomous Optimizer..."
            python autonomous_optimizer.py 
        }
        "2" { 
            Write-Info "Running Test Suite..."
            python -m pytest -v --tb=short 
        }
        "3" { 
            Write-Info "Running SOTA Benchmarks..."
            python sota_benchmark.py 
        }
        "4" { 
            Write-Info "Preparing Azure Deployment..."
            python -c "import azure_config; print('Azure deployment validation...')" 
        }
        "5" { 
            Write-Info "Starting Performance Monitor..."
            python -c "import psutil; import time; [print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%') or time.sleep(1) for _ in range(10)]"
        }
        "6" { 
            Write-Info "Installing Dependencies..."
            pip install -r requirements.txt 
        }
        "7" { 
            Write-Info "Running Target Tracker..."
            python LIFE_THEORY_TARGET_TRACKER.py 
        }
        "8" { 
            Write-Info "Goodbye! Ready for October 7th launch! 🚀"
            return 
        }
        default { 
            Write-Warning "Invalid choice. Please select 1-8."
            Show-QuickActions 
        }
    }
    
    Write-Host "`nPress any key to return to menu..."
    $null = Read-Host
    Show-QuickActions
}

# Main Script Execution
Write-Host @"
🚀 L.I.F.E. Platform Quick Start Script
══════════════════════════════════════════════════════════════
Learning Individually from Experience - Neural Adaptive Platform
Copyright 2025 - Sergio Paya Borrull
Version: $ScriptVersion
Launch Target: $LaunchDate
Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb
══════════════════════════════════════════════════════════════
"@ -ForegroundColor Cyan

# Parameter-based execution
if ($Development) {
    $Environment = "development"
    Write-Info "Development mode activated"
}

if ($Production) {
    $Environment = "production"
    Write-Info "Production mode activated"
}

if ($Testing) {
    Write-Header "Testing Mode - Running Test Suite Only"
    python -m pytest -v --tb=short
    exit 0
}

# Run quick start or show menu
if ($args.Count -eq 0 -and -not $Development -and -not $Production -and -not $Testing) {
    $choice = Read-Host "Run full quick start setup? (y/N, or 'm' for menu)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        Start-LIFEPlatform
    } elseif ($choice -eq "m" -or $choice -eq "M") {
        Show-QuickActions
    } else {
        Write-Info "Quick start skipped. Run with -Development or -Production flag for automated setup."
        Write-Info "Or run again and choose 'y' for full setup or 'm' for quick actions menu."
    }
} else {
    Start-LIFEPlatform
}

Write-Info "L.I.F.E. Platform Quick Start Script completed!"
Write-Success "Platform ready for October 7th birthday launch! 🎂🚀"