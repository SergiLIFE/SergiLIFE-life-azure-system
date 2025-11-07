# L.I.F.E Platform AI Agent Instructions

**L.I.F.E** (Learning Individually from Experience) is a production neuroadaptive learning platform on Azure Marketplace (`9a600d96-fe1e-420b-902a-a0c42c561adb`).

## Critical File Corruption Issue

**URGENT**: Many core files (including `venturi_gates_system.py`, `requirements.txt`) have encoding corruption. Always handle gracefully:

```python
def safe_read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()
```

## System Architecture

1. **Neural Processing Core** (`algorithms/python-core/experimentP2L_REPAIRED.py`): Complete Azure ML, IoT, and Key Vault integration with EEG processing via dataclasses (`EEGMetrics`, `LearningOutcome`) and enums (`LearningStage`, `NeuralState`). **ALL neural operations MUST be async.**

2. **Unity VR Integration** (`unity/VREnvironmentController.cs`): Real-time VR environment adjustments based on EEG focus and stress levels. Connects to L.I.F.E Platform API for neuroadaptive learning in virtual environments.

3. **Azure ML AutoML Pipeline** (`azure_ml/life_automl_pipeline.py`): Complete AutoML stress classification with AKS deployment, model versioning, and real-time inference capabilities.

4. **Venturi Gates System** (`algorithms/python-core/venturi_gates_system.py`): Three-gate fluid dynamics orchestrator (may be corrupted - handle carefully).

5. **Azure Functions** (`azure_functions/function_app.py`): SaaS marketplace webhooks using Azure Functions v2 (`@app.route`).

6. **Infrastructure** (`infra/*.bicep`): Bicep templates for Azure deployment.

7. **Azure Authentication Helper** (`azure_auth_helper.py`): Simplified Azure CLI installation and authentication assistant.

8. **686+ Python files** in `algorithms/python-core/` - use semantic search to navigate efficiently.

## Essential Development Patterns

### Async Neural Processing (REQUIRED)
```python
# ALL neural operations must be async - core architectural requirement
async def process_eeg_stream(self, eeg_data: np.ndarray) -> EEGMetrics:
    alpha_power = await self._calculate_band_power(eeg_data, 8, 12)
    return EEGMetrics(timestamp=datetime.now(), alpha_power=alpha_power)

# Use dataclasses for immutable metrics
@dataclass
class EEGMetrics:
    timestamp: datetime
    alpha_power: float
    attention_index: float
```

### Windows-First Development
```cmd
# Always use cmd.exe syntax - project is Windows-oriented
python -m venv venv
venv\Scripts\activate  # Note: backslashes, not forward slashes
pip install -r requirements.txt
```

### Directory Creation Pattern
```python
# ALWAYS auto-create directories before file operations
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs("tracking_data/kpis", exist_ok=True)
```

### Azure Authentication (OIDC-Only)
```python
# NO connection strings or .env files - OIDC only
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
# All Azure services use managed identity/service principal
```

## Critical Workflows

### VS Code Task System (100+ Tasks Available)
**Always prefer VS Code tasks over manual commands:**
- `🔬 Run All Tests` - Primary test suite (`pytest -v --tb=short`)
- `⚡ Ultimate Full-Cycle Ecosystem Test` - Complete system validation  
- `🔧 Validate L.I.F.E. Environment` - Environment validation
- `🌐 Flawless Connection Validator` - Azure connection check
- `🧠 Launch L.I.F.E Theory Platform` - Local platform server

### Azure Multi-Tenant Setup
```cmd
az login --allow-no-subscriptions
az account tenant list --output table
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

## Key File Locations & Navigation

### Core Algorithm Files
- `algorithms/python-core/advanced_life_quantum_integration.py` - **NEWEST**: Complete quantum-neural integration with PyTorch transformers, Azure Quantum optimization, circuit breaker patterns, federated learning
- `algorithms/python-core/experimentP2L_REPAIRED.py` - Main L.I.F.E algorithm with complete Azure integration (ML, IoT, Key Vault)
- `algorithms/python-core/life_algorithm_complete_azure_integration.py` - Standalone complete implementation
- `algorithms/python-core/venturi_gates_system.py` - 3-gate fluid dynamics (may be corrupted)
- `algorithms/python-core/campaign_manager.py` - Async campaign operations

### Unity VR Integration
- `unity/UnityAdaptiveLearningManager_Fixed.cs` - **NEWEST**: Advanced Unity VR integration with quantum-neural optimization, real-time EEG adaptation, circuit breaker patterns
- `unity/VREnvironmentController.cs` - Real-time VR environment adjustments based on EEG data
- Unity API endpoint: `https://life-functions-app.azurewebsites.net/api/`
- EEG thresholds: High focus (0.7), Low stress (0.3), Neuroplasticity (0.5)
- Complexity adjustment rate: 0.2 (20% increases)
- **New Features**: Quantum optimization integration, Hjorth parameter processing, circuit breaker fault tolerance

