# PhysioNet & Open Science EEG Data Ingestion - Reference Card

## 🚀 Installation (1 minute)

```bash
# Install required packages
pip install pyedflib requests scipy numpy

# Verify installation
python -c "import pyedflib, requests; print('✅ Ready')"
```

## ⚡ Quick Commands

### Download & Process in 3 Lines
```python
from physionet_eeg_ingest import PhysioNetIngestor
import asyncio

async def quick_process():
    ingestor = PhysioNetIngestor()
    eeg_data = await ingestor.download_dataset("bci_iv_2a", subject_id=1)
    eeg_array, metadata = ingestor.parse_edf_file("temp.edf")
    results = ingestor.process_eeg_signal(eeg_array[0])
    print(f"Quality: {results['quality']['score']:.1f}/100")

asyncio.run(quick_process())
```

## 📊 Dataset Codes

| Code | Dataset | Subjects | Channels | Use |
|------|---------|----------|----------|-----|
| `bci_iv_2a` | Motor Imagery | 9 | 22 | Training |
| `sleep_edf` | Sleep Staging | 197 | 2 | Sleep |
| `eeg_ecg_coupling` | Brain-Heart | 109 | 64 | Autonomic |
| `pt_seizure` | Seizure (CHB-MIT) | 24 | 23 | Clinical |
| `temple_university_seizure` | TUH Hospital | 109 | 21 | Abnormality |

## 🔍 Key Methods

### Download
```python
# Download specific dataset
eeg_data = await ingestor.download_dataset(
    "bci_iv_2a",        # dataset code
    subject_id=1,       # subject number
    session=1           # session (if applicable)
)
```

### Parse
```python
# Parse EDF file
eeg_array, metadata = ingestor.parse_edf_file(
    "filename.edf",     # file path
    channels=None       # optional: specific channels
)
# Returns: (ndarray of channels×samples, dict of metadata)
```

### Process
```python
# Process EEG signal
results = ingestor.process_eeg_signal(
    raw_signal,         # numpy array of signal
    sampling_rate=250   # Hz (default 250)
)
# Returns: dict with quality, frequency, artifacts, processed
```

### Export
```python
from physionet_eeg_ingest import DataFormatConverter
converter = DataFormatConverter()

# CSV
converter.numpy_to_csv(eeg_array, "out.csv", channel_names=[...])

# NumPy
converter.numpy_to_npy(eeg_array, "out.npy")

# Load CSV
data = converter.csv_to_numpy("in.csv", skip_header=1)
```

## 📈 Results Structure

```python
results = {
    "quality": {
        "score": 87.5,              # 0-100
        "rating": "Good",           # Excellent/Good/Fair/Poor
        "snr_db": 14.2,             # Signal-to-noise ratio
        "peak_to_peak_uv": 156.3,   # Voltage range
        "variance": 892.4           # Signal stability
    },
    "frequency": {
        "delta_power_percent": 8.2,
        "theta_power_percent": 12.1,
        "alpha_power_percent": 18.7,
        "beta_power_percent": 42.3,
        "gamma_power_percent": 18.7
    },
    "artifacts": {
        "blink_events": 127,
        "blink_percentage": 3.2,
        "muscle_artifact_power": 0.045,
        "line_noise_present": False
    },
    "processed": {
        "filtered_signal": [...],   # First 1000 samples
        "filter_type": "Butterworth 4th order",
        "frequency_range_hz": "0.5-40",
        "rms_after_filter": 45.2
    }
}
```

## 🎯 Common Workflows

### Single Subject Download & Analysis
```python
async def analyze_one():
    ingestor = PhysioNetIngestor()
    # Download
    data = await ingestor.download_dataset("bci_iv_2a", subject_id=1, session=1)
    # Parse
    eeg_array, metadata = ingestor.parse_edf_file("temp.edf")
    # Process
    results = ingestor.process_eeg_signal(eeg_array[0])
    return results
```

