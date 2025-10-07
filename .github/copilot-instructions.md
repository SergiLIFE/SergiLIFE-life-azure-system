# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)


## Project-Specific Conventions

- **Logging:** All logs are Unicode-safe, ASCII-only, and exported for compliance. Scripts auto-create `logs/` directory with absolute paths (e.g., `logs/life_benchmark.log`, `logs/autonomous_optimizer.log`).

```python
# Always use dataclasses for neural metrics
@dataclass
class EEGMetrics:
    timestamp: datetime
    alpha_power: float
    # ... 8 more required fields


# Async for ALL EEG processing
async def process_eeg_stream(self, eeg_data: np.ndarray) -> EEGMetrics:
    # Band power extraction: alpha (8-12Hz), beta (12-30Hz), etc.
    alpha_power = self._calculate_band_power(eeg_data, 8, 12)
```



### 📊 **Performance Metrics (Latest Validation)**

```
✅ Production Deployment Test Results
   ├── Core Algorithm Test: PASSED
   ├── Azure Functions Test: PASSED
   ├── EEG Data Pipeline Test: PASSED
   ├── Enterprise Analytics Test: PASSED
   ├── Security & Compliance Test: PASSED
   ├── Performance Benchmarking: PASSED
   ├── Overall Status: PRODUCTION_READY
   └── Success Rate: 100.0%
```

### 🎯 **Launch Readiness Status**

- **Marketplace Certification:** 9/9 sections complete ✅
- **Azure Infrastructure:** Fully deployed and operational ✅
- **Code Optimization:** Production deployment tests passed ✅
- **Documentation:** Complete and ready for customers ✅
- **Launch Date:** September 27, 2025 (6 days remaining) 🚀

## Examples

- To run a full validation cycle:
  - `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- To deploy to Azure:
  - `azd up` (after running `setup-azure-oidc.ps1`)

---


