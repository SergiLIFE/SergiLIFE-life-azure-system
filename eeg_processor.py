"""
EEG Processor for L.I.F.E Theory
Real-time EEG signal processing with Venturi enhancement

Copyright 2025 - Sergio Paya Borrull
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from lifetheory import LIFEEEGProcessor, create_eeg_life_processor, LearningExperience

logger = logging.getLogger(__name__)

class EEGQualityAssessment:
    """EEG signal quality assessment using Venturi principles"""
    
    def __init__(self, sampling_rate: float = 250.0):
        self.sampling_rate = sampling_rate
        self.quality_thresholds = {
            "excellent": 0.9,
            "good": 0.7,
            "fair": 0.5,
            "poor": 0.3
        }
    
    def assess_signal_quality(self, eeg_data: np.ndarray) -> Dict[str, float]:
        """Assess EEG signal quality using multiple metrics"""
        metrics = {}
        
        # Signal-to-noise ratio estimation
        metrics["snr"] = self._calculate_snr(eeg_data)
        
        # Artifact detection
        metrics["artifact_ratio"] = self._detect_artifacts(eeg_data)
        
        # Signal stability
        metrics["stability"] = self._assess_stability(eeg_data)
        
        # Frequency content quality
        metrics["frequency_quality"] = self._assess_frequency_content(eeg_data)
        
        # Overall quality score
        metrics["overall_quality"] = self._calculate_overall_quality(metrics)
        
        return metrics
    
    def _calculate_snr(self, signal: np.ndarray) -> float:
        """Calculate signal-to-noise ratio"""
        # Simple SNR estimation using signal power vs high-freq noise
        signal_power = np.var(signal)
        
        # High-frequency noise estimation (>100 Hz)
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/self.sampling_rate)
        high_freq_mask = np.abs(freqs) > 100
        noise_power = np.mean(np.abs(fft[high_freq_mask])**2)
        
        if noise_power > 0:
            snr = 10 * np.log10(signal_power / noise_power)
            return np.clip(snr / 20.0, 0.0, 1.0)  # Normalize to 0-1
        return 1.0
    
    def _detect_artifacts(self, signal: np.ndarray) -> float:
        """Detect artifacts in EEG signal"""
        # Detect extreme values (artifacts)
        threshold = 3 * np.std(signal)
        artifacts = np.abs(signal) > threshold
        artifact_ratio = np.sum(artifacts) / len(signal)
        
        return 1.0 - artifact_ratio  # Return quality (inverse of artifact ratio)
    
    def _assess_stability(self, signal: np.ndarray) -> float:
        """Assess signal stability over time"""
        # Calculate variance in signal variance over windows
        window_size = int(self.sampling_rate)  # 1 second windows
        variances = []
        
        for i in range(0, len(signal) - window_size, window_size):
            window = signal[i:i + window_size]
            variances.append(np.var(window))
        
        if len(variances) > 1:
            stability = 1.0 / (1.0 + np.var(variances))
            return np.clip(stability, 0.0, 1.0)
        return 1.0
    
    def _assess_frequency_content(self, signal: np.ndarray) -> float:
        """Assess quality of frequency content"""
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/self.sampling_rate)
        power = np.abs(fft)**2
        
        # Check for reasonable power distribution in EEG bands
        bands = {
            "delta": (0.5, 4.0),
            "theta": (4.0, 8.0),
            "alpha": (8.0, 13.0),
            "beta": (13.0, 30.0)
        }
        
        band_powers = []
        for low_freq, high_freq in bands.values():
            band_mask = (np.abs(freqs) >= low_freq) & (np.abs(freqs) <= high_freq)
            band_power = np.sum(power[band_mask])
            band_powers.append(band_power)
        
        # Quality based on balanced power distribution
        total_power = sum(band_powers)
        if total_power > 0:
            normalized_powers = np.array(band_powers) / total_power
            # Penalize extreme imbalances
            balance_score = 1.0 - np.var(normalized_powers)
            return np.clip(balance_score, 0.0, 1.0)
        return 0.5
    
    def _calculate_overall_quality(self, metrics: Dict[str, float]) -> float:
        """Calculate overall quality score"""
        weights = {
            "snr": 0.3,
            "artifact_ratio": 0.3,
            "stability": 0.2,
            "frequency_quality": 0.2
        }
        
        overall = sum(weights[key] * metrics[key] for key in weights.keys())
        return np.clip(overall, 0.0, 1.0)

class VenturiEEGProcessor:
    """Venturi-enhanced EEG processor"""
    
    def __init__(self, sampling_rate: float = 250.0, venturi_factor: float = 1.2):
        self.sampling_rate = sampling_rate
        self.venturi_factor = venturi_factor
        self.quality_assessor = EEGQualityAssessment(sampling_rate)
        
    def venturi1_eeg_quality(self, eeg_data: np.ndarray) -> Dict[str, Any]:
        """Venturi Gate 1: EEG Quality Enhancement"""
        # Assess initial quality
        initial_quality = self.quality_assessor.assess_signal_quality(eeg_data)
        
        # Apply Venturi enhancement based on quality
        enhanced_signal = self._apply_venturi_enhancement(eeg_data, initial_quality["overall_quality"])
        
        # Re-assess quality after enhancement
        final_quality = self.quality_assessor.assess_signal_quality(enhanced_signal)
        
        return {
            "enhanced_signal": enhanced_signal,
            "initial_quality": initial_quality,
            "final_quality": final_quality,
            "enhancement_factor": final_quality["overall_quality"] / max(initial_quality["overall_quality"], 0.001)
        }
    
    def _apply_venturi_enhancement(self, signal: np.ndarray, quality_score: float) -> np.ndarray:
        """Apply Venturi effect for signal enhancement"""
        # Venturi effect: acceleration through constriction
        constriction_factor = 1.0 / (1.0 + quality_score * self.venturi_factor)
        acceleration_factor = self.venturi_factor * (1.0 - quality_score)
        
        # Apply adaptive filtering based on signal quality
        if quality_score < 0.5:
            # Low quality: apply noise reduction
            enhanced = self._noise_reduction(signal)
        else:
            # High quality: preserve signal fidelity
            enhanced = signal.copy()
        
        # Apply Venturi transformation
        enhanced = enhanced * constriction_factor * (1.0 + acceleration_factor)
        
        return enhanced
    
    def _noise_reduction(self, signal: np.ndarray) -> np.ndarray:
        """Apply noise reduction to low-quality signals"""
        # Simple moving average filter for noise reduction
        window_size = max(5, int(self.sampling_rate * 0.02))  # 20ms window
        
        if len(signal) < window_size:
            return signal
        
        # Apply moving average
        filtered = np.convolve(signal, np.ones(window_size)/window_size, mode='same')
        
        return filtered

class EEGProcessor:
    """Main EEG processor integrating L.I.F.E Theory and Venturi enhancement"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
        
        self.sampling_rate = config.get("sampling_rate", 250.0)
        self.life_processor = create_eeg_life_processor(config)
        self.venturi_processor = VenturiEEGProcessor(
            self.sampling_rate, 
            config.get("venturi_factor", 1.2)
        )
        
        # Frequency band definitions
        self.frequency_bands = {
            "delta": (0.5, 4.0),
            "theta": (4.0, 8.0),
            "alpha": (8.0, 13.0),
            "beta": (13.0, 30.0),
            "gamma": (30.0, 100.0)
        }
        
        logger.info("EEG Processor initialized with L.I.F.E Theory and Venturi enhancement")
    
    def process(self, eeg_data: np.ndarray, channels: List[str] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main EEG processing pipeline"""
        if context is None:
            context = {}
        
        results = {
            "timestamp": datetime.now(),
            "sampling_rate": self.sampling_rate,
            "channels": channels or [f"CH{i+1}" for i in range(len(eeg_data))],
            "processing_stages": {}
        }
        
        try:
            # Stage 1: Venturi quality enhancement
            venturi_results = {}
            enhanced_data = []
            
            for i, channel_data in enumerate(eeg_data):
                channel_name = results["channels"][i]
                channel_result = self.venturi_processor.venturi1_eeg_quality(channel_data)
                venturi_results[channel_name] = channel_result
                enhanced_data.append(channel_result["enhanced_signal"])
            
            results["processing_stages"]["venturi_enhancement"] = venturi_results
            enhanced_data = np.array(enhanced_data)
            
            # Stage 2: L.I.F.E Theory processing
            life_results = self.life_processor.process_eeg(enhanced_data, results["channels"])
            results["processing_stages"]["life_processing"] = life_results
            
            # Stage 3: Feature extraction
            features = self._extract_comprehensive_features(enhanced_data, life_results)
            results["features"] = features
            
            # Stage 4: Performance assessment
            performance = self._assess_processing_performance(venturi_results, life_results)
            results["performance"] = performance
            
            # Create learning experience for adaptation
            self._create_learning_experience(eeg_data, enhanced_data, performance, context)
            
            logger.info(f"EEG processing completed with performance: {performance['overall_score']:.3f}")
            
        except Exception as e:
            logger.error(f"Error in EEG processing: {e}")
            results["error"] = str(e)
        
        return results
    
    def _extract_comprehensive_features(self, enhanced_data: np.ndarray, life_results: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Extract comprehensive EEG features"""
        features = {}
        
        # Extract frequency band features for each channel
        for i, channel_name in enumerate(life_results.keys()):
            channel_data = life_results[channel_name]
            channel_features = self.life_processor.extract_frequency_features(channel_data)
            features[channel_name] = channel_features
        
        # Global features across all channels
        features["global"] = {
            "total_power": np.sum([np.var(data) for data in life_results.values()]),
            "channel_correlation": self._calculate_channel_correlations(life_results),
            "spectral_centroid": self._calculate_spectral_centroid(enhanced_data),
            "temporal_complexity": self._calculate_temporal_complexity(enhanced_data)
        }
        
        return features
    
    def _calculate_channel_correlations(self, channel_data: Dict[str, np.ndarray]) -> float:
        """Calculate average correlation between channels"""
        channels = list(channel_data.values())
        if len(channels) < 2:
            return 0.0
        
        correlations = []
        for i in range(len(channels)):
            for j in range(i+1, len(channels)):
                if len(channels[i]) == len(channels[j]):
                    corr = np.corrcoef(channels[i], channels[j])[0, 1]
                    if not np.isnan(corr):
                        correlations.append(abs(corr))
        
        return np.mean(correlations) if correlations else 0.0
    
    def _calculate_spectral_centroid(self, data: np.ndarray) -> float:
        """Calculate spectral centroid across all channels"""
        all_centroids = []
        
        for channel_data in data:
            fft = np.fft.fft(channel_data)
            freqs = np.fft.fftfreq(len(channel_data), 1/self.sampling_rate)
            magnitude = np.abs(fft)
            
            # Calculate centroid
            centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
            all_centroids.append(abs(centroid))
        
        return np.mean(all_centroids)
    
    def _calculate_temporal_complexity(self, data: np.ndarray) -> float:
        """Calculate temporal complexity measure"""
        complexities = []
        
        for channel_data in data:
            # Simple complexity measure based on variance of differences
            diff_var = np.var(np.diff(channel_data))
            signal_var = np.var(channel_data)
            
            if signal_var > 0:
                complexity = diff_var / signal_var
                complexities.append(complexity)
        
        return np.mean(complexities) if complexities else 0.0
    
    def _assess_processing_performance(self, venturi_results: Dict, life_results: Dict) -> Dict[str, float]:
        """Assess overall processing performance"""
        # Aggregate quality improvements from Venturi processing
        quality_improvements = []
        for channel_result in venturi_results.values():
            improvement = channel_result["enhancement_factor"]
            quality_improvements.append(improvement)
        
        venturi_performance = np.mean(quality_improvements)
        
        # Assess L.I.F.E processing performance
        life_performance = self.life_processor.get_performance_metrics()
        
        # Overall performance score
        overall_score = 0.6 * venturi_performance + 0.4 * life_performance.get("mean_performance", 0.5)
        
        return {
            "venturi_enhancement": venturi_performance,
            "life_performance": life_performance["mean_performance"],
            "overall_score": overall_score,
            "quality_improvement": np.mean(quality_improvements),
            "processing_efficiency": life_performance.get("venturi_efficiency", 1.0)
        }
    
    def _create_learning_experience(self, original_data: np.ndarray, processed_data: np.ndarray, 
                                   performance: Dict[str, float], context: Dict[str, Any]) -> None:
        """Create learning experience for L.I.F.E adaptation"""
        experience = LearningExperience(
            timestamp=datetime.now(),
            input_data=original_data.flatten(),
            output_data=processed_data.flatten(),
            context=context,
            performance_metric=performance["overall_score"],
            adaptation_factor=performance.get("quality_improvement", 1.0)
        )
        
        self.life_processor.adapt(experience)
    
    def get_processor_status(self) -> Dict[str, Any]:
        """Get current processor status and metrics"""
        life_metrics = self.life_processor.get_performance_metrics()
        
        return {
            "sampling_rate": self.sampling_rate,
            "life_metrics": life_metrics,
            "venturi_factor": self.venturi_processor.venturi_factor,
            "frequency_bands": self.frequency_bands,
            "ready": True
        }
    
    def save_processor_state(self, filepath: str) -> None:
        """Save processor state"""
        self.life_processor.save_state(filepath)
        logger.info(f"EEG Processor state saved to {filepath}")
    
    def load_processor_state(self, filepath: str) -> None:
        """Load processor state"""
        self.life_processor.load_state(filepath)
        logger.info(f"EEG Processor state loaded from {filepath}")

# Factory function for Azure Functions integration
def create_eeg_processor(config: Dict[str, Any] = None) -> EEGProcessor:
    """Create EEG processor for Azure Functions deployment"""
    if config is None:
        config = {
            "sampling_rate": 250.0,
            "learning_rate": 0.005,
            "venturi_factor": 1.2,
            "max_experiences": 5000
        }
    
    return EEGProcessor(config)

# Example usage
if __name__ == "__main__":
    # Create EEG processor
    processor = create_eeg_processor()
    
    # Simulate EEG data (4 channels, 1000 samples)
    eeg_data = np.random.randn(4, 1000) * 50  # Typical EEG amplitude range
    channels = ["Fp1", "Fp2", "C3", "C4"]
    
    # Process EEG data
    results = processor.process(eeg_data, channels, {"experiment": "demo"})
    
    # Display results
    print("EEG Processing Results:")
    print(f"Channels processed: {results['channels']}")
    print(f"Overall performance: {results['performance']['overall_score']:.3f}")
    print(f"Quality improvement: {results['performance']['quality_improvement']:.3f}")
    
    # Show processor status
    status = processor.get_processor_status()
    print(f"\nProcessor Status:")
    print(f"L.I.F.E experiences: {status['life_metrics']['experience_count']}")
    print(f"Processing efficiency: {status['life_metrics']['venturi_efficiency']:.3f}")
    
    print("\nEEG processing demonstration completed successfully!")
