"""
L.I.F.E Theory Module 2: Advanced Pattern Recognition
Machine learning and pattern recognition with adaptive learning

Copyright 2025 - Sergio Paya Borrull
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA, FastICA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# Import L.I.F.E Theory core
from lifetheory import AdaptationParameters, CoreLIFEAlgorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Types of patterns that can be recognized"""

    TEMPORAL = "temporal_pattern"
    SPATIAL = "spatial_pattern"
    SPECTRAL = "spectral_pattern"
    BEHAVIORAL = "behavioral_pattern"
    NEURAL = "neural_pattern"
    PHYSIOLOGICAL = "physiological_pattern"


class LearningMode(Enum):
    """Learning modes for pattern recognition"""

    SUPERVISED = "supervised_learning"
    UNSUPERVISED = "unsupervised_learning"
    SEMI_SUPERVISED = "semi_supervised_learning"
    REINFORCEMENT = "reinforcement_learning"
    ADAPTIVE = "adaptive_learning"


@dataclass
class PatternFeatures:
    """Pattern feature representation"""

    raw_features: np.ndarray = field(default_factory=lambda: np.array([]))
    reduced_features: np.ndarray = field(default_factory=lambda: np.array([]))
    statistical_features: Dict[str, float] = field(default_factory=dict)
    complexity_measures: Dict[str, float] = field(default_factory=dict)
    quality_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class ClassificationResult:
    """Classification result structure"""

    predicted_class: int = -1
    confidence: float = 0.0
    class_probabilities: List[float] = field(default_factory=list)
    decision_boundary_distance: float = 0.0
    feature_importance: List[float] = field(default_factory=list)


@dataclass
class ClusteringResult:
    """Clustering result structure"""

    cluster_labels: List[int] = field(default_factory=list)
    cluster_centers: np.ndarray = field(default_factory=lambda: np.array([]))
    silhouette_score: float = 0.0
    inertia: float = 0.0
    num_clusters: int = 0


