#!/usr/bin/env python3
"""
Accuracy Ensemble Classifier - Advanced ML Model Ensemble for EEG Pattern Recognition
High-accuracy ensemble classification system for neuroadaptive learning

This module implements an advanced ensemble classification system that combines
multiple machine learning models to achieve optimal accuracy in EEG pattern
recognition while maintaining ultra-low latency performance.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnsembleStrategy(Enum):
    """Ensemble combination strategies"""

    MAJORITY_VOTING = "majority_voting"
    WEIGHTED_VOTING = "weighted_voting"
    STACKED_GENERALIZATION = "stacked_generalization"
    ADAPTIVE_WEIGHTING = "adaptive_weighting"
    CONFIDENCE_WEIGHTED = "confidence_weighted"


class ClassifierType(Enum):
    """Available classifier types"""

    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    LOGISTIC_REGRESSION = "logistic_regression"
    SVM = "svm"
    KNN = "knn"
    NAIVE_BAYES = "naive_bayes"
    DECISION_TREE = "decision_tree"


@dataclass
class ClassifierConfig:
    """Configuration for individual classifiers"""

    classifier_type: ClassifierType
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    enabled: bool = True


@dataclass
class EnsembleConfig:
    """Configuration for the ensemble classifier"""

    strategy: EnsembleStrategy = EnsembleStrategy.WEIGHTED_VOTING
    classifiers: List[ClassifierConfig] = field(default_factory=list)
    confidence_threshold: float = 0.8
    adaptation_rate: float = 0.01
    max_models: int = 10
    cross_validation_folds: int = 5
    feature_selection: bool = True
    parallel_processing: bool = True
    max_workers: int = 4


@dataclass
class ClassificationResult:
    """Result of ensemble classification"""

    predicted_class: int
    confidence: float
    probabilities: np.ndarray
    individual_predictions: Dict[str, int]
    individual_confidences: Dict[str, float]
    ensemble_metrics: Dict[str, float]
    processing_time: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class PerformanceMetrics:
    """Performance metrics for ensemble evaluation"""

    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    auc_roc: float = 0.0
    confusion_matrix: np.ndarray = field(default_factory=lambda: np.zeros((2, 2)))
    training_time: float = 0.0
    inference_time: float = 0.0
    model_sizes: Dict[str, int] = field(default_factory=dict)


class BaseClassifierWrapper:
    """
    Wrapper for individual classifiers with standardized interface

    Provides unified training, prediction, and evaluation methods
    """

    def __init__(self, config: ClassifierConfig):
        self.config = config
        self.model = None
        self.is_trained = False
        self.training_time = 0.0
        self.feature_importance = None

        # Initialize the actual classifier
        self._initialize_classifier()

    def _initialize_classifier(self):
        """Initialize the specific classifier based on type"""
        if self.config.classifier_type == ClassifierType.RANDOM_FOREST:
            self.model = RandomForestClassifier(
                n_estimators=self.config.hyperparameters.get("n_estimators", 100),
                max_depth=self.config.hyperparameters.get("max_depth", None),
                random_state=42,
            )
        elif self.config.classifier_type == ClassifierType.GRADIENT_BOOSTING:
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.hyperparameters.get("n_estimators", 100),
                learning_rate=self.config.hyperparameters.get("learning_rate", 0.1),
                max_depth=self.config.hyperparameters.get("max_depth", 3),
                random_state=42,
            )
        elif self.config.classifier_type == ClassifierType.LOGISTIC_REGRESSION:
            self.model = LogisticRegression(
                C=self.config.hyperparameters.get("C", 1.0),
                max_iter=self.config.hyperparameters.get("max_iter", 1000),
                random_state=42,
            )
        elif self.config.classifier_type == ClassifierType.SVM:
            self.model = SVC(
                C=self.config.hyperparameters.get("C", 1.0),
                kernel=self.config.hyperparameters.get("kernel", "rbf"),
                probability=True,
                random_state=42,
            )
        elif self.config.classifier_type == ClassifierType.KNN:
            self.model = KNeighborsClassifier(
                n_neighbors=self.config.hyperparameters.get("n_neighbors", 5)
            )
        elif self.config.classifier_type == ClassifierType.NAIVE_BAYES:
            self.model = GaussianNB()
        elif self.config.classifier_type == ClassifierType.DECISION_TREE:
            self.model = DecisionTreeClassifier(
                max_depth=self.config.hyperparameters.get("max_depth", None),
                random_state=42,
            )

    async def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """
        Train the classifier asynchronously

        Args:
            X: Feature matrix
            y: Target labels

        Returns:
            Success status
        """
        try:
            start_time = time.perf_counter()

            # Run training in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=1) as executor:
                await loop.run_in_executor(executor, self.model.fit, X, y)

            self.training_time = time.perf_counter() - start_time
            self.is_trained = True

            # Extract feature importance if available
            if hasattr(self.model, "feature_importances_"):
                self.feature_importance = self.model.feature_importances_

            logger.info(
                f"Trained {self.config.classifier_type.value} in {self.training_time:.4f}s"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to train {self.config.classifier_type.value}: {e}")
            return False

    async def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with confidence scores

        Args:
            X: Feature matrix

        Returns:
            Tuple of (predictions, probabilities)
        """
        if not self.is_trained:
            raise RuntimeError(
                f"Classifier {self.config.classifier_type.value} is not trained"
            )

        try:
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=1) as executor:
                predictions = await loop.run_in_executor(
                    executor, self.model.predict, X
                )
                probabilities = await loop.run_in_executor(
                    executor, self._get_probabilities, X
                )

            return predictions, probabilities

        except Exception as e:
            logger.error(
                f"Failed to predict with {self.config.classifier_type.value}: {e}"
            )
            return np.zeros(len(X), dtype=int), np.zeros((len(X), 2))

    def _get_probabilities(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        else:
            # For classifiers without predict_proba, use decision function
            decision = self.model.decision_function(X)
            # Convert to probabilities using sigmoid
            probs = 1 / (1 + np.exp(-decision))
            return np.column_stack([1 - probs, probs])

    def get_model_size(self) -> int:
        """Get approximate model size in bytes"""
        # Rough estimation based on model parameters
        if hasattr(self.model, "n_features_in_"):
            return self.model.n_features_in_ * 8  # Assume 8 bytes per feature
        return 1024  # Default size


class AccuracyEnsembleClassifier:
    """
    High-accuracy ensemble classifier for EEG pattern recognition

    Combines multiple machine learning models using advanced ensemble strategies
    to achieve optimal classification accuracy while maintaining performance.
    """

    def __init__(self, config: EnsembleConfig):
        self.config = config
        self.classifiers = {}
        self.meta_classifier = None
        self.is_trained = False
        self.performance_history = []
        self.feature_selector = None

        # Initialize classifiers
        self._initialize_classifiers()

        logger.info(
            f"Accuracy Ensemble Classifier initialized with {len(self.classifiers)} models"
        )

    def _initialize_classifiers(self):
        """Initialize all configured classifiers"""
        for classifier_config in self.config.classifiers:
            if classifier_config.enabled:
                wrapper = BaseClassifierWrapper(classifier_config)
                self.classifiers[classifier_config.classifier_type.value] = wrapper

    async def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ) -> bool:
        """
        Train the ensemble classifier

        Args:
            X: Training feature matrix
            y: Training target labels
            validation_data: Optional validation data for early stopping

        Returns:
            Training success status
        """
        try:
            start_time = time.perf_counter()

            # Feature selection if enabled
            if self.config.feature_selection:
                X = self._perform_feature_selection(X, y)

            # Train individual classifiers
            training_tasks = []
            for name, classifier in self.classifiers.items():
                task = classifier.train(X, y)
                training_tasks.append(task)

            # Train in parallel if enabled
            if self.config.parallel_processing:
                await asyncio.gather(*training_tasks)
            else:
                for task in training_tasks:
                    await task

            # Train meta-classifier for stacked generalization
            if self.config.strategy == EnsembleStrategy.STACKED_GENERALIZATION:
                await self._train_meta_classifier(X, y)

            self.training_time = time.perf_counter() - start_time
            self.is_trained = True

            # Evaluate performance
            if validation_data:
                await self.evaluate(validation_data[0], validation_data[1])

            logger.info(f"Ensemble training completed in {self.training_time:.4f}s")
            return True

        except Exception as e:
            logger.error(f"Ensemble training failed: {e}")
            return False

    async def predict(self, X: np.ndarray) -> ClassificationResult:
        """
        Make ensemble prediction

        Args:
            X: Feature matrix for prediction

        Returns:
            ClassificationResult with prediction details
        """
        if not self.is_trained:
            raise RuntimeError("Ensemble classifier is not trained")

        start_time = time.perf_counter()

        # Feature selection if enabled
        if self.config.feature_selection and self.feature_selector is not None:
            X = self.feature_selector.transform(X)

        # Get predictions from all classifiers
        predictions = {}
        probabilities = {}
        confidences = {}

        prediction_tasks = []
        for name, classifier in self.classifiers.items():
            task = self._get_classifier_prediction(classifier, X, name)
            prediction_tasks.append(task)

        # Gather predictions
        results = await asyncio.gather(*prediction_tasks)

        for name, (pred, prob) in zip(self.classifiers.keys(), results):
            predictions[name] = pred[0] if len(pred) > 0 else 0
            probabilities[name] = prob[0] if len(prob) > 0 else np.array([0.5, 0.5])
            confidences[name] = float(np.max(prob))

        # Combine predictions based on strategy
        final_prediction, final_confidence, final_probabilities = (
            await self._combine_predictions(predictions, probabilities, confidences)
        )

        processing_time = time.perf_counter() - start_time

        # Calculate ensemble metrics
        ensemble_metrics = self._calculate_ensemble_metrics(predictions, confidences)

        return ClassificationResult(
            predicted_class=int(final_prediction),
            confidence=float(final_confidence),
            probabilities=final_probabilities,
            individual_predictions=predictions,
            individual_confidences=confidences,
            ensemble_metrics=ensemble_metrics,
            processing_time=processing_time,
        )

    async def _get_classifier_prediction(
        self, classifier: BaseClassifierWrapper, X: np.ndarray, name: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Get prediction from a single classifier"""
        try:
            return await classifier.predict(X)
        except Exception as e:
            logger.warning(f"Prediction failed for {name}: {e}")
            # Return default prediction
            return np.array([0]), np.array([[0.5, 0.5]])

    async def _combine_predictions(
        self,
        predictions: Dict[str, int],
        probabilities: Dict[str, np.ndarray],
        confidences: Dict[str, float],
    ) -> Tuple[int, float, np.ndarray]:
        """Combine predictions using the configured ensemble strategy"""
        if self.config.strategy == EnsembleStrategy.MAJORITY_VOTING:
            return self._majority_voting(predictions)
        elif self.config.strategy == EnsembleStrategy.WEIGHTED_VOTING:
            return self._weighted_voting(predictions, confidences)
        elif self.config.strategy == EnsembleStrategy.CONFIDENCE_WEIGHTED:
            return self._confidence_weighted_voting(predictions, confidences)
        elif self.config.strategy == EnsembleStrategy.ADAPTIVE_WEIGHTING:
            return self._adaptive_weighted_voting(predictions, confidences)
        elif self.config.strategy == EnsembleStrategy.STACKED_GENERALIZATION:
            return await self._stacked_prediction(predictions, probabilities)
        else:
            return self._majority_voting(predictions)

    def _majority_voting(
        self, predictions: Dict[str, int]
    ) -> Tuple[int, float, np.ndarray]:
        """Simple majority voting"""
        pred_values = list(predictions.values())
        unique, counts = np.unique(pred_values, return_counts=True)
        majority_class = unique[np.argmax(counts)]
        confidence = counts[np.argmax(counts)] / len(pred_values)

        # Create probability distribution
        probabilities = np.zeros(2)
        probabilities[majority_class] = confidence
        probabilities[1 - majority_class] = 1 - confidence

        return majority_class, confidence, probabilities

    def _weighted_voting(
        self, predictions: Dict[str, int], confidences: Dict[str, float]
    ) -> Tuple[int, float, np.ndarray]:
        """Weighted voting based on classifier weights"""
        class_0_weight = 0.0
        class_1_weight = 0.0

        for name, pred in predictions.items():
            weight = self.classifiers[name].config.weight
            confidence = confidences[name]

            if pred == 0:
                class_0_weight += weight * confidence
            else:
                class_1_weight += weight * confidence

        total_weight = class_0_weight + class_1_weight
        if total_weight == 0:
            return 0, 0.5, np.array([0.5, 0.5])

        class_0_prob = class_0_weight / total_weight
        class_1_prob = class_1_weight / total_weight

        predicted_class = 0 if class_0_prob > class_1_prob else 1
        confidence = max(class_0_prob, class_1_prob)

        return predicted_class, confidence, np.array([class_0_prob, class_1_prob])

    def _confidence_weighted_voting(
        self, predictions: Dict[str, int], confidences: Dict[str, float]
    ) -> Tuple[int, float, np.ndarray]:
        """Voting weighted by individual classifier confidence"""
        class_0_weight = 0.0
        class_1_weight = 0.0

        for name, pred in predictions.items():
            confidence = confidences[name]

            if pred == 0:
                class_0_weight += confidence
            else:
                class_1_weight += confidence

        total_weight = class_0_weight + class_1_weight
        if total_weight == 0:
            return 0, 0.5, np.array([0.5, 0.5])

        class_0_prob = class_0_weight / total_weight
        class_1_prob = class_1_weight / total_weight

        predicted_class = 0 if class_0_prob > class_1_prob else 1
        confidence = max(class_0_prob, class_1_prob)

        return predicted_class, confidence, np.array([class_0_prob, class_1_prob])

    def _adaptive_weighted_voting(
        self, predictions: Dict[str, int], confidences: Dict[str, float]
    ) -> Tuple[int, float, np.ndarray]:
        """Adaptive weighting based on recent performance"""
        # Use recent performance to adjust weights
        performance_weights = {}
        for name in predictions.keys():
            recent_perf = self._get_recent_performance(name)
            performance_weights[name] = max(0.1, recent_perf)  # Minimum weight

        class_0_weight = 0.0
        class_1_weight = 0.0

        for name, pred in predictions.items():
            weight = performance_weights[name] * confidences[name]

            if pred == 0:
                class_0_weight += weight
            else:
                class_1_weight += weight

        total_weight = class_0_weight + class_1_weight
        if total_weight == 0:
            return 0, 0.5, np.array([0.5, 0.5])

        class_0_prob = class_0_weight / total_weight
        class_1_prob = class_1_weight / total_weight

        predicted_class = 0 if class_0_prob > class_1_prob else 1
        confidence = max(class_0_prob, class_1_prob)

        return predicted_class, confidence, np.array([class_0_prob, class_1_prob])

    async def _stacked_prediction(
        self, predictions: Dict[str, int], probabilities: Dict[str, np.ndarray]
    ) -> Tuple[int, float, np.ndarray]:
        """Stacked generalization prediction"""
        if self.meta_classifier is None or not self.meta_classifier.is_trained:
            # Fallback to majority voting
            return self._majority_voting(predictions)

        # Create feature matrix from base classifier predictions
        n_samples = 1  # Single prediction
        n_classes = len(probabilities)
        feature_matrix = np.zeros(
            (n_samples, len(predictions) * 2)
        )  # predictions + probabilities

        for i, (name, pred) in enumerate(predictions.items()):
            feature_matrix[0, i] = pred
            feature_matrix[0, i + len(predictions)] = np.max(probabilities[name])

        # Get meta-classifier prediction
        meta_pred, meta_prob = await self.meta_classifier.predict(feature_matrix)

        predicted_class = int(meta_pred[0])
        confidence = float(np.max(meta_prob))
        final_probabilities = meta_prob[0]

        return predicted_class, confidence, final_probabilities

    async def _train_meta_classifier(self, X: np.ndarray, y: np.ndarray):
        """Train the meta-classifier for stacked generalization"""
        # Generate predictions from base classifiers
        base_predictions = []
        for name, classifier in self.classifiers.items():
            if classifier.is_trained:
                pred, prob = await classifier.predict(X)
                base_predictions.extend([pred, np.max(prob, axis=1)])

        if not base_predictions:
            return

        # Create meta-features
        meta_features = np.column_stack(base_predictions)

        # Train meta-classifier
        meta_config = ClassifierConfig(
            classifier_type=ClassifierType.LOGISTIC_REGRESSION,
            hyperparameters={"C": 1.0, "max_iter": 1000},
        )
        self.meta_classifier = BaseClassifierWrapper(meta_config)
        await self.meta_classifier.train(meta_features, y)

    def _perform_feature_selection(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Perform feature selection to reduce dimensionality"""
        from sklearn.feature_selection import SelectKBest, f_classif

        # Select top features
        n_features = min(X.shape[1], max(10, X.shape[1] // 2))
        selector = SelectKBest(f_classif, k=n_features)
        X_selected = selector.fit_transform(X, y)

        self.feature_selector = selector
        return X_selected

    def _calculate_ensemble_metrics(
        self, predictions: Dict[str, int], confidences: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate ensemble-level metrics"""
        n_classifiers = len(predictions)

        # Agreement score (fraction of classifiers agreeing with majority)
        pred_values = list(predictions.values())
        unique, counts = np.unique(pred_values, return_counts=True)
        majority_count = np.max(counts)
        agreement = majority_count / n_classifiers

        # Average confidence
        avg_confidence = np.mean(list(confidences.values()))

        # Diversity score (1 - agreement, higher diversity is better for ensemble)
        diversity = 1.0 - agreement

        # Confidence variance (lower is better)
        confidence_variance = np.var(list(confidences.values()))

        return {
            "agreement_score": agreement,
            "average_confidence": avg_confidence,
            "diversity_score": diversity,
            "confidence_variance": confidence_variance,
            "n_classifiers": n_classifiers,
        }

    def _get_recent_performance(self, classifier_name: str) -> float:
        """Get recent performance score for a classifier"""
        # Simple implementation - return 1.0 for now
        # In practice, this would track historical performance
        return 1.0

    async def evaluate(self, X: np.ndarray, y: np.ndarray) -> PerformanceMetrics:
        """
        Evaluate ensemble performance on test data

        Args:
            X: Test feature matrix
            y: True labels

        Returns:
            PerformanceMetrics object
        """
        try:
            predictions = []
            inference_times = []

            # Make predictions
            for i in range(len(X)):
                start_time = time.perf_counter()
                result = await self.predict(X[i : i + 1])
                inference_times.append(time.perf_counter() - start_time)
                predictions.append(result.predicted_class)

            predictions = np.array(predictions)

            # Calculate metrics
            from sklearn.metrics import (
                accuracy_score,
                confusion_matrix,
                f1_score,
                precision_score,
                recall_score,
                roc_auc_score,
            )

            accuracy = accuracy_score(y, predictions)
            precision = precision_score(
                y, predictions, average="weighted", zero_division=0
            )
            recall = recall_score(y, predictions, average="weighted", zero_division=0)
            f1 = f1_score(y, predictions, average="weighted", zero_division=0)

            # AUC-ROC (only for binary classification)
            try:
                auc = roc_auc_score(y, predictions)
            except:
                auc = 0.5

            conf_matrix = confusion_matrix(y, predictions)

            # Model sizes
            model_sizes = {
                name: clf.get_model_size() for name, clf in self.classifiers.items()
            }

            metrics = PerformanceMetrics(
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                auc_roc=auc,
                confusion_matrix=conf_matrix,
                training_time=self.training_time,
                inference_time=np.mean(inference_times),
                model_sizes=model_sizes,
            )

            self.performance_history.append(metrics)

            logger.info(f"Ensemble evaluation - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
            return metrics

        except Exception as e:
            logger.error(f"Ensemble evaluation failed: {e}")
            return PerformanceMetrics()

    def get_ensemble_status(self) -> Dict[str, Any]:
        """Get comprehensive ensemble status"""
        classifier_status = {}
        for name, classifier in self.classifiers.items():
            classifier_status[name] = {
                "trained": classifier.is_trained,
                "training_time": classifier.training_time,
                "model_size": classifier.get_model_size(),
                "weight": classifier.config.weight,
                "type": classifier.config.classifier_type.value,
            }

        return {
            "is_trained": self.is_trained,
            "strategy": self.config.strategy.value,
            "n_classifiers": len(self.classifiers),
            "feature_selection": self.config.feature_selection,
            "parallel_processing": self.config.parallel_processing,
            "classifier_status": classifier_status,
            "performance_history_length": len(self.performance_history),
            "latest_performance": (
                self.performance_history[-1] if self.performance_history else None
            ),
        }


# Factory function for easy instantiation
def create_accuracy_ensemble_classifier(
    strategy: EnsembleStrategy = EnsembleStrategy.WEIGHTED_VOTING, max_models: int = 7
) -> AccuracyEnsembleClassifier:
    """
    Factory function to create an accuracy ensemble classifier

    Args:
        strategy: Ensemble combination strategy
        max_models: Maximum number of models in ensemble

    Returns:
        Configured AccuracyEnsembleClassifier instance
    """
    # Default classifier configurations
    default_classifiers = [
        ClassifierConfig(
            ClassifierType.RANDOM_FOREST,
            {"n_estimators": 100, "max_depth": 10},
            weight=1.2,
        ),
        ClassifierConfig(
            ClassifierType.GRADIENT_BOOSTING,
            {"n_estimators": 100, "learning_rate": 0.1},
            weight=1.1,
        ),
        ClassifierConfig(
            ClassifierType.LOGISTIC_REGRESSION, {"C": 1.0, "max_iter": 1000}, weight=0.9
        ),
        ClassifierConfig(ClassifierType.SVM, {"C": 1.0, "kernel": "rbf"}, weight=1.0),
        ClassifierConfig(ClassifierType.KNN, {"n_neighbors": 5}, weight=0.8),
        ClassifierConfig(ClassifierType.NAIVE_BAYES, weight=0.7),
        ClassifierConfig(ClassifierType.DECISION_TREE, {"max_depth": 5}, weight=0.8),
    ]

    # Limit to max_models
    selected_classifiers = default_classifiers[:max_models]

    config = EnsembleConfig(
        strategy=strategy,
        classifiers=selected_classifiers,
        confidence_threshold=0.8,
        adaptation_rate=0.01,
        max_models=max_models,
        cross_validation_folds=5,
        feature_selection=True,
        parallel_processing=True,
        max_workers=4,
    )

    return AccuracyEnsembleClassifier(config)


# Example usage and demonstration
async def demonstrate_ensemble_classifier():
    """Demonstrate the accuracy ensemble classifier"""
    print("🎯 Accuracy Ensemble Classifier Demonstration")
    print("=" * 60)

    # Create ensemble classifier
    ensemble = create_accuracy_ensemble_classifier(
        strategy=EnsembleStrategy.WEIGHTED_VOTING, max_models=5
    )

    print("📋 Ensemble Configuration:")
    print(f"Strategy: {ensemble.config.strategy.value}")
    print(f"Number of classifiers: {len(ensemble.classifiers)}")
    print(f"Feature selection: {ensemble.config.feature_selection}")
    print(f"Parallel processing: {ensemble.config.parallel_processing}")

    # Generate synthetic EEG-like data
    print("🧠 Generating synthetic EEG classification data...")
    np.random.seed(42)
    n_samples = 1000
    n_features = 64  # Typical EEG features

    # Create two classes: normal vs. abnormal EEG patterns
    X = np.random.randn(n_samples, n_features)

    # Add class-specific patterns
    y = np.random.randint(0, 2, n_samples)

    # Add some class separation
    for i in range(n_samples):
        if y[i] == 1:  # Abnormal patterns
            X[i, :10] += np.random.randn(10) * 2  # Stronger alpha waves
            X[i, 10:20] += np.random.randn(10) * 1.5  # Beta wave anomalies

    # Split data
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

    # Train ensemble
    print("🚀 Training ensemble classifier...")
    train_start = time.perf_counter()
    success = await ensemble.train(X_train, y_train, validation_data=(X_test, y_test))
    train_time = time.perf_counter() - train_start

    if not success:
        print("❌ Training failed")
        return

    print(f"Training completed in {train_time:.2f}s")

    # Evaluate performance
    print("📊 Evaluating ensemble performance...")
    eval_start = time.perf_counter()
    metrics = await ensemble.evaluate(X_test, y_test)
    eval_time = time.perf_counter() - eval_start

    print("\n🔬 PERFORMANCE METRICS")
    print(f"Accuracy: {metrics.accuracy:.4f}")
    print(f"Precision: {metrics.precision:.4f}")
    print(f"Recall: {metrics.recall:.4f}")
    print(f"F1 Score: {metrics.f1_score:.4f}")
    print(f"AUC-ROC: {metrics.auc_roc:.4f}")
    print(f"Evaluation time: {eval_time:.2f}s")
    print(f"Average inference time: {metrics.inference_time:.4f}s")

    # Test individual predictions
    print("\n🧪 TESTING INDIVIDUAL PREDICTIONS")
    test_samples = X_test[:5]
    true_labels = y_test[:5]

    for i, (sample, true_label) in enumerate(zip(test_samples, true_labels)):
        result = await ensemble.predict(sample.reshape(1, -1))

        print(f"\nSample {i+1}:")
        print(f"  True label: {true_label}")
        print(f"  Predicted: {result.predicted_class}")
        print(f"  Confidence: {result.confidence:.4f}")
        print(f"  Processing time: {result.processing_time:.6f}s")
        print(f"  Ensemble agreement: {result.ensemble_metrics['agreement_score']:.3f}")

        # Show individual classifier predictions
        print("  Individual predictions:")
        for name, pred in result.individual_predictions.items():
            conf = result.individual_confidences[name]
            print(f"    {name}: {pred} (conf: {conf:.3f})")

    # Display ensemble status
    print("\n📈 ENSEMBLE STATUS")
    status = ensemble.get_ensemble_status()
    print(f"Trained: {status['is_trained']}")
    print(f"Strategy: {status['strategy']}")
    print(f"Classifiers: {status['n_classifiers']}")
    print(f"Feature selection: {status['feature_selection']}")
    print(f"Parallel processing: {status['parallel_processing']}")

    print("\n🏗️ CLASSIFIER DETAILS")
    for name, clf_status in status["classifier_status"].items():
        print(f"{name}:")
        print(f"  Trained: {clf_status['trained']}")
        print(f"  Training time: {clf_status['training_time']:.4f}s")
        print(f"  Model size: {clf_status['model_size']} bytes")
        print(f"  Weight: {clf_status['weight']}")

    print("\n🎉 Ensemble classifier demonstration completed successfully!")


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_ensemble_classifier())
    print("\n🎉 Ensemble classifier demonstration completed successfully!")


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_ensemble_classifier())
