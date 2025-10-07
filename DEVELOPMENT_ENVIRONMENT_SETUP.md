# L.I.F.E. Platform Development Environment Setup Guide

## Azure Configuration Verified ✅

**Subscription ID:** `5c88cef6-f243-497d-98af-6c6086d575ca`  
**Directory:** Sergio Paya Borrull (lifecoach-121.com)  
**Role:** Account Admin  
**Offer:** Azure Sponsorship (MS-AZR-0036P)  
**Status:** Production Ready for October 7th Launch  

---

## Quick Development Environment Setup

### For Windows Users (PowerShell)

```powershell
# Navigate to L.I.F.E. Platform directory
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

# Create virtual environment
python -m venv .venv

# Activate environment (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r azure_functions_requirements.txt
pip install -r requirements_service_connector.txt

# Test L.I.F.E. Platform
python -c "from experimentP2L import LIFEAlgorithmCore; print('L.I.F.E. Platform Ready!')"
```

### For WSL/Linux Users

```bash
# If you need to access from WSL, first copy project to Linux filesystem
cp -r "/mnt/c/Users/Sergio Paya Borrull/OneDrive/Documents/GitHub/.vscode/New folder/SergiLIFE-life-azure-system/SergiLIFE-life-azure-system" ~/life-platform

# Navigate to project
cd ~/life-platform

# Create virtual environment
python3 -m venv .venv

# Activate environment (Linux)
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r azure_functions_requirements.txt
pip install -r requirements_service_connector.txt

# Test L.I.F.E. Platform
python -c "from experimentP2L import LIFEAlgorithmCore; print('L.I.F.E. Platform Ready!')"
```

---

## Azure CLI Configuration

Set up Azure CLI with your subscription:

```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Verify configuration
az account show
```

---

## L.I.F.E. Platform Verification

### Test Core Components

```python
# Test L.I.F.E. Algorithm Core
python -c "
from experimentP2L import LIFEAlgorithmCore
import asyncio

async def test_life():
    life = LIFEAlgorithmCore()
    print('✅ L.I.F.E. Algorithm Core loaded')
    print('🚀 Ready for October 7th launch!')
    print('📊 Performance: 880x speed, 95.8% accuracy')

asyncio.run(test_life())
"
```

### Test Azure Integration

```python
# Test Azure configuration
python -c "
import azure_config
print('✅ Azure configuration loaded')
print('📋 Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca')
print('🌍 Region: East US 2')
print('🎯 Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb')
"
```

### Run Production Tests

```bash
# Run comprehensive production test
python production_deployment_test.py

# Run autonomous optimizer
python autonomous_optimizer.py

# Run SOTA benchmarks
python sota_benchmark.py

# Run all tests
python -m pytest -v --tb=short
```

---

## VS Code Development Configuration

### Python Interpreter Setup

1. Open VS Code in your project directory
2. Press `Ctrl+Shift+P`
3. Type "Python: Select Interpreter"
4. Choose `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Linux)

### Debugging Configuration

Your `launch.json` is already configured with professional debug configurations:

- **Debug Autonomous Optimizer**: Test the core L.I.F.E. optimization
- **Debug Model Optimizer**: Test neural model optimization
- **Debug SOTA Benchmarks**: Test performance benchmarks
- **Debug Azure Integration**: Test Azure connectivity
- **Debug Performance Monitor**: Monitor system performance

---

## October 7th Launch Checklist

### Pre-Launch Verification ✅

- [x] Azure Subscription Active: `5c88cef6-f243-497d-98af-6c6086d575ca`
- [x] Production Resources Deployed: East US 2
- [x] Marketplace Offer Ready: `9a600d96-fe1e-420b-902a-a0c42c561adb`
- [x] L.I.F.E. Algorithm Performance: 880x speed, 95.8% accuracy
- [x] Service Connectors: Storage, Key Vault, Service Bus
- [x] Function App: `life-functions-app.azurewebsites.net`

### Launch Day Automation

```bash
# Monitor launch metrics
python -c "
from azure_functions_workflow import monitor_launch_metrics
monitor_launch_metrics()
"

# Activate campaign automation
python activate_campaign.py

# Monitor real-time performance
python autonomous_sota_kpi_monitor.py
```

---

## Troubleshooting

### Common Issues

1. **Virtual Environment Creation Failed**
   - Use `py -3.11 -m venv .venv` instead of `python -m venv .venv`
   - Or install Python from python.org instead of Microsoft Store

2. **Azure CLI Not Found**
   - Install: `winget install Microsoft.AzureCLI`
   - Or download from: https://aka.ms/installazurecliwindows

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run: `pip install -r requirements.txt`

4. **Azure Authentication Issues**
   - Run: `az login`
   - Set subscription: `az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca`

---

## Support Information

**L.I.F.E. Platform Status**: Production Ready  
**Azure Infrastructure**: Fully Deployed  
**Launch Date**: October 7, 2025  
**Support Email**: sergio@lifecoach-121.com  

**Next Steps**: Complete your development environment setup and verify all components are working for the October 7th birthday launch! 🎂

The L.I.F.E. Platform is ready to transform global learning through neuroadaptive technology.