### Azure ML Pipeline
- `azure_ml/life_automl_pipeline.py` - Complete AutoML stress classification pipeline
- Features: 64-channel EEG processing, AKS deployment with auto-scaling (1-10 replicas)
- Model versioning and enterprise registry integration
- GDPR-compliant with model explainability

### Azure Integration
- `azure_functions/function_app.py` - Marketplace webhooks (`@app.route` v2 model)
- `azure_auth_helper.py` - Azure CLI installation and authentication assistant
- `AZURE_CONFIGURATION_GUIDE.md` - Complete Azure setup and authentication guide
- `infra/*.bicep` - Infrastructure as Code templates
- `marketplace_integration_setup.py` - SaaS marketplace automation

### Project Navigation Tips
- **686+ Python files** in `algorithms/python-core/` - use semantic search
- **100+ VS Code tasks** - prefer tasks over manual commands
- **Handle encoding errors** - files may be corrupted, use try/except when reading

## Azure Resources (East US 2)
- **Subscription:** Microsoft Azure Sponsorship (`5c88cef6-f243-497d-98af-6c6086d575ca`)
- **Tenant:** `e716161a-5e85-4d6d-82f9-96bcdd2e65ac`
- Functions: `life-functions-app` (marketplace webhooks)
- Storage: `stlifeplatformprod`
- Key Vault: `kv-life-platform-prod` (EEG-API-KEY, IOT-HUB-CONNECTION-STRING)
- Service Bus: `sb-life-platform-prod`
- ML Workspace: `life-ml-workspace`
- IoT Hub: `life-iot-hub`
- AKS Cluster: `life-aks-cluster` (AutoML model deployment)

## Essential Development Patterns

**Async Neural Processing (CRITICAL):**
```python
# All EEG processing must be async - found in experimentP2L_REPAIRED.py
async def process_eeg_stream(self, eeg_data: np.ndarray) -> EEGMetrics:
    # Use await for neural operations
    alpha_power = await self._calculate_band_power(eeg_data, 8, 12)
    attention_index = await self._calculate_attention_index(alpha_power, beta_power)
    return metrics

# Venturi Gates integration for sub-millisecond processing
venturi_system = create_3_venturi_system()
processed_signal = venturi_system.process_through_gates(eeg_signal)
```

**Dataclass Usage Pattern:**
```python
# All metrics are immutable dataclasses - see experimentP2L_REPAIRED.py
@dataclass
class UserTraits:
    user_id: str
    curiosity: float  # 0.0-1.0
    persistence: float
    openness: float
    processing_speed: float
    learning_efficiency: float

@dataclass 
class EEGMetrics:
    attention_index: float
    learning_efficiency: float
```

**Azure Functions Deployment:**
```cmd
# Deploy with remote build - handles Python version differences
az functionapp deployment source config-zip --name life-functions-app --resource-group life-platform-prod --src deployment.zip --build remote

# Test marketplace webhooks after deployment
curl -X POST https://life-functions-app.azurewebsites.net/api/marketplace-webhook \
  -H "Content-Type: application/json" \
  -d '{"subscriptionId":"test123","action":"Subscribe","planId":"life-individual"}'
```

**Marketplace Integration Pattern:**
```python
# Azure Functions v2 model with SaaS fulfillment - see azure_functions/function_app.py
@app.route(route="marketplace-webhook", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
async def marketplace_webhook(req: func.HttpRequest) -> func.HttpResponse:
    webhook_data = req.get_json()
    subscription_id = webhook_data.get("subscriptionId")
    action = webhook_data.get("action")  # Subscribe, Unsubscribe, ChangePlan
    
    if action == "Subscribe":
        result = await provision_life_platform_access(subscription_id, plan_id)
    # Handle lifecycle events and provision L.I.F.E. platform access
```

**Campaign Manager (Async Pattern):**
```python
# All campaign operations are async - see campaign_manager.py
async def launch_campaign(self, campaign_type: str, target_audience: str) -> str:
    campaign_id = await self._create_campaign_metadata()
    await self.generate_outreach_campaign(target_audience)
    return campaign_id
```

## File Structure & Key Locations

