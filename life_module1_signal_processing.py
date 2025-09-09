"""
L.I.F.E Theory Module 1: Advanced Signal Processing
Core signal processing algorithms with adaptive learning

Copyright 2025 - Sergio Paya Borrull
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import butter, filtfilt, hilbert, spectrogram

# Import L.I.F.E Theory core
from lifetheory import CoreLIFEAlgorithm, ExperienceMemory, AdaptationParameters

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalType(Enum):
    """Types of signals that can be processed"""
    EEG = "electroencephalogram"
    ECG = "electrocardiogram"
    EMG = "electromyogram"
    AUDIO = "audio_signal"
    SENSOR = "sensor_data"
    BIOMEDICAL = "biomedical_signal"
    GENERAL = "general_signal"

class ProcessingMode(Enum):
    """Signal processing modes"""
    REAL_TIME = "real_time"
    BATCH = "batch_processing"
    STREAMING = "streaming"
    ADAPTIVE = "adaptive_learning"

@dataclass
class SignalFeatures:
    """Comprehensive signal feature extraction"""
    temporal_features: Dict[str, float] = field(default_factory=dict)
    frequency_features: Dict[str, float] = field(default_factory=dict)
    statistical_features: Dict[str, float] = field(default_factory=dict)
    complexity_features: Dict[str, float] = field(default_factory=dict)
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default features if empty"""
        if not self.temporal_features:
            self.temporal_features = {
                "mean": 0.0,
                "std": 0.0,
                "rms": 0.0,
                "peak_to_peak": 0.0,
                "zero_crossings": 0.0
            }

@dataclass
class AdaptiveFilter:
    """Adaptive filtering configuration"""
    filter_type: str = "butterworth"
    order: int = 4
    cutoff_frequencies: List[float] = field(default_factory=lambda: [1.0, 50.0])
    adaptation_rate: float = 0.01
    learning_enabled: bool = True
    performance_history: List[float] = field(default_factory=list)

