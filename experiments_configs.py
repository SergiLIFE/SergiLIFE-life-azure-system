#!/usr/bin/env python3
"""
L.I.F.E Platform - Experiments Configuration System
Advanced experimental design, execution, and analysis framework

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExperimentConfig:
    """Configuration manager for L.I.F.E platform experiments"""

    def __init__(self, experiments_path: str = None):
        self.experiments_path = (
            Path(experiments_path) if experiments_path else Path.cwd() / "experiments"
        )
        self.experiments_path.mkdir(exist_ok=True)
        self.active_experiments = self._load_active_experiments()

    def _load_active_experiments(self) -> Dict[str, Any]:
        """Load active experiments from storage"""
        experiments_file = self.experiments_path / "active_experiments.json"
        if experiments_file.exists():
            with open(experiments_file, "r") as f:
                return json.load(f)
        return {}

    def _save_active_experiments(self):
        """Save active experiments to storage"""
        experiments_file = self.experiments_path / "active_experiments.json"
        with open(experiments_file, "w") as f:
            json.dump(self.active_experiments, f, indent=2)

    def create_experiment(
        self,
        name: str,
        experiment_type: str,
        parameters: Dict[str, Any],
        duration_hours: int = 24,
    ) -> str:
        """Create new experiment configuration"""

        experiment_id = str(uuid.uuid4())
        experiment_config = {
            "id": experiment_id,
            "name": name,
            "type": experiment_type,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "duration_hours": duration_hours,
            "parameters": parameters,
            "metrics": [],
            "results": {},
            "metadata": {"creator": "L.I.F.E Platform", "version": "1.0.0"},
        }

        # Add experiment-specific configurations
        if experiment_type == "eeg_learning":
            experiment_config.update(self._get_eeg_experiment_config())
        elif experiment_type == "venturi_optimization":
            experiment_config.update(self._get_venturi_experiment_config())
        elif experiment_type == "quantum_processing":
            experiment_config.update(self._get_quantum_experiment_config())
        elif experiment_type == "adaptive_learning":
            experiment_config.update(self._get_adaptive_learning_config())
        elif experiment_type == "neural_pattern_analysis":
            experiment_config.update(self._get_neural_pattern_config())

        self.active_experiments[experiment_id] = experiment_config
        self._save_active_experiments()

        # Create experiment directory
        exp_dir = self.experiments_path / experiment_id
        exp_dir.mkdir(exist_ok=True)

        # Save detailed config
        with open(exp_dir / "config.json", "w") as f:
            json.dump(experiment_config, f, indent=2)

        logger.info(f"Experiment created: {name} ({experiment_id})")
        return experiment_id

    def _get_eeg_experiment_config(self) -> Dict[str, Any]:
        """Get EEG experiment specific configuration"""
        return {
            "eeg_settings": {
                "sampling_rate": 256,  # Hz
                "channels": 64,
                "reference": "average",
                "filter_settings": {
                    "high_pass": 0.1,  # Hz
                    "low_pass": 100,  # Hz
                    "notch": 50,  # Hz
                },
                "artifact_threshold": 100,  # microvolts
            },
            "learning_parameters": {
                "session_duration": 30,  # minutes
                "adaptation_rate": 0.01,
                "feedback_delay": 500,  # ms
                "difficulty_adjustment": "dynamic",
            },
            "success_criteria": {
                "min_accuracy": 0.85,
                "max_response_time": 2000,  # ms
                "signal_quality": 0.90,
            },
        }

    def _get_venturi_experiment_config(self) -> Dict[str, Any]:
        """Get Venturi gates experiment configuration"""
        return {
            "venturi_settings": {
                "gate_count": 3,
                "flow_rate_range": [100, 200],  # L/min
                "pressure_range": [1.5, 3.0],  # bar
                "optimization_target": "efficiency",
                "parallel_processing": True,
            },
            "optimization_parameters": {
                "algorithm": "gradient_descent",
                "learning_rate": 0.001,
                "max_iterations": 1000,
                "convergence_threshold": 0.001,
            },
            "success_criteria": {
                "min_efficiency": 0.95,
                "stability_factor": 0.98,
                "throughput_target": 400,  # L/min
            },
        }

    def _get_quantum_experiment_config(self) -> Dict[str, Any]:
        """Get quantum processing experiment configuration"""
        return {
            "quantum_settings": {
                "qubit_count": 16,
                "gate_types": ["X", "Y", "Z", "CNOT", "Hadamard"],
                "coherence_time": 100,  # microseconds
                "error_correction": "surface_code",
                "measurement_shots": 1024,
            },
            "circuit_parameters": {
                "depth_limit": 20,
                "entanglement_strategy": "linear",
                "optimization_level": 3,
                "transpilation": "automatic",
            },
            "success_criteria": {
                "min_fidelity": 0.99,
                "quantum_advantage": 2.0,
                "coherence_retention": 0.95,
            },
        }

    def _get_adaptive_learning_config(self) -> Dict[str, Any]:
        """Get adaptive learning experiment configuration"""
        return {
            "learning_settings": {
                "algorithm": "reinforcement_learning",
                "network_architecture": "transformer",
                "hidden_layers": [512, 256, 128],
                "activation": "relu",
                "dropout_rate": 0.2,
            },
            "adaptation_parameters": {
                "learning_rate": 0.001,
                "batch_size": 32,
                "memory_size": 10000,
                "exploration_rate": 0.1,
                "discount_factor": 0.95,
            },
            "success_criteria": {
                "convergence_time": 1000,  # iterations
                "final_accuracy": 0.95,
                "stability_score": 0.90,
            },
        }

    def _get_neural_pattern_config(self) -> Dict[str, Any]:
        """Get neural pattern analysis experiment configuration"""
        return {
            "pattern_settings": {
                "analysis_window": 1000,  # ms
                "frequency_bands": {
                    "delta": [0.5, 4],
                    "theta": [4, 8],
                    "alpha": [8, 13],
                    "beta": [13, 30],
                    "gamma": [30, 100],
                },
                "spatial_resolution": 64,  # channels
                "temporal_resolution": 4,  # ms
            },
            "classification_parameters": {
                "feature_extraction": "wavelet",
                "classifier": "svm",
                "cross_validation": 5,
                "feature_selection": "mutual_information",
            },
            "success_criteria": {
                "classification_accuracy": 0.92,
                "pattern_specificity": 0.88,
                "temporal_precision": 0.85,
            },
        }

    def start_experiment(self, experiment_id: str) -> bool:
        """Start an experiment"""
        if experiment_id not in self.active_experiments:
            logger.error(f"Experiment {experiment_id} not found")
            return False

        experiment = self.active_experiments[experiment_id]
        experiment["status"] = "running"
        experiment["started_at"] = datetime.now().isoformat()

        # Calculate end time
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=experiment["duration_hours"])
        experiment["estimated_end"] = end_time.isoformat()

        self._save_active_experiments()
        logger.info(f"Experiment started: {experiment['name']}")
        return True

    def stop_experiment(self, experiment_id: str) -> bool:
        """Stop an experiment"""
        if experiment_id not in self.active_experiments:
            logger.error(f"Experiment {experiment_id} not found")
            return False

        experiment = self.active_experiments[experiment_id]
        experiment["status"] = "stopped"
        experiment["stopped_at"] = datetime.now().isoformat()

        self._save_active_experiments()
        logger.info(f"Experiment stopped: {experiment['name']}")
        return True

    def update_experiment_metrics(self, experiment_id: str, metrics: Dict[str, Any]):
        """Update experiment metrics"""
        if experiment_id not in self.active_experiments:
            logger.error(f"Experiment {experiment_id} not found")
            return False

        experiment = self.active_experiments[experiment_id]
        metric_entry = {"timestamp": datetime.now().isoformat(), "metrics": metrics}

        experiment["metrics"].append(metric_entry)
        self._save_active_experiments()

        # Save to experiment directory
        exp_dir = self.experiments_path / experiment_id
        metrics_file = exp_dir / "metrics.json"

        if metrics_file.exists():
            with open(metrics_file, "r") as f:
                all_metrics = json.load(f)
        else:
            all_metrics = []

        all_metrics.append(metric_entry)

        with open(metrics_file, "w") as f:
            json.dump(all_metrics, f, indent=2)

        return True

    def get_experiment_status(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment status and progress"""
        if experiment_id not in self.active_experiments:
            return None

        experiment = self.active_experiments[experiment_id]

        # Calculate progress
        progress = 0
        if experiment["status"] == "running" and "started_at" in experiment:
            start_time = datetime.fromisoformat(experiment["started_at"])
            current_time = datetime.now()
            duration = timedelta(hours=experiment["duration_hours"])

            elapsed = current_time - start_time
            progress = min(
                100, (elapsed.total_seconds() / duration.total_seconds()) * 100
            )

        return {
            "id": experiment_id,
            "name": experiment["name"],
            "type": experiment["type"],
            "status": experiment["status"],
            "progress": progress,
            "metrics_count": len(experiment["metrics"]),
            "created_at": experiment["created_at"],
            "started_at": experiment.get("started_at"),
            "estimated_end": experiment.get("estimated_end"),
        }

    def list_experiments(self, status: str = None) -> list:
        """List experiments, optionally filtered by status"""
        experiments = []
        for exp_id, exp_data in self.active_experiments.items():
            if status is None or exp_data.get("status") == status:
                experiments.append(self.get_experiment_status(exp_id))

        return sorted(experiments, key=lambda x: x["created_at"], reverse=True)

    def analyze_experiment_results(self, experiment_id: str) -> Dict[str, Any]:
        """Analyze experiment results and generate insights"""
        if experiment_id not in self.active_experiments:
            return {"error": "Experiment not found"}

        experiment = self.active_experiments[experiment_id]

        if not experiment["metrics"]:
            return {"error": "No metrics available for analysis"}

        # Extract metrics data
        metrics_data = [entry["metrics"] for entry in experiment["metrics"]]

        # Basic statistical analysis
        analysis = {
            "experiment_id": experiment_id,
            "total_measurements": len(metrics_data),
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": {},
        }

        # Calculate summary statistics for numeric metrics
        numeric_metrics = {}
        for metrics in metrics_data:
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_metrics:
                        numeric_metrics[key] = []
                    numeric_metrics[key].append(value)

        for metric_name, values in numeric_metrics.items():
            if values:
                analysis["summary"][metric_name] = {
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "min": np.min(values),
                    "max": np.max(values),
                    "trend": "increasing" if values[-1] > values[0] else "decreasing",
                }

        # Check success criteria
        experiment_type = experiment["type"]
        success_criteria = experiment.get(
            f"{experiment_type.split('_')[0]}_settings", {}
        ).get("success_criteria", {})

        if success_criteria and numeric_metrics:
            analysis["success_evaluation"] = {}
            for criteria_name, threshold in success_criteria.items():
                if criteria_name in numeric_metrics:
                    latest_value = numeric_metrics[criteria_name][-1]
                    analysis["success_evaluation"][criteria_name] = {
                        "threshold": threshold,
                        "current_value": latest_value,
                        "meets_criteria": (
                            latest_value >= threshold
                            if isinstance(threshold, (int, float))
                            else False
                        ),
                    }

        return analysis


