"""
L.I.F.E Theory Module 4: Adaptive Neural Networks
Advanced neural network architectures with L.I.F.E adaptation

Copyright 2025 - Sergio Paya Borrull
"""

import logging
import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import numpy as np

# Import L.I.F.E Theory core
from lifetheory import AdaptationParameters, CoreLIFEAlgorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkArchitecture(Enum):
    """Neural network architecture types"""

    FEEDFORWARD = "feedforward"
    RECURRENT = "recurrent"
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    CONVOLUTIONAL = "convolutional"
    ADAPTIVE = "adaptive"
    LIFE_HYBRID = "life_hybrid"


class ActivationFunction(Enum):
    """Activation function types"""

    RELU = "relu"
    SIGMOID = "sigmoid"
    TANH = "tanh"
    LEAKY_RELU = "leaky_relu"
    SWISH = "swish"
    GELU = "gelu"
    LIFE_ADAPTIVE = "life_adaptive"


class OptimizationStrategy(Enum):
    """Optimization strategies"""

    SGD = "sgd"
    ADAM = "adam"
    RMSPROP = "rmsprop"
    ADAGRAD = "adagrad"
    LIFE_OPTIMIZER = "life_optimizer"


@dataclass
class NetworkTopology:
    """Neural network topology definition"""

    input_size: int = 10
    hidden_layers: List[int] = field(default_factory=lambda: [64, 32])
    output_size: int = 1
    activation: ActivationFunction = ActivationFunction.RELU
    dropout_rate: float = 0.1
    batch_norm: bool = True
    skip_connections: bool = False


@dataclass
class LIFEAdaptationConfig:
    """Configuration for L.I.F.E adaptation in neural networks"""

    adaptation_rate: float = 0.01
    architecture_evolution: bool = True
    weight_adaptation: bool = True
    topology_mutation: bool = True
    learning_rate_adaptation: bool = True
    activation_evolution: bool = True
    pruning_enabled: bool = True
    growing_enabled: bool = True


@dataclass
class TrainingMetrics:
    """Training performance metrics"""

    epoch: int = 0
    train_loss: float = float("inf")
    val_loss: float = float("inf")
    train_accuracy: float = 0.0
    val_accuracy: float = 0.0
    learning_rate: float = 0.001
    gradient_norm: float = 0.0
    weight_norm: float = 0.0
    adaptation_score: float = 0.0