**Core Algorithm Files:**
- `algorithms/python-core/experimentP2L_REPAIRED.py` - Main L.I.F.E algorithm with dataclasses
- `algorithms/python-core/venturi_gates_system.py` - 3-gate fluid dynamics orchestrator
- `algorithms/python-core/azure_config.py` - OIDC-only Azure configuration

**Azure Integration:**
- `azure_functions/function_app.py` - Marketplace webhook handlers (`@app.route` with Python v2 model)
- `infra/main.bicep` - Infrastructure as Code for production deployment
- `marketplace_integration_setup.py` - Automated marketplace setup and configuration
- `AZURE_MARKETPLACE_INTEGRATION_GUIDE.md` - Complete integration documentation

**Infrastructure & Deployment:**
- `infra/` - Complete Bicep templates for multi-environment deployment
- `azure_functions_requirements.txt` - Specific dependencies for Azure Functions runtime
- Automated deployment via `automation/batch-scripts/` for Windows workflows

**Testing & Validation:**
- Use VS Code tasks for common workflows - avoid manual terminal commands
- Directory auto-creation: `os.makedirs(LOGS_DIR, exist_ok=True)` before file operations
- Campaign tracking: `tracking_data/{kpis,outreach,conversions,analytics}/`

**Deployment Notes:**
- Python 3.11 required in Azure (local may be 3.13)  
- OIDC authentication only - no connection strings or environment files
- All secrets in Azure Key Vault: `kv-life-platform-prod`

**Current Project State (November 2025):**
- **ADVANCED QUANTUM-NEURAL INTEGRATION COMPLETE** - Section 2 code fully integrated with PyTorch, Azure Quantum, and advanced EEG processing
- **New Advanced Components Added:**
  - `algorithms/python-core/advanced_life_quantum_integration.py` - Complete quantum-neural system with PyTorch transformers, Azure Quantum optimization, circuit breaker patterns
  - `unity/UnityAdaptiveLearningManager_Fixed.cs` - Advanced Unity VR integration with real-time EEG adaptation and quantum optimization
  - `test_advanced_life_integration.py` - Comprehensive test suite for quantum-neural integration
- **Critical file encoding issues** in `algorithms/python-core/` (venturi_gates_system.py, azure_config.py, campaign_manager.py) - handle with try/except when reading
- **686+ Python files** - use semantic search and file patterns to navigate efficiently  
- **100+ VS Code tasks** defined in `.vscode/tasks.json` - always prefer tasks over manual commands
- **Production marketplace integration** via `marketplace_integration_setup.py` with SaaS fulfillment API
- **Complete Bicep infrastructure** in `infra/` with multi-environment templates (main.bicep, microsoft-demo.bicep)
- **Extensive demo ecosystem** - 7 specialized demo scripts for different market segments (clinical, education, enterprise)

## Critical Development Guidelines

**Testing Requirements:**
- **Always** run 100-cycle EEG test before committing neural processing changes
- **Use VS Code tasks exclusively** - 100+ available tasks with emojis for easy identification
- **Primary validation flow:** `🔧 Validate L.I.F.E. Environment` → `🔬 Run All Tests` → `⚡ Ultimate Full-Cycle Ecosystem Test`
- **Azure connection validation:** `🌐 Flawless Connection Validator` before any deployment
- **Demo testing:** 7 specialized demo tasks for market segments (🏥 Hospital EEG, 🎓 Education K-12, 🏢 Enterprise AI)
- **Marketplace webhook testing:** Use curl commands from `AZURE_MARKETPLACE_INTEGRATION_GUIDE.md`

**Import Patterns:**
- **Handle encoding errors gracefully:** Use try/except blocks when importing from `algorithms/python-core/`
- Long filenames: `from algorithms.python_core import experimentP2L_REPAIRED`
- Venturi system: `from algorithms.python_core.venturi_gates_system import create_3_venturi_system`
- Azure integration: `from azure_functions.function_app import app`
- **Campaign system:** `from algorithms.python_core.campaign_manager import CampaignManager`

**Deployment Checklist:**
1. **Validate environment:** VS Code task `🔧 Validate L.I.F.E. Environment`
2. **Test neural core:** Direct Python import with async validation
3. **Deploy to staging:** Use Bicep templates in `infra/`
4. **Marketplace integration:** Follow `marketplace_integration_setup.py` workflow
5. **Production deployment:** Remote build with Azure CLI

**File Navigation Tips:**
- **Use semantic search** for finding specific patterns across 686+ Python files
- **File patterns:** Core algorithms in `algorithms/python-core/`, infrastructure in `infra/`
- **Encoding issues:** Handle gracefully with try/except when reading corrupted files