class ExperimentRunner:
    """Runs and monitors L.I.F.E platform experiments"""

    def __init__(self, config: ExperimentConfig):
        self.config = config

    def run_eeg_learning_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Run EEG learning experiment simulation"""
        experiment = self.config.active_experiments.get(experiment_id)
        if not experiment or experiment["type"] != "eeg_learning":
            return {"error": "Invalid experiment for EEG learning"}

        # Simulate EEG learning experiment
        results = []
        for session in range(10):  # 10 learning sessions
            # Simulate progressive learning
            accuracy = min(0.95, 0.60 + (session * 0.035) + np.random.normal(0, 0.02))
            response_time = max(800, 2000 - (session * 120) + np.random.normal(0, 50))
            signal_quality = min(
                0.98, 0.85 + (session * 0.013) + np.random.normal(0, 0.01)
            )

            session_metrics = {
                "session": session + 1,
                "accuracy": round(accuracy, 3),
                "response_time": round(response_time, 1),
                "signal_quality": round(signal_quality, 3),
                "learning_rate": round(0.01 + (session * 0.001), 4),
            }

            results.append(session_metrics)

            # Update experiment metrics
            self.config.update_experiment_metrics(experiment_id, session_metrics)

        return {
            "experiment_type": "eeg_learning",
            "sessions_completed": len(results),
            "final_accuracy": results[-1]["accuracy"],
            "improvement": results[-1]["accuracy"] - results[0]["accuracy"],
            "results": results,
        }

    def run_venturi_optimization_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Run Venturi gates optimization experiment"""
        experiment = self.config.active_experiments.get(experiment_id)
        if not experiment or experiment["type"] != "venturi_optimization":
            return {"error": "Invalid experiment for Venturi optimization"}

        # Simulate optimization process
        results = []
        base_efficiency = 0.85

        for iteration in range(20):  # 20 optimization iterations
            # Simulate optimization progress
            efficiency = min(
                0.98, base_efficiency + (iteration * 0.006) + np.random.normal(0, 0.005)
            )
            flow_rate = 350 + (iteration * 2.5) + np.random.normal(0, 5)
            pressure = 2.2 + np.random.normal(0, 0.1)

            iteration_metrics = {
                "iteration": iteration + 1,
                "efficiency": round(efficiency, 4),
                "flow_rate": round(flow_rate, 1),
                "pressure": round(pressure, 2),
                "convergence": min(1.0, iteration / 15),
            }

            results.append(iteration_metrics)
            self.config.update_experiment_metrics(experiment_id, iteration_metrics)

        return {
            "experiment_type": "venturi_optimization",
            "iterations_completed": len(results),
            "final_efficiency": results[-1]["efficiency"],
            "optimization_gain": results[-1]["efficiency"] - results[0]["efficiency"],
            "results": results,
        }