class LIFESignalProcessor:
    """Advanced signal processor with L.I.F.E Theory integration"""
    
    def __init__(self, sampling_rate: float = 1000.0, signal_type: SignalType = SignalType.GENERAL):
        self.sampling_rate = sampling_rate
        self.signal_type = signal_type
        
        # Initialize L.I.F.E algorithm for adaptive processing
        life_config = {
            "learning_rate": 0.01,
            "max_experiences": 5000,
            "venturi_gate_factor": 1.1
        }
        self.life_algorithm = CoreLIFEAlgorithm(
            learning_rate=life_config["learning_rate"],
            max_experiences=life_config["max_experiences"],
            adaptation_params=AdaptationParameters(
                learning_rate=life_config["learning_rate"],
                decay_factor=0.95,
                threshold=0.1
            )
        )
        
        # Adaptive filtering system
        self.adaptive_filters = {
            "lowpass": AdaptiveFilter("butterworth", 4, [50.0], 0.01),
            "highpass": AdaptiveFilter("butterworth", 4, [1.0], 0.01),
            "bandpass": AdaptiveFilter("butterworth", 4, [1.0, 50.0], 0.01),
            "notch": AdaptiveFilter("butterworth", 2, [50.0], 0.005)  # Power line noise
        }
        
        # Processing history for adaptation
        self.processing_history = []
        self.performance_metrics = {
            "snr_improvement": [],
            "artifacts_removed": [],
            "processing_time": [],
            "adaptation_score": []
        }
        
        logger.info(f"L.I.F.E Signal Processor initialized for {signal_type.value}")
    
    def extract_comprehensive_features(self, signal: np.ndarray) -> SignalFeatures:
        """Extract comprehensive features from signal"""
        try:
            features = SignalFeatures()
            
            # Temporal features
            features.temporal_features = {
                "mean": float(np.mean(signal)),
                "std": float(np.std(signal)),
                "rms": float(np.sqrt(np.mean(signal**2))),
                "peak_to_peak": float(np.ptp(signal)),
                "zero_crossings": float(len(np.where(np.diff(np.signbit(signal)))[0])),
                "skewness": float(self._calculate_skewness(signal)),
                "kurtosis": float(self._calculate_kurtosis(signal)),
                "energy": float(np.sum(signal**2))
            }
            
            # Frequency domain features
            freqs, psd = signal.welch(signal, fs=self.sampling_rate, nperseg=min(256, len(signal)//4))
            features.frequency_features = {
                "dominant_frequency": float(freqs[np.argmax(psd)]),
                "spectral_centroid": float(np.sum(freqs * psd) / np.sum(psd)),
                "spectral_bandwidth": float(self._calculate_spectral_bandwidth(freqs, psd)),
                "spectral_rolloff": float(self._calculate_spectral_rolloff(freqs, psd)),
                "total_power": float(np.sum(psd)),
                "mean_frequency": float(np.mean(freqs)),
                "median_frequency": float(np.median(freqs))
            }
            
            # Statistical features
            features.statistical_features = {
                "variance": float(np.var(signal)),
                "min_value": float(np.min(signal)),
                "max_value": float(np.max(signal)),
                "median": float(np.median(signal)),
                "iqr": float(np.percentile(signal, 75) - np.percentile(signal, 25)),
                "mad": float(np.median(np.abs(signal - np.median(signal)))),  # Median Absolute Deviation
                "range": float(np.max(signal) - np.min(signal))
            }
            
            # Complexity features
            features.complexity_features = {
                "sample_entropy": float(self._calculate_sample_entropy(signal)),
                "approximate_entropy": float(self._calculate_approximate_entropy(signal)),
                "spectral_entropy": float(self._calculate_spectral_entropy(psd)),
                "lempel_ziv_complexity": float(self._calculate_lz_complexity(signal)),
                "fractal_dimension": float(self._calculate_fractal_dimension(signal))
            }
            
            # Quality metrics
            features.quality_metrics = {
                "snr_estimate": float(self._estimate_snr(signal)),
                "artifact_probability": float(self._estimate_artifact_probability(signal)),
                "signal_quality_index": float(self._calculate_signal_quality_index(signal)),
                "noise_level": float(self._estimate_noise_level(signal)),
                "stability_index": float(self._calculate_stability_index(signal))
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return SignalFeatures()
    
    def adaptive_filter_signal(self, signal: np.ndarray, filter_name: str = "bandpass") -> np.ndarray:
        """Apply adaptive filtering with L.I.F.E learning"""
        try:
            if filter_name not in self.adaptive_filters:
                raise ValueError(f"Unknown filter: {filter_name}")
            
            adaptive_filter = self.adaptive_filters[filter_name]
            
            # Apply current filter
            if filter_name == "lowpass":
                filtered_signal = self._apply_lowpass_filter(signal, adaptive_filter.cutoff_frequencies[0], adaptive_filter.order)
            elif filter_name == "highpass":
                filtered_signal = self._apply_highpass_filter(signal, adaptive_filter.cutoff_frequencies[0], adaptive_filter.order)
            elif filter_name == "bandpass":
                filtered_signal = self._apply_bandpass_filter(signal, adaptive_filter.cutoff_frequencies, adaptive_filter.order)
            elif filter_name == "notch":
                filtered_signal = self._apply_notch_filter(signal, adaptive_filter.cutoff_frequencies[0], adaptive_filter.order)
            else:
                filtered_signal = signal.copy()
            
            # Evaluate filtering performance
            original_snr = self._estimate_snr(signal)
            filtered_snr = self._estimate_snr(filtered_signal)
            performance = filtered_snr / (original_snr + 1e-8)
            
            # Adapt filter parameters using L.I.F.E
            if adaptive_filter.learning_enabled:
                self._adapt_filter_parameters(adaptive_filter, performance)
            
            # Record performance
            adaptive_filter.performance_history.append(performance)
            if len(adaptive_filter.performance_history) > 1000:
                adaptive_filter.performance_history = adaptive_filter.performance_history[-1000:]
            
            return filtered_signal
            
        except Exception as e:
            logger.error(f"Error in adaptive filtering: {str(e)}")
            return signal.copy()
    
    def process_signal_with_life(self, signal: np.ndarray, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process signal through L.I.F.E Theory algorithm with comprehensive analysis"""
        try:
            start_time = datetime.now()
            
            # Extract features before processing
            original_features = self.extract_comprehensive_features(signal)
            
            # Apply adaptive preprocessing
            preprocessed_signal = self._adaptive_preprocessing(signal)
            
            # Process through L.I.F.E algorithm
            processed_signal = self.life_algorithm.process(preprocessed_signal, context or {})
            
            # Extract features after processing
            processed_features = self.extract_comprehensive_features(processed_signal)
            
            # Apply adaptive filtering
            filtered_signal = self.adaptive_filter_signal(processed_signal, "bandpass")
            final_features = self.extract_comprehensive_features(filtered_signal)
            
            # Calculate performance metrics
            performance_metrics = self._calculate_processing_performance(
                signal, preprocessed_signal, processed_signal, filtered_signal
            )
            
            # Adapt processing based on performance
            self._adapt_processing_pipeline(performance_metrics)
            
            # Prepare results
            processing_time = (datetime.now() - start_time).total_seconds()
            
            results = {
                "original_signal": signal,
                "preprocessed_signal": preprocessed_signal,
                "processed_signal": processed_signal,
                "filtered_signal": filtered_signal,
                "original_features": original_features,
                "processed_features": processed_features,
                "final_features": final_features,
                "performance_metrics": performance_metrics,
                "processing_time": processing_time,
                "life_metrics": self.life_algorithm.get_performance_metrics(),
                "adaptation_history": self.life_algorithm.get_adaptation_history()
            }
            
            # Update processing history
            self.processing_history.append({
                "timestamp": start_time.isoformat(),
                "performance": performance_metrics,
                "processing_time": processing_time
            })
            
            logger.info(f"Signal processing completed in {processing_time:.3f}s")
            return results
            
        except Exception as e:
            logger.error(f"Error in L.I.F.E signal processing: {str(e)}")
            return {
                "original_signal": signal,
                "filtered_signal": signal,
                "error": str(e),
                "processing_time": 0.0
            }
    
    def _adaptive_preprocessing(self, signal: np.ndarray) -> np.ndarray:
        """Adaptive preprocessing based on signal characteristics"""
        try:
            # Detect signal characteristics
            signal_power = np.mean(signal**2)
            noise_estimate = self._estimate_noise_level(signal)
            
            # Adaptive normalization
            if signal_power > 1000:  # High amplitude signal
                normalized_signal = signal / np.std(signal)
            else:
                normalized_signal = signal.copy()
            
            # Adaptive artifact removal
            if noise_estimate > 0.3:  # High noise
                cleaned_signal = self._remove_artifacts(normalized_signal)
            else:
                cleaned_signal = normalized_signal
            
            return cleaned_signal
            
        except Exception as e:
            logger.error(f"Error in adaptive preprocessing: {str(e)}")
            return signal.copy()
    
    def _remove_artifacts(self, signal: np.ndarray) -> np.ndarray:
        """Remove artifacts using adaptive threshold"""
        try:
            # Calculate adaptive threshold
            median_val = np.median(signal)
            mad = np.median(np.abs(signal - median_val))
            threshold = median_val + 5 * mad
            
            # Remove extreme values
            cleaned_signal = signal.copy()
            outliers = np.abs(cleaned_signal) > threshold
            
            if np.any(outliers):
                # Replace outliers with interpolated values
                outlier_indices = np.where(outliers)[0]
                for idx in outlier_indices:
                    if idx > 0 and idx < len(cleaned_signal) - 1:
                        cleaned_signal[idx] = (cleaned_signal[idx-1] + cleaned_signal[idx+1]) / 2
                    elif idx == 0:
                        cleaned_signal[idx] = cleaned_signal[idx+1]
                    else:
                        cleaned_signal[idx] = cleaned_signal[idx-1]
            
            return cleaned_signal
            
        except Exception as e:
            logger.error(f"Error removing artifacts: {str(e)}")
            return signal.copy()
    
    def _apply_bandpass_filter(self, signal: np.ndarray, cutoffs: List[float], order: int) -> np.ndarray:
        """Apply Butterworth bandpass filter"""
        try:
            low_cutoff, high_cutoff = cutoffs
            nyquist = self.sampling_rate / 2
            low = low_cutoff / nyquist
            high = high_cutoff / nyquist
            
            b, a = butter(order, [low, high], btype='band')
            filtered_signal = filtfilt(b, a, signal)
            
            return filtered_signal
            
        except Exception as e:
            logger.error(f"Error in bandpass filtering: {str(e)}")
            return signal.copy()
    
    def _apply_lowpass_filter(self, signal: np.ndarray, cutoff: float, order: int) -> np.ndarray:
        """Apply Butterworth lowpass filter"""
        try:
            nyquist = self.sampling_rate / 2
            normal_cutoff = cutoff / nyquist
            
            b, a = butter(order, normal_cutoff, btype='low')
            filtered_signal = filtfilt(b, a, signal)
            
            return filtered_signal
            
        except Exception as e:
            logger.error(f"Error in lowpass filtering: {str(e)}")
            return signal.copy()
    
    def _apply_highpass_filter(self, signal: np.ndarray, cutoff: float, order: int) -> np.ndarray:
        """Apply Butterworth highpass filter"""
        try:
            nyquist = self.sampling_rate / 2
            normal_cutoff = cutoff / nyquist
            
            b, a = butter(order, normal_cutoff, btype='high')
            filtered_signal = filtfilt(b, a, signal)
            
            return filtered_signal
            
        except Exception as e:
            logger.error(f"Error in highpass filtering: {str(e)}")
            return signal.copy()
    
    def _apply_notch_filter(self, signal: np.ndarray, notch_freq: float, order: int) -> np.ndarray:
        """Apply notch filter for power line noise"""
        try:
            nyquist = self.sampling_rate / 2
            low = (notch_freq - 1) / nyquist
            high = (notch_freq + 1) / nyquist
            
            b, a = butter(order, [low, high], btype='bandstop')
            filtered_signal = filtfilt(b, a, signal)
            
            return filtered_signal
            
        except Exception as e:
            logger.error(f"Error in notch filtering: {str(e)}")
            return signal.copy()
    
    def _calculate_processing_performance(self, original: np.ndarray, preprocessed: np.ndarray, 
                                        processed: np.ndarray, filtered: np.ndarray) -> Dict[str, float]:
        """Calculate comprehensive processing performance metrics"""
        try:
            # SNR improvements
            original_snr = self._estimate_snr(original)
            processed_snr = self._estimate_snr(processed)
            filtered_snr = self._estimate_snr(filtered)
            
            # Artifact reduction
            original_artifacts = self._estimate_artifact_probability(original)
            filtered_artifacts = self._estimate_artifact_probability(filtered)
            
            # Signal preservation
            correlation_processed = np.corrcoef(original, processed)[0, 1] if len(original) == len(processed) else 0.0
            correlation_filtered = np.corrcoef(original, filtered)[0, 1] if len(original) == len(filtered) else 0.0
            
            metrics = {
                "snr_improvement": filtered_snr / (original_snr + 1e-8),
                "artifact_reduction": (original_artifacts - filtered_artifacts) / (original_artifacts + 1e-8),
                "signal_preservation": correlation_filtered,
                "processing_gain": processed_snr / (original_snr + 1e-8),
                "overall_performance": (filtered_snr / (original_snr + 1e-8) + correlation_filtered) / 2,
                "original_snr": original_snr,
                "processed_snr": processed_snr,
                "filtered_snr": filtered_snr
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance: {str(e)}")
            return {"overall_performance": 0.5, "error": str(e)}
    
    def _adapt_processing_pipeline(self, performance_metrics: Dict[str, float]):
        """Adapt processing pipeline based on performance"""
        try:
            overall_performance = performance_metrics.get("overall_performance", 0.5)
            
            # Update performance history
            self.performance_metrics["adaptation_score"].append(overall_performance)
            
            # Adapt L.I.F.E algorithm parameters
            if overall_performance > 0.8:
                # Good performance, slightly increase learning rate
                current_lr = self.life_algorithm.adaptation_params.learning_rate
                new_lr = min(0.1, current_lr * 1.05)
                self.life_algorithm.adaptation_params.learning_rate = new_lr
            elif overall_performance < 0.5:
                # Poor performance, decrease learning rate and increase adaptation
                current_lr = self.life_algorithm.adaptation_params.learning_rate
                new_lr = max(0.001, current_lr * 0.9)
                self.life_algorithm.adaptation_params.learning_rate = new_lr
            
            # Adapt filter parameters
            for filter_name, adaptive_filter in self.adaptive_filters.items():
                if len(adaptive_filter.performance_history) > 10:
                    recent_performance = np.mean(adaptive_filter.performance_history[-10:])
                    if recent_performance < 0.7:
                        # Adapt filter parameters
                        adaptive_filter.adaptation_rate = min(0.05, adaptive_filter.adaptation_rate * 1.1)
            
        except Exception as e:
            logger.error(f"Error in pipeline adaptation: {str(e)}")
    
    # Helper methods for feature calculation
    def _calculate_skewness(self, signal: np.ndarray) -> float:
        """Calculate skewness of signal"""
        try:
            mean_val = np.mean(signal)
            std_val = np.std(signal)
            if std_val == 0:
                return 0.0
            return np.mean(((signal - mean_val) / std_val) ** 3)
        except:
            return 0.0
    
    def _calculate_kurtosis(self, signal: np.ndarray) -> float:
        """Calculate kurtosis of signal"""
        try:
            mean_val = np.mean(signal)
            std_val = np.std(signal)
            if std_val == 0:
                return 0.0
            return np.mean(((signal - mean_val) / std_val) ** 4) - 3
        except:
            return 0.0
    
    def _calculate_spectral_bandwidth(self, freqs: np.ndarray, psd: np.ndarray) -> float:
        """Calculate spectral bandwidth"""
        try:
            centroid = np.sum(freqs * psd) / np.sum(psd)
            bandwidth = np.sqrt(np.sum(((freqs - centroid) ** 2) * psd) / np.sum(psd))
            return bandwidth
        except:
            return 0.0
    
    def _calculate_spectral_rolloff(self, freqs: np.ndarray, psd: np.ndarray, rolloff_percent: float = 0.85) -> float:
        """Calculate spectral rolloff frequency"""
        try:
            cumsum_psd = np.cumsum(psd)
            total_power = cumsum_psd[-1]
            rolloff_index = np.where(cumsum_psd >= rolloff_percent * total_power)[0]
            if len(rolloff_index) > 0:
                return freqs[rolloff_index[0]]
            return freqs[-1]
        except:
            return 0.0
    
    def _calculate_sample_entropy(self, signal: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        """Calculate sample entropy"""
        try:
            N = len(signal)
            if N < m + 1:
                return 0.0
            
            patterns = np.array([signal[i:i+m] for i in range(N-m+1)])
            
            def _maxdist(xi, xj, m):
                return max([abs(ua - va) for ua, va in zip(xi, xj)])
            
            phi = np.zeros(2)
            for m_i in [m, m+1]:
                patterns_m = np.array([signal[i:i+m_i] for i in range(N-m_i+1)])
                C = np.zeros(N-m_i+1)
                
                for i in range(N-m_i+1):
                    template = patterns_m[i]
                    for j in range(N-m_i+1):
                        if _maxdist(template, patterns_m[j], m_i) <= r * np.std(signal):
                            C[i] += 1
                
                phi[m_i-m] = np.mean(np.log(C / (N-m_i+1)))
            
            return phi[0] - phi[1]
        except:
            return 0.0
    
    def _calculate_approximate_entropy(self, signal: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        """Calculate approximate entropy"""
        try:
            N = len(signal)
            if N < m + 1:
                return 0.0
            
            def _maxdist(xi, xj):
                return max([abs(ua - va) for ua, va in zip(xi, xj)])
            
            def _phi(m):
                patterns = np.array([signal[i:i+m] for i in range(N-m+1)])
                C = np.zeros(N-m+1)
                
                for i in range(N-m+1):
                    template = patterns[i]
                    for j in range(N-m+1):
                        if _maxdist(template, patterns[j]) <= r * np.std(signal):
                            C[i] += 1
                
                phi = np.mean(np.log(C / (N-m+1)))
                return phi
            
            return _phi(m) - _phi(m+1)
        except:
            return 0.0
    
    def _calculate_spectral_entropy(self, psd: np.ndarray) -> float:
        """Calculate spectral entropy"""
        try:
            # Normalize PSD
            psd_norm = psd / np.sum(psd)
            psd_norm = psd_norm[psd_norm > 0]  # Remove zeros
            
            # Calculate entropy
            entropy = -np.sum(psd_norm * np.log2(psd_norm))
            return entropy
        except:
            return 0.0
    
    def _calculate_lz_complexity(self, signal: np.ndarray) -> float:
        """Calculate Lempel-Ziv complexity"""
        try:
            # Binarize signal
            binary_signal = (signal > np.median(signal)).astype(int)
            
            # Calculate LZ complexity
            i = 0
            C = 0
            n = len(binary_signal)
            
            while i < n:
                l = 1
                found = False
                
                while i + l <= n and not found:
                    substr = binary_signal[i:i+l]
                    for j in range(i):
                        if j + l <= i:
                            if np.array_equal(substr, binary_signal[j:j+l]):
                                found = True
                                break
                    if not found:
                        l += 1
                
                C += 1
                i += l
            
            # Normalize
            return C / (n / np.log2(n)) if n > 1 else 0.0
        except:
            return 0.0
    
    def _calculate_fractal_dimension(self, signal: np.ndarray) -> float:
        """Calculate Higuchi fractal dimension"""
        try:
            N = len(signal)
            kmax = min(10, N//4)
            
            if kmax < 2:
                return 1.0
            
            Lk = []
            
            for k in range(1, kmax + 1):
                Lm = []
                for m in range(k):
                    Lmi = 0
                    maxI = (N - m - 1) // k
                    for i in range(maxI):
                        Lmi += abs(signal[m + (i + 1) * k] - signal[m + i * k])
                    
                    if maxI > 0:
                        Lmi = Lmi * (N - 1) / (maxI * k * k)
                        Lm.append(Lmi)
                
                if Lm:
                    Lk.append(np.mean(Lm))
            
            if len(Lk) < 2:
                return 1.0
            
            # Linear regression in log-log space
            k_vals = np.arange(1, len(Lk) + 1)
            log_k = np.log(k_vals)
            log_Lk = np.log(Lk)
            
            slope = np.polyfit(log_k, log_Lk, 1)[0]
            return -slope
        except:
            return 1.0
    
    def _estimate_snr(self, signal: np.ndarray) -> float:
        """Estimate signal-to-noise ratio"""
        try:
            # Use difference method to estimate noise
            signal_power = np.mean(signal**2)
            noise_power = np.var(np.diff(signal)) / 2
            
            if noise_power == 0:
                return float('inf')
            
            snr_db = 10 * np.log10(signal_power / noise_power)
            return max(0, snr_db)
        except:
            return 0.0
    
    def _estimate_artifact_probability(self, signal: np.ndarray) -> float:
        """Estimate probability of artifacts in signal"""
        try:
            # Use statistical measures to estimate artifacts
            median_val = np.median(signal)
            mad = np.median(np.abs(signal - median_val))
            
            # Count outliers
            threshold = median_val + 5 * mad
            outliers = np.sum(np.abs(signal) > threshold)
            
            artifact_prob = outliers / len(signal)
            return min(1.0, artifact_prob)
        except:
            return 0.5
    
    def _calculate_signal_quality_index(self, signal: np.ndarray) -> float:
        """Calculate overall signal quality index"""
        try:
            # Combine multiple quality measures
            snr = self._estimate_snr(signal)
            artifacts = self._estimate_artifact_probability(signal)
            stability = self._calculate_stability_index(signal)
            
            # Normalize SNR to 0-1
            snr_norm = min(1.0, snr / 40.0)  # 40 dB is good SNR
            
            # Quality index (higher is better)
            quality = (snr_norm + (1 - artifacts) + stability) / 3
            return quality
        except:
            return 0.5
    
    def _estimate_noise_level(self, signal: np.ndarray) -> float:
        """Estimate noise level in signal"""
        try:
            # High frequency variance as noise estimate
            diff_signal = np.diff(signal)
            noise_variance = np.var(diff_signal)
            signal_variance = np.var(signal)
            
            noise_level = noise_variance / (signal_variance + 1e-8)
            return min(1.0, noise_level)
        except:
            return 0.5
    
    def _calculate_stability_index(self, signal: np.ndarray) -> float:
        """Calculate signal stability index"""
        try:
            # Divide signal into segments and check consistency
            segment_size = max(10, len(signal) // 10)
            segments = [signal[i:i+segment_size] for i in range(0, len(signal), segment_size)]
            
            if len(segments) < 2:
                return 1.0
            
            # Calculate variance of segment means
            segment_means = [np.mean(seg) for seg in segments if len(seg) > 5]
            if len(segment_means) < 2:
                return 1.0
            
            mean_variance = np.var(segment_means)
            signal_variance = np.var(signal)
            
            stability = 1.0 - min(1.0, mean_variance / (signal_variance + 1e-8))
            return stability
        except:
            return 0.5
    
    def _adapt_filter_parameters(self, adaptive_filter: AdaptiveFilter, performance: float):
        """Adapt filter parameters based on performance"""
        try:
            if performance < 0.7:  # Poor performance
                # Adjust cutoff frequencies
                if adaptive_filter.filter_type == "bandpass" and len(adaptive_filter.cutoff_frequencies) == 2:
                    low, high = adaptive_filter.cutoff_frequencies
                    # Slightly expand the band
                    new_low = max(0.5, low * 0.95)
                    new_high = min(self.sampling_rate / 2 - 1, high * 1.05)
                    adaptive_filter.cutoff_frequencies = [new_low, new_high]
                
            elif performance > 0.9:  # Excellent performance
                # Slightly narrow the filter for better selectivity
                if adaptive_filter.filter_type == "bandpass" and len(adaptive_filter.cutoff_frequencies) == 2:
                    low, high = adaptive_filter.cutoff_frequencies
                    new_low = min(low * 1.02, high - 1)
                    new_high = max(high * 0.98, low + 1)
                    adaptive_filter.cutoff_frequencies = [new_low, new_high]
        
        except Exception as e:
            logger.error(f"Error adapting filter parameters: {str(e)}")
    
    def get_processor_status(self) -> Dict[str, Any]:
        """Get comprehensive processor status"""
        try:
            return {
                "signal_type": self.signal_type.value,
                "sampling_rate": self.sampling_rate,
                "processing_history_count": len(self.processing_history),
                "adaptive_filters": {name: {
                    "type": f.filter_type,
                    "order": f.order,
                    "cutoff_frequencies": f.cutoff_frequencies,
                    "performance_history_length": len(f.performance_history)
                } for name, f in self.adaptive_filters.items()},
                "life_algorithm_status": self.life_algorithm.get_performance_metrics(),
                "recent_performance": {
                    "avg_snr_improvement": np.mean(self.performance_metrics["snr_improvement"][-10:]) 
                                         if self.performance_metrics["snr_improvement"] else 0.0,
                    "avg_adaptation_score": np.mean(self.performance_metrics["adaptation_score"][-10:])
                                          if self.performance_metrics["adaptation_score"] else 0.0
                }
            }
        except Exception as e:
            return {"error": str(e)}

def create_life_signal_processor(sampling_rate: float = 1000.0, 
                               signal_type: SignalType = SignalType.GENERAL) -> LIFESignalProcessor:
    """Factory function to create L.I.F.E signal processor"""
    return LIFESignalProcessor(sampling_rate, signal_type)

# Example usage and testing
def test_life_signal_processor():
    """Test L.I.F.E signal processor functionality"""
    print("Testing L.I.F.E Theory Signal Processor...")
    
    # Create processor
    processor = create_life_signal_processor(1000.0, SignalType.EEG)
    
    # Generate test signal
    t = np.linspace(0, 2, 2000)  # 2 seconds at 1000 Hz
    clean_signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 25 * t)
    noisy_signal = clean_signal + 0.3 * np.random.randn(len(t))
    
    print(f"Generated test signal: {len(noisy_signal)} samples")
    
    # Process signal
    results = processor.process_signal_with_life(noisy_signal)
    
    print(f"Processing completed in {results['processing_time']:.3f} seconds")
    print(f"SNR improvement: {results['performance_metrics']['snr_improvement']:.3f}")
    print(f"Overall performance: {results['performance_metrics']['overall_performance']:.3f}")
    
    # Extract and display features
    features = results['final_features']
    print(f"\nSignal Features:")
    print(f"  RMS: {features.temporal_features['rms']:.3f}")
    print(f"  Dominant frequency: {features.frequency_features['dominant_frequency']:.1f} Hz")
    print(f"  Signal quality index: {features.quality_metrics['signal_quality_index']:.3f}")
    print(f"  SNR estimate: {features.quality_metrics['snr_estimate']:.1f} dB")
    
    # Test adaptive filtering
    print(f"\nTesting adaptive filtering...")
    filtered_signal = processor.adaptive_filter_signal(noisy_signal, "bandpass")
    print(f"Filtered signal length: {len(filtered_signal)}")
    
    # Get processor status
    status = processor.get_processor_status()
    print(f"\nProcessor Status:")
    print(f"  Signal type: {status['signal_type']}")
    print(f"  Processing history: {status['processing_history_count']} entries")
    print(f"  Recent SNR improvement: {status['recent_performance']['avg_snr_improvement']:.3f}")
    
    return processor, results

if __name__ == "__main__":
    # Run tests
    processor, results = test_life_signal_processor()
    print("\nL.I.F.E Signal Processor testing completed successfully!")
