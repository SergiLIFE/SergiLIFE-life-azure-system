# Neuroadaptive Cloud Deployment (Azure Functions + IoT + Dashboard)

This guide packages and deploys the L.I.F.E neuroadaptive features to Azure.

## Build the deployment package

Windows (cmd.exe):

```
python build_deployment_package.py
```

Output: `deployment_package.zip`

## Deploy to Azure Functions (config-zip)

Replace placeholders with your values:

```
az functionapp deployment source config-zip ^
  --resource-group life-platform-prod ^
  --name <your-function-app-name> ^
  --src deployment_package.zip
```

## Stream EEG via IoT Hub (device-side)

```
set AZURE_IOTHUB_DEVICE_CONNECTION_STRING=HostName=...;DeviceId=...;SharedAccessKey=...
```

Python snippet:

```python
import asyncio, json, random
from eeg_iothub_stream import stream_eeg_to_platform

async def demo_headset():
    # Async generator yielding EEG samples
    while True:
        sample = {"ts": 0, "channels": [random.uniform(-5,5) for _ in range(8)]}
        yield sample
        await asyncio.sleep(0.0039)

asyncio.run(stream_eeg_to_platform(demo_headset()))
```

## Add dashboard tab

Include `dashboard_tab_neuroadaptive.html` into your dashboard and ensure `eeg_dashboard.js` is loaded.

## KPIs

Import `kpi_monitor.py` and call `compute_kpis(...)` for simple metrics.

## Clinical Validation

```python
from clinical_validation_framework import ClinicalValidationFramework
life_algo_equations = {"eq2": lambda mean_signal=0.0, **_: mean_signal/10.0}
clinical_validator = ClinicalValidationFramework(life_algo_equations)
trial_config = clinical_validator.design_clinical_trial(
    primary_endpoint="attention_improvement",
    secondary_endpoints=["academic_performance", "self_regulation"],
    effect_size=0.5,
    power=0.8,
)

# Sample EEG data list
patient_eeg_data = [10.0, 12.0, 15.0]
summary = asyncio.run(clinical_validator.validate_all_equations(patient_eeg_data, clinical_threshold=0.95))
print(summary)
```
