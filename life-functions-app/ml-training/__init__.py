"""
ML Training Pipeline Azure Function
Layer 4: Adaptive learning algorithms with real-time model updates

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import logging
import pickle
from datetime import datetime
from typing import Any, Dict, List

import azure.functions as func
import numpy as np

# ML imports (would be available in Azure ML environment)
try:
    from sklearn.metrics import accuracy_score, f1_score
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("ML libraries not available, using simulation mode")

# Configure logging for enterprise deployment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThompsonSamplingBandit:
    """Thompson Sampling for contextual bandit content optimization"""

    def __init__(self, n_arms: int = 10, n_features: int = 8):
        self.n_arms = n_arms
        self.n_features = n_features

        # Initialize beta distributions for each arm
        self.alpha = np.ones((n_arms, n_features))  # Success counts
        self.beta = np.ones((n_arms, n_features))  # Failure counts

        # Track performance
        self.total_rewards = np.zeros(n_arms)
        self.total_pulls = np.zeros(n_arms)

    def select_arm(self, context: np.ndarray) -> int:
        """Select arm using Thompson Sampling"""
        try:
            # Sample from beta distributions
            theta_samples = np.random.beta(self.alpha, self.beta)

            # Calculate expected reward for each arm given context
            expected_rewards = np.dot(theta_samples, context)

            # Select arm with highest expected reward
            return int(np.argmax(expected_rewards))

        except Exception as e:
            logger.error("Thompson sampling failed: %s", e)
            return np.random.randint(self.n_arms)

    def update(self, arm: int, context: np.ndarray, reward: float):
        """Update beta distributions based on observed reward"""
        try:
            # Update counts (simplified update rule)
            reward_vector = context * reward
            self.alpha[arm] += reward_vector
            self.beta[arm] += context - reward_vector

            # Track overall performance
            self.total_rewards[arm] += reward
            self.total_pulls[arm] += 1

        except Exception as e:
            logger.error("Thompson sampling update failed: %s", e)

    def get_arm_statistics(self) -> Dict[str, Any]:
        """Get performance statistics for all arms"""
        return {
            "total_rewards": self.total_rewards.tolist(),
            "total_pulls": self.total_pulls.tolist(),
            "average_rewards": (
                self.total_rewards / (self.total_pulls + 1e-10)
            ).tolist(),
            "regret_bounds": [
                np.sqrt(arm * np.log(sum(self.total_pulls))) / (pulls + 1)
                for arm, pulls in enumerate(self.total_pulls)
            ],
        }


class NeuroplasticityModel:
    """Neuroplasticity modeling with growth equations"""

    def __init__(self):
        self.plasticity_params = {
            "baseline_growth": 0.01,
            "experience_factor": 0.1,
            "stress_decay": 0.05,
            "consolidation_threshold": 0.75,
        }

        # Track neuroplasticity state
        self.experience_history = []
        self.plasticity_scores = []

    def calculate_neuroplasticity(
        self, eeg_features: Dict[str, float], learning_outcome: Dict[str, float]
    ) -> float:
        """Calculate neuroplasticity score based on experience and outcomes"""
        try:
            # Extract relevant features
            theta_power = eeg_features.get("theta_power", 0.0)
            alpha_power = eeg_features.get("alpha_power", 0.0)
            coherence = eeg_features.get("mean_coherence", 0.0)

            # Learning outcome metrics
            retention = learning_outcome.get("knowledge_retention", 0.5)
            improvement = learning_outcome.get("skill_improvement", 0.0)

            # Neuroplasticity equation: P = θ × (α + coherence) ×
            # (retention + improvement)
            plasticity_score = (
                theta_power
                * (alpha_power + coherence)
                * (retention + improvement + self.plasticity_params["baseline_growth"])
            )

            # Apply experience factor
            if self.experience_history:
                experience_factor = np.mean(self.experience_history[-10:])
                plasticity_score *= (
                    1 + experience_factor * self.plasticity_params["experience_factor"]
                )

            # Bound between 0 and 1
            plasticity_score = min(1.0, max(0.0, plasticity_score))

            # Update history
            self.experience_history.append(plasticity_score)
            self.plasticity_scores.append(plasticity_score)

            # Keep only recent history
            if len(self.experience_history) > 100:
                self.experience_history = self.experience_history[-100:]
                self.plasticity_scores = self.plasticity_scores[-100:]

            return plasticity_score

        except Exception as e:
            logger.error("Neuroplasticity calculation failed: %s", e)
            return 0.5

    def predict_growth_potential(self, current_score: float) -> Dict[str, float]:
        """Predict future neuroplasticity growth potential"""
        try:
            if len(self.plasticity_scores) < 5:
                return {"growth_potential": 0.1, "confidence": 0.5}

            # Simple trend analysis
            recent_trend = np.polyfit(
                range(len(self.plasticity_scores[-10:])),
                self.plasticity_scores[-10:],
                1,
            )[0]

            growth_potential = max(0.0, recent_trend * 10)
            confidence = min(1.0, len(self.plasticity_scores) / 20.0)

            return {
                "growth_potential": float(growth_potential),
                "confidence": float(confidence),
                "trend_slope": float(recent_trend),
            }

        except Exception as e:
            logger.error("Growth potential prediction failed: %s", e)
            return {"growth_potential": 0.0, "confidence": 0.0}


class FuzzyPIDController:
    """Fuzzy PID controller for intelligent system response optimization"""

    def __init__(self):
        self.pid_params = {
            "kp": 1.0,  # Proportional gain
            "ki": 0.1,  # Integral gain
            "kd": 0.05,  # Derivative gain
        }

        self.error_history = []
        self.integral_error = 0.0
        self.previous_error = 0.0

    def fuzzy_adjustment(self, error: float, error_rate: float) -> Dict[str, float]:
        """Apply fuzzy logic to adjust PID parameters"""
        try:
            # Fuzzy membership functions
            def membership_low(x):
                return max(0, 1 - abs(x) / 0.5)

            def membership_medium(x):
                return max(0, 1 - abs(x - 0.5) / 0.3)

            def membership_high(x):
                return max(0, (abs(x) - 0.3) / 0.7) if abs(x) > 0.3 else 0

            # Fuzzify inputs
            error_membership = {
                "low": membership_low(abs(error)),
                "medium": membership_medium(abs(error)),
                "high": membership_high(abs(error)),
            }

            error_rate_membership = {
                "low": membership_low(abs(error_rate)),
                "medium": membership_medium(abs(error_rate)),
                "high": membership_high(abs(error_rate)),
            }

            # Fuzzy rules (simplified)
            kp_adjust = (
                error_membership["low"] * error_rate_membership["low"] * 0.8
                + error_membership["medium"] * error_rate_membership["medium"] * 1.0
                + error_membership["high"] * error_rate_membership["high"] * 1.2
            )

            ki_adjust = (
                error_membership["low"] * error_rate_membership["low"] * 0.05
                + error_membership["medium"] * error_rate_membership["medium"] * 0.1
                + error_membership["high"] * error_rate_membership["high"] * 0.15
            )

            kd_adjust = (
                error_membership["low"] * error_rate_membership["low"] * 0.02
                + error_membership["medium"] * error_rate_membership["medium"] * 0.05
                + error_membership["high"] * error_rate_membership["high"] * 0.08
            )

            return {
                "kp_adjusted": float(self.pid_params["kp"] * kp_adjust),
                "ki_adjusted": float(self.pid_params["ki"] * ki_adjust),
                "kd_adjusted": float(self.pid_params["kd"] * kd_adjust),
                "fuzzy_confidence": float((kp_adjust + ki_adjust + kd_adjust) / 3),
            }

        except Exception as e:
            logger.error("Fuzzy adjustment failed: %s", e)
            return {
                "kp_adjusted": self.pid_params["kp"],
                "ki_adjusted": self.pid_params["ki"],
                "kd_adjusted": self.pid_params["kd"],
                "fuzzy_confidence": 0.5,
            }

    def compute_control_signal(self, setpoint: float, process_variable: float) -> float:
        """Compute PID control signal with fuzzy adaptation"""
        try:
            error = setpoint - process_variable

            # Update integral and derivative terms
            self.integral_error += error
            derivative_error = error - self.previous_error

            # Apply fuzzy adjustment
            fuzzy_params = self.fuzzy_adjustment(error, derivative_error)

            # Compute control signal
            control_signal = (
                fuzzy_params["kp_adjusted"] * error
                + fuzzy_params["ki_adjusted"] * self.integral_error
                + fuzzy_params["kd_adjusted"] * derivative_error
            )

            # Update history
            self.previous_error = error
            self.error_history.append(error)

            if len(self.error_history) > 100:
                self.error_history = self.error_history[-100:]

            return control_signal

        except Exception as e:
            logger.error("PID control computation failed: %s", e)
            return 0.0


class LIFE_ML_Pipeline:
    """Complete ML pipeline for L.I.F.E. platform"""

    def __init__(self):
        self.thompson_bandit = ThompsonSamplingBandit()
        self.neuroplasticity_model = NeuroplasticityModel()
        self.fuzzy_pid = FuzzyPIDController()

        # Neural network for pattern recognition (simplified)
        if ML_AVAILABLE:
            self.pattern_recognizer = MLPClassifier(
                hidden_layer_sizes=(64, 32),
                activation="relu",
                solver="adam",
                max_iter=1000,
            )
            self.is_trained = False
        else:
            self.pattern_recognizer = None
            self.is_trained = False

        # Training data
        self.training_data = []
        self.training_labels = []

    def process_learning_session(
        self, quantum_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a complete learning session through the ML pipeline"""
        try:
            # Extract features from quantum result
            trait_scores = quantum_result.get("trait_projection", {}).get(
                "trait_scores", {}
            )
            eeg_features = quantum_result.get("frequency_features", {})

            # Simulate learning outcome (would come from user interaction data)
            learning_outcome = {
                "knowledge_retention": np.random.uniform(0.6, 0.9),
                "skill_improvement": np.random.uniform(0.1, 0.4),
                "neural_adaptation": np.random.uniform(0.7, 0.95),
            }

            # Step 1: Neuroplasticity modeling
            plasticity_score = self.neuroplasticity_model.calculate_neuroplasticity(
                eeg_features, learning_outcome
            )

            growth_potential = self.neuroplasticity_model.predict_growth_potential(
                plasticity_score
            )

            # Step 2: Thompson sampling for content optimization
            context_features = np.array(
                [
                    trait_scores.get("focus_trait", 0.5),
                    trait_scores.get("memory_trait", 0.5),
                    trait_scores.get("attention_trait", 0.5),
                    trait_scores.get("learning_trait", 0.5),
                    plasticity_score,
                    eeg_features.get("mean_coherence", 0.5),
                    learning_outcome["knowledge_retention"],
                    learning_outcome["skill_improvement"],
                ]
            )

            recommended_content_arm = self.thompson_bandit.select_arm(context_features)

            # Simulate reward based on learning outcome
            reward = (
                learning_outcome["knowledge_retention"]
                * learning_outcome["skill_improvement"]
            )
            self.thompson_bandit.update(
                recommended_content_arm, context_features, reward
            )

            # Step 3: Fuzzy PID control for system optimization
            target_engagement = 0.85  # Target engagement score
            current_engagement = learning_outcome["neural_adaptation"]

            control_signal = self.fuzzy_pid.compute_control_signal(
                target_engagement, current_engagement
            )

            # Step 4: Pattern recognition training
            if self.pattern_recognizer and len(self.training_data) > 10:
                self._update_pattern_recognizer(context_features, learning_outcome)

            # Compile ML insights
            ml_insights = {
                "timestamp": datetime.now().isoformat(),
                "user_id": quantum_result.get("user_id", "unknown"),
                "session_id": quantum_result.get("session_id", "unknown"),
                "neuroplasticity_score": plasticity_score,
                "growth_potential": growth_potential,
                "recommended_content_arm": recommended_content_arm,
                "content_optimization_reward": reward,
                "system_control_signal": control_signal,
                "learning_outcome": learning_outcome,
                "thompson_bandit_stats": self.thompson_bandit.get_arm_statistics(),
                "pattern_recognizer_trained": self.is_trained,
                "training_data_size": len(self.training_data),
            }

            logger.info(
                "ML pipeline processed session for user %s: "
                "plasticity=%.2f, reward=%.2f",
                ml_insights["user_id"],
                plasticity_score,
                reward,
            )

            return ml_insights

        except Exception as e:
            logger.error("ML pipeline processing failed: %s", e)
            return {
                "timestamp": datetime.now().isoformat(),
                "processing_stage": "ml_error",
                "error": str(e),
            }

    def _update_pattern_recognizer(
        self, features: np.ndarray, outcome: Dict[str, float]
    ):
        """Update pattern recognition model"""
        try:
            # Create training example
            feature_vector = features.tolist()
            label = (
                1 if outcome["knowledge_retention"] > 0.75 else 0
            )  # Binary classification

            self.training_data.append(feature_vector)
            self.training_labels.append(label)

            # Retrain if we have enough data
            if len(self.training_data) >= 50 and len(self.training_data) % 25 == 0:
                X = np.array(self.training_data)
                y = np.array(self.training_labels)

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )

                self.pattern_recognizer.fit(X_train, y_train)
                self.is_trained = True

                # Evaluate
                y_pred = self.pattern_recognizer.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average="weighted")

                logger.info(
                    "Pattern recognizer updated: " "accuracy=%.2f, f1=%.2f",
                    accuracy,
                    f1,
                )

        except Exception as e:
            logger.error(f"Pattern recognizer update failed: {e}")

    def get_model_snapshot(self) -> Dict[str, Any]:
        """Get current model state for persistence"""
        return {
            "thompson_bandit": {
                "alpha": self.thompson_bandit.alpha.tolist(),
                "beta": self.thompson_bandit.beta.tolist(),
                "total_rewards": self.thompson_bandit.total_rewards.tolist(),
                "total_pulls": self.thompson_bandit.total_pulls.tolist(),
            },
            "neuroplasticity_model": {
                "experience_history": self.neuroplasticity_model.experience_history,
                "plasticity_scores": self.neuroplasticity_model.plasticity_scores,
                "params": self.neuroplasticity_model.plasticity_params,
            },
            "fuzzy_pid": {
                "pid_params": self.fuzzy_pid.pid_params,
                "integral_error": self.fuzzy_pid.integral_error,
                "previous_error": self.fuzzy_pid.previous_error,
                "error_history_length": len(self.fuzzy_pid.error_history),
            },
            "training_data_size": len(self.training_data),
            "is_trained": self.is_trained,
            "snapshot_timestamp": datetime.now().isoformat(),
        }


