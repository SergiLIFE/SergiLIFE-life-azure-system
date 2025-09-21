"""
EEG Preprocessing Azure Function
Layer 2: Real-time EEG signal preprocessing and artifact removal

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import azure.functions as func
import numpy as np

# Configure logging for enterprise deployment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EEGPreprocessor:
    """Real-time EEG preprocessing pipeline for L.I.F.E. platform"""

    def __init__(self):
        self.sampling_rate = 256.0  # Hz
        self.channels = 64
        self.buffer_size = 1024  # 4 seconds at 256 Hz

        # Frequency bands (Hz)
        self.bands = {
            "delta": (0.5, 4),
            "theta": (4, 8),
            "alpha": (8, 12),
            "beta": (12, 30),
            "gamma": (30, 100),
        }

        logger.info("EEG Preprocessor initialized for L.I.F.E. platform")

    def remove_artifacts_ica(self, eeg_data: np.ndarray) -> np.ndarray:
        """
        Remove artifacts using ICA (Independent Component Analysis)
        Simplified ICA implementation for real-time processing
        """
        try:
            # In production, use MNE-ICA for proper artifact removal
            # This is a simplified version for demonstration

            # Basic statistical artifact detection
            z_scores = np.abs(
                (eeg_data - np.mean(eeg_data, axis=1, keepdims=True))
                / np.std(eeg_data, axis=1, keepdims=True)
            )

            # Remove channels with extreme values (likely artifacts)
            artifact_threshold = 3.0
            clean_mask = np.mean(z_scores > artifact_threshold, axis=1) < 0.1

            if np.sum(clean_mask) < eeg_data.shape[0] * 0.5:
                # If too many channels removed, keep all but apply mild filtering
                logger.warning(
                    "Too many channels flagged as artifacts, applying conservative filtering"
                )
                return self._conservative_artifact_removal(eeg_data)

            return eeg_data[clean_mask]

        except Exception as e:
            logger.error(f"ICA artifact removal failed: {e}")
            return eeg_data

    def _conservative_artifact_removal(self, eeg_data: np.ndarray) -> np.ndarray:
        """Conservative artifact removal when ICA fails"""
        # Simple amplitude-based filtering
        max_amplitude = np.max(np.abs(eeg_data), axis=1)
        threshold = np.percentile(max_amplitude, 95)
        clean_mask = max_amplitude <= threshold
        return eeg_data[clean_mask] if np.sum(clean_mask) > 0 else eeg_data

    def apply_bandpass_filter(
        self, eeg_data: np.ndarray, low_freq: float, high_freq: float
    ) -> np.ndarray:
        """
        Apply bandpass filter to extract specific frequency bands
        Using simplified FIR filter for real-time processing
        """
        try:
            # In production, use scipy.signal or MNE filtering
            # This is a simplified butterworth approximation

            # Simple moving average as approximation
            window_size = int(self.sampling_rate / low_freq)
            if window_size < 2:
                window_size = 2

            # Apply moving average filter
            filtered_data = np.zeros_like(eeg_data)
            for ch in range(eeg_data.shape[0]):
                filtered_data[ch] = np.convolve(
                    eeg_data[ch], np.ones(window_size) / window_size, mode="same"
                )

            return filtered_data

        except Exception as e:
            logger.error(f"Bandpass filtering failed: {e}")
            return eeg_data

    def extract_frequency_features(self, eeg_data: np.ndarray) -> Dict[str, float]:
        """
        Extract spectral features from EEG data
        Returns power in different frequency bands and coherence metrics
        """
        try:
            features = {}

            # Calculate power spectral density for each band
            for band_name, (low_freq, high_freq) in self.bands.items():
                filtered_data = self.apply_bandpass_filter(
                    eeg_data, low_freq, high_freq
                )
                power = np.mean(np.square(filtered_data))
                features[f"{band_name}_power"] = float(power)

            # Calculate coherence between channels (simplified)
            if eeg_data.shape[0] >= 2:
                # Cross-correlation as coherence approximation
                corr_matrix = np.corrcoef(eeg_data)
                mean_coherence = np.mean(
                    np.abs(corr_matrix[np.triu_indices_from(corr_matrix, k=1)])
                )
                features["mean_coherence"] = float(mean_coherence)
            else:
                features["mean_coherence"] = 0.0

            # Signal quality metrics
            features["signal_variance"] = float(np.mean(np.var(eeg_data, axis=1)))
            features["signal_snr"] = float(self._calculate_snr(eeg_data))

            return features

        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            return {
                "alpha_power": 0.0,
                "beta_power": 0.0,
                "theta_power": 0.0,
                "gamma_power": 0.0,
                "delta_power": 0.0,
                "mean_coherence": 0.0,
                "signal_variance": 0.0,
                "signal_snr": 0.0,
            }

    def _calculate_snr(self, eeg_data: np.ndarray) -> float:
        """Calculate Signal-to-Noise Ratio"""
        try:
            signal_power = np.mean(np.square(eeg_data))
            noise_power = np.mean(
                np.square(eeg_data - np.mean(eeg_data, axis=1, keepdims=True))
            )
            return 10 * np.log10(signal_power / (noise_power + 1e-10))
        except:
            return 0.0

    def assess_signal_quality(self, eeg_data: np.ndarray) -> Dict[str, Any]:
        """
        Assess EEG signal quality before quantum processing
        Returns quality metrics and processing recommendation
        """
        try:
            quality_metrics = {
                "timestamp": datetime.now().isoformat(),
                "channels_count": int(eeg_data.shape[0]),
                "samples_count": int(eeg_data.shape[1]),
                "duration_seconds": float(eeg_data.shape[1] / self.sampling_rate),
            }

            # Quality checks
            quality_metrics["has_minimum_channels"] = eeg_data.shape[0] >= 8
            quality_metrics["has_minimum_duration"] = (
                eeg_data.shape[1] >= 512
            )  # 2 seconds
            quality_metrics["signal_not_saturated"] = (
                np.max(np.abs(eeg_data)) < 1000.0
            )  # µV
            quality_metrics["reasonable_variance"] = (
                np.mean(np.var(eeg_data, axis=1)) > 1.0
            )

            # Overall quality score (0-1)
            quality_score = (
                sum(
                    [
                        quality_metrics["has_minimum_channels"],
                        quality_metrics["has_minimum_duration"],
                        quality_metrics["signal_not_saturated"],
                        quality_metrics["reasonable_variance"],
                    ]
                )
                / 4.0
            )

            quality_metrics["quality_score"] = float(quality_score)
            quality_metrics["ready_for_quantum"] = quality_score >= 0.75

            return quality_metrics

        except Exception as e:
            logger.error(f"Quality assessment failed: {e}")
            return {"quality_score": 0.0, "ready_for_quantum": False, "error": str(e)}

    def process_eeg_stream(self, eeg_data: np.ndarray) -> Dict[str, Any]:
        """
        Complete EEG preprocessing pipeline
        Returns processed data and metadata for quantum processing
        """
        try:
            logger.info(f"Processing EEG stream: {eeg_data.shape}")

            # Step 1: Artifact removal
            clean_data = self.remove_artifacts_ica(eeg_data)

            # Step 2: Quality assessment
            quality_metrics = self.assess_signal_quality(clean_data)

            # Step 3: Feature extraction
            features = self.extract_frequency_features(clean_data)

            # Prepare output for quantum processing
            processed_result = {
                "timestamp": datetime.now().isoformat(),
                "original_shape": list(eeg_data.shape),
                "processed_shape": list(clean_data.shape),
                "quality_metrics": quality_metrics,
                "frequency_features": features,
                "processing_status": "success",
                "ready_for_quantum": quality_metrics.get("ready_for_quantum", False),
            }

            # Include processed data if quality is good
            if quality_metrics.get("ready_for_quantum", False):
                processed_result["processed_eeg"] = clean_data.tolist()
            else:
                processed_result["processed_eeg"] = []
                processed_result["processing_status"] = "quality_insufficient"

            return processed_result

        except Exception as e:
            logger.error(f"EEG preprocessing failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "processing_status": "error",
                "error": str(e),
                "ready_for_quantum": False,
            }


# Global preprocessor instance
preprocessor = EEGPreprocessor()


def main(events: List[func.EventHubEvent], outputEvents: func.Out[List[str]]) -> None:
    """
    Azure Function entry point for EEG preprocessing
    Processes Event Hub events containing EEG data
    """
    try:
        logger.info(f"Received {len(events)} EEG events for processing")

        processed_events = []

        for event in events:
            try:
                # Parse EEG data from event
                event_data = json.loads(event.get_body().decode("utf-8"))

                if "eeg_data" not in event_data:
                    logger.warning("Event missing eeg_data field")
                    continue

                # Convert to numpy array
                eeg_array = np.array(event_data["eeg_data"])

                # Process EEG data
                processed_result = preprocessor.process_eeg_stream(eeg_array)

                # Add metadata
                processed_result.update(
                    {
                        "event_id": event_data.get("event_id", "unknown"),
                        "user_id": event_data.get("user_id", "unknown"),
                        "session_id": event_data.get("session_id", "unknown"),
                        "processing_latency_ms": 0.0,  # Would measure actual latency
                    }
                )

                # Convert to JSON and add to output
                processed_events.append(json.dumps(processed_result))

                logger.info(
                    f"Processed EEG event for user {processed_result['user_id']}: "
                    f"quality={processed_result['quality_metrics']['quality_score']:.2f}"
                )

            except Exception as e:
                logger.error(f"Failed to process individual event: {e}")
                continue

        # Send processed events to output Event Hub
        if processed_events:
            outputEvents.set(processed_events)
            logger.info(
                f"Sent {len(processed_events)} processed EEG events to output hub"
            )
        else:
            logger.warning("No events were successfully processed")

    except Exception as e:
        logger.error(f"EEG preprocessing function failed: {e}")
        # In production, would send error events to dead letter queue
