# MNE-Python Demo Data Download & Preprocessing Documentation

**Date:** October 12, 2025  
**Purpose:** Documentation for L.I.F.E. Platform October 15 Demo

---

## Overview

MNE-Python provides sample EEG datasets that can be used for demonstrations without requiring physical EEG hardware.

---

## Quick Reference: Sample Datasets Available

### 1. **Sample Dataset** (Recommended for demos)
- **Type:** Auditory/visual experiment
- **Channels:** 60 EEG channels
- **Duration:** ~15 minutes
- **Download:** Automatic via MNE

```python
import mne

# Download sample dataset
sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = sample_data_folder / 'MEG' / 'sample' / 'sample_audvis_raw.fif'
raw = mne.io.read_raw_fif(sample_data_raw_file)
```

### 2. **EEGBCIDataset** (Motor imagery)
- **Type:** Motor imagery (left/right hand)
- **Channels:** 22 EEG channels
- **Subjects:** Multiple subjects available

### 3. **PhysioNet Motor Movement/Imagery**
- **Type:** Motor tasks and imagery
- **Channels:** 64 EEG channels
- **Download:** Via MNE datasets

---

## Basic Preprocessing Steps

### Step 1: Load Raw Data
```python
import mne

raw = mne.io.read_raw_fif('sample_audvis_raw.fif', preload=True)
```

### Step 2: Filter Data
```python
# Bandpass filter: 0.5-50 Hz (removes DC drift and high-frequency noise)
raw.filter(l_freq=0.5, h_freq=50.0)
```

### Step 3: Set Montage (Electrode Positions)
```python
# Standard 10-20 system
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)
```

### Step 4: Extract Epochs
```python
# Find events in the data
events = mne.find_events(raw)

# Create epochs (segments) around events
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, baseline=(None, 0))
```

### Step 5: Compute Power Spectral Density
```python
# Calculate frequency band power
psd = epochs.compute_psd(fmin=0.5, fmax=50)
```

---

## Integration with L.I.F.E. Algorithm

The preprocessed MNE data feeds directly into `LIFEAlgorithmCore.process_eeg_stream()`:

```python
from experimentP2L import LIFEAlgorithmCore
import asyncio

life = LIFEAlgorithmCore()

# Convert MNE epoch to numpy array
eeg_data = epochs.get_data()[0]  # Shape: (channels, time_points)

# Process with L.I.F.E. algorithm
metrics = asyncio.run(life.process_eeg_stream(eeg_data))

print(f"Coherence: {metrics.coherence}")
print(f"Attention: {metrics.attention_index}")
print(f"Learning Efficiency: {metrics.learning_efficiency}")
```

---

## Demo Scenarios

### Healthcare Demo
- **Dataset:** Sample auditory/visual
- **Focus:** Attention monitoring during cognitive tasks
- **Metrics:** Alpha power, attention index

### Education Demo
- **Dataset:** Motor imagery
- **Focus:** Learning progress tracking
- **Metrics:** Learning efficiency, neural state transitions

### Enterprise Demo
- **Dataset:** Resting state EEG
- **Focus:** Cognitive load assessment
- **Metrics:** Beta/gamma ratio, coherence

---

## File Locations

**Sample Data Storage:**
- Windows: `C:\Users\{username}\mne_data\`
- Downloaded automatically on first use
- ~1.5 GB for sample dataset

**L.I.F.E. Results:**
- Logs: `logs/life_demo.log`
- Results: `results/mne_demo_results.json`

---

## Quick Start Commands (Documentation Only)

**No code execution needed - for reference only:**

```bash
# Install MNE (if needed)
pip install mne

# Python script to download and preprocess
python mne_demo_preprocess.py
```

---

## Demo Day Checklist

- [ ] MNE-Python installed (`pip show mne`)
- [ ] Sample dataset downloaded (~1.5 GB)
- [ ] Preprocessing script tested
- [ ] L.I.F.E. algorithm integration verified
- [ ] Results visualization ready

---

## Troubleshooting

**Issue:** Download fails  
**Solution:** Use `mne.datasets.sample.data_path(force_update=True)`

**Issue:** Memory error  
**Solution:** Use `raw.crop(tmax=60)` to limit duration

**Issue:** Missing channels  
**Solution:** Use `raw.pick_types(eeg=True)` to select EEG only

---

## References

- MNE-Python: https://mne.tools
- Sample Dataset: https://mne.tools/stable/overview/datasets_index.html
- L.I.F.E. Algorithm: `experimentP2L.I.F.E...py`

---

**Copyright 2025 - Sergio Paya Borrull**  
**L.I.F.E. Platform - Demo Documentation**