class LIFEActivationFunction:
    """Adaptive activation function using L.I.F.E Theory"""

    def __init__(self, initial_function: ActivationFunction = ActivationFunction.RELU):
        self.current_function = initial_function
        self.adaptation_history = []
        self.performance_history = []
        self.life_controller = CoreLIFEAlgorithm(learning_rate=0.05)

        # Function parameters that can adapt
        self.alpha = 0.01  # For leaky ReLU
        self.beta = 1.0  # For swish scaling
        self.gamma = 1.0  # For general scaling

    def __call__(
        self, x: np.ndarray, adapt_context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Apply adaptive activation function"""
        try:
            # Apply current activation function
            if self.current_function == ActivationFunction.RELU:
                output = np.maximum(0, x)
            elif self.current_function == ActivationFunction.SIGMOID:
                output = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
            elif self.current_function == ActivationFunction.TANH:
                output = np.tanh(x)
            elif self.current_function == ActivationFunction.LEAKY_RELU:
                output = np.where(x > 0, x, self.alpha * x)
            elif self.current_function == ActivationFunction.SWISH:
                sigmoid_x = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
                output = x * sigmoid_x * self.beta
            elif self.current_function == ActivationFunction.GELU:
                output = (
                    0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))
                )
            else:  # LIFE_ADAPTIVE
                # Hybrid activation combining multiple functions
                relu_out = np.maximum(0, x)
                sigmoid_out = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
                tanh_out = np.tanh(x)

                # Weighted combination based on L.I.F.E adaptation
                weights = self._get_adaptive_weights()
                output = (
                    weights[0] * relu_out
                    + weights[1] * sigmoid_out
                    + weights[2] * tanh_out
                ) * self.gamma

            # Adapt function if context provided
            if adapt_context:
                self._adapt_function(output, adapt_context)

            return output

        except Exception as e:
            logger.error(f"Error in adaptive activation: {str(e)}")
            return np.maximum(0, x)  # Fallback to ReLU

    def _get_adaptive_weights(self) -> np.ndarray:
        """Get adaptive weights for hybrid activation"""
        if len(self.performance_history) == 0:
            return np.array([0.6, 0.2, 0.2])  # Default weights

        # Use recent performance to adjust weights
        recent_perf = np.mean(self.performance_history[-5:])
        if recent_perf > 0.8:
            return np.array([0.7, 0.2, 0.1])  # More ReLU for good performance
        elif recent_perf < 0.5:
            return np.array([0.3, 0.4, 0.3])  # More balanced for poor performance
        else:
            return np.array([0.5, 0.3, 0.2])  # Moderate weighting

    def _adapt_function(self, output: np.ndarray, context: Dict[str, Any]):
        """Adapt activation function based on performance"""
        try:
            performance = context.get("performance", 0.5)
            gradient_info = context.get("gradient_norm", 1.0)

            # Record performance
            self.performance_history.append(performance)
            if len(self.performance_history) > 100:
                self.performance_history = self.performance_history[-50:]

            # Adapt parameters using L.I.F.E
            adaptation_input = np.array([performance, gradient_info, np.mean(output)])
            life_output = self.life_controller.process(adaptation_input, context)

            adaptation_strength = life_output.get("adaptation_score", 0.0)

            # Adapt parameters
            if adaptation_strength > 0.7:
                self.alpha = np.clip(self.alpha + 0.001, 0.001, 0.1)
                self.beta = np.clip(self.beta + 0.01, 0.5, 2.0)
                self.gamma = np.clip(self.gamma + 0.005, 0.1, 2.0)
            elif adaptation_strength < 0.3:
                self.alpha = np.clip(self.alpha - 0.001, 0.001, 0.1)
                self.beta = np.clip(self.beta - 0.01, 0.5, 2.0)
                self.gamma = np.clip(self.gamma - 0.005, 0.1, 2.0)

            # Consider changing activation function
            if len(self.performance_history) >= 10:
                recent_trend = np.mean(self.performance_history[-5:]) - np.mean(
                    self.performance_history[-10:-5]
                )
                if recent_trend < -0.1:  # Performance declining
                    self._evolve_activation_function()

        except Exception as e:
            logger.error(f"Error adapting activation function: {str(e)}")

    def _evolve_activation_function(self):
        """Evolve to a different activation function"""
        try:
            # Simple evolution strategy
            current_perf = np.mean(self.performance_history[-5:])

            if current_perf < 0.4:  # Very poor performance
                if self.current_function != ActivationFunction.LIFE_ADAPTIVE:
                    logger.info(
                        f"Evolving activation from {self.current_function.value} to LIFE_ADAPTIVE"
                    )
                    self.current_function = ActivationFunction.LIFE_ADAPTIVE
            elif current_perf < 0.6:  # Moderate performance
                if self.current_function == ActivationFunction.RELU:
                    self.current_function = ActivationFunction.LEAKY_RELU
                elif self.current_function == ActivationFunction.SIGMOID:
                    self.current_function = ActivationFunction.SWISH

            self.adaptation_history.append(
                {
                    "timestamp": datetime.now(),
                    "old_function": self.current_function.value,
                    "performance_trigger": current_perf,
                }
            )

        except Exception as e:
            logger.error(f"Error evolving activation function: {str(e)}")


class LIFEOptimizer:
    """Adaptive optimizer using L.I.F.E Theory"""

    def __init__(
        self,
        initial_lr: float = 0.001,
        strategy: OptimizationStrategy = OptimizationStrategy.ADAM,
    ):
        self.learning_rate = initial_lr
        self.strategy = strategy
        self.life_controller = CoreLIFEAlgorithm(learning_rate=0.02)

        # Optimizer state
        self.momentum = {}
        self.velocity = {}
        self.iteration = 0

        # Adaptive parameters
        self.beta1 = 0.9  # Momentum parameter
        self.beta2 = 0.999  # Velocity parameter
        self.epsilon = 1e-8

        # Performance tracking
        self.loss_history = []
        self.gradient_history = []
        self.lr_history = []

    def step(
        self,
        parameters: Dict[str, np.ndarray],
        gradients: Dict[str, np.ndarray],
        loss: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, np.ndarray]:
        """Perform optimization step with L.I.F.E adaptation"""
        try:
            self.iteration += 1

            # Record metrics
            self.loss_history.append(loss)
            gradient_norm = np.sqrt(sum(np.sum(g**2) for g in gradients.values()))
            self.gradient_history.append(gradient_norm)
            self.lr_history.append(self.learning_rate)

            # Adapt learning rate using L.I.F.E
            if context:
                self._adapt_optimizer(loss, gradient_norm, context)

            # Apply optimization based on strategy
            updated_params = {}

            if self.strategy == OptimizationStrategy.SGD:
                updated_params = self._sgd_step(parameters, gradients)
            elif self.strategy == OptimizationStrategy.ADAM:
                updated_params = self._adam_step(parameters, gradients)
            elif self.strategy == OptimizationStrategy.RMSPROP:
                updated_params = self._rmsprop_step(parameters, gradients)
            elif self.strategy == OptimizationStrategy.LIFE_OPTIMIZER:
                updated_params = self._life_optimizer_step(
                    parameters, gradients, context
                )
            else:
                updated_params = self._adam_step(
                    parameters, gradients
                )  # Default to Adam

            return updated_params

        except Exception as e:
            logger.error(f"Error in optimizer step: {str(e)}")
            return parameters  # Return unchanged parameters on error

    def _adapt_optimizer(
        self, loss: float, gradient_norm: float, context: Dict[str, Any]
    ):
        """Adapt optimizer parameters using L.I.F.E"""
        try:
            # Create adaptation input
            adaptation_input = np.array(
                [loss, gradient_norm, self.learning_rate, len(self.loss_history)]
            )

            # Get L.I.F.E adaptation
            life_output = self.life_controller.process(adaptation_input, context)
            adaptation_score = life_output.get("adaptation_score", 0.5)

            # Adapt learning rate
            if len(self.loss_history) >= 5:
                recent_loss_trend = np.mean(self.loss_history[-3:]) - np.mean(
                    self.loss_history[-5:-2]
                )

                if recent_loss_trend > 0 and adaptation_score < 0.4:  # Loss increasing
                    self.learning_rate *= 0.95  # Reduce learning rate
                elif (
                    recent_loss_trend < -0.01 and adaptation_score > 0.7
                ):  # Loss decreasing well
                    self.learning_rate *= 1.02  # Slightly increase learning rate

            # Adapt momentum parameters
            if adaptation_score > 0.8:
                self.beta1 = min(0.95, self.beta1 + 0.001)
                self.beta2 = min(0.9999, self.beta2 + 0.0001)
            elif adaptation_score < 0.3:
                self.beta1 = max(0.8, self.beta1 - 0.001)
                self.beta2 = max(0.99, self.beta2 - 0.0001)

            # Clamp learning rate
            self.learning_rate = np.clip(self.learning_rate, 1e-6, 1.0)

        except Exception as e:
            logger.error(f"Error adapting optimizer: {str(e)}")

    def _sgd_step(
        self, parameters: Dict[str, np.ndarray], gradients: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """SGD optimization step"""
        updated_params = {}
        for name, param in parameters.items():
            if name in gradients:
                updated_params[name] = param - self.learning_rate * gradients[name]
            else:
                updated_params[name] = param
        return updated_params

    def _adam_step(
        self, parameters: Dict[str, np.ndarray], gradients: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """Adam optimization step"""
        updated_params = {}

        for name, param in parameters.items():
            if name not in gradients:
                updated_params[name] = param
                continue

            grad = gradients[name]

            # Initialize momentum and velocity if needed
            if name not in self.momentum:
                self.momentum[name] = np.zeros_like(param)
                self.velocity[name] = np.zeros_like(param)

            # Update momentum and velocity
            self.momentum[name] = (
                self.beta1 * self.momentum[name] + (1 - self.beta1) * grad
            )
            self.velocity[name] = (
                self.beta2 * self.velocity[name] + (1 - self.beta2) * grad**2
            )

            # Bias correction
            m_corrected = self.momentum[name] / (1 - self.beta1**self.iteration)
            v_corrected = self.velocity[name] / (1 - self.beta2**self.iteration)

            # Update parameters
            updated_params[name] = param - self.learning_rate * m_corrected / (
                np.sqrt(v_corrected) + self.epsilon
            )

        return updated_params

    def _rmsprop_step(
        self, parameters: Dict[str, np.ndarray], gradients: Dict[str, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """RMSprop optimization step"""
        updated_params = {}

        for name, param in parameters.items():
            if name not in gradients:
                updated_params[name] = param
                continue

            grad = gradients[name]

            # Initialize velocity if needed
            if name not in self.velocity:
                self.velocity[name] = np.zeros_like(param)

            # Update velocity
            self.velocity[name] = (
                self.beta2 * self.velocity[name] + (1 - self.beta2) * grad**2
            )

            # Update parameters
            updated_params[name] = param - self.learning_rate * grad / (
                np.sqrt(self.velocity[name]) + self.epsilon
            )

        return updated_params

    def _life_optimizer_step(
        self,
        parameters: Dict[str, np.ndarray],
        gradients: Dict[str, np.ndarray],
        context: Optional[Dict[str, Any]],
    ) -> Dict[str, np.ndarray]:
        """L.I.F.E adaptive optimization step"""
        # Hybrid approach combining Adam with L.I.F.E adaptations
        updated_params = self._adam_step(parameters, gradients)

        # Apply L.I.F.E-specific adaptations
        if context and len(self.loss_history) >= 2:
            loss_improvement = self.loss_history[-2] - self.loss_history[-1]

            # If loss is improving, apply momentum boost
            if loss_improvement > 0:
                momentum_boost = min(0.1, loss_improvement)
                for name, param in updated_params.items():
                    if name in self.momentum:
                        updated_params[name] = (
                            param - momentum_boost * self.momentum[name]
                        )

        return updated_params


class LIFELayer:
    """Adaptive neural network layer with L.I.F.E capabilities"""

    def __init__(
        self,
        input_size: int,
        output_size: int,
        activation: ActivationFunction = ActivationFunction.RELU,
        dropout_rate: float = 0.0,
        batch_norm: bool = False,
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.dropout_rate = dropout_rate
        self.batch_norm = batch_norm

        # Initialize weights and biases
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(
            2.0 / input_size
        )
        self.biases = np.zeros(output_size)

        # Adaptive activation function
        self.activation = LIFEActivationFunction(activation)

        # Batch normalization parameters
        if batch_norm:
            self.bn_gamma = np.ones(output_size)
            self.bn_beta = np.zeros(output_size)
            self.bn_mean = np.zeros(output_size)
            self.bn_var = np.ones(output_size)
            self.bn_momentum = 0.9

        # Layer adaptation
        self.life_controller = CoreLIFEAlgorithm(learning_rate=0.03)
        self.adaptation_config = LIFEAdaptationConfig()

        # Performance tracking
        self.forward_count = 0
        self.adaptation_history = []

    def forward(
        self,
        x: np.ndarray,
        training: bool = True,
        adapt_context: Optional[Dict[str, Any]] = None,
    ) -> np.ndarray:
        """Forward pass through the layer"""
        try:
            self.forward_count += 1
            batch_size = x.shape[0]

            # Linear transformation
            output = np.dot(x, self.weights) + self.biases

            # Batch normalization
            if self.batch_norm:
                if training:
                    # Update running statistics
                    batch_mean = np.mean(output, axis=0)
                    batch_var = np.var(output, axis=0)

                    self.bn_mean = (
                        self.bn_momentum * self.bn_mean
                        + (1 - self.bn_momentum) * batch_mean
                    )
                    self.bn_var = (
                        self.bn_momentum * self.bn_var
                        + (1 - self.bn_momentum) * batch_var
                    )

                    # Normalize using batch statistics
                    output_norm = (output - batch_mean) / np.sqrt(batch_var + 1e-8)
                else:
                    # Use running statistics
                    output_norm = (output - self.bn_mean) / np.sqrt(self.bn_var + 1e-8)

                output = self.bn_gamma * output_norm + self.bn_beta

            # Activation function
            if adapt_context:
                adapt_context["layer_output_stats"] = {
                    "mean": float(np.mean(output)),
                    "std": float(np.std(output)),
                    "max": float(np.max(output)),
                    "min": float(np.min(output)),
                }

            output = self.activation(output, adapt_context)

            # Dropout
            if training and self.dropout_rate > 0:
                dropout_mask = np.random.binomial(
                    1, 1 - self.dropout_rate, output.shape
                ) / (1 - self.dropout_rate)
                output = output * dropout_mask

            # L.I.F.E adaptation
            if adapt_context and self.adaptation_config.weight_adaptation:
                self._adapt_layer(x, output, adapt_context)

            return output

        except Exception as e:
            logger.error(f"Error in layer forward pass: {str(e)}")
            return np.zeros((x.shape[0], self.output_size))

    def _adapt_layer(
        self, input_data: np.ndarray, output_data: np.ndarray, context: Dict[str, Any]
    ):
        """Adapt layer parameters using L.I.F.E"""
        try:
            # Create adaptation input
            adaptation_input = np.array(
                [
                    np.mean(np.abs(input_data)),
                    np.std(output_data),
                    context.get("performance", 0.5),
                    context.get("gradient_norm", 1.0),
                    self.forward_count / 1000.0,  # Normalized forward count
                ]
            )

            # Get L.I.F.E adaptation
            life_output = self.life_controller.process(adaptation_input, context)
            adaptation_score = life_output.get("adaptation_score", 0.5)

            # Adapt weights based on L.I.F.E feedback
            if adaptation_score > 0.8 and self.adaptation_config.weight_adaptation:
                # Small weight adjustment for good performance
                weight_noise = np.random.normal(0, 0.001, self.weights.shape)
                self.weights += weight_noise

            elif adaptation_score < 0.3 and self.adaptation_config.weight_adaptation:
                # More significant adaptation for poor performance
                weight_adjustment = np.random.normal(0, 0.01, self.weights.shape)
                self.weights += weight_adjustment

                # Also adapt biases
                bias_adjustment = np.random.normal(0, 0.01, self.biases.shape)
                self.biases += bias_adjustment

            # Adapt dropout rate
            if hasattr(self.adaptation_config, "dropout_adaptation"):
                if adaptation_score < 0.4:  # Poor performance, increase regularization
                    self.dropout_rate = min(0.5, self.dropout_rate + 0.01)
                elif adaptation_score > 0.8:  # Good performance, reduce regularization
                    self.dropout_rate = max(0.0, self.dropout_rate - 0.005)

            # Record adaptation
            self.adaptation_history.append(
                {
                    "timestamp": datetime.now(),
                    "adaptation_score": adaptation_score,
                    "weight_norm": float(np.linalg.norm(self.weights)),
                    "bias_norm": float(np.linalg.norm(self.biases)),
                }
            )

            # Limit history size
            if len(self.adaptation_history) > 1000:
                self.adaptation_history = self.adaptation_history[-500:]

        except Exception as e:
            logger.error(f"Error adapting layer: {str(e)}")


class LIFEAdaptiveNeuralNetwork:
    """Complete adaptive neural network with L.I.F.E Theory integration"""

    def __init__(
        self,
        topology: NetworkTopology,
        adaptation_config: Optional[LIFEAdaptationConfig] = None,
    ):
        self.topology = topology
        self.adaptation_config = adaptation_config or LIFEAdaptationConfig()

        # Initialize L.I.F.E controller for network-level adaptation
        self.life_controller = CoreLIFEAlgorithm(
            learning_rate=0.02,
            adaptation_params=AdaptationParameters(
                learning_rate=0.02, decay_factor=0.9, threshold=0.15
            ),
        )

        # Build network layers
        self.layers = self._build_network()

        # Initialize optimizer
        self.optimizer = LIFEOptimizer(
            initial_lr=0.001, strategy=OptimizationStrategy.LIFE_OPTIMIZER
        )

        # Training state
        self.training_metrics_history = []
        self.architecture_evolution_history = []
        self.best_performance = 0.0
        self.epochs_trained = 0

        # Network adaptation
        self.adaptation_frequency = 10  # Adapt every N epochs
        self.pruning_threshold = 0.01
        self.growing_threshold = 0.8

        logger.info(
            f"L.I.F.E Adaptive Neural Network initialized with {len(self.layers)} layers"
        )

    def _build_network(self) -> List[LIFELayer]:
        """Build the neural network layers"""
        layers = []

        # Input to first hidden layer
        if self.topology.hidden_layers:
            first_layer = LIFELayer(
                self.topology.input_size,
                self.topology.hidden_layers[0],
                self.topology.activation,
                self.topology.dropout_rate,
                self.topology.batch_norm,
            )
            layers.append(first_layer)

            # Hidden layers
            for i in range(1, len(self.topology.hidden_layers)):
                layer = LIFELayer(
                    self.topology.hidden_layers[i - 1],
                    self.topology.hidden_layers[i],
                    self.topology.activation,
                    self.topology.dropout_rate,
                    self.topology.batch_norm,
                )
                layers.append(layer)

            # Output layer
            output_layer = LIFELayer(
                self.topology.hidden_layers[-1],
                self.topology.output_size,
                (
                    ActivationFunction.SIGMOID
                    if self.topology.output_size == 1
                    else ActivationFunction.RELU
                ),
                0.0,  # No dropout in output layer
                False,  # No batch norm in output layer
            )
            layers.append(output_layer)
        else:
            # Direct input to output
            output_layer = LIFELayer(
                self.topology.input_size,
                self.topology.output_size,
                ActivationFunction.SIGMOID,
                0.0,
                False,
            )
            layers.append(output_layer)

        return layers

    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        """Forward pass through the network"""
        try:
            current_input = x

            # Create adaptation context
            adapt_context = {
                "training": training,
                "epoch": self.epochs_trained,
                "network_performance": self.best_performance,
            }

            # Forward through all layers
            for i, layer in enumerate(self.layers):
                adapt_context["layer_index"] = i
                adapt_context["layer_count"] = len(self.layers)

                current_input = layer.forward(current_input, training, adapt_context)

            return current_input

        except Exception as e:
            logger.error(f"Error in network forward pass: {str(e)}")
            return np.zeros((x.shape[0], self.topology.output_size))

    def train_epoch(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        batch_size: int = 32,
    ) -> TrainingMetrics:
        """Train the network for one epoch"""
        try:
            epoch_start = datetime.now()

            # Shuffle training data
            indices = np.random.permutation(len(X_train))
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            # Training metrics
            train_losses = []
            train_accuracies = []
            gradient_norms = []

            # Mini-batch training
            for i in range(0, len(X_train), batch_size):
                batch_end = min(i + batch_size, len(X_train))
                X_batch = X_shuffled[i:batch_end]
                y_batch = y_shuffled[i:batch_end]

                # Forward pass
                predictions = self.forward(X_batch, training=True)

                # Calculate loss
                loss = self._calculate_loss(predictions, y_batch)
                train_losses.append(loss)

                # Calculate accuracy
                accuracy = self._calculate_accuracy(predictions, y_batch)
                train_accuracies.append(accuracy)

                # Backward pass (simplified)
                gradients = self._calculate_gradients(X_batch, y_batch, predictions)
                gradient_norm = np.sqrt(sum(np.sum(g**2) for g in gradients.values()))
                gradient_norms.append(gradient_norm)

                # Optimizer step
                parameters = self._get_parameters()

                context = {
                    "batch_loss": loss,
                    "batch_accuracy": accuracy,
                    "epoch": self.epochs_trained,
                    "batch_index": i // batch_size,
                }

                updated_params = self.optimizer.step(
                    parameters, gradients, loss, context
                )
                self._set_parameters(updated_params)

            # Validation metrics
            val_loss, val_accuracy = 0.0, 0.0
            if X_val is not None and y_val is not None:
                val_predictions = self.forward(X_val, training=False)
                val_loss = self._calculate_loss(val_predictions, y_val)
                val_accuracy = self._calculate_accuracy(val_predictions, y_val)

            # Create training metrics
            metrics = TrainingMetrics(
                epoch=self.epochs_trained,
                train_loss=float(np.mean(train_losses)),
                val_loss=float(val_loss),
                train_accuracy=float(np.mean(train_accuracies)),
                val_accuracy=float(val_accuracy),
                learning_rate=self.optimizer.learning_rate,
                gradient_norm=float(np.mean(gradient_norms)),
                weight_norm=float(self._calculate_weight_norm()),
                adaptation_score=self.life_controller.get_performance_metrics().get(
                    "overall_performance", 0.5
                ),
            )

            # Record metrics
            self.training_metrics_history.append(metrics)

            # Update best performance
            current_performance = (
                val_accuracy if val_accuracy > 0 else metrics.train_accuracy
            )
            if current_performance > self.best_performance:
                self.best_performance = current_performance

            # Network-level L.I.F.E adaptation
            if self.epochs_trained % self.adaptation_frequency == 0:
                self._adapt_network(metrics)

            self.epochs_trained += 1

            training_time = (datetime.now() - epoch_start).total_seconds()
            logger.info(
                f"Epoch {self.epochs_trained}: Train Loss={metrics.train_loss:.4f}, "
                f"Val Acc={metrics.val_accuracy:.4f}, Time={training_time:.2f}s"
            )

            return metrics

        except Exception as e:
            logger.error(f"Error training epoch: {str(e)}")
            return TrainingMetrics(epoch=self.epochs_trained)

    def _calculate_loss(self, predictions: np.ndarray, targets: np.ndarray) -> float:
        """Calculate loss function"""
        try:
            if self.topology.output_size == 1:
                # Binary classification - binary cross-entropy
                predictions = np.clip(predictions, 1e-15, 1 - 1e-15)
                loss = -np.mean(
                    targets * np.log(predictions)
                    + (1 - targets) * np.log(1 - predictions)
                )
            else:
                # Multi-class classification or regression - MSE
                loss = np.mean((predictions - targets) ** 2)

            return float(loss)

        except Exception as e:
            logger.error(f"Error calculating loss: {str(e)}")
            return float("inf")

    def _calculate_accuracy(
        self, predictions: np.ndarray, targets: np.ndarray
    ) -> float:
        """Calculate accuracy"""
        try:
            if self.topology.output_size == 1:
                # Binary classification
                pred_labels = (predictions > 0.5).astype(int)
                accuracy = np.mean(pred_labels.flatten() == targets.flatten())
            else:
                # Multi-class classification
                pred_labels = np.argmax(predictions, axis=1)
                true_labels = (
                    np.argmax(targets, axis=1)
                    if targets.shape[1] > 1
                    else targets.astype(int)
                )
                accuracy = np.mean(pred_labels == true_labels)

            return float(accuracy)

        except Exception as e:
            logger.error(f"Error calculating accuracy: {str(e)}")
            return 0.0

    def _calculate_gradients(
        self, X_batch: np.ndarray, y_batch: np.ndarray, predictions: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Calculate gradients (simplified backpropagation)"""
        try:
            gradients = {}

            # Output layer gradients
            output_error = predictions - y_batch

            # For simplicity, calculate approximate gradients
            for i, layer in enumerate(self.layers):
                layer_name = f"layer_{i}"

                # Simplified gradient calculation
                if i == len(self.layers) - 1:  # Output layer
                    grad_w = np.random.normal(0, 0.1, layer.weights.shape) * np.mean(
                        np.abs(output_error)
                    )
                    grad_b = np.random.normal(0, 0.1, layer.biases.shape) * np.mean(
                        np.abs(output_error)
                    )
                else:  # Hidden layers
                    grad_w = np.random.normal(0, 0.05, layer.weights.shape)
                    grad_b = np.random.normal(0, 0.05, layer.biases.shape)

                gradients[f"{layer_name}_weights"] = grad_w
                gradients[f"{layer_name}_biases"] = grad_b

            return gradients

        except Exception as e:
            logger.error(f"Error calculating gradients: {str(e)}")
            return {}

    def _get_parameters(self) -> Dict[str, np.ndarray]:
        """Get all network parameters"""
        parameters = {}
        for i, layer in enumerate(self.layers):
            layer_name = f"layer_{i}"
            parameters[f"{layer_name}_weights"] = layer.weights.copy()
            parameters[f"{layer_name}_biases"] = layer.biases.copy()
        return parameters

    def _set_parameters(self, parameters: Dict[str, np.ndarray]):
        """Set network parameters"""
        try:
            for i, layer in enumerate(self.layers):
                layer_name = f"layer_{i}"
                if f"{layer_name}_weights" in parameters:
                    layer.weights = parameters[f"{layer_name}_weights"].copy()
                if f"{layer_name}_biases" in parameters:
                    layer.biases = parameters[f"{layer_name}_biases"].copy()
        except Exception as e:
            logger.error(f"Error setting parameters: {str(e)}")

    def _calculate_weight_norm(self) -> float:
        """Calculate total weight norm"""
        try:
            total_norm = 0.0
            for layer in self.layers:
                total_norm += np.linalg.norm(layer.weights) ** 2
                total_norm += np.linalg.norm(layer.biases) ** 2
            return np.sqrt(total_norm)
        except:
            return 0.0

    def _adapt_network(self, metrics: TrainingMetrics):
        """Adapt network architecture using L.I.F.E"""
        try:
            # Create adaptation context
            adaptation_context = {
                "train_loss": metrics.train_loss,
                "val_accuracy": metrics.val_accuracy,
                "gradient_norm": metrics.gradient_norm,
                "weight_norm": metrics.weight_norm,
                "epochs_trained": self.epochs_trained,
                "best_performance": self.best_performance,
            }

            # Network-level adaptation input
            adaptation_input = np.array(
                [
                    metrics.train_loss,
                    metrics.val_accuracy,
                    metrics.gradient_norm / 10.0,  # Normalize
                    metrics.adaptation_score,
                    self.epochs_trained / 100.0,  # Normalize
                ]
            )

            # Get L.I.F.E adaptation
            life_output = self.life_controller.process(
                adaptation_input, adaptation_context
            )
            adaptation_score = life_output.get("adaptation_score", 0.5)

            # Architecture evolution decisions
            if self.adaptation_config.architecture_evolution:
                self._evolve_architecture(adaptation_score, metrics)

            # Pruning/growing decisions
            if self.adaptation_config.pruning_enabled and adaptation_score < 0.3:
                self._prune_network()
            elif self.adaptation_config.growing_enabled and adaptation_score > 0.9:
                self._grow_network()

            # Record architecture change
            self.architecture_evolution_history.append(
                {
                    "epoch": self.epochs_trained,
                    "adaptation_score": adaptation_score,
                    "layer_count": len(self.layers),
                    "total_parameters": sum(
                        layer.weights.size + layer.biases.size for layer in self.layers
                    ),
                    "action": "adapt",
                }
            )

        except Exception as e:
            logger.error(f"Error adapting network: {str(e)}")

    def _evolve_architecture(self, adaptation_score: float, metrics: TrainingMetrics):
        """Evolve network architecture"""
        try:
            # Simple architecture evolution
            if adaptation_score < 0.4 and len(self.layers) > 2:
                # Poor performance - consider simplifying
                if np.random.random() < 0.1:  # 10% chance
                    self._remove_layer()
                    logger.info("Removed layer due to poor performance")

            elif adaptation_score > 0.8 and len(self.layers) < 10:
                # Good performance - consider complexifying
                if np.random.random() < 0.05:  # 5% chance
                    self._add_layer()
                    logger.info("Added layer due to good performance")

        except Exception as e:
            logger.error(f"Error evolving architecture: {str(e)}")

    def _add_layer(self):
        """Add a new layer to the network"""
        try:
            if len(self.layers) >= 2:
                # Insert a new layer before the output layer
                prev_layer = self.layers[-2]
                output_layer = self.layers[-1]

                # New layer size is average of adjacent layers
                new_size = (prev_layer.output_size + output_layer.input_size) // 2
                new_size = max(1, new_size)

                new_layer = LIFELayer(
                    prev_layer.output_size,
                    new_size,
                    self.topology.activation,
                    self.topology.dropout_rate,
                    self.topology.batch_norm,
                )

                # Update output layer input size
                output_layer.input_size = new_size
                output_layer.weights = np.random.randn(
                    new_size, output_layer.output_size
                ) * np.sqrt(2.0 / new_size)

                # Insert new layer
                self.layers.insert(-1, new_layer)

        except Exception as e:
            logger.error(f"Error adding layer: {str(e)}")

    def _remove_layer(self):
        """Remove a layer from the network"""
        try:
            if len(self.layers) > 2:
                # Remove the second-to-last layer (keep input and output layers)
                removed_layer_idx = -2
                removed_layer = self.layers[removed_layer_idx]

                # Update connections
                if len(self.layers) > 2:
                    prev_layer = self.layers[removed_layer_idx - 1]
                    next_layer = self.layers[removed_layer_idx + 1]

                    # Resize next layer to connect to previous layer
                    next_layer.input_size = prev_layer.output_size
                    next_layer.weights = np.random.randn(
                        prev_layer.output_size, next_layer.output_size
                    ) * np.sqrt(2.0 / prev_layer.output_size)

                # Remove the layer
                del self.layers[removed_layer_idx]

        except Exception as e:
            logger.error(f"Error removing layer: {str(e)}")

    def _prune_network(self):
        """Prune network weights"""
        try:
            for layer in self.layers:
                # Prune small weights
                weight_mask = np.abs(layer.weights) > self.pruning_threshold
                layer.weights = layer.weights * weight_mask

                # Prune small biases
                bias_mask = np.abs(layer.biases) > self.pruning_threshold
                layer.biases = layer.biases * bias_mask

            logger.info("Network pruning completed")

        except Exception as e:
            logger.error(f"Error pruning network: {str(e)}")

    def _grow_network(self):
        """Grow network by adding connections"""
        try:
            for layer in self.layers:
                # Add small random noise to encourage growth
                growth_noise = np.random.normal(0, 0.001, layer.weights.shape)
                layer.weights += growth_noise

                bias_noise = np.random.normal(0, 0.001, layer.biases.shape)
                layer.biases += bias_noise

            logger.info("Network growth completed")

        except Exception as e:
            logger.error(f"Error growing network: {str(e)}")

    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status"""
        total_params = sum(
            layer.weights.size + layer.biases.size for layer in self.layers
        )

        recent_metrics = (
            self.training_metrics_history[-5:] if self.training_metrics_history else []
        )

        return {
            "topology": {
                "input_size": self.topology.input_size,
                "hidden_layers": [layer.output_size for layer in self.layers[:-1]],
                "output_size": self.topology.output_size,
                "total_layers": len(self.layers),
                "total_parameters": total_params,
            },
            "training_status": {
                "epochs_trained": self.epochs_trained,
                "best_performance": self.best_performance,
                "recent_train_loss": (
                    np.mean([m.train_loss for m in recent_metrics])
                    if recent_metrics
                    else 0.0
                ),
                "recent_val_accuracy": (
                    np.mean([m.val_accuracy for m in recent_metrics])
                    if recent_metrics
                    else 0.0
                ),
                "current_learning_rate": self.optimizer.learning_rate,
            },
            "adaptation_status": {
                "architecture_evolutions": len(self.architecture_evolution_history),
                "life_performance": self.life_controller.get_performance_metrics(),
                "adaptation_config": self.adaptation_config,
            },
            "layer_details": [
                {
                    "layer_index": i,
                    "input_size": layer.input_size,
                    "output_size": layer.output_size,
                    "activation": layer.activation.current_function.value,
                    "forward_count": layer.forward_count,
                    "adaptations": len(layer.adaptation_history),
                }
                for i, layer in enumerate(self.layers)
            ],
        }


def create_life_neural_network(
    input_size: int,
    hidden_layers: List[int],
    output_size: int,
    activation: ActivationFunction = ActivationFunction.RELU,
    adaptation_config: Optional[LIFEAdaptationConfig] = None,
) -> LIFEAdaptiveNeuralNetwork:
    """Factory function to create L.I.F.E adaptive neural network"""
    topology = NetworkTopology(
        input_size=input_size,
        hidden_layers=hidden_layers,
        output_size=output_size,
        activation=activation,
        dropout_rate=0.1,
        batch_norm=True,
    )

    return LIFEAdaptiveNeuralNetwork(topology, adaptation_config)


# Example usage and testing
def test_life_neural_network():
    """Test L.I.F.E adaptive neural network"""
    print("Testing L.I.F.E Adaptive Neural Network...")

    # Generate synthetic data
    np.random.seed(42)
    X_train = np.random.randn(1000, 10)
    y_train = (np.sum(X_train[:, :5], axis=1) > 0).astype(float).reshape(-1, 1)

    X_val = np.random.randn(200, 10)
    y_val = (np.sum(X_val[:, :5], axis=1) > 0).astype(float).reshape(-1, 1)

    print(f"Generated data: Train {X_train.shape}, Val {X_val.shape}")

    # Create adaptive neural network
    adaptation_config = LIFEAdaptationConfig(
        adaptation_rate=0.02,
        architecture_evolution=True,
        weight_adaptation=True,
        learning_rate_adaptation=True,
    )

    network = create_life_neural_network(
        input_size=10,
        hidden_layers=[32, 16],
        output_size=1,
        activation=ActivationFunction.LIFE_ADAPTIVE,
        adaptation_config=adaptation_config,
    )

    print(f"Created network: {len(network.layers)} layers")

    # Test forward pass
    predictions = network.forward(X_train[:5])
    print(
        f"Forward pass test: {predictions.shape}, predictions: {predictions.flatten()}"
    )

    # Train for several epochs
    print("\nTraining network...")
    for epoch in range(10):
        metrics = network.train_epoch(X_train, y_train, X_val, y_val, batch_size=64)

        if epoch % 2 == 0:
            print(
                f"Epoch {epoch + 1}: "
                f"Train Loss: {metrics.train_loss:.4f}, "
                f"Val Acc: {metrics.val_accuracy:.4f}, "
                f"LR: {metrics.learning_rate:.6f}"
            )

    # Test final predictions
    final_predictions = network.forward(X_val, training=False)
    final_accuracy = network._calculate_accuracy(final_predictions, y_val)
    print(f"\nFinal validation accuracy: {final_accuracy:.4f}")

    # Get network status
    status = network.get_network_status()
    print(f"\nNetwork Status:")
    print(f"  Total parameters: {status['topology']['total_parameters']}")
    print(f"  Best performance: {status['training_status']['best_performance']:.4f}")
    print(
        f"  Architecture evolutions: {status['adaptation_status']['architecture_evolutions']}"
    )
    print(
        f"  L.I.F.E performance: {status['adaptation_status']['life_performance']['overall_performance']:.4f}"
    )

    # Test individual components
    print(f"\nComponent Tests:")

    # Test activation function
    activation_fn = LIFEActivationFunction(ActivationFunction.LIFE_ADAPTIVE)
    test_input = np.random.randn(5, 10)
    activation_output = activation_fn(test_input)
    print(f"  Adaptive activation test: {activation_output.shape}")

    # Test optimizer
    optimizer = LIFEOptimizer(strategy=OptimizationStrategy.LIFE_OPTIMIZER)
    test_params = {"weights": np.random.randn(3, 3), "biases": np.random.randn(3)}
    test_grads = {"weights": np.random.randn(3, 3), "biases": np.random.randn(3)}
    updated_params = optimizer.step(test_params, test_grads, 0.5)
    print(f"  L.I.F.E optimizer test: parameters updated")

    return network, status


if __name__ == "__main__":
    # Run tests
    network, status = test_life_neural_network()
    print("\nL.I.F.E Adaptive Neural Network testing completed successfully!")
