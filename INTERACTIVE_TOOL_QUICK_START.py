#!/usr/bin/env python3
"""
INTERACTIVE EEG DATA INGESTION TOOL - QUICK REFERENCE

🧠 Real-time search, download & upload EEG datasets from PhysioNet & Open Science

═══════════════════════════════════════════════════════════════════════════════

🚀 INSTALLATION (1 MINUTE)

pip install pyedflib requests scipy numpy

# Optional: Azure upload
pip install azure-storage-blob azure-identity

═══════════════════════════════════════════════════════════════════════════════

▶️ RUN THE TOOL

python interactive_eeg_ingestion_tool.py

═══════════════════════════════════════════════════════════════════════════════

📊 DATASET TYPES (Choose from menu)

1. Motor Imagery          → BCI IV-2a (9 subjects, 250 Hz)
2. Sleep Staging        → Sleep-EDF (197 subjects, 100 Hz)
3. Brain-Heart Coupling → EEG-ECG (109 subjects, 256 Hz)
4. Seizure Detection    → CHB-MIT, TUH (24-109 subjects)
5. Abnormality Detection → TUH (200 subjects)
6. Neuroplasticity      → Motor learning (9 subjects)
7. Resting State        → OpenNeuro (300+ subjects)
8. Cognitive Tasks      → N-back, working memory (200+ subjects)
9. Pathological EEG     → Seizure/epilepsy clinical data

═══════════════════════════════════════════════════════════════════════════════

⚡ WORKFLOW

1. Run tool
   python interactive_eeg_ingestion_tool.py

2. Select dataset type
   Enter: 1 (Motor Imagery)

3. Select specific dataset
   Enter: 1 (BCI IV-2a)

4. Enter subject number
   Enter: 1

5. (Optional) Enter session
   Enter: 1

6. (Optional) Upload to Azure
   Enter: y/n

7. (Optional) Process with L.I.F.E.
   Enter: y/n

RESULT: ✅ Downloaded, processed, and ready to use!

═══════════════════════════════════════════════════════════════════════════════

🔍 KEYWORD SEARCH

Menu Option: Search by keyword (Option 8)

Examples:
  motor    → All motor imagery datasets
  sleep    → All sleep-related datasets
  seizure  → All seizure/epilepsy datasets
  cognitive → All cognitive task datasets
  abnormal → All abnormality detection datasets

═══════════════════════════════════════════════════════════════════════════════

📁 FILES SAVED

Local cache: physionet_cache/
  bci_iv_2a_S001_session1.edf
  sleep_edf_S001_session1.edf
  ... (auto-cached for fast access)

Azure (if uploaded):
  https://stlifeplatformprod.blob.core.windows.net/eeg-data/[dataset]/[subject].edf

═══════════════════════════════════════════════════════════════════════════════

📊 OUTPUT AFTER DOWNLOAD

Quality Assessment:
  Score: 87.5/100
  SNR: 14.2 dB
  Peak-to-Peak: 156.3 µV

Frequency Analysis:
  Delta (0.5-4 Hz):    8.2%
  Theta (4-8 Hz):     12.1%
  Alpha (8-12 Hz):    18.7%
  Beta (12-30 Hz):    42.3%
  Gamma (30-100 Hz):  18.7%

Artifact Detection:
  Blinks: 127 (3.2%)
  Muscle: 0.045 units
  Line Noise: Clear

═══════════════════════════════════════════════════════════════════════════════

💻 EXAMPLE SESSION

$ python interactive_eeg_ingestion_tool.py

🧠 L.I.F.E. Interactive EEG Data Ingestion Tool
════════════════════════════════════════════════

📊 Select EEG Dataset Type:

  1. Motor Imagery
  2. Sleep Staging
  3. EEG-ECG Coupling
  ...
  10. Search by keyword
  11. List all datasets
  12. Exit

👉 Enter your choice: 1

📊 Motor Imagery - Available Sources:

  1. BCI Competition IV-2a (9 subjects, 22 channels, 250 Hz)

👉 Select source: 1

📊 Dataset: BCI Competition IV-2a
════════════════════════════════════════════════════════════════════════════════
Source:          PhysioNet
Subjects:        9
Channels:        22
Sampling Rate:   250 Hz
Description:     Motor imagery EEG during movement imagination
Paper:           https://doi.org/10.1109/TNSRE.2008.927637
URL:             https://physionet.org/files/eegmmidb/1.0.0

👉 Enter subject ID (1-9): 1

👉 Enter session ID (1-2): 1

⏳ Starting download...

📥 Downloading bci_iv_2a...
   Subject: 1
   Session: 1

📡 Connecting to PhysioNet...
📊 File size: 4.32 MB
Progress: 100.0% (4.32/4.32 MB)

✅ Downloaded 4.32 MB (4537344 bytes)

✅ Saved locally: physionet_cache/bci_iv_2a_S001_session1.edf

❓ Upload to Azure Blob Storage? (y/n): y

📤 Preparing Azure upload...
   Container: eeg-data
   Dataset: BCI IV-2a

📡 Uploading to Azure...
   URL: https://stlifeplatformprod.blob.core.windows.net/eeg-data/PhysioNet/BCI IV-2a/S001.edf

✅ Successfully uploaded to Azure!

❓ Process with L.I.F.E. algorithm? (y/n): y

🧠 Processing with L.I.F.E. algorithm...

✅ Processing Complete!

📊 Quality Assessment:
   Score: 87.5/100
   Rating: Good
   SNR: 14.2 dB

📈 Frequency Analysis:
   DELTA: 8.2%
   THETA: 12.1%
   ALPHA: 18.7%
   BETA: 42.3%
   GAMMA: 18.7%

═══════════════════════════════════════════════════════════════════════════════

🎯 QUICK COMMANDS

# Just download (no upload/processing)
# Response to prompts: 1 → 1 → 1 → 1 → n → n

# Full pipeline (download + upload + process)
# Response to prompts: 1 → 1 → 1 → 1 → y → y

# Search for motor imagery
# Response to prompts: 8 → "motor" → 1

═══════════════════════════════════════════════════════════════════════════════

❓ FAQ

Q: Which dataset should I start with?
A: BCI IV-2a (Motor Imagery) - smallest (4.3 MB), fast download

Q: How long does download take?
A: 30 seconds - 5 minutes depending on file size and connection

Q: Can I cancel the download?
A: Press Ctrl+C to interrupt (files are cached, try again to resume)

Q: Where are files stored?
A: physionet_cache/ directory (auto-created)

Q: Can I delete cached files?
A: Yes, delete physionet_cache/ and redownload

Q: Do I need Azure for this to work?
A: No - Azure upload is optional

Q: What if PhysioNet is slow?
A: Tool has 60-second timeout, try again later

Q: Can I process multiple subjects automatically?
A: Not via menu - see advanced usage in INTERACTIVE_INGESTION_TOOL_GUIDE.md

═══════════════════════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING

Connection timeout?
  → Check internet connection
  → PhysioNet may be slow, try again
  → File is cached, retry uses cache

Invalid subject ID?
  → Check available range shown in menu
  → BCI IV-2a has 9 subjects (1-9)
  → Sleep-EDF has 197 subjects (1-197)

Azure upload fails?
  → Run: az login
  → Check Azure credentials
  → Ensure stlifeplatformprod storage account access

Missing dependencies?
  → pip install pyedflib requests scipy numpy

═══════════════════════════════════════════════════════════════════════════════

📚 DETAILED DOCUMENTATION

For complete information, see:
  INTERACTIVE_INGESTION_TOOL_GUIDE.md

═══════════════════════════════════════════════════════════════════════════════

✨ FEATURES

✓ Real-time dataset discovery
✓ Interactive menu system
✓ Download progress tracking
✓ Multi-dataset support (9+ types)
✓ Azure integration
✓ L.I.F.E. algorithm ready
✓ Keyword search
✓ Automatic caching
✓ Error recovery
✓ Production-ready

═══════════════════════════════════════════════════════════════════════════════

🚀 START NOW!

python interactive_eeg_ingestion_tool.py

═══════════════════════════════════════════════════════════════════════════════

Status: ✅ Production Ready
Last Updated: October 17, 2025
"""

if __name__ == "__main__":
    print(__doc__)
