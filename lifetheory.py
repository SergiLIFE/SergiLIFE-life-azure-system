"""
L.I.F.E Theory - Learning Individually From Experience
Core Algorithm Implementation

Copyright 2025 - Sergio Paya Borrull
Revolutionary AI Learning System
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LearningExperience:
    """Individual learning experience record"""
    timestamp: datetime
    input_data: np.ndarray
    output_data: np.ndarray
    context: Dict[str, Any]
    performance_metric: float
    adaptation_factor: float = 1.0
    
@dataclass
class AdaptationParameters:
    """Parameters controlling L.I.F.E adaptation behavior"""
    learning_rate: float = 0.01
    experience_weight_decay: float = 0.95
    adaptation_threshold: float = 0.1
    max_experiences: int = 10000
    venturi_gate_factor: float = 1.2
    quantum_enhancement: bool = False

class ExperienceMemory:
    """Memory system for storing and retrieving learning experiences"""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.experiences: List[LearningExperience] = []
        self.performance_history: List[float] = []
        
    def add_experience(self, experience: LearningExperience) -> None:
        """Add new experience to memory"""
        self.experiences.append(experience)
        self.performance_history.append(experience.performance_metric)
        
        # Maintain memory size limit
        if len(self.experiences) > self.max_size:
            self.experiences.pop(0)
            self.performance_history.pop(0)
            
    def get_recent_experiences(self, count: int = 100) -> List[LearningExperience]:
        """Retrieve most recent experiences"""
        return self.experiences[-count:]
    
    def get_best_experiences(self, count: int = 10) -> List[LearningExperience]:
        """Retrieve best performing experiences"""
        if not self.experiences:
            return []
            
        sorted_experiences = sorted(
            self.experiences, 
            key=lambda x: x.performance_metric, 
            reverse=True
        )
        return sorted_experiences[:count]
    
    def get_performance_trend(self, window: int = 100) -> float:
        """Calculate recent performance trend"""
        if len(self.performance_history) < window:
            return 0.0
            
        recent = self.performance_history[-window:]
        return np.mean(recent[-window//2:]) - np.mean(recent[:window//2])

class VenturiGateSystem:
    """Venturi Gate System for enhanced signal processing"""
    
    def __init__(self, gate_count: int = 3, efficiency_factor: float = 1.2):
        self.gate_count = gate_count
        self.efficiency_factor = efficiency_factor
        self.gate_states = np.ones(gate_count)
        
    def process_signal(self, signal: np.ndarray) -> np.ndarray:
        """Apply Venturi gate processing to signal"""
        processed = signal.copy()
        
        for i, gate_state in enumerate(self.gate_states):
            # Apply Venturi effect - signal acceleration through constriction
            constriction_factor = 1.0 / (1.0 + gate_state * self.efficiency_factor)
            acceleration_factor = self.efficiency_factor * gate_state
            
            processed = processed * constriction_factor * acceleration_factor
            
        return processed
    
    def adapt_gates(self, performance_feedback: float) -> None:
        """Adapt gate states based on performance feedback"""
        adaptation = 0.01 * performance_feedback
        self.gate_states = np.clip(
            self.gate_states + adaptation,
            0.1, 2.0
        )

class LIFEProcessor(ABC):
    """Abstract base class for L.I.F.E processing components"""
    
    @abstractmethod
    def process(self, data: np.ndarray, context: Dict[str, Any]) -> np.ndarray:
        """Process data through L.I.F.E algorithm"""
        pass
    
    @abstractmethod
    def adapt(self, experience: LearningExperience) -> None:
        """Adapt processor based on experience"""
        pass

class CoreLIFEAlgorithm(LIFEProcessor):
    """Core L.I.F.E Theory Algorithm Implementation"""
    
    def __init__(self, params: AdaptationParameters):
        self.params = params
        self.memory = ExperienceMemory(params.max_experiences)
        self.venturi_system = VenturiGateSystem()
        self.adaptation_matrix = np.eye(10)  # Base adaptation matrix
        self.performance_baseline = 0.5
        
        logger.info("L.I.F.E Algorithm initialized")
        
    def process(self, data: np.ndarray, context: Dict[str, Any] = None) -> np.ndarray:
        """Main L.I.F.E processing pipeline"""
        if context is None:
            context = {}
            
        try:
            # Stage 1: Signal preprocessing with Venturi gates
            preprocessed = self.venturi_system.process_signal(data)
            
            # Stage 2: Experience-based adaptation
            adapted_data = self._apply_experience_adaptation(preprocessed)
            
            # Stage 3: Individual learning component
            processed = self._individual_learning_process(adapted_data, context)
            
            # Stage 4: Performance optimization
            optimized = self._optimize_output(processed)
            
            return optimized
            
        except Exception as e:
            logger.error(f"Error in L.I.F.E processing: {e}")
            return data  # Fallback to original data
    
    def _apply_experience_adaptation(self, data: np.ndarray) -> np.ndarray:
        """Apply learning from previous experiences"""
        if not self.memory.experiences:
            return data
            
        # Get best experiences for adaptation
        best_experiences = self.memory.get_best_experiences(10)
        
        # Calculate weighted adaptation based on experience quality
        adaptation_weights = np.array([exp.performance_metric for exp in best_experiences])
        adaptation_weights = adaptation_weights / np.sum(adaptation_weights)
        
        # Apply experience-based modifications
        adapted = data.copy()
        for i, experience in enumerate(best_experiences):
            weight = adaptation_weights[i] * experience.adaptation_factor
            # Simple linear combination for demonstration
            if experience.input_data.shape == data.shape:
                adapted += weight * (experience.output_data - experience.input_data)
                
        return adapted
    
    def _individual_learning_process(self, data: np.ndarray, context: Dict[str, Any]) -> np.ndarray:
        """Core individual learning mechanism"""
        # Apply adaptation matrix learned from individual experiences
        if data.ndim == 1 and len(data) <= self.adaptation_matrix.shape[0]:
            # Pad data if necessary
            padded_data = np.zeros(self.adaptation_matrix.shape[0])
            padded_data[:len(data)] = data
            processed = np.dot(self.adaptation_matrix, padded_data)
            return processed[:len(data)]
        
        # For larger arrays, apply element-wise adaptation
        adaptation_factor = 1.0 + self.params.learning_rate * np.random.normal(0, 0.1, data.shape)
        return data * adaptation_factor
    
    def _optimize_output(self, data: np.ndarray) -> np.ndarray:
        """Final optimization stage"""
        # Apply performance-based optimization
        performance_trend = self.memory.get_performance_trend()
        optimization_factor = 1.0 + 0.1 * performance_trend
        
        return data * optimization_factor
    
    def adapt(self, experience: LearningExperience) -> None:
        """Adapt algorithm based on new experience"""
        # Store experience
        self.memory.add_experience(experience)
        
        # Update Venturi gates
        self.venturi_system.adapt_gates(experience.performance_metric)
        
        # Update adaptation matrix
        self._update_adaptation_matrix(experience)
        
        # Update performance baseline
        self._update_performance_baseline()
        
        logger.info(f"L.I.F.E adapted with performance: {experience.performance_metric}")
    
    def _update_adaptation_matrix(self, experience: LearningExperience) -> None:
        """Update the core adaptation matrix"""
        performance_delta = experience.performance_metric - self.performance_baseline
        learning_adjustment = self.params.learning_rate * performance_delta
        
        # Simple matrix update (in practice, this would be more sophisticated)
        adaptation_update = np.eye(self.adaptation_matrix.shape[0]) * learning_adjustment
        self.adaptation_matrix += adaptation_update
        
        # Normalize to prevent runaway adaptation
        self.adaptation_matrix = np.clip(self.adaptation_matrix, -2.0, 2.0)
    
    def _update_performance_baseline(self) -> None:
        """Update performance baseline from recent experiences"""
        if len(self.memory.performance_history) >= 10:
            recent_performance = np.mean(self.memory.performance_history[-10:])
            self.performance_baseline = (
                0.9 * self.performance_baseline + 
                0.1 * recent_performance
            )
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        if not self.memory.performance_history:
            return {"mean_performance": 0.0, "trend": 0.0, "experience_count": 0}
            
        return {
            "mean_performance": np.mean(self.memory.performance_history),
            "recent_performance": np.mean(self.memory.performance_history[-10:]) if len(self.memory.performance_history) >= 10 else 0.0,
            "trend": self.memory.get_performance_trend(),
            "experience_count": len(self.memory.experiences),
            "venturi_efficiency": np.mean(self.venturi_system.gate_states)
        }
    
    def save_state(self, filepath: str) -> None:
        """Save L.I.F.E algorithm state"""
        state = {
            "adaptation_matrix": self.adaptation_matrix.tolist(),
            "performance_baseline": self.performance_baseline,
            "venturi_gates": self.venturi_system.gate_states.tolist(),
            "experience_count": len(self.memory.experiences),
            "performance_history": self.memory.performance_history[-100:]  # Save last 100
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"L.I.F.E state saved to {filepath}")
    
    def load_state(self, filepath: str) -> None:
        """Load L.I.F.E algorithm state"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.adaptation_matrix = np.array(state["adaptation_matrix"])
            self.performance_baseline = state["performance_baseline"]
            self.venturi_system.gate_states = np.array(state["venturi_gates"])
            
            # Restore performance history
            self.memory.performance_history = state["performance_history"]
            
            logger.info(f"L.I.F.E state loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load L.I.F.E state: {e}")

