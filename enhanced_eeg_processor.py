#!/usr/bin/env python3
"""
Enhanced EEG Processor for 85%+ Accuracy Achievement
L.I.F.E Platform - Revolutionary Signal Processing Enhancement

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import logging
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from sklearn.decomposition import FastICA

logger = logging.getLogger(__name__)


@dataclass
class AccuracyMetrics:
    """Metrics for tracking accuracy improvements"""

    current_accuracy: float
    target_accuracy: float = 0.85
    improvement_needed: float = 0.0
    stage_contribution: Dict[str, float] = None

    def __post_init__(self):
        improvement = max(0, self.target_accuracy - self.current_accuracy)
        self.improvement_needed = improvement
        if self.stage_contribution is None:
            self.stage_contribution = {}


class EnhancedEEGProcessor:
    """
    Enhanced EEG Processing System designed specifically for >85% accuracy
    Integrates advanced signal processing with Venturi enhancement
    """

    def __init__(self, target_accuracy: float = 0.85):
        self.target_accuracy = target_accuracy
        self.sampling_rate = 250  # Hz
        self.frequency_bands = {
            "delta": (0.5, 4),
            "theta": (4, 8),
            "alpha": (8, 13),
            "beta": (13, 30),
            "gamma": (30, 50),
        }

        # Enhanced processing parameters for accuracy
        self.accuracy_params = {
            "ica_components": 20,
            "artifact_threshold": 3.0,
            "filter_order": 5,
            "window_length": 2.0,  # seconds
            "overlap_ratio": 0.5,
        }

        # Venturi integration parameters
        self.venturi_params = {
            "gate1_acceleration": 1.25,  # Optimized for accuracy
            "gate2_pressure_diff": 1.618,  # Golden ratio
            "gate3_recovery_rate": 0.866,  # sqrt(3)/2
        }

        msg = f"Enhanced EEG Processor initialized - Target: {target_accuracy:.1%}"
        logger.info(msg)

    def adaptive_preprocessing(
        self, eeg_data: np.ndarray, channel_names: List[str] = None
    ) -> np.ndarray:
        """
        Adaptive preprocessing pipeline optimized for maximum accuracy

        Args:
            eeg_data: Raw EEG data (channels x samples)
            channel_names: List of channel names

        Returns:
            Preprocessed EEG data
        """
        logger.info("Starting adaptive preprocessing for accuracy optimization")

        # Stage 1: Advanced artifact removal
        clean_data = self._advanced_artifact_removal(eeg_data)
        logger.info("✅ Advanced artifact removal completed")

        # Stage 2: Adaptive filtering
        filtered_data = self._adaptive_bandpass_filter(clean_data)
        logger.info("✅ Adaptive filtering completed")

        # Stage 3: Signal conditioning
        conditioned_data = self._signal_conditioning(filtered_data)
        logger.info("✅ Signal conditioning completed")

        return conditioned_data

    def _advanced_artifact_removal(self, eeg_data: np.ndarray) -> np.ndarray:
        """Advanced ICA-based artifact removal with accuracy optimization"""

        # Enhanced ICA with more components for better artifact separation
        ica = FastICA(
            n_components=self.accuracy_params["ica_components"],
            random_state=42,
            max_iter=1000,
            tol=1e-6,
        )

        # Apply ICA
        ica_components = ica.fit_transform(eeg_data.T).T

        # Enhanced artifact detection
        artifact_components = self._detect_artifacts_enhanced(ica_components)

        # Remove artifacts and reconstruct
        clean_components = ica_components.copy()
        clean_components[artifact_components] = 0

        # Reconstruct clean data
        clean_data = ica.inverse_transform(clean_components.T).T

        logger.info(f"Removed {len(artifact_components)} artifact components")
        return clean_data

    def _detect_artifacts_enhanced(self, ica_components: np.ndarray) -> List[int]:
        """Enhanced artifact detection using multiple criteria"""

        artifact_indices = []

        for i, component in enumerate(ica_components):
            # Criterion 1: High frequency content (muscle artifacts)
            high_freq_power = self._calculate_high_frequency_power(component)

            # Criterion 2: Statistical outliers (eye movements, cardiac)
            statistical_score = self._calculate_statistical_outlier_score(component)

            # Criterion 3: Temporal characteristics (line noise)
            temporal_score = self._calculate_temporal_artifact_score(component)

            # Combined artifact score
            combined_score = (high_freq_power + statistical_score + temporal_score) / 3

            if combined_score > self.accuracy_params["artifact_threshold"]:
                artifact_indices.append(i)

        return artifact_indices

    def _calculate_high_frequency_power(self, component: np.ndarray) -> float:
        """Calculate high frequency power ratio for muscle artifact detection"""

        # FFT analysis
        freqs = fftfreq(len(component), 1 / self.sampling_rate)
        fft_vals = np.abs(fft(component))

        # Power in high frequencies (>50 Hz)
        high_freq_mask = freqs > 50
        high_freq_power = np.sum(fft_vals[high_freq_mask])
        total_power = np.sum(fft_vals)

        return high_freq_power / total_power if total_power > 0 else 0

    def _calculate_statistical_outlier_score(self, component: np.ndarray) -> float:
        """Calculate statistical outlier score for eye movement detection"""

        # Kurtosis (peakedness) - eye movements have high kurtosis
        kurtosis = np.mean((component - np.mean(component)) ** 4) / (
            np.std(component) ** 4
        )

        # Normalize kurtosis score
        kurtosis_score = min(kurtosis / 10, 1.0)

        return kurtosis_score

    def _calculate_temporal_artifact_score(self, component: np.ndarray) -> float:
        """Calculate temporal artifact score for line noise detection"""

        # Check for 50/60 Hz line noise
        freqs = fftfreq(len(component), 1 / self.sampling_rate)
        fft_vals = np.abs(fft(component))

        # Power at 50 Hz and 60 Hz
        power_50hz = np.max(fft_vals[np.abs(freqs - 50) < 1])
        power_60hz = np.max(fft_vals[np.abs(freqs - 60) < 1])
        total_power = np.sum(fft_vals)

        line_noise_ratio = (
            (power_50hz + power_60hz) / total_power if total_power > 0 else 0
        )

        return line_noise_ratio

    def _adaptive_bandpass_filter(self, eeg_data: np.ndarray) -> np.ndarray:
        """Adaptive bandpass filtering optimized for classification accuracy"""

        # Design adaptive filter based on signal characteristics
        signal_quality = self._assess_signal_quality(eeg_data)

        # Adjust filter parameters based on signal quality
        if signal_quality > 0.8:
            # High quality signal - use narrow bands
            low_freq = 0.5
            high_freq = 45
        elif signal_quality > 0.5:
            # Medium quality - moderate filtering
            low_freq = 1.0
            high_freq = 40
        else:
            # Low quality - aggressive filtering
            low_freq = 2.0
            high_freq = 35

        # Apply Butterworth bandpass filter
        nyquist = self.sampling_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist

        b, a = signal.butter(
            self.accuracy_params["filter_order"], [low, high], btype="band"
        )

        # Apply filter to each channel
        filtered_data = np.zeros_like(eeg_data)
        for i in range(eeg_data.shape[0]):
            filtered_data[i] = signal.filtfilt(b, a, eeg_data[i])

        logger.info(f"Applied adaptive bandpass filter: {low_freq}-{high_freq} Hz")
        return filtered_data

    def _assess_signal_quality(self, eeg_data: np.ndarray) -> float:
        """Assess overall signal quality for adaptive processing"""

        quality_scores = []

        for channel in eeg_data:
            # SNR estimation
            snr = self._estimate_snr(channel)

            # Artifact contamination estimation
            artifact_level = self._estimate_artifact_level(channel)

            # Signal stability
            stability = self._estimate_signal_stability(channel)

            # Combine scores
            channel_quality = (snr + (1 - artifact_level) + stability) / 3
            quality_scores.append(channel_quality)

        return np.mean(quality_scores)

    def _estimate_snr(self, channel: np.ndarray) -> float:
        """Estimate signal-to-noise ratio"""

        # Simple SNR estimation using signal variance vs noise floor
        signal_power = np.var(channel)

        # Estimate noise from high frequencies
        b, a = signal.butter(5, 0.8, btype="high", fs=self.sampling_rate)
        noise_estimate = signal.filtfilt(b, a, channel)
        noise_power = np.var(noise_estimate)

        snr = signal_power / noise_power if noise_power > 0 else 1.0
        return min(snr / 10, 1.0)  # Normalize

    def _estimate_artifact_level(self, channel: np.ndarray) -> float:
        """Estimate artifact contamination level"""

        # High amplitude spikes (artifacts)
        threshold = 5 * np.std(channel)
        spike_ratio = np.sum(np.abs(channel) > threshold) / len(channel)

        return min(spike_ratio * 10, 1.0)  # Normalize

    def _estimate_signal_stability(self, channel: np.ndarray) -> float:
        """Estimate signal stability over time"""

        # Divide signal into segments and check variance consistency
        segment_length = int(self.sampling_rate * 2)  # 2-second segments
        num_segments = len(channel) // segment_length

        if num_segments < 2:
            return 0.5  # Insufficient data

        segment_variances = []
        for i in range(num_segments):
            start = i * segment_length
            end = start + segment_length
            segment_var = np.var(channel[start:end])
            segment_variances.append(segment_var)

        # Stability = inverse of variance of segment variances
        stability = 1 / (
            1 + np.var(segment_variances) / np.mean(segment_variances) ** 2
        )

        return stability

    def _signal_conditioning(self, eeg_data: np.ndarray) -> np.ndarray:
        """Final signal conditioning for optimal feature extraction"""

        # Normalize each channel
        conditioned_data = np.zeros_like(eeg_data)

        for i in range(eeg_data.shape[0]):
            channel = eeg_data[i]

            # Remove DC offset
            channel = channel - np.mean(channel)

            # Robust scaling (less sensitive to outliers)
            median = np.median(channel)
            mad = np.median(np.abs(channel - median))  # Median Absolute Deviation

            if mad > 0:
                conditioned_data[i] = (channel - median) / (1.4826 * mad)
            else:
                conditioned_data[i] = channel

        return conditioned_data

    def extract_optimized_features(self, eeg_data: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Extract optimized features designed for maximum classification accuracy

        Args:
            eeg_data: Preprocessed EEG data (channels x samples)

        Returns:
            Dictionary of extracted features
        """
        logger.info("Extracting optimized features for accuracy")

        features = {}

        # 1. Enhanced spectral features
        features.update(self._extract_enhanced_spectral_features(eeg_data))

        # 2. Time-domain features
        features.update(self._extract_time_domain_features(eeg_data))

        # 3. Connectivity features
        features.update(self._extract_connectivity_features(eeg_data))

        # 4. Wavelet features
        features.update(self._extract_wavelet_features(eeg_data))

        # 5. Venturi-enhanced features
        features.update(self._extract_venturi_features(eeg_data))

        logger.info(
            f"Extracted {sum(len(f) for f in features.values())} features total"
        )
        return features

    def _extract_enhanced_spectral_features(
        self, eeg_data: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Extract enhanced spectral features for better classification"""

        spectral_features = {}

        for band_name, (low_freq, high_freq) in self.frequency_bands.items():
            band_powers = []

            for channel in eeg_data:
                # Welch's method for robust power spectral density
                freqs, psd = signal.welch(
                    channel,
                    fs=self.sampling_rate,
                    nperseg=int(self.sampling_rate * 2),  # 2-second windows
                    overlap=None,
                )

                # Extract band power
                band_mask = (freqs >= low_freq) & (freqs <= high_freq)
                band_power = np.trapz(psd[band_mask], freqs[band_mask])
                band_powers.append(band_power)

            spectral_features[f"{band_name}_power"] = np.array(band_powers)

            # Relative band power
            total_power = np.sum(
                [
                    np.sum(spectral_features[f"{b}_power"])
                    for b in self.frequency_bands.keys()
                    if f"{b}_power" in spectral_features
                ]
            )

            if total_power > 0:
                spectral_features[f"{band_name}_relative_power"] = (
                    spectral_features[f"{band_name}_power"] / total_power
                )

        # Cross-band ratios (important for classification)
        if "alpha_power" in spectral_features and "beta_power" in spectral_features:
            spectral_features["alpha_beta_ratio"] = spectral_features["alpha_power"] / (
                spectral_features["beta_power"] + 1e-10
            )

        if "theta_power" in spectral_features and "beta_power" in spectral_features:
            spectral_features["theta_beta_ratio"] = spectral_features["theta_power"] / (
                spectral_features["beta_power"] + 1e-10
            )

        return spectral_features

    def _extract_time_domain_features(
        self, eeg_data: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Extract time-domain features"""

        time_features = {}

        # Statistical moments
        time_features["mean"] = np.mean(eeg_data, axis=1)
        time_features["std"] = np.std(eeg_data, axis=1)
        time_features["skewness"] = self._calculate_skewness(eeg_data)
        time_features["kurtosis"] = self._calculate_kurtosis(eeg_data)

        # Signal complexity measures
        time_features["zero_crossings"] = self._calculate_zero_crossings(eeg_data)
        time_features["hjorth_activity"] = self._calculate_hjorth_activity(eeg_data)
        time_features["hjorth_mobility"] = self._calculate_hjorth_mobility(eeg_data)
        time_features["hjorth_complexity"] = self._calculate_hjorth_complexity(eeg_data)

        return time_features

    def _extract_connectivity_features(
        self, eeg_data: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Extract connectivity features between channels"""

        connectivity_features = {}

        # Cross-correlation
        connectivity_features["max_cross_correlation"] = (
            self._calculate_max_cross_correlation(eeg_data)
        )

        # Coherence
        connectivity_features["mean_coherence"] = self._calculate_mean_coherence(
            eeg_data
        )

        return connectivity_features

    def _extract_wavelet_features(self, eeg_data: np.ndarray) -> Dict[str, np.ndarray]:
        """Extract wavelet-based features"""

        wavelet_features = {}

        # Simple wavelet energy features (placeholder for full implementation)
        for i in range(eeg_data.shape[0]):
            channel = eeg_data[i]

            # Discrete wavelet transform energy
            # This is a simplified version - full implementation would use PyWavelets
            high_freq_energy = np.sum(np.diff(channel) ** 2)
            wavelet_features[f"wavelet_energy_{i}"] = np.array([high_freq_energy])

        return wavelet_features

    def _extract_venturi_features(self, eeg_data: np.ndarray) -> Dict[str, np.ndarray]:
        """Extract Venturi-enhanced features using fluid dynamics principles"""

        venturi_features = {}

        # Apply Venturi gates processing
        gate1_output = self._apply_venturi_gate1(eeg_data)
        gate2_output = self._apply_venturi_gate2(gate1_output)
        gate3_output = self._apply_venturi_gate3(gate2_output)

        # Extract features from Venturi-processed signal
        venturi_features["venturi_signal_power"] = np.mean(gate3_output**2, axis=1)
        venturi_features["venturi_signal_coherence"] = (
            self._calculate_venturi_coherence(gate3_output)
        )
        venturi_features["venturi_flow_pattern"] = self._calculate_flow_pattern(
            gate3_output
        )

        return venturi_features

    def _apply_venturi_gate1(self, eeg_data: np.ndarray) -> np.ndarray:
        """Apply Venturi Gate 1: Signal acceleration"""

        acceleration = self.venturi_params["gate1_acceleration"]

        # Apply signal acceleration using Torricelli's law simulation
        accelerated_signal = eeg_data * acceleration

        # Apply constriction effect
        constriction_factor = 0.8
        constricted_signal = accelerated_signal * constriction_factor

        return constricted_signal

    def _apply_venturi_gate2(self, eeg_data: np.ndarray) -> np.ndarray:
        """Apply Venturi Gate 2: Pressure differential optimization"""

        golden_ratio = self.venturi_params["gate2_pressure_diff"]

        # Apply pressure differential using golden ratio
        pressure_modulated = eeg_data * golden_ratio

        # Bernoulli's principle simulation
        velocity_factor = np.sqrt(2 * golden_ratio)
        processed_signal = pressure_modulated / velocity_factor

        return processed_signal

    def _apply_venturi_gate3(self, eeg_data: np.ndarray) -> np.ndarray:
        """Apply Venturi Gate 3: Flow recovery and amplification"""

        recovery_rate = self.venturi_params["gate3_recovery_rate"]

        # Flow recovery using sqrt(3)/2 factor
        recovered_signal = eeg_data * recovery_rate

        # Final amplification
        amplification = 1.4
        final_signal = recovered_signal * amplification

        return final_signal

    def _calculate_venturi_coherence(self, venturi_data: np.ndarray) -> np.ndarray:
        """Calculate coherence in Venturi-processed signal"""

        coherence_values = []

        for i in range(venturi_data.shape[0]):
            for j in range(i + 1, venturi_data.shape[0]):
                # Cross-correlation as coherence measure
                correlation = np.corrcoef(venturi_data[i], venturi_data[j])[0, 1]
                coherence_values.append(abs(correlation))

        return np.array(coherence_values)

    def _calculate_flow_pattern(self, venturi_data: np.ndarray) -> np.ndarray:
        """Calculate flow pattern characteristics"""

        # Analyze flow patterns using gradient analysis
        flow_patterns = []

        for channel in venturi_data:
            gradient = np.gradient(channel)
            flow_complexity = np.std(gradient) / (np.mean(np.abs(gradient)) + 1e-10)
            flow_patterns.append(flow_complexity)

        return np.array(flow_patterns)

    # Helper methods for statistical calculations
    def _calculate_skewness(self, data: np.ndarray) -> np.ndarray:
        """Calculate skewness for each channel"""
        mean_vals = np.mean(data, axis=1, keepdims=True)
        std_vals = np.std(data, axis=1, keepdims=True)
        normalized = (data - mean_vals) / (std_vals + 1e-10)
        skewness = np.mean(normalized**3, axis=1)
        return skewness

    def _calculate_kurtosis(self, data: np.ndarray) -> np.ndarray:
        """Calculate kurtosis for each channel"""
        mean_vals = np.mean(data, axis=1, keepdims=True)
        std_vals = np.std(data, axis=1, keepdims=True)
        normalized = (data - mean_vals) / (std_vals + 1e-10)
        kurtosis = np.mean(normalized**4, axis=1) - 3  # Excess kurtosis
        return kurtosis

    def _calculate_zero_crossings(self, data: np.ndarray) -> np.ndarray:
        """Calculate zero crossings rate for each channel"""
        zero_crossings = []
        for channel in data:
            crossings = np.sum(np.diff(np.sign(channel)) != 0)
            zero_crossings.append(crossings / len(channel))
        return np.array(zero_crossings)

    def _calculate_hjorth_activity(self, data: np.ndarray) -> np.ndarray:
        """Calculate Hjorth activity parameter"""
        return np.var(data, axis=1)

    def _calculate_hjorth_mobility(self, data: np.ndarray) -> np.ndarray:
        """Calculate Hjorth mobility parameter"""
        activity = self._calculate_hjorth_activity(data)
        first_derivative = np.diff(data, axis=1)
        derivative_activity = np.var(first_derivative, axis=1)
        mobility = np.sqrt(derivative_activity / (activity + 1e-10))
        return mobility

    def _calculate_hjorth_complexity(self, data: np.ndarray) -> np.ndarray:
        """Calculate Hjorth complexity parameter"""
        mobility = self._calculate_hjorth_mobility(data)
        first_derivative = np.diff(data, axis=1)
        derivative_mobility = self._calculate_hjorth_mobility(first_derivative)
        complexity = derivative_mobility / (mobility + 1e-10)
        return complexity

    def _calculate_max_cross_correlation(self, data: np.ndarray) -> np.ndarray:
        """Calculate maximum cross-correlation between all channel pairs"""
        max_correlations = []

        for i in range(data.shape[0]):
            for j in range(i + 1, data.shape[0]):
                correlation = np.corrcoef(data[i], data[j])[0, 1]
                max_correlations.append(abs(correlation))

        return np.array(max_correlations)

    def _calculate_mean_coherence(self, data: np.ndarray) -> np.ndarray:
        """Calculate mean coherence across all frequencies"""
        coherence_values = []

        for i in range(data.shape[0]):
            for j in range(i + 1, data.shape[0]):
                # Simplified coherence calculation
                freqs, coherence = signal.coherence(
                    data[i],
                    data[j],
                    fs=self.sampling_rate,
                    nperseg=int(self.sampling_rate),
                )
                mean_coherence = np.mean(coherence)
                coherence_values.append(mean_coherence)

        return np.array(coherence_values)

    def process_for_accuracy(
        self, eeg_data: np.ndarray, channel_names: List[str] = None
    ) -> Dict[str, np.ndarray]:
        """
        Complete processing pipeline optimized for >85% accuracy

        Args:
            eeg_data: Raw EEG data (channels x samples)
            channel_names: Optional channel names

        Returns:
            Dictionary of processed features ready for classification
        """
        logger.info("Starting complete accuracy-optimized processing pipeline")

        # Stage 1: Enhanced preprocessing
        preprocessed_data = self.adaptive_preprocessing(eeg_data, channel_names)
        logger.info("✅ Preprocessing completed")

        # Stage 2: Feature extraction
        features = self.extract_optimized_features(preprocessed_data)
        logger.info("✅ Feature extraction completed")

        # Stage 3: Feature optimization
        optimized_features = self._optimize_features_for_accuracy(features)
        logger.info("✅ Feature optimization completed")

        logger.info("🎯 Accuracy-optimized processing pipeline completed successfully")
        return optimized_features

    def _optimize_features_for_accuracy(
        self, features: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """Final feature optimization for maximum accuracy"""

        optimized = {}

        # Normalize all features
        for feature_name, feature_values in features.items():
            if len(feature_values) > 0:
                # Robust normalization
                median = np.median(feature_values)
                mad = np.median(np.abs(feature_values - median))

                if mad > 0:
                    normalized = (feature_values - median) / (1.4826 * mad)
                else:
                    normalized = feature_values - median

                optimized[feature_name] = normalized
            else:
                optimized[feature_name] = feature_values

        return optimized


if __name__ == "__main__":
    # Example usage
    processor = EnhancedEEGProcessor(target_accuracy=0.85)

    # Simulate EEG data
    num_channels = 22
    num_samples = 2500  # 10 seconds at 250 Hz
    simulated_eeg = np.random.randn(num_channels, num_samples)

    # Process for accuracy
    features = processor.process_for_accuracy(simulated_eeg)

    print(f"Processed {num_channels} channels, {num_samples} samples")
    print(f"Extracted {len(features)} feature types")
    print(f"Total features: {sum(len(f) for f in features.values())}")
    print(f"Total features: {sum(len(f) for f in features.values())}")
