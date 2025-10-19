#!/usr/bin/env python3
"""
PhysioNet & Open Science EEG Data Ingestion System
L.I.F.E Platform - Real EEG Scan Test Results Loader

Supports:
- PhysioNet BCI Competition IV-2a (Motor Imagery)
- PhysioNet Sleep-EDF (Sleep staging)
- PhysioNet EEG-ECG Coupling
- OpenNeuro EEG datasets
- Custom EDF/CSV uploads

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import requests
from scipy import signal

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class EEGDataset:
    """EEG Dataset metadata"""

    name: str
    source: str  # physionet, openneuro, local
    subject_id: str
    session: str
    channels: int
    sampling_rate: float
    duration_seconds: float
    data_format: str  # edf, csv, npy
    clinical_notes: str = ""
    dataset_url: str = ""


@dataclass
class EEGScanResult:
    """Ingested EEG scan result"""

    dataset: EEGDataset
    raw_signal: np.ndarray  # Shape: (channels, samples)
    processed_signal: np.ndarray
    quality_metrics: Dict
    frequency_analysis: Dict
    artifact_detection: Dict
    timestamp: str
    file_path: str


class PhysioNetIngestor:
    """PhysioNet & Open Science EEG Data Ingestion"""

    # PhysioNet dataset URLs
    PHYSIONET_DATASETS = {
        "bci_iv_2a": {
            "url_base": "https://physionet.org/files/eegmmidb/1.0.0",
            "description": "BCI Competition IV-2a: Motor Imagery EEG",
            "subjects": 9,
            "channels": 22,
            "sampling_rate": 250,
        },
        "sleep_edf": {
            "url_base": "https://physionet.org/files/sleep-edfx/1.0.0",
            "description": "Sleep-EDF: Sleep staging with EEG",
            "subjects": 197,
            "channels": 2,
            "sampling_rate": 100,
        },
        "eeg_ecg_coupling": {
            "url_base": "https://physionet.org/files/eegmmidb/1.0.0",
            "description": "EEG-ECG coupling during rest",
            "subjects": 109,
            "channels": 64,
            "sampling_rate": 256,
        },
        "pt_seizure": {
            "url_base": "https://physionet.org/files/chbmit/1.0.0",
            "description": "Seizure data (CHB-MIT scalp EEG)",
            "subjects": 24,
            "channels": 23,
            "sampling_rate": 256,
        },
        "temple_university_seizure": {
            "url_base": "https://physionet.org/files/tuh_eeg/1.0.0",
            "description": "Temple University Hospital EEG",
            "subjects": 109,
            "channels": 21,
            "sampling_rate": 250,
        },
    }

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="physionet_")
        self.cache_dir = Path("physionet_cache")
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"PhysioNet Ingestor initialized. Cache: {self.cache_dir}")

    async def download_dataset(
        self, dataset_name: str, subject_id: int = 1, session: int = 1
    ) -> Optional[bytes]:
        """Download EEG data from PhysioNet"""

        if dataset_name not in self.PHYSIONET_DATASETS:
            logger.error(f"Unknown dataset: {dataset_name}")
            return None

        dataset_info = self.PHYSIONET_DATASETS[dataset_name]
        logger.info(f"Downloading {dataset_name}: {dataset_info['description']}")

        try:
            if dataset_name == "bci_iv_2a":
                return await self._download_bci_iv_2a(subject_id, session)
            elif dataset_name == "sleep_edf":
                return await self._download_sleep_edf(subject_id)
            elif dataset_name == "eeg_ecg_coupling":
                return await self._download_eeg_ecg(subject_id)
            elif dataset_name == "pt_seizure":
                return await self._download_chb_mit(subject_id)
            elif dataset_name == "temple_university_seizure":
                return await self._download_tuh(subject_id)

        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None

    async def _download_bci_iv_2a(self, subject: int, session: int) -> Optional[bytes]:
        """Download BCI Competition IV-2a data"""
        url = (
            f"{self.PHYSIONET_DATASETS['bci_iv_2a']['url_base']}/S{subject:03d}/"
            f"S{subject:03d}R{session:02d}.edf"
        )

        try:
            logger.info(f"Fetching: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            logger.info(f"Downloaded {len(response.content)} bytes")
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download from {url}: {e}")
            return None

    async def _download_sleep_edf(self, subject: int) -> Optional[bytes]:
        """Download Sleep-EDF data"""
        # Sleep-EDF structure: sleep-cassette/SC4nnnE0-PSG.edf or SC4nnnEC-PSG.edf
        url = (
            f"{self.PHYSIONET_DATASETS['sleep_edf']['url_base']}/sleep-cassette/"
            f"SC4{subject:03d}E0-PSG.edf"
        )

        try:
            logger.info(f"Fetching Sleep-EDF: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download Sleep-EDF: {e}")
            return None

    async def _download_eeg_ecg(self, subject: int) -> Optional[bytes]:
        """Download EEG-ECG coupling data"""
        url = (
            f"{self.PHYSIONET_DATASETS['eeg_ecg_coupling']['url_base']}/S{subject:03d}/"
            f"S{subject:03d}R02.edf"
        )

        try:
            logger.info(f"Fetching EEG-ECG: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download EEG-ECG: {e}")
            return None

    async def _download_chb_mit(self, subject: int) -> Optional[bytes]:
        """Download CHB-MIT Seizure data"""
        url = (
            f"{self.PHYSIONET_DATASETS['pt_seizure']['url_base']}/chb{subject:02d}/"
            f"chb{subject:02d}_01.edf"
        )

        try:
            logger.info(f"Fetching CHB-MIT: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download CHB-MIT: {e}")
            return None

    async def _download_tuh(self, subject: int) -> Optional[bytes]:
        """Download Temple University Hospital data"""
        # TUH structure more complex, using simplified path
        url = (
            f"{self.PHYSIONET_DATASETS['temple_university_seizure']['url_base']}/"
            f"dev/abnormal/01_tcp_le/000/{subject:06d}.edf"
        )

        try:
            logger.info(f"Fetching TUH: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download TUH: {e}")
            return None

    def parse_edf_file(
        self, file_path: str, channels: Optional[List[int]] = None
    ) -> Tuple[np.ndarray, Dict]:
        """Parse EDF file and extract EEG data"""

        try:
            from pyedflib import EdfReader

            reader = EdfReader(file_path)

            # Get signal info
            n_signals = reader.signals_in_file
            signal_labels = reader.getSignalLabels()

            logger.info(f"EDF file has {n_signals} signals: {signal_labels}")

            # Extract EEG channels (typically labeled with EEG prefix)
            eeg_channels_idx = [
                i for i, label in enumerate(signal_labels) if "EEG" in label.upper()
            ]

            if not eeg_channels_idx:
                # Fallback: use first channels
                eeg_channels_idx = list(range(min(22, n_signals)))

            if channels:
                eeg_channels_idx = eeg_channels_idx[: len(channels)]

            # Read signals
            eeg_data = []
            for idx in eeg_channels_idx:
                signal_data = reader.readSignal(idx)
                eeg_data.append(signal_data)

            reader.close()

            eeg_array = np.array(eeg_data)

            # Get metadata
            metadata = {
                "n_channels": len(eeg_data),
                "total_signals": n_signals,
                "signal_labels": signal_labels,
                "eeg_channels": [signal_labels[i] for i in eeg_channels_idx],
                "duration_sec": reader.file_duration,
                "sampling_rate": reader.getSampleFrequency(eeg_channels_idx[0]),
            }

            logger.info(f"Parsed EDF: {metadata}")
            return eeg_array, metadata

        except ImportError:
            logger.error("pyedflib not installed. Install with: pip install pyedflib")
            return None, None
        except Exception as e:
            logger.error(f"Failed to parse EDF: {e}")
            return None, None

    def process_eeg_signal(
        self, raw_signal: np.ndarray, sampling_rate: float = 250
    ) -> Dict:
        """Process raw EEG signal"""

        results = {}

        try:
            # 1. Quality assessment
            results["quality"] = self._assess_signal_quality(raw_signal)

            # 2. Frequency analysis
            results["frequency"] = self._analyze_frequency_bands(
                raw_signal, sampling_rate
            )

            # 3. Artifact detection
            results["artifacts"] = self._detect_artifacts(raw_signal)

            # 4. Signal processing
            results["processed"] = self._apply_filters(raw_signal, sampling_rate)

            logger.info(
                f"Signal processing complete. Quality: {results['quality']['score']:.2f}"
            )

        except Exception as e:
            logger.error(f"Signal processing error: {e}")

        return results

    def _assess_signal_quality(self, signal_data: np.ndarray) -> Dict:
        """Assess EEG signal quality"""

        metrics = {}

        # Signal-to-noise ratio estimation
        signal_rms = np.sqrt(np.mean(signal_data**2))
        noise_rms = np.sqrt(np.mean(np.diff(signal_data) ** 2)) / np.sqrt(2)
        metrics["snr_db"] = 20 * np.log10(signal_rms / (noise_rms + 1e-10))

        # Peak-to-peak voltage
        metrics["peak_to_peak_uv"] = np.max(signal_data) - np.min(signal_data)

        # Signal variance
        metrics["variance"] = np.var(signal_data)

        # Score out of 100
        snr_score = min(100, max(0, (metrics["snr_db"] + 20) * 2))
        pp_score = 100 if 10 < metrics["peak_to_peak_uv"] < 300 else 50
        var_score = min(100, metrics["variance"] / 10)

        metrics["score"] = (snr_score + pp_score + var_score) / 3
        metrics["rating"] = (
            "Excellent"
            if metrics["score"] > 80
            else (
                "Good"
                if metrics["score"] > 60
                else "Fair" if metrics["score"] > 40 else "Poor"
            )
        )

        return metrics

    def _analyze_frequency_bands(
        self, signal_data: np.ndarray, sampling_rate: float
    ) -> Dict:
        """Analyze EEG frequency bands"""

        # Compute FFT
        freqs = np.fft.rfftfreq(len(signal_data), 1 / sampling_rate)
        fft_vals = np.abs(np.fft.rfft(signal_data))

        # Define bands
        bands = {
            "delta": (0.5, 4),  # Deep sleep
            "theta": (4, 8),  # Drowsiness
            "alpha": (8, 12),  # Relaxation
            "beta": (12, 30),  # Alertness
            "gamma": (30, 100),  # Cognition
        }

        results = {}
        total_power = np.sum(fft_vals**2)

        for band_name, (low, high) in bands.items():
            mask = (freqs >= low) & (freqs <= high)
            band_power = np.sum(fft_vals[mask] ** 2)
            results[f"{band_name}_power_percent"] = 100 * band_power / total_power
            results[f"{band_name}_peak_freq"] = (
                freqs[np.argmax(fft_vals[mask])] if np.any(mask) else 0
            )

        return results

    def _detect_artifacts(self, signal_data: np.ndarray) -> Dict:
        """Detect common EEG artifacts"""

        artifacts = {}

        # Eye blinks: high amplitude peaks
        threshold = 5 * np.std(signal_data)
        blink_count = np.sum(np.abs(signal_data) > threshold)
        artifacts["blink_events"] = int(blink_count)
        artifacts["blink_percentage"] = 100 * blink_count / len(signal_data)

        # Muscle artifacts: high-frequency bursts
        # Simple: check for sustained high variance in 15-30 Hz
        high_freq = signal.hilbert(signal_data[::10])
        muscle_power = np.mean(np.abs(high_freq) ** 2)
        artifacts["muscle_artifact_power"] = float(muscle_power)

        # Line noise (50/60 Hz)
        freqs = np.fft.rfftfreq(len(signal_data), 1 / 250)
        fft_vals = np.abs(np.fft.rfft(signal_data))
        line_mask = ((freqs > 49) & (freqs < 51)) | ((freqs > 59) & (freqs < 61))
        line_noise = np.sum(fft_vals[line_mask] ** 2)
        artifacts["line_noise_present"] = line_noise > np.mean(fft_vals**2) * 10

        return artifacts

    def _apply_filters(self, signal_data: np.ndarray, sampling_rate: float) -> Dict:
        """Apply standard EEG filters"""

        # Bandpass 0.5-40 Hz (standard EEG)
        nyquist = sampling_rate / 2
        low = 0.5 / nyquist
        high = 40 / nyquist

        # Design IIR Butterworth filter
        b, a = signal.butter(4, [low, high], btype="band")
        filtered = signal.filtfilt(b, a, signal_data)

        return {
            "filtered_signal": filtered.tolist()[:1000],  # First 1000 samples
            "filter_type": "Butterworth 4th order",
            "frequency_range_hz": "0.5-40",
            "rms_after_filter": float(np.sqrt(np.mean(filtered**2))),
        }


class OpenNeuroIngestor:
    """OpenNeuro (BIDS-compliant) EEG Dataset Ingestion"""

    OPENNEURO_DATASETS = {
        "ds002778": {"name": "Motor Imagery Pilot", "subjects": 2},
        "ds003505": {"name": "Neurotypical EEG", "subjects": 17},
        "ds001810": {"name": "Working Memory", "subjects": 26},
    }

    async def download_dataset(self, dataset_id: str) -> Optional[str]:
        """Download OpenNeuro BIDS dataset"""

        if dataset_id not in self.OPENNEURO_DATASETS:
            logger.error(f"Unknown OpenNeuro dataset: {dataset_id}")
            return None

        url = f"https://openneuro.org/crn/datasets/{dataset_id}"
        logger.info(f"OpenNeuro dataset {dataset_id} available at: {url}")
        logger.info("Use AWS CLI to sync: aws s3 sync --no-sign-request ...")

        return url


class DataFormatConverter:
    """Convert between different EEG data formats"""

    @staticmethod
    def numpy_to_csv(
        data: np.ndarray, output_path: str, channel_names: Optional[List[str]] = None
    ):
        """Convert numpy array to CSV"""
        if channel_names is None:
            channel_names = [f"CH{i+1}" for i in range(data.shape[0])]

        df_data = np.vstack([channel_names[:, None], data.T])
        np.savetxt(output_path, df_data, delimiter=",", fmt="%s", header="Channels")
        logger.info(f"Exported to CSV: {output_path}")

    @staticmethod
    def numpy_to_npy(data: np.ndarray, output_path: str):
        """Save numpy array to NPY format"""
        np.save(output_path, data)
        logger.info(f"Exported to NPY: {output_path}")

    @staticmethod
    def csv_to_numpy(csv_path: str, skip_header: int = 1) -> np.ndarray:
        """Load CSV to numpy array"""
        data = np.loadtxt(csv_path, delimiter=",", skiprows=skip_header)
        logger.info(f"Loaded CSV: {csv_path}, shape: {data.shape}")
        return data


async def main():
    """Demo: Ingest and process real EEG data"""

    ingestor = PhysioNetIngestor()

    print("\n" + "=" * 80)
    print("🧠 L.I.F.E. PhysioNet & Open Science EEG Data Ingestion System")
    print("=" * 80)

    # Available datasets
    print("\n📊 Available PhysioNet Datasets:")
    for name, info in ingestor.PHYSIONET_DATASETS.items():
        print(
            f"  • {name}: {info['description']}"
            f" ({info['subjects']} subjects, {info['channels']} channels)"
        )

    print("\n📊 Available OpenNeuro Datasets:")
    for dataset_id, info in OpenNeuroIngestor.OPENNEURO_DATASETS.items():
        print(f"  • {dataset_id}: {info['name']} ({info['subjects']} subjects)")

    # Example: Download BCI IV-2a data
    print("\n✅ Example: Downloading BCI Competition IV-2a (Subject 1, Session 1)...")

    data = await ingestor.download_dataset("bci_iv_2a", subject_id=1, session=1)

    if data:
        # Save to temp file
        temp_file = os.path.join(ingestor.temp_dir, "eeg_sample.edf")
        with open(temp_file, "wb") as f:
            f.write(data)

        # Parse EDF
        print(f"\n📂 Parsing EDF file: {temp_file}")
        eeg_array, metadata = ingestor.parse_edf_file(temp_file)

        if eeg_array is not None:
            print(f"✅ Successfully loaded EEG data: {eeg_array.shape}")
            print(f"   Metadata: {json.dumps(metadata, indent=2)}")

            # Process signal
            print("\n🔬 Processing EEG signal...")
            processing_results = ingestor.process_eeg_signal(
                eeg_array[0], sampling_rate=metadata["sampling_rate"]
            )

            print("\n📈 Processing Results:")
            print(f"   Quality Score: {processing_results['quality']['score']:.2f}/100")
            print(f"   Quality Rating: {processing_results['quality']['rating']}")
            print(f"   SNR: {processing_results['quality']['snr_db']:.2f} dB")
            print(
                f"   Peak-to-Peak: {processing_results['quality']['peak_to_peak_uv']:.2f} µV"
            )

            print("\n📊 Frequency Analysis:")
            for band, power in processing_results["frequency"].items():
                if "percent" in band:
                    print(f"   {band}: {power:.2f}%")

            print("\n🎯 Artifact Detection:")
            print(f"   Blinks: {processing_results['artifacts']['blink_events']}")
            print(
                f"   Blink Percentage: {processing_results['artifacts']['blink_percentage']:.2f}%"
            )
            print(
                f"   Line Noise: {processing_results['artifacts']['line_noise_present']}"
            )

    print("\n" + "=" * 80)
    print("✨ PhysioNet/OpenNeuro ingestion complete!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