### Batch Process All Subjects
```python
async def batch_all():
    ingestor = PhysioNetIngestor()
    all_results = []
    
    for subj in range(1, 10):  # 9 subjects
        data = await ingestor.download_dataset("bci_iv_2a", subject_id=subj)
        eeg_array, meta = ingestor.parse_edf_file(f"S{subj}.edf")
        results = ingestor.process_eeg_signal(eeg_array[0])
        all_results.append(results)
    
    return all_results
```

### Process All Channels
```python
def process_all_channels(eeg_array, sampling_rate=250):
    ingestor = PhysioNetIngestor()
    results = []
    
    for channel_idx in range(eeg_array.shape[0]):
        channel_results = ingestor.process_eeg_signal(
            eeg_array[channel_idx],
            sampling_rate=sampling_rate
        )
        results.append(channel_results)
    
    return results
```

### Integrate with L.I.F.E.
```python
async def life_integration():
    from experimentP2L import LIFEAlgorithmCore
    from physionet_eeg_ingest import PhysioNetIngestor
    
    # Ingest
    ingestor = PhysioNetIngestor()
    eeg_data = await ingestor.download_dataset("bci_iv_2a", subject_id=1)
    eeg_array, meta = ingestor.parse_edf_file("temp.edf")
    
    # Process with PhysioNet
    physionet_results = ingestor.process_eeg_signal(eeg_array[0])
    
    # Process with L.I.F.E.
    life = LIFEAlgorithmCore()
    life_results = await life.process_eeg_stream(eeg_array)
    
    # Combine
    combined = {
        "physionet": physionet_results,
        "life": life_results
    }
    
    return combined
```

## 🏥 Signal Quality Quick Reference

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| Quality Score | >85 | 70-85 | 50-70 | <50 |
| SNR (dB) | >15 | 10-15 | 5-10 | <5 |
| Peak-to-Peak (µV) | 50-200 | 30-250 | 20-300 | <20\|>300 |
| Blink % | <2% | 2-5% | 5-10% | >10% |

## 🧠 EEG Band Interpretation

| Band | Hz Range | Typical % | Indicates |
|------|----------|-----------|-----------|
| Delta | 0.5-4 | 5-10% | Deep sleep |
| Theta | 4-8 | 10-20% | Drowsiness, learning |
| Alpha | 8-12 | 15-30% | Relaxation, idling |
| Beta | 12-30 | 30-50% | Motor control, focus |
| Gamma | 30-100 | 5-20% | Cognition, perception |

## ⚙️ Configuration

### Modify Sampling Rate
```python
# Default is 250 Hz for BCI IV-2a
results = ingestor.process_eeg_signal(
    eeg_array[0],
    sampling_rate=100  # For Sleep-EDF
)
```

### Specify Channels
```python
# Select specific channels from file
eeg_array, metadata = ingestor.parse_edf_file(
    "temp.edf",
    channels=[0, 1, 2]  # Only first 3 channels
)
```

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `ImportError: pyedflib` | `pip install pyedflib` |
| Timeout downloading | Check internet, try again (files cached) |
| No EEG channels found | Different naming convention, try channels param |
| Memory error | Process channels individually or use shorter windows |
| Connection refused | PhysioNet server temporarily down, wait and retry |

## 📊 Live Demo

Run interactive menu:
```bash
python physionet_life_integration.py
```

Choose:
- **Option 1:** Quick single subject demo
- **Option 2:** Batch process all 9 subjects
- **Option 3:** Data export examples
- **Option 4:** Run all examples

## 📚 Full Documentation

See `PHYSIONET_EEG_INGESTION_GUIDE.md` for:
- Complete API reference
- Dataset specifications
- Installation troubleshooting
- Clinical data standards
- Advanced integration examples

## 🔗 External Resources

- **PhysioNet:** https://physionet.org/
- **BCI Competition IV:** https://www.bbci.de/competition/iv/
- **OpenNeuro:** https://openneuro.org/
- **EDF Format:** https://www.edfplus.info/
- **MNE-Python:** https://mne.tools/

---

**Last Updated:** October 17, 2025  
**Status:** ✅ Production Ready