# Global ML pipeline instance
ml_pipeline = LIFE_ML_Pipeline()


def main(
    timer: func.TimerRequest,
    quantumResults: List[func.Document],
    modelOutput: func.Out[bytes],
) -> None:
    """
    Azure Function entry point for ML training pipeline
    Processes quantum results and updates ML models
    """
    try:
        logger.info(
            "ML training triggered, processing %d quantum results", len(quantumResults)
        )

        processed_sessions = []

        for result in quantumResults:
            try:
                # Convert document to dict
                quantum_data = dict(result)

                # Process through ML pipeline
                ml_insights = ml_pipeline.process_learning_session(quantum_data)

                processed_sessions.append(ml_insights)

                logger.info(
                    "Processed ML insights for user %s",
                    ml_insights.get("user_id", "unknown"),
                )

            except Exception as e:
                logger.error(f"Failed to process quantum result: {e}")
                continue

        # Generate model snapshot for persistence
        if processed_sessions:
            model_snapshot = ml_pipeline.get_model_snapshot()

            # Serialize and store model
            model_bytes = pickle.dumps(model_snapshot)
            modelOutput.set(model_bytes)

            logger.info(
                "ML training completed: processed %d sessions, " "saved model snapshot",
                len(processed_sessions),
            )

    except Exception as e:
        logger.error("ML training function failed: %s", e)