class LIFEEEGProcessor(CoreLIFEAlgorithm):
    """Specialized L.I.F.E processor for EEG signals"""
    
    def __init__(self, params: AdaptationParameters, sampling_rate: float = 250.0):
        super().__init__(params)
        self.sampling_rate = sampling_rate
        self.frequency_bands = {
            "delta": (0.5, 4.0),
            "theta": (4.0, 8.0),
            "alpha": (8.0, 13.0),
            "beta": (13.0, 30.0),
            "gamma": (30.0, 100.0)
        }
        
    def process_eeg(self, eeg_data: np.ndarray, channels: List[str] = None) -> Dict[str, np.ndarray]:
        """Process EEG data with L.I.F.E algorithm"""
        results = {}
        
        # Process each channel individually (L.I.F.E principle)
        for i, channel_data in enumerate(eeg_data):
            channel_name = channels[i] if channels and i < len(channels) else f"CH{i+1}"
            
            # Apply L.I.F.E processing
            processed = self.process(channel_data, {"channel": channel_name, "type": "eeg"})
            results[channel_name] = processed
            
        return results
    
    def extract_frequency_features(self, eeg_data: np.ndarray) -> Dict[str, float]:
        """Extract frequency band features from EEG"""
        features = {}
        
        # Simple power spectral density calculation
        fft = np.fft.fft(eeg_data)
        freqs = np.fft.fftfreq(len(eeg_data), 1/self.sampling_rate)
        power = np.abs(fft) ** 2
        
        for band_name, (low_freq, high_freq) in self.frequency_bands.items():
            band_mask = (freqs >= low_freq) & (freqs <= high_freq)
            band_power = np.mean(power[band_mask])
            features[f"{band_name}_power"] = band_power
            
        return features