class LIFEPatternRecognizer:
    """Advanced pattern recognition with L.I.F.E Theory integration"""

    def __init__(self, pattern_type: PatternType = PatternType.TEMPORAL):
        self.pattern_type = pattern_type

        # Initialize L.I.F.E algorithm for adaptive pattern learning
        self.life_algorithm = CoreLIFEAlgorithm(
            learning_rate=0.02,
            max_experiences=10000,
            adaptation_params=AdaptationParameters(
                learning_rate=0.02, decay_factor=0.9, threshold=0.15
            ),
        )

        # Pattern recognition models
        self.models = {
            "neural_network": MLPClassifier(
                hidden_layer_sizes=(100, 50), max_iter=500, random_state=42
            ),
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "kmeans": KMeans(n_clusters=5, random_state=42),
            "dbscan": DBSCAN(eps=0.5, min_samples=5),
        }

        # Feature processing
        self.feature_processors = {
            "scaler": StandardScaler(),
            "pca": PCA(n_components=0.95),
            "ica": FastICA(n_components=None, random_state=42),
        }

        # Pattern memory and adaptation
        self.pattern_memory = []
        self.adaptation_history = []
        self.performance_metrics = {
            "accuracy_history": [],
            "f1_history": [],
            "adaptation_scores": [],
            "pattern_complexity": [],
        }

        # Model training status
        self.trained_models = set()
        self.feature_dimensions = {}

        logger.info(f"L.I.F.E Pattern Recognizer initialized for {pattern_type.value}")

    def extract_pattern_features(
        self, data: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> PatternFeatures:
        """Extract comprehensive pattern features from data"""
        try:
            features = PatternFeatures()

            # Ensure data is 2D (samples x features)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            elif data.ndim > 2:
                data = data.reshape(data.shape[0], -1)

            features.raw_features = data.copy()

            # Statistical features
            features.statistical_features = {
                "mean": float(np.mean(data)),
                "std": float(np.std(data)),
                "variance": float(np.var(data)),
                "skewness": float(self._calculate_skewness(data.flatten())),
                "kurtosis": float(self._calculate_kurtosis(data.flatten())),
                "entropy": float(self._calculate_entropy(data.flatten())),
                "energy": float(np.sum(data**2)),
                "rms": float(np.sqrt(np.mean(data**2))),
            }

            # Complexity measures
            features.complexity_measures = {
                "lz_complexity": float(self._calculate_lz_complexity(data.flatten())),
                "approximate_entropy": float(
                    self._calculate_approximate_entropy(data.flatten())
                ),
                "sample_entropy": float(self._calculate_sample_entropy(data.flatten())),
                "fractal_dimension": float(
                    self._calculate_fractal_dimension(data.flatten())
                ),
                "spectral_entropy": float(
                    self._calculate_spectral_entropy(data.flatten())
                ),
            }

            # Quality metrics
            features.quality_metrics = {
                "signal_to_noise": float(self._estimate_snr(data.flatten())),
                "data_quality": float(self._assess_data_quality(data)),
                "feature_stability": float(self._calculate_feature_stability(data)),
                "information_content": float(self._calculate_information_content(data)),
            }

            # Dimensionality reduction
            if data.shape[1] > 10:  # Only reduce if we have enough features
                try:
                    if hasattr(self.feature_processors["pca"], "components_"):
                        reduced_data = self.feature_processors["pca"].transform(data)
                    else:
                        reduced_data = self.feature_processors["pca"].fit_transform(
                            data
                        )
                    features.reduced_features = reduced_data
                except:
                    features.reduced_features = data.copy()
            else:
                features.reduced_features = data.copy()

            return features

        except Exception as e:
            logger.error(f"Error extracting pattern features: {str(e)}")
            return PatternFeatures()

    def train_pattern_classifier(
        self, X: np.ndarray, y: np.ndarray, model_name: str = "neural_network"
    ) -> Dict[str, Any]:
        """Train pattern classifier with L.I.F.E adaptation"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Unknown model: {model_name}")

            start_time = datetime.now()

            # Preprocess features
            X_processed = self._preprocess_features(X, fit=True)

            # Extract pattern features
            pattern_features = self.extract_pattern_features(X_processed)

            # Train model
            model = self.models[model_name]

            if model_name in ["neural_network", "random_forest"]:
                # Supervised learning
                model.fit(X_processed, y)

                # Predict on training data for evaluation
                y_pred = model.predict(X_processed)

                # Calculate metrics
                accuracy = accuracy_score(y, y_pred)
                f1 = f1_score(y, y_pred, average="weighted")
                precision = precision_score(y, y_pred, average="weighted")
                recall = recall_score(y, y_pred, average="weighted")

                metrics = {
                    "accuracy": accuracy,
                    "f1_score": f1,
                    "precision": precision,
                    "recall": recall,
                }

                # Get feature importance if available
                if hasattr(model, "feature_importances_"):
                    feature_importance = model.feature_importances_.tolist()
                elif hasattr(model, "coefs_"):
                    # For neural networks, use average absolute weights
                    feature_importance = np.mean(
                        np.abs(model.coefs_[0]), axis=1
                    ).tolist()
                else:
                    feature_importance = []

            else:
                # Unsupervised learning
                cluster_labels = model.fit_predict(X_processed)

                metrics = {
                    "num_clusters": len(np.unique(cluster_labels)),
                    "silhouette_score": self._calculate_silhouette_score(
                        X_processed, cluster_labels
                    ),
                }
                feature_importance = []

            # Adapt using L.I.F.E algorithm
            adaptation_context = {
                "model_type": model_name,
                "performance": metrics.get(
                    "accuracy", metrics.get("silhouette_score", 0.5)
                ),
                "feature_count": X_processed.shape[1],
                "sample_count": X_processed.shape[0],
            }

            adapted_features = self.life_algorithm.process(
                X_processed.flatten()[:1000],  # Use subset for adaptation
                adaptation_context,
            )

            # Update performance history
            self.performance_metrics["accuracy_history"].append(
                metrics.get("accuracy", 0.5)
            )
            self.performance_metrics["f1_history"].append(metrics.get("f1_score", 0.5))

            # Mark model as trained
            self.trained_models.add(model_name)
            self.feature_dimensions[model_name] = X_processed.shape[1]

            training_time = (datetime.now() - start_time).total_seconds()

            result = {
                "model_name": model_name,
                "training_metrics": metrics,
                "feature_importance": feature_importance,
                "pattern_features": pattern_features,
                "adaptation_result": adapted_features,
                "training_time": training_time,
                "life_metrics": self.life_algorithm.get_performance_metrics(),
                "success": True,
            }

            logger.info(
                f"Model {model_name} trained successfully in {training_time:.2f}s"
            )
            return result

        except Exception as e:
            logger.error(f"Error training model {model_name}: {str(e)}")
            return {
                "model_name": model_name,
                "success": False,
                "error": str(e),
                "training_time": 0.0,
            }

    def classify_pattern(
        self, X: np.ndarray, model_name: str = "neural_network"
    ) -> ClassificationResult:
        """Classify pattern using trained model"""
        try:
            if model_name not in self.trained_models:
                raise ValueError(f"Model {model_name} not trained yet")

            # Preprocess features
            X_processed = self._preprocess_features(X, fit=False)

            # Ensure correct dimensions
            if X_processed.shape[1] != self.feature_dimensions[model_name]:
                # Pad or truncate features
                if X_processed.shape[1] < self.feature_dimensions[model_name]:
                    padding = np.zeros(
                        (
                            X_processed.shape[0],
                            self.feature_dimensions[model_name] - X_processed.shape[1],
                        )
                    )
                    X_processed = np.hstack([X_processed, padding])
                else:
                    X_processed = X_processed[:, : self.feature_dimensions[model_name]]

            model = self.models[model_name]

            # Make prediction
            if hasattr(model, "predict_proba"):
                # Classification with probabilities
                predictions = model.predict(X_processed)
                probabilities = model.predict_proba(X_processed)

                result = ClassificationResult(
                    predicted_class=int(predictions[0]) if len(predictions) > 0 else -1,
                    confidence=(
                        float(np.max(probabilities[0]))
                        if len(probabilities) > 0
                        else 0.0
                    ),
                    class_probabilities=(
                        probabilities[0].tolist() if len(probabilities) > 0 else []
                    ),
                    decision_boundary_distance=(
                        float(np.max(probabilities[0]) - np.sort(probabilities[0])[-2])
                        if len(probabilities) > 0 and len(probabilities[0]) > 1
                        else 0.0
                    ),
                )

                # Feature importance for this prediction
                if hasattr(model, "feature_importances_"):
                    result.feature_importance = model.feature_importances_.tolist()

            else:
                # Simple prediction
                predictions = model.predict(X_processed)
                result = ClassificationResult(
                    predicted_class=int(predictions[0]) if len(predictions) > 0 else -1,
                    confidence=0.5,  # Unknown confidence for non-probabilistic models
                )

            # Adapt based on prediction confidence
            if result.confidence < 0.7:  # Low confidence prediction
                adaptation_context = {
                    "low_confidence": True,
                    "predicted_class": result.predicted_class,
                    "confidence": result.confidence,
                }
                self.life_algorithm.process(
                    X_processed.flatten()[:100], adaptation_context
                )

            return result

        except Exception as e:
            logger.error(f"Error in pattern classification: {str(e)}")
            return ClassificationResult()

    def discover_patterns(
        self, X: np.ndarray, method: str = "kmeans"
    ) -> ClusteringResult:
        """Discover patterns using unsupervised learning"""
        try:
            # Preprocess features
            X_processed = self._preprocess_features(X, fit=True)

            if method == "kmeans":
                # Determine optimal number of clusters
                optimal_k = self._find_optimal_clusters(X_processed)
                self.models["kmeans"].set_params(n_clusters=optimal_k)

                cluster_labels = self.models["kmeans"].fit_predict(X_processed)
                cluster_centers = self.models["kmeans"].cluster_centers_
                inertia = self.models["kmeans"].inertia_

            elif method == "dbscan":
                cluster_labels = self.models["dbscan"].fit_predict(X_processed)
                cluster_centers = np.array([])  # DBSCAN doesn't have explicit centers
                inertia = 0.0

            else:
                raise ValueError(f"Unknown clustering method: {method}")

            # Calculate clustering quality
            silhouette = self._calculate_silhouette_score(X_processed, cluster_labels)

            result = ClusteringResult(
                cluster_labels=cluster_labels.tolist(),
                cluster_centers=cluster_centers,
                silhouette_score=silhouette,
                inertia=inertia,
                num_clusters=len(
                    np.unique(cluster_labels[cluster_labels != -1])
                ),  # Exclude noise points
            )

            # Adapt based on clustering quality
            adaptation_context = {
                "clustering_method": method,
                "silhouette_score": silhouette,
                "num_clusters": result.num_clusters,
                "data_points": X_processed.shape[0],
            }

            self.life_algorithm.process(
                X_processed.flatten()[:1000], adaptation_context
            )

            logger.info(
                f"Pattern discovery completed: {result.num_clusters} clusters found"
            )
            return result

        except Exception as e:
            logger.error(f"Error in pattern discovery: {str(e)}")
            return ClusteringResult()

    def adaptive_pattern_learning(
        self,
        X: np.ndarray,
        y: Optional[np.ndarray] = None,
        learning_mode: LearningMode = LearningMode.ADAPTIVE,
    ) -> Dict[str, Any]:
        """Adaptive pattern learning using L.I.F.E Theory"""
        try:
            start_time = datetime.now()

            # Extract initial pattern features
            initial_features = self.extract_pattern_features(X)

            results = {
                "learning_mode": learning_mode.value,
                "initial_features": initial_features,
                "adaptation_steps": [],
                "final_performance": {},
                "learning_trajectory": [],
            }

            # Determine learning approach
            if learning_mode == LearningMode.SUPERVISED and y is not None:
                # Supervised adaptive learning
                for step in range(5):  # Multiple adaptation steps
                    # Train classifier
                    training_result = self.train_pattern_classifier(
                        X, y, "neural_network"
                    )

                    # Evaluate and adapt
                    performance = training_result["training_metrics"]["accuracy"]

                    # Adapt features based on performance
                    if performance < 0.8:
                        X = self._enhance_features(
                            X, training_result["feature_importance"]
                        )

                    results["adaptation_steps"].append(
                        {
                            "step": step,
                            "performance": performance,
                            "feature_count": X.shape[1],
                        }
                    )

                    results["learning_trajectory"].append(performance)

                results["final_performance"] = training_result["training_metrics"]

            elif learning_mode == LearningMode.UNSUPERVISED:
                # Unsupervised adaptive learning
                for step in range(3):
                    # Discover patterns
                    clustering_result = self.discover_patterns(X, "kmeans")

                    # Adapt based on clustering quality
                    if clustering_result.silhouette_score < 0.5:
                        X = self._transform_features_for_clustering(X)

                    results["adaptation_steps"].append(
                        {
                            "step": step,
                            "silhouette_score": clustering_result.silhouette_score,
                            "num_clusters": clustering_result.num_clusters,
                        }
                    )

                    results["learning_trajectory"].append(
                        clustering_result.silhouette_score
                    )

                results["final_performance"] = {
                    "silhouette_score": clustering_result.silhouette_score,
                    "num_clusters": clustering_result.num_clusters,
                }

            elif learning_mode == LearningMode.ADAPTIVE:
                # Pure L.I.F.E adaptive learning
                adaptation_scores = []

                for step in range(10):
                    # Process through L.I.F.E algorithm
                    adapted_data = self.life_algorithm.process(
                        X.flatten()[:1000],  # Use subset
                        {"step": step, "learning_mode": "adaptive"},
                    )

                    # Calculate adaptation score
                    adaptation_score = self.life_algorithm.get_performance_metrics()[
                        "overall_performance"
                    ]
                    adaptation_scores.append(adaptation_score)

                    results["adaptation_steps"].append(
                        {
                            "step": step,
                            "adaptation_score": adaptation_score,
                            "experiences": len(
                                self.life_algorithm.experience_memory.experiences
                            ),
                        }
                    )

                results["learning_trajectory"] = adaptation_scores
                results["final_performance"] = {
                    "final_adaptation_score": adaptation_scores[-1],
                    "learning_improvement": adaptation_scores[-1]
                    - adaptation_scores[0],
                }

            # Record learning session
            learning_time = (datetime.now() - start_time).total_seconds()
            results["learning_time"] = learning_time

            # Update adaptation history
            self.adaptation_history.append(
                {
                    "timestamp": start_time.isoformat(),
                    "learning_mode": learning_mode.value,
                    "final_performance": results["final_performance"],
                    "learning_time": learning_time,
                }
            )

            logger.info(f"Adaptive pattern learning completed in {learning_time:.2f}s")
            return results

        except Exception as e:
            logger.error(f"Error in adaptive pattern learning: {str(e)}")
            return {"error": str(e), "learning_mode": learning_mode.value}

    def _preprocess_features(self, X: np.ndarray, fit: bool = False) -> np.ndarray:
        """Preprocess features for model training/prediction"""
        try:
            # Ensure 2D array
            if X.ndim == 1:
                X = X.reshape(1, -1)
            elif X.ndim > 2:
                X = X.reshape(X.shape[0], -1)

            # Scale features
            if fit:
                X_scaled = self.feature_processors["scaler"].fit_transform(X)
            else:
                X_scaled = self.feature_processors["scaler"].transform(X)

            return X_scaled

        except Exception as e:
            logger.error(f"Error preprocessing features: {str(e)}")
            return X.copy() if X.ndim == 2 else X.reshape(1, -1)

    def _find_optimal_clusters(self, X: np.ndarray, max_k: int = 10) -> int:
        """Find optimal number of clusters using elbow method"""
        try:
            max_k = min(max_k, X.shape[0] - 1)
            if max_k < 2:
                return 2

            inertias = []
            K_range = range(2, max_k + 1)

            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X)
                inertias.append(kmeans.inertia_)

            # Find elbow point
            if len(inertias) < 2:
                return 2

            # Calculate second derivative to find elbow
            diffs = np.diff(inertias)
            diff2 = np.diff(diffs)

            if len(diff2) > 0:
                elbow_index = np.argmax(diff2) + 2  # +2 because we start from k=2
                return min(max_k, max(2, elbow_index))
            else:
                return min(5, max_k)  # Default to 5 clusters

        except Exception as e:
            logger.error(f"Error finding optimal clusters: {str(e)}")
            return 3  # Default

    def _calculate_silhouette_score(self, X: np.ndarray, labels: np.ndarray) -> float:
        """Calculate silhouette score for clustering"""
        try:
            from sklearn.metrics import silhouette_score

            # Remove noise points (label -1) for DBSCAN
            valid_mask = labels != -1
            if np.sum(valid_mask) < 2:
                return 0.0

            X_valid = X[valid_mask]
            labels_valid = labels[valid_mask]

            if len(np.unique(labels_valid)) < 2:
                return 0.0

            score = silhouette_score(X_valid, labels_valid)
            return float(score)

        except Exception as e:
            logger.error(f"Error calculating silhouette score: {str(e)}")
            return 0.0

    def _enhance_features(
        self, X: np.ndarray, feature_importance: List[float]
    ) -> np.ndarray:
        """Enhance features based on importance scores"""
        try:
            if not feature_importance or len(feature_importance) != X.shape[1]:
                return X.copy()

            # Create polynomial features for important features
            importance_threshold = np.mean(feature_importance)
            important_features = np.array(feature_importance) > importance_threshold

            enhanced_X = X.copy()

            # Add interaction terms for important features
            for i, is_important_i in enumerate(important_features):
                if is_important_i:
                    for j, is_important_j in enumerate(important_features):
                        if is_important_j and i < j:
                            interaction = (X[:, i] * X[:, j]).reshape(-1, 1)
                            enhanced_X = np.hstack([enhanced_X, interaction])

            return enhanced_X

        except Exception as e:
            logger.error(f"Error enhancing features: {str(e)}")
            return X.copy()

    def _transform_features_for_clustering(self, X: np.ndarray) -> np.ndarray:
        """Transform features to improve clustering"""
        try:
            # Apply ICA transformation
            if X.shape[1] > 1:
                transformed_X = self.feature_processors["ica"].fit_transform(X)
                return transformed_X
            else:
                return X.copy()

        except Exception as e:
            logger.error(f"Error transforming features: {str(e)}")
            return X.copy()

    # Helper methods for feature calculations (reuse from signal processor)
    def _calculate_skewness(self, data: np.ndarray) -> float:
        try:
            mean_val = np.mean(data)
            std_val = np.std(data)
            if std_val == 0:
                return 0.0
            return np.mean(((data - mean_val) / std_val) ** 3)
        except:
            return 0.0

    def _calculate_kurtosis(self, data: np.ndarray) -> float:
        try:
            mean_val = np.mean(data)
            std_val = np.std(data)
            if std_val == 0:
                return 0.0
            return np.mean(((data - mean_val) / std_val) ** 4) - 3
        except:
            return 0.0

    def _calculate_entropy(self, data: np.ndarray) -> float:
        try:
            # Histogram-based entropy
            hist, _ = np.histogram(data, bins=50, density=True)
            hist = hist + 1e-12  # Avoid log(0)
            entropy = -np.sum(hist * np.log2(hist))
            return entropy
        except:
            return 0.0

    def _calculate_lz_complexity(self, data: np.ndarray) -> float:
        """Simplified LZ complexity calculation"""
        try:
            binary_data = (data > np.median(data)).astype(int)
            return len(
                set(tuple(binary_data[i : i + 4]) for i in range(len(binary_data) - 3))
            ) / len(binary_data)
        except:
            return 0.0

    def _calculate_approximate_entropy(
        self, data: np.ndarray, m: int = 2, r: float = 0.2
    ) -> float:
        """Simplified approximate entropy"""
        try:
            N = len(data)
            if N < 50:
                return 0.0
            return np.var(data) / (np.mean(data) ** 2 + 1e-8)
        except:
            return 0.0

    def _calculate_sample_entropy(self, data: np.ndarray) -> float:
        """Simplified sample entropy"""
        try:
            return self._calculate_approximate_entropy(data)
        except:
            return 0.0

    def _calculate_fractal_dimension(self, data: np.ndarray) -> float:
        """Simplified fractal dimension"""
        try:
            diff_data = np.diff(data)
            return 1.0 + np.log(np.mean(np.abs(diff_data))) / np.log(len(data))
        except:
            return 1.0

    def _calculate_spectral_entropy(self, data: np.ndarray) -> float:
        """Simplified spectral entropy"""
        try:
            fft_data = np.abs(np.fft.fft(data))
            psd = fft_data**2
            psd_norm = psd / np.sum(psd)
            psd_norm = psd_norm[psd_norm > 0]
            return -np.sum(psd_norm * np.log2(psd_norm))
        except:
            return 0.0

    def _estimate_snr(self, data: np.ndarray) -> float:
        """Estimate signal-to-noise ratio"""
        try:
            signal_power = np.mean(data**2)
            noise_power = np.var(np.diff(data)) / 2
            if noise_power == 0:
                return 100.0
            return 10 * np.log10(signal_power / noise_power)
        except:
            return 0.0

    def _assess_data_quality(self, data: np.ndarray) -> float:
        """Assess overall data quality"""
        try:
            # Check for NaN/inf values
            if np.any(~np.isfinite(data)):
                return 0.0

            # Check for constant values
            if np.std(data) == 0:
                return 0.2

            # Check for reasonable range
            data_range = np.ptp(data)
            if data_range == 0:
                return 0.3

            # Combined quality score
            return 0.8 + 0.2 * min(1.0, np.std(data) / np.mean(np.abs(data) + 1e-8))
        except:
            return 0.5

    def _calculate_feature_stability(self, data: np.ndarray) -> float:
        """Calculate feature stability across samples"""
        try:
            if data.shape[0] < 2:
                return 1.0

            # Calculate coefficient of variation for each feature
            feature_cvs = []
            for i in range(data.shape[1]):
                feature_col = data[:, i]
                if np.std(feature_col) == 0:
                    cv = 0.0
                else:
                    cv = np.std(feature_col) / (np.mean(np.abs(feature_col)) + 1e-8)
                feature_cvs.append(cv)

            # Stability is inverse of variability
            avg_cv = np.mean(feature_cvs)
            stability = 1.0 / (1.0 + avg_cv)
            return stability
        except:
            return 0.5

    def _calculate_information_content(self, data: np.ndarray) -> float:
        """Calculate information content of data"""
        try:
            # Use entropy as information measure
            flattened = data.flatten()
            return self._calculate_entropy(flattened) / np.log2(len(flattened))
        except:
            return 0.5

    def get_recognizer_status(self) -> Dict[str, Any]:
        """Get comprehensive recognizer status"""
        return {
            "pattern_type": self.pattern_type.value,
            "trained_models": list(self.trained_models),
            "pattern_memory_size": len(self.pattern_memory),
            "adaptation_history_size": len(self.adaptation_history),
            "recent_accuracy": (
                np.mean(self.performance_metrics["accuracy_history"][-5:])
                if self.performance_metrics["accuracy_history"]
                else 0.0
            ),
            "recent_f1": (
                np.mean(self.performance_metrics["f1_history"][-5:])
                if self.performance_metrics["f1_history"]
                else 0.0
            ),
            "life_algorithm_status": self.life_algorithm.get_performance_metrics(),
            "feature_dimensions": self.feature_dimensions,
        }


def create_life_pattern_recognizer(
    pattern_type: PatternType = PatternType.TEMPORAL,
) -> LIFEPatternRecognizer:
    """Factory function to create L.I.F.E pattern recognizer"""
    return LIFEPatternRecognizer(pattern_type)


# Example usage and testing
def test_life_pattern_recognizer():
    """Test L.I.F.E pattern recognizer functionality"""
    print("Testing L.I.F.E Theory Pattern Recognizer...")

    # Create recognizer
    recognizer = create_life_pattern_recognizer(PatternType.NEURAL)

    # Generate test data
    np.random.seed(42)

    # Classification data
    X_class = np.random.randn(200, 10)
    y_class = np.random.randint(0, 3, 200)

    # Clustering data
    X_cluster = np.random.randn(100, 5)

    print(
        f"Generated test data: {X_class.shape} for classification, {X_cluster.shape} for clustering"
    )

    # Test feature extraction
    features = recognizer.extract_pattern_features(X_class[:10])
    print(
        f"Extracted features - Raw: {features.raw_features.shape}, Reduced: {features.reduced_features.shape}"
    )
    print(f"Statistical features: {len(features.statistical_features)}")
    print(f"Quality metrics: {features.quality_metrics}")

    # Test supervised learning
    print("\nTesting supervised pattern learning...")
    training_result = recognizer.train_pattern_classifier(
        X_class, y_class, "neural_network"
    )
    print(f"Training accuracy: {training_result['training_metrics']['accuracy']:.3f}")
    print(f"Training F1 score: {training_result['training_metrics']['f1_score']:.3f}")

    # Test classification
    test_sample = X_class[:1]
    classification = recognizer.classify_pattern(test_sample, "neural_network")
    print(
        f"Classification result: Class {classification.predicted_class}, Confidence {classification.confidence:.3f}"
    )

    # Test unsupervised learning
    print("\nTesting unsupervised pattern discovery...")
    clustering_result = recognizer.discover_patterns(X_cluster, "kmeans")
    print(f"Discovered {clustering_result.num_clusters} clusters")
    print(f"Silhouette score: {clustering_result.silhouette_score:.3f}")

    # Test adaptive learning
    print("\nTesting adaptive pattern learning...")
    adaptive_result = recognizer.adaptive_pattern_learning(
        X_class, y_class, LearningMode.ADAPTIVE
    )
    print(f"Adaptive learning steps: {len(adaptive_result['adaptation_steps'])}")
    print(f"Learning trajectory: {adaptive_result['learning_trajectory']}")

    # Get status
    status = recognizer.get_recognizer_status()
    print(f"\nRecognizer Status:")
    print(f"  Pattern type: {status['pattern_type']}")
    print(f"  Trained models: {status['trained_models']}")
    print(f"  Recent accuracy: {status['recent_accuracy']:.3f}")

    return recognizer, adaptive_result


if __name__ == "__main__":
    # Run tests
    recognizer, results = test_life_pattern_recognizer()
    print("\nL.I.F.E Pattern Recognizer testing completed successfully!")