# Example usage and demonstration
if __name__ == "__main__":
    print("🧪 L.I.F.E Platform - Experiments Configuration System")
    print("=" * 60)

    # Initialize experiment system
    config = ExperimentConfig()
    runner = ExperimentRunner(config)

    # Create sample experiments
    experiment_types = [
        (
            "EEG Learning Optimization",
            "eeg_learning",
            {"subject_count": 10, "learning_paradigm": "adaptive"},
        ),
        (
            "Venturi Gates Performance",
            "venturi_optimization",
            {"target_efficiency": 0.97, "max_iterations": 20},
        ),
        (
            "Quantum Processing Analysis",
            "quantum_processing",
            {"qubit_count": 16, "circuit_depth": 15},
        ),
        (
            "Adaptive Learning Study",
            "adaptive_learning",
            {"network_size": "large", "dataset": "clinical"},
        ),
        (
            "Neural Pattern Recognition",
            "neural_pattern_analysis",
            {"pattern_types": ["attention", "memory"]},
        ),
    ]

    created_experiments = []

    for name, exp_type, params in experiment_types:
        print(f"\n🧪 Creating {name} experiment...")
        exp_id = config.create_experiment(name, exp_type, params, duration_hours=2)
        created_experiments.append(exp_id)
        print(f"✅ Experiment created: {exp_id[:8]}...")

    # Start and run some experiments
    if created_experiments:
        print(f"\n🚀 Starting experiments...")

        # Start EEG learning experiment
        eeg_exp_id = created_experiments[0]
        config.start_experiment(eeg_exp_id)
        eeg_results = runner.run_eeg_learning_experiment(eeg_exp_id)
        print(
            f"✅ EEG Learning completed: {eeg_results['final_accuracy']:.3f} accuracy"
        )

        # Start Venturi optimization experiment
        venturi_exp_id = created_experiments[1]
        config.start_experiment(venturi_exp_id)
        venturi_results = runner.run_venturi_optimization_experiment(venturi_exp_id)
        print(
            f"✅ Venturi Optimization completed: {venturi_results['final_efficiency']:.4f} efficiency"
        )

    # List all experiments
    print(f"\n📊 Active Experiments Summary:")
    print("-" * 40)
    experiments = config.list_experiments()

    for exp in experiments:
        print(f"🧪 {exp['name'][:25]:25} | {exp['status']:8} | {exp['progress']:5.1f}%")

    # Analyze experiment results
    if created_experiments:
        print(f"\n📈 Analysis Results:")
        print("-" * 25)

        for exp_id in created_experiments[:2]:  # Analyze first two experiments
            analysis = config.analyze_experiment_results(exp_id)
            if "error" not in analysis:
                exp_name = config.active_experiments[exp_id]["name"]
                print(f"📊 {exp_name}: {analysis['total_measurements']} measurements")

                if "success_evaluation" in analysis:
                    success_count = sum(
                        1
                        for criteria in analysis["success_evaluation"].values()
                        if criteria.get("meets_criteria", False)
                    )
                    total_criteria = len(analysis["success_evaluation"])
                    print(
                        f"   Success Rate: {success_count}/{total_criteria} criteria met"
                    )

    print(f"\n✅ Experiments Configuration System Ready!")
    print("🧪 Use ExperimentConfig for experiment management")
    print("🚀 Use ExperimentRunner for experiment execution")
    print("📊 Use analyze_experiment_results for insights")