def create_life_algorithm(config: Dict[str, Any] = None) -> CoreLIFEAlgorithm:
    """Factory function to create L.I.F.E algorithm instance"""
    if config is None:
        config = {}
    
    params = AdaptationParameters(
        learning_rate=config.get("learning_rate", 0.01),
        experience_weight_decay=config.get("experience_weight_decay", 0.95),
        adaptation_threshold=config.get("adaptation_threshold", 0.1),
        max_experiences=config.get("max_experiences", 10000),
        venturi_gate_factor=config.get("venturi_gate_factor", 1.2),
        quantum_enhancement=config.get("quantum_enhancement", False)
    )
    
    return CoreLIFEAlgorithm(params)

def create_eeg_life_processor(config: Dict[str, Any] = None) -> LIFEEEGProcessor:
    """Factory function to create EEG-specialized L.I.F.E processor"""
    if config is None:
        config = {}
    
    params = AdaptationParameters(
        learning_rate=config.get("learning_rate", 0.005),  # Lower for EEG
        experience_weight_decay=config.get("experience_weight_decay", 0.98),
        adaptation_threshold=config.get("adaptation_threshold", 0.05),
        max_experiences=config.get("max_experiences", 5000),
        venturi_gate_factor=config.get("venturi_gate_factor", 1.1),
        quantum_enhancement=config.get("quantum_enhancement", False)
    )
    
    sampling_rate = config.get("sampling_rate", 250.0)
    
    return LIFEEEGProcessor(params, sampling_rate)

# Example usage and demonstration
if __name__ == "__main__":
    # Create L.I.F.E algorithm
    life_algo = create_life_algorithm()
    
    # Simulate some data processing
    test_data = np.random.randn(100)
    processed_data = life_algo.process(test_data)
    
    # Create experience and adapt
    experience = LearningExperience(
        timestamp=datetime.now(),
        input_data=test_data,
        output_data=processed_data,
        context={"test": "demonstration"},
        performance_metric=0.85
    )
    
    life_algo.adapt(experience)
    
    # Display metrics
    metrics = life_algo.get_performance_metrics()
    print("L.I.F.E Algorithm Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    print("\nL.I.F.E Theory demonstration completed successfully!")
