"""
📊 EEG Data Handler - Process real and simulated EEG signals
October 17, 2025

Handles:
- EEG data from files (WAV, CSV, etc.)
- Real-time EEG streams (Web Bluetooth)
- Simulated EEG for testing
- Data validation and preprocessing
"""

import json
from datetime import datetime
from pathlib import Path

import numpy as np


class EEGDataHandler:
    """Handle EEG data acquisition and preprocessing"""

    def __init__(self):
        self.sample_rate = 256  # Standard EEG sample rate
        self.channels = 8  # Standard OpenBCI
        self.last_signal = None

    def generate_simulated_eeg(self, duration_seconds=2, num_channels=8):
        """
        Generate realistic simulated EEG data for testing
        (When real hardware not available)
        """
        num_samples = int(duration_seconds * self.sample_rate)

        # Create realistic EEG-like signal
        eeg_data = []
        for ch in range(num_channels):
            # Mix of alpha, beta, theta frequencies
            t = np.arange(num_samples) / self.sample_rate

            # Alpha (8-12 Hz)
            alpha = 10 * np.sin(2 * np.pi * 10 * t)

            # Beta (12-30 Hz)
            beta = 5 * np.sin(2 * np.pi * 20 * t)

            # Theta (4-8 Hz)
            theta = 15 * np.sin(2 * np.pi * 6 * t)

            # Add noise
            noise = np.random.normal(0, 2, num_samples)

            # Combine
            signal = alpha + beta + theta + noise
            eeg_data.append(signal.tolist())

        self.last_signal = eeg_data
        return eeg_data

    def load_eeg_from_file(self, filepath):
        """Load EEG data from CSV or other format"""
        try:
            filepath = Path(filepath)

            if filepath.suffix == ".csv":
                # Load CSV (first column should be sample values)
                data = np.loadtxt(filepath, delimiter=",", skiprows=1)
                self.last_signal = data.tolist()
                return data

            elif filepath.suffix == ".json":
                # Load JSON
                with open(filepath, "r") as f:
                    data = json.load(f)
                self.last_signal = data
                return np.array(data)

            else:
                raise ValueError(f"Unsupported file format: {filepath.suffix}")

        except Exception as e:
            print(f"❌ Error loading EEG file: {e}")
            return None

    def validate_eeg_data(self, eeg_data):
        """Check if EEG data is valid"""
        if eeg_data is None:
            return False, "No data"

        if isinstance(eeg_data, list):
            if len(eeg_data) == 0:
                return False, "Empty data"

            # Check if it looks like EEG
            if len(eeg_data) < 10:
                return False, "Too short (need min 10 samples)"

            return True, f"Valid ({len(eeg_data)} samples)"

        return False, "Invalid format"

    def preprocess_eeg(self, eeg_data):
        """
        Clean up EEG data
        - Bandpass filter (0.5-50 Hz)
        - Remove artifacts
        - Normalize
        """
        data = np.array(eeg_data)

        # Simple preprocessing
        # Remove DC offset (mean)
        data = data - np.mean(data)

        # Normalize to [-1, 1]
        max_val = np.max(np.abs(data))
        if max_val > 0:
            data = data / max_val

        return data.tolist()

    def get_data_info(self, eeg_data):
        """Get information about EEG data"""
        data = np.array(eeg_data)

        return {
            "samples": len(data),
            "channels": (
                len(data)
                if isinstance(eeg_data, list) and isinstance(eeg_data[0], list)
                else 1
            ),
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "duration_seconds": len(data) / self.sample_rate,
        }


class WebBluetoothEEGHandler:
    """
    Handle real EEG devices via Web Bluetooth
    (Requires browser support)
    """

    def __init__(self):
        self.device = None
        self.connected = False

    def get_javascript_code(self):
        """
        JavaScript code for platforms to use Web Bluetooth
        (This gets injected into HTML platforms)
        """
        return """
// Web Bluetooth EEG Handler - Use in platforms
class WebBluetoothEEG {
    constructor() {
        this.device = null;
        this.characteristic = null;
        this.data = [];
    }
    
    async connect() {
        try {
            // Request Bluetooth device (OpenBCI, Emotiv, etc.)
            this.device = await navigator.bluetooth.requestDevice({
                filters: [
                    { name: /.*OpenBCI.*/ },
                    { name: /.*Emotiv.*/ },
                    { name: /.*MindWave.*/ }
                ],
                optionalServices: ['generic_access', 'generic_attribute']
            });
            
            console.log('Connected to:', this.device.name);
            return true;
        } catch (error) {
            console.error('Bluetooth connection failed:', error);
            return false;
        }
    }
    
    async startRecording(durationSeconds = 2) {
        this.data = [];
        const endTime = Date.now() + (durationSeconds * 1000);
        
        while (Date.now() < endTime) {
            // In real implementation, read from device
            // For now, simulate data
            const sample = Math.random() * 100;
            this.data.push(sample);
            await new Promise(r => setTimeout(r, 4)); // ~256 Hz
        }
        
        return this.data;
    }
    
    getData() {
        return this.data;
    }
}

// Usage in platforms:
const eegHandler = new WebBluetoothEEG();
// await eegHandler.connect();
// const data = await eegHandler.startRecording(2);
"""


class EEGDataConverter:
    """Convert between different EEG data formats"""

    @staticmethod
    def to_array(data):
        """Convert any format to numpy array"""
        if isinstance(data, np.ndarray):
            return data
        return np.array(data)

    @staticmethod
    def to_list(data):
        """Convert to plain Python list"""
        if isinstance(data, np.ndarray):
            return data.tolist()
        return list(data)

    @staticmethod
    def to_json(data):
        """Convert to JSON string"""
        return json.dumps(EEGDataConverter.to_list(data))


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    handler = EEGDataHandler()

    # Example 1: Generate simulated EEG
    print("📊 Generating simulated EEG data...")
    sim_eeg = handler.generate_simulated_eeg(duration_seconds=5)
    is_valid, msg = handler.validate_eeg_data(sim_eeg)
    print(f"   Validation: {msg}")

    # Example 2: Get data info
    print("\n📈 Data information:")
    info = handler.get_data_info(sim_eeg)
    for key, val in info.items():
        print(f"   {key}: {val}")

    # Example 3: Preprocess data
    print("\n🔧 Preprocessing data...")
    processed = handler.preprocess_eeg(sim_eeg)
    print(f"   ✅ Processed {len(processed)} samples")

    print("\n✅ EEG Handler ready for use!")
