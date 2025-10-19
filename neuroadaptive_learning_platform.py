#!/usr/bin/env python3
"""
L.I.F.E. Neuroadaptive Learning Platform
Optimal Implementation for Real-Time EEG-Based Personalized Learning

Copyright 2025 - Sergio Paya Borrull
Based on experimentP2L L.I.F.E. Theory Algorithm
Integrates Research Data Library for Maximum Efficacy

Purpose: Real-time neuroadaptive learning that adapts to individual brain states
"""

import asyncio
import json
import logging
import math
import os
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

# Optional dependency: numpy (used only for a simple mean). Fallback to pure Python if unavailable.
try:  # pragma: no cover - optional import
    import numpy as np  # type: ignore

    _HAS_NUMPY = True
except Exception:  # noqa: BLE001 - broad to catch any import-time issues
    np = None  # type: ignore
    _HAS_NUMPY = False


def _safe_mean(values: List[float]) -> float:
    """Return the arithmetic mean without requiring numpy.

    Handles empty lists by returning 0.0 to keep downstream math stable.
    """
    if not values:
        return 0.0
    # Guard against non-finite entries
    total = 0.0
    count = 0
    for v in values:
        try:
            if v is None:
                continue
            total += float(v)
            count += 1
        except (TypeError, ValueError):
            continue
    return (total / count) if count else 0.0


# Add research library to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Import L.I.F.E. Theory Algorithm Core
try:
    # Try importing from experimentP2L file
    import importlib.util

    exp_file = os.path.join(
        SCRIPT_DIR,
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
    )
    if os.path.exists(exp_file):
        spec = importlib.util.spec_from_file_location("experimentP2L", exp_file)
        experimentP2L = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(experimentP2L)
        LIFEAlgorithmCore = experimentP2L.LIFEAlgorithmCore
        EEGMetrics = experimentP2L.EEGMetrics
        LearningStage = experimentP2L.LearningStage
        NeuralState = experimentP2L.NeuralState
    else:
        raise ImportError("experimentP2L file not found")
except ImportError:
    print("Warning: Using minimal L.I.F.E. implementation for standalone operation")
    # Minimal fallback implementation
    from dataclasses import dataclass
    from datetime import datetime
    from enum import Enum

    class LearningStage(Enum):
        ACQUISITION = "acquisition"
        CONSOLIDATION = "consolidation"
        RETRIEVAL = "retrieval"
        ADAPTATION = "adaptation"

    class NeuralState(Enum):
        RESTING = "resting"
        ACTIVE = "active"
        LEARNING = "learning"
        MEMORY_FORMATION = "memory_formation"

    @dataclass
    class EEGMetrics:
        timestamp: datetime
        alpha_power: float
        beta_power: float
        theta_power: float
        delta_power: float
        gamma_power: float
        coherence_score: float
        attention_index: float
        learning_efficiency: float

    class LIFEAlgorithmCore:
        def __init__(self, config=None):
            self.config = config or {}
            self.version = "2025.1.0-MINIMAL"


# Import research data library
try:
    from research_data_library import ResearchDataLibrary, initialize_research_library

    RESEARCH_LIB_AVAILABLE = True
except ImportError:
    print("Warning: Research data library not available - using minimal version")
    RESEARCH_LIB_AVAILABLE = False

# Configure logging (robust against path issues on Windows/OneDrive)
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
handlers: List[logging.Handler] = []
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file_path = os.path.join(
        LOG_DIR,
        f"neuroadaptive_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    )
    handlers.append(logging.FileHandler(log_file_path, encoding="utf-8"))
except Exception:
    # Fall back to a shorter path if necessary
    try:
        import tempfile

        alt_dir = os.path.join(tempfile.gettempdir(), "life_logs")
        os.makedirs(alt_dir, exist_ok=True)
        alt_log = os.path.join(
            alt_dir, f"neuroadaptive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        handlers.append(logging.FileHandler(alt_log, encoding="utf-8"))
    except Exception:
        # Final fallback: console-only logging
        pass

handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)
logger = logging.getLogger(__name__)


@dataclass
class IndividualTraits:
    """Individual learner characteristics for personalization"""

    cognitive_style: str  # visual, auditory, kinesthetic, reading_writing
    curiosity: float  # 0.0 to 1.0
    resilience: float  # 0.0 to 1.0
    openness: float  # 0.0 to 1.0
    focus_duration: float  # minutes
    preferred_complexity: str  # low, medium, high
    learning_pace: str  # slow, moderate, fast


@dataclass
class ContentAdaptation:
    """Dynamic content adaptation parameters"""

    complexity_level: float  # 0.0 (simple) to 1.0 (complex)
    pacing_speed: float  # 0.5 (slow) to 2.0 (fast)
    interaction_frequency: float  # interactions per minute
    visual_density: float  # 0.0 (minimal) to 1.0 (rich)
    challenge_level: float  # 0.0 (easy) to 1.0 (difficult)
    break_recommendation: bool = False
    content_type_adjustment: str = "maintain"  # simplify, maintain, intensify


@dataclass
class LearningSession:
    """Complete learning session tracking"""

    session_id: str
    student_id: str
    start_time: datetime
    traits: IndividualTraits
    eeg_samples: List[EEGMetrics] = field(default_factory=list)
    adaptations: List[ContentAdaptation] = field(default_factory=list)
    engagement_history: List[float] = field(default_factory=list)
    knowledge_checks: List[Tuple[str, bool, float]] = field(
        default_factory=list
    )  # (topic, correct, confidence)
    session_quality_score: float = 0.0
    neuroplasticity_index: float = 0.0
    recommendation: str = ""


class NeuroadaptiveLearningPlatform:
    """
    Main platform for real-time EEG-based adaptive learning

    Implements L.I.F.E. Theory principles:
    - Individual trait adaptation (Equation 1)
    - Neuroplasticity tracking (Equation 2)
    - Quantum trait projection (Equation 3)
    - Experience correlation (Equation 4)
    - Adaptive learning rate (Equation 9)
    """

    def __init__(self):
        logger.info("=" * 80)
        logger.info("L.I.F.E. NEUROADAPTIVE LEARNING PLATFORM - INITIALIZING")
        logger.info("=" * 80)

        # Initialize L.I.F.E. Algorithm Core
        self.life_algorithm = LIFEAlgorithmCore(
            config={
                "learning_rate": 0.01,
                "neural_sampling_rate": 256,
                "eeg_channels": 64,
                "real_time_processing": True,
                "adaptation_sensitivity": 0.8,
            }
        )

        # Initialize research data library if available
        if RESEARCH_LIB_AVAILABLE:
            self.research_library = initialize_research_library()
            logger.info(
                f"Research Data Library v{self.research_library.version} initialized"
            )
        else:
            self.research_library = None
            logger.info("Operating without research data library")

        # Active sessions
        self.active_sessions: Dict[str, LearningSession] = {}

        # Engagement thresholds (based on research)
        self.engagement_thresholds = {
            "critical_low": 0.4,  # Intervention required
            "low": 0.6,  # Adapt content
            "optimal": 0.75,  # Maintain
            "high": 0.9,  # Can increase challenge
        }

        # Adaptation history for optimization
        self.adaptation_history: List[Dict] = []

        logger.info(f"L.I.F.E. Algorithm Core v{self.life_algorithm.version} loaded")
        logger.info("Platform ready for neuroadaptive learning sessions")
        logger.info("=" * 80)

    async def start_learning_session(
        self, student_id: str, traits: IndividualTraits
    ) -> str:
        """
        Initialize a new neuroadaptive learning session

        Args:
            student_id: Unique student identifier
            traits: Individual learner characteristics

        Returns:
            session_id for tracking
        """
        session_id = f"NAL-{student_id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session = LearningSession(
            session_id=session_id,
            student_id=student_id,
            start_time=datetime.now(),
            traits=traits,
        )

        self.active_sessions[session_id] = session

        logger.info(f"Started learning session: {session_id}")
        logger.info(
            f"Student: {student_id} | Cognitive Style: {traits.cognitive_style}"
        )
        logger.info(
            f"Traits: Curiosity={traits.curiosity:.2f}, Resilience={traits.resilience:.2f}, Openness={traits.openness:.2f}"
        )

        return session_id

    async def process_eeg_and_adapt(
        self, session_id: str, eeg_data: List[float]
    ) -> ContentAdaptation:
        """
        Core adaptive learning loop - Process EEG and adapt content in real-time

        This implements the L.I.F.E. Theory optimal use case:
        1. Process EEG data (256 Hz, 64 channels)
        2. Detect engagement/attention/cognitive load
        3. Apply Equation 1 (Trait Modulation) if engagement drops
        4. Apply Equation 9 (Adaptive Learning Rate) for pacing
        5. Return content adaptation recommendations

        Args:
            session_id: Active session identifier
            eeg_data: Raw EEG data (simulated or real)

        Returns:
            ContentAdaptation with recommended changes
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Process EEG using research library if available
        if RESEARCH_LIB_AVAILABLE and self.research_library:
            eeg_result = self.research_library.process_raw_eeg(
                eeg_data, sampling_rate=256
            )
            engagement = eeg_result["engagement"]
            focus = eeg_result["focus"]
            stress = eeg_result["stress"]
            quality = eeg_result["quality_score"]
        else:
            # Fallback: Calculate engagement from EEG data
            engagement = self._calculate_engagement_fallback(eeg_data)
            focus = engagement * 0.85  # Approximate
            stress = 0.3  # Neutral
            quality = 0.8  # Assume good

        # Store engagement history
        session.engagement_history.append(engagement)

        # Initialize adaptation with current state
        adaptation = ContentAdaptation(
            complexity_level=0.6,  # Medium default
            pacing_speed=1.0,  # Normal speed
            interaction_frequency=2.0,  # 2 interactions per minute
            visual_density=0.5,
            challenge_level=0.6,
        )

        # === EQUATION 1: TRAIT MODULATION ===
        # If engagement drops, modulate traits to increase attention
        if engagement < self.engagement_thresholds["low"]:
            logger.info(f"⚠️ Low engagement detected: {engagement:.3f}")

            # Apply trait modulation (Equation 1 from L.I.F.E. Theory)
            trait_adaptation_factor = self._equation1_trait_modulation(
                current_trait=engagement,
                eeg_engagement=engagement,
                environmental_factor=1.0,
                individual_traits=session.traits,
            )

            # Adjust content based on modulation
            adaptation.complexity_level = max(
                0.3, adaptation.complexity_level * trait_adaptation_factor
            )
            adaptation.interaction_frequency = min(
                4.0, adaptation.interaction_frequency * 1.5
            )
            adaptation.content_type_adjustment = "simplify"

            logger.info(
                f"✓ Applied Equation 1 (Trait Modulation): Factor={trait_adaptation_factor:.3f}"
            )
            logger.info(f"  → Reduced complexity to {adaptation.complexity_level:.2f}")
            logger.info(
                f"  → Increased interactions to {adaptation.interaction_frequency:.1f}/min"
            )

        elif engagement < self.engagement_thresholds["critical_low"]:
            # Critical intervention
            logger.warning(f"🚨 CRITICAL: Very low engagement: {engagement:.3f}")
            adaptation.break_recommendation = True
            adaptation.content_type_adjustment = "simplify"
            adaptation.complexity_level = 0.2  # Maximum simplification
            adaptation.interaction_frequency = 5.0  # Very frequent interactions

        # === EQUATION 9: ADAPTIVE LEARNING RATE ===
        # Adjust pacing based on cognitive state (beta power indicates processing)
        beta_power = self._estimate_beta_power(eeg_data)
        learning_rate_adjustment = self._equation9_adaptive_learning_rate(beta_power)

        adaptation.pacing_speed = learning_rate_adjustment

        logger.info(
            f"✓ Applied Equation 9 (Adaptive Learning Rate): Speed={adaptation.pacing_speed:.2f}x"
        )

        # === EQUATION 2: NEUROPLASTICITY TRACKING ===
        # Track neural adaptation over time
        if len(session.engagement_history) > 10:
            neuroplasticity = self._equation2_neuroplasticity_growth(
                session.engagement_history[-10:], session.traits
            )
            session.neuroplasticity_index = neuroplasticity
            logger.info(f"✓ Neuroplasticity Index: {neuroplasticity:.3f}")

        # Optimize challenge level based on zone of proximal development
        if engagement > self.engagement_thresholds["high"] and stress < 0.4:
            # Learner is ready for more challenge
            adaptation.challenge_level = min(0.9, adaptation.challenge_level + 0.15)
            adaptation.complexity_level = min(0.9, adaptation.complexity_level + 0.1)
            adaptation.content_type_adjustment = "intensify"
            logger.info(
                f"✓ Increasing challenge: Engagement high ({engagement:.3f}), stress low ({stress:.2f})"
            )

        # Store adaptation
        session.adaptations.append(adaptation)

        # Log current state
        logger.info(
            f"Session {session_id} | Engagement: {engagement:.3f} | Focus: {focus:.3f} | Adaptations: {len(session.adaptations)}"
        )

        return adaptation

    def _equation1_trait_modulation(
        self,
        current_trait: float,
        eeg_engagement: float,
        environmental_factor: float,
        individual_traits: IndividualTraits,
    ) -> float:
        """
        Equation 1: Individual Trait Modulation

        Modulates learning traits based on neural feedback
        T'(i) = T(i) + α * ΔE(i) * F(env) * w(individual)

        where:
        - T(i): Current trait value
        - α: Learning rate (0.01)
        - ΔE(i): Change in engagement
        - F(env): Environmental factor
        - w(individual): Individual weighting
        """
        alpha = 0.01
        delta_engagement = eeg_engagement - current_trait

        # Individual weighting based on traits
        individual_weight = (
            individual_traits.curiosity * 0.3
            + individual_traits.resilience * 0.4
            + individual_traits.openness * 0.3
        )

        modulation = (
            current_trait
            + alpha * delta_engagement * environmental_factor * individual_weight
        )

        # Clamp to valid range
        return max(0.1, min(1.0, modulation))

    def _equation9_adaptive_learning_rate(self, beta_power: float) -> float:
        """
        Equation 9: Adaptive Learning Rate

        Adjusts content pacing based on cognitive processing state
        η(t) = η₀ * (1 + tanh(β(t) - β₀))

        where:
        - η₀: Base learning rate (1.0)
        - β(t): Current beta power
        - β₀: Baseline beta power (0.5)
        """
        eta_0 = 1.0
        beta_baseline = 0.5

        learning_rate = eta_0 * (1 + math.tanh(beta_power - beta_baseline))

        # Clamp to reasonable range (0.5x to 2.0x speed)
        return max(0.5, min(2.0, learning_rate))

    def _equation2_neuroplasticity_growth(
        self, engagement_window: List[float], traits: IndividualTraits
    ) -> float:
        """
        Equation 2: Neuroplasticity Growth Tracking

        P(t) = P(t-1) + γ * (E(t) - E_threshold) * w(resilience)

        where:
        - P(t): Neuroplasticity index at time t
        - γ: Growth rate (0.02)
        - E(t): Current engagement
        - E_threshold: Threshold for growth (0.6)
        """
        gamma = 0.02
        threshold = 0.6

        avg_engagement = sum(engagement_window) / len(engagement_window)
        growth = gamma * (avg_engagement - threshold) * traits.resilience

        # Cumulative growth with decay
        plasticity = 0.5 + growth * len(engagement_window)

        return max(0.0, min(1.0, plasticity))

    def _calculate_engagement_fallback(self, eeg_data: List[float]) -> float:
        """Calculate engagement when research library unavailable"""
        # Simple heuristic: higher values = higher engagement
        if len(eeg_data) == 0:
            return 0.5

        mean_signal = sum(eeg_data) / len(eeg_data)
        std_signal = (
            sum((x - mean_signal) ** 2 for x in eeg_data) / len(eeg_data)
        ) ** 0.5

        # Normalize to 0-1 range
        engagement = (mean_signal - 10) / 40  # Assuming EEG range 10-50
        engagement = max(0.3, min(0.95, engagement))

        return engagement

    def _estimate_beta_power(self, eeg_data: List[float]) -> float:
        """Estimate beta band power for learning rate adjustment"""
        # Simple approximation
        if len(eeg_data) < 10:
            return 0.5

        # High-frequency component (beta band is 12-30 Hz)
        high_freq_power = sum(
            abs(eeg_data[i] - eeg_data[i - 1]) for i in range(1, len(eeg_data))
        )
        high_freq_power /= len(eeg_data)

        # Normalize
        beta_power = high_freq_power / 10.0
        return max(0.1, min(1.0, beta_power))

    async def end_learning_session(self, session_id: str) -> Dict:
        """
        Complete learning session and generate comprehensive report

        Args:
            session_id: Session to end

        Returns:
            Session summary with recommendations
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Calculate session metrics
        duration_minutes = (datetime.now() - session.start_time).total_seconds() / 60
        avg_engagement = (
            sum(session.engagement_history) / len(session.engagement_history)
            if session.engagement_history
            else 0.0
        )
        adaptation_count = len(session.adaptations)

        # Quality score based on consistent high engagement
        high_engagement_ratio = (
            sum(1 for e in session.engagement_history if e > 0.75)
            / len(session.engagement_history)
            if session.engagement_history
            else 0
        )
        session.session_quality_score = high_engagement_ratio * 100

        # Generate recommendations
        if avg_engagement < 0.6:
            session.recommendation = (
                "Consider shorter sessions or more interactive content"
            )
        elif avg_engagement > 0.8:
            session.recommendation = "Excellent engagement - ready for advanced content"
        else:
            session.recommendation = "Continue with current approach - good progress"

        # Create summary
        summary = {
            "session_id": session_id,
            "student_id": session.student_id,
            "duration_minutes": duration_minutes,
            "average_engagement": avg_engagement,
            "neuroplasticity_index": session.neuroplasticity_index,
            "adaptations_applied": adaptation_count,
            "quality_score": session.session_quality_score,
            "recommendation": session.recommendation,
            "total_eeg_samples": len(session.eeg_samples),
            "engagement_trend": (
                "improving"
                if len(session.engagement_history) > 5
                and session.engagement_history[-1] > session.engagement_history[0]
                else "stable"
            ),
        }

        logger.info("=" * 80)
        logger.info(f"SESSION COMPLETE: {session_id}")
        logger.info(f"Duration: {duration_minutes:.1f} minutes")
        logger.info(f"Average Engagement: {avg_engagement:.3f}")
        logger.info(f"Neuroplasticity Index: {session.neuroplasticity_index:.3f}")
        logger.info(f"Quality Score: {session.session_quality_score:.1f}%")
        logger.info(f"Adaptations Applied: {adaptation_count}")
        logger.info(f"Recommendation: {session.recommendation}")
        logger.info("=" * 80)

        # Remove from active sessions
        del self.active_sessions[session_id]

        return summary

    async def run_demo_session(self, duration_seconds: int = 60):
        """
        Run a demonstration neuroadaptive learning session

        Args:
            duration_seconds: How long to run the demo
        """
        logger.info("\n" + "=" * 80)
        logger.info("STARTING DEMO NEUROADAPTIVE LEARNING SESSION")
        logger.info("=" * 80 + "\n")

        # Create sample student
        demo_traits = IndividualTraits(
            cognitive_style="visual",
            curiosity=0.85,
            resilience=0.75,
            openness=0.90,
            focus_duration=25.0,
            preferred_complexity="medium",
            learning_pace="moderate",
        )

        # Start session
        session_id = await self.start_learning_session("DEMO-STUDENT-001", demo_traits)

        # Simulate EEG stream with varying engagement
        cycles = duration_seconds // 2  # Process every 2 seconds

        for i in range(cycles):
            # Generate simulated EEG data
            # Engagement varies: starts medium, dips, then recovers
            if i < cycles // 3:
                base_engagement = 0.7  # Good start
            elif i < 2 * cycles // 3:
                base_engagement = 0.5  # Attention drift
            else:
                base_engagement = 0.8  # Recovery after adaptation

            # Add some noise
            noise = random.uniform(-0.1, 0.1)
            simulated_eeg = [
                base_engagement * 30 + noise + random.uniform(-5, 5) for _ in range(256)
            ]

            # Process and adapt
            adaptation = await self.process_eeg_and_adapt(session_id, simulated_eeg)

            # Show adaptation decision
            if adaptation.content_type_adjustment != "maintain":
                logger.info(
                    f"  💡 ADAPTATION: {adaptation.content_type_adjustment.upper()}"
                )

            if adaptation.break_recommendation:
                logger.info(f"  ⏸️  BREAK RECOMMENDED")

            await asyncio.sleep(0.5)  # Small delay for readability

        # End session and get summary
        summary = await self.end_learning_session(session_id)

        logger.info("\n" + "=" * 80)
        logger.info("DEMO SESSION SUMMARY")
        logger.info("=" * 80)
        for key, value in summary.items():
            logger.info(f"{key}: {value}")
        logger.info("=" * 80 + "\n")

        return summary


# ============================================================================
# ADVANCED FEATURES: MIT NeuroChat Approach & Research Extensions
# ============================================================================


@dataclass
class NocturnalOptimizationResult:
    """Results from nocturnal research optimization"""

    timestamp: datetime
    datasets_ingested: int
    parameters_optimized: Dict[str, float]
    performance_improvement: float
    new_k_params: List[float]
    new_eta_params: List[float]
    validation_score: float


@dataclass
class HyperscanningSession:
    """Multi-student brain synchrony analysis"""

    session_id: str
    student_ids: List[str]
    start_time: datetime
    synchrony_matrix: Optional[List[List[float]]] = None
    group_engagement: float = 0.0
    synchrony_score: float = 0.0
    collaborative_recommendations: List[str] = field(default_factory=list)
    teacher_student_synchrony: Dict[str, float] = field(default_factory=dict)


class NocturnalLearningOptimizer:
    """
    Nocturnal Research Mode for Continuous Improvement

    Uses off-peak hours to ingest external EEG datasets and self-optimize
    Implements Equation 7: Self-Calibration for continuous improvement
    """

    def __init__(self, platform: NeuroadaptiveLearningPlatform):
        self.platform = platform
        self.optimization_history: List[NocturnalOptimizationResult] = []
        self.last_optimization = None

        # External dataset sources
        self.dataset_sources = [
            "PhysioNet/eegmmidb",  # Motor movement/imagery
            "OpenNeuro/ds003061",  # Resting state EEG
            "OpenNeuro/ds002778",  # Cognitive workload
            "PhysioNet/sleep-edf",  # Sleep EEG patterns
            "OpenNeuro/ds004504",  # Learning and memory
        ]

        logger.info("🦉 Nocturnal Learning Optimizer initialized")

    def is_low_activity_period(self) -> bool:
        """Check if current time is suitable for nocturnal optimization"""
        current_hour = datetime.now().hour

        # Low activity: 2 AM - 6 AM (typical off-peak)
        # Or configurable based on usage patterns
        return 2 <= current_hour <= 6

    async def optimize_during_sleep(self) -> Optional[NocturnalOptimizationResult]:
        """
        Main nocturnal optimization routine

        Runs during low-activity periods to:
        1. Ingest external EEG datasets
        2. Run self-calibration (Equation 7)
        3. Deploy optimized parameters
        """
        if not self.is_low_activity_period():
            return None

        logger.info("🦉 Starting nocturnal optimization cycle...")

        try:
            # Step 1: Ingest external EEG datasets
            datasets_ingested = await self.ingest_external_eeg_data()

            if datasets_ingested == 0:
                logger.info("No new datasets available for ingestion")
                return None

            # Step 2: Run self-calibration (Equation 7)
            logger.info("Running Equation 7: Self-Calibration...")

            # Parameter ranges for optimization
            k_params_candidates = [
                [0.01, 0.015, 0.012],  # Current production
                [0.008, 0.012, 0.010],  # Conservative
                [0.012, 0.018, 0.015],  # Aggressive
                [0.009, 0.014, 0.011],  # Balanced
            ]

            eta_params_candidates = [
                [0.8, 0.85, 0.82],  # Current production
                [0.75, 0.80, 0.78],  # Lower threshold
                [0.82, 0.87, 0.85],  # Higher threshold
                [0.78, 0.83, 0.81],  # Moderate
            ]

            best_performance = 0.0
            best_k_params = k_params_candidates[0]
            best_eta_params = eta_params_candidates[0]

            # Test each parameter combination
            for k_params in k_params_candidates:
                for eta_params in eta_params_candidates:
                    # Run Equation 7 self-calibration
                    optimized = self._equation7_self_calibration(k_params, eta_params)

                    # Validate performance on ingested data
                    performance = await self._validate_parameters(optimized)

                    if performance > best_performance:
                        best_performance = performance
                        best_k_params = k_params
                        best_eta_params = eta_params

            # Step 3: Deploy optimized parameters if improvement detected
            improvement_threshold = 0.05  # 5% minimum improvement

            if best_performance > improvement_threshold:
                await self.deploy_optimized_parameters(best_k_params, best_eta_params)

                result = NocturnalOptimizationResult(
                    timestamp=datetime.now(),
                    datasets_ingested=datasets_ingested,
                    parameters_optimized={
                        "k_learning_rate": best_k_params[0],
                        "k_memory": best_k_params[1],
                        "k_adaptation": best_k_params[2],
                        "eta_attention": best_eta_params[0],
                        "eta_focus": best_eta_params[1],
                        "eta_resilience": best_eta_params[2],
                    },
                    performance_improvement=best_performance,
                    new_k_params=best_k_params,
                    new_eta_params=best_eta_params,
                    validation_score=best_performance,
                )

                self.optimization_history.append(result)
                self.last_optimization = result

                logger.info(f"✅ Nocturnal optimization complete!")
                logger.info(f"   Performance improvement: {best_performance:.1%}")
                logger.info(f"   Datasets processed: {datasets_ingested}")

                return result
            else:
                logger.info(
                    f"No significant improvement found ({best_performance:.1%} < {improvement_threshold:.1%})"
                )
                return None

        except Exception as e:
            logger.error(f"Nocturnal optimization failed: {e}")
            return None

    async def ingest_external_eeg_data(self) -> int:
        """
        Ingest external EEG datasets for research and optimization

        Sources: PhysioNet, OpenNeuro, and other public repositories
        """
        ingested_count = 0

        for source in self.dataset_sources:
            try:
                logger.info(f"Ingesting dataset: {source}")

                # Simulate dataset ingestion (in production, would download/parse real datasets)
                if source == "PhysioNet/eegmmidb":
                    # Motor movement/imagery data
                    await self._process_motor_imagery_data()
                    ingested_count += 1

                elif source == "OpenNeuro/ds003061":
                    # Resting state EEG
                    await self._process_resting_state_data()
                    ingested_count += 1

                elif source == "OpenNeuro/ds002778":
                    # Cognitive workload data
                    await self._process_cognitive_workload_data()
                    ingested_count += 1

                elif source == "PhysioNet/sleep-edf":
                    # Sleep EEG patterns
                    await self._process_sleep_eeg_data()
                    ingested_count += 1

                elif source == "OpenNeuro/ds004504":
                    # Learning and memory data
                    await self._process_learning_memory_data()
                    ingested_count += 1

                # Small delay to avoid overwhelming system
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.warning(f"Failed to ingest {source}: {e}")
                continue

        logger.info(f"Successfully ingested {ingested_count} datasets")
        return ingested_count

    def _equation7_self_calibration(
        self, k_params: List[float], eta_params: List[float]
    ) -> Dict:
        """
        Equation 7: Self-Calibration for Continuous Improvement

        Calibrates system parameters based on external data validation
        K'(t) = K(t) + α × ∇L(K, η) × β(t)

        where:
        - K: Learning parameters [k_learning, k_memory, k_adaptation]
        - η: Threshold parameters [eta_attention, eta_focus, eta_resilience]
        - ∇L: Loss gradient from external validation
        - β(t): Confidence factor from data quality
        """
        alpha = 0.01  # Learning rate for self-calibration
        beta_confidence = 0.85  # Confidence in external data

        # Simulate loss gradient calculation (in production: real validation)
        loss_gradient = {
            "k_learning": random.uniform(-0.1, 0.1),
            "k_memory": random.uniform(-0.1, 0.1),
            "k_adaptation": random.uniform(-0.1, 0.1),
            "eta_attention": random.uniform(-0.05, 0.05),
            "eta_focus": random.uniform(-0.05, 0.05),
            "eta_resilience": random.uniform(-0.05, 0.05),
        }

        # Apply self-calibration
        optimized = {
            "k_learning": k_params[0]
            + alpha * loss_gradient["k_learning"] * beta_confidence,
            "k_memory": k_params[1]
            + alpha * loss_gradient["k_memory"] * beta_confidence,
            "k_adaptation": k_params[2]
            + alpha * loss_gradient["k_adaptation"] * beta_confidence,
            "eta_attention": eta_params[0]
            + alpha * loss_gradient["eta_attention"] * beta_confidence,
            "eta_focus": eta_params[1]
            + alpha * loss_gradient["eta_focus"] * beta_confidence,
            "eta_resilience": eta_params[2]
            + alpha * loss_gradient["eta_resilience"] * beta_confidence,
        }

        logger.info(f"Equation 7 applied: Self-calibration complete")
        return optimized

    async def _validate_parameters(self, optimized_params: Dict) -> float:
        """
        Validate optimized parameters against ingested datasets

        Returns performance improvement score (0.0 to 1.0)
        """
        # Simulate validation against external datasets
        # In production: would run actual validation tests

        base_performance = 0.75  # Current baseline
        new_performance = base_performance + random.uniform(-0.05, 0.15)

        improvement = max(0.0, new_performance - base_performance)

        return improvement

    async def deploy_optimized_parameters(
        self, k_params: List[float], eta_params: List[float]
    ):
        """
        Deploy optimized parameters to production system
        """
        logger.info("Deploying optimized parameters to production...")

        # Update platform parameters
        self.platform.engagement_thresholds = {
            "critical_low": eta_params[0] - 0.1,  # attention threshold
            "low": eta_params[0],  # attention threshold
            "optimal": eta_params[1],  # focus threshold
            "high": eta_params[1] + 0.1,  # focus threshold + buffer
        }

        # Update adaptation parameters
        self.platform.life_algorithm.adaptation_parameters = {
            "individual_learning_rate": k_params[0],
            "memory_strength": k_params[1],
            "attention_decay": k_params[2],
            "skill_transfer_coefficient": 0.3,
            "neural_plasticity_index": eta_params[2],  # resilience
        }

        logger.info("✅ Optimized parameters deployed successfully")

    # Dataset processing methods (simulated for demo)
    async def _process_motor_imagery_data(self):
        """Process motor movement/imagery EEG data"""
        await asyncio.sleep(0.05)  # Simulate processing time

    async def _process_resting_state_data(self):
        """Process resting state EEG data"""
        await asyncio.sleep(0.05)

    async def _process_cognitive_workload_data(self):
        """Process cognitive workload EEG data"""
        await asyncio.sleep(0.05)

    async def _process_sleep_eeg_data(self):
        """Process sleep EEG patterns"""
        await asyncio.sleep(0.05)

    async def _process_learning_memory_data(self):
        """Process learning and memory EEG data"""
        await asyncio.sleep(0.05)


class MultiStudentHyperscanning:
    """
    Multi-Student Hyperscanning for Group Learning Optimization

    Monitors multiple students simultaneously and analyzes group brain synchrony
    Implements Equation 4: Experience Correlation Matrix
    """

    def __init__(self, platform: NeuroadaptiveLearningPlatform):
        self.platform = platform
        self.active_sessions: Dict[str, HyperscanningSession] = {}

        # Synchrony thresholds
        self.synchrony_thresholds = {
            "low": 0.3,  # Poor group synchrony
            "moderate": 0.5,  # Acceptable synchrony
            "high": 0.7,  # Good synchrony
            "excellent": 0.8,  # Exceptional synchrony
        }

        logger.info("🧠 Multi-Student Hyperscanning initialized")

    async def start_group_session(
        self, session_id: str, student_ids: List[str], teacher_id: Optional[str] = None
    ) -> str:
        """
        Start a hyperscanning session for multiple students

        Args:
            session_id: Unique group session identifier
            student_ids: List of student IDs participating
            teacher_id: Optional teacher ID for teacher-student synchrony

        Returns:
            Group session ID
        """
        session = HyperscanningSession(
            session_id=session_id, student_ids=student_ids, start_time=datetime.now()
        )

        # Initialize synchrony matrix
        n_students = len(student_ids)
        session.synchrony_matrix = [
            [0.0 for _ in range(n_students)] for _ in range(n_students)
        ]

        self.active_sessions[session_id] = session

        logger.info(f"Started hyperscanning session: {session_id}")
        logger.info(f"Students: {len(student_ids)} | Teacher: {teacher_id or 'None'}")

        return session_id

    async def analyze_group_synchrony(
        self, session_id: str, student_eeg_streams: List[List[float]]
    ) -> Dict:
        """
        Analyze inter-student brain synchrony using Equation 4

        Args:
            session_id: Active group session
            student_eeg_streams: List of EEG data arrays (one per student)

        Returns:
            Synchrony analysis results
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Group session {session_id} not found")

        try:
            # Extract engagement levels from EEG data
            engagement_levels = []
            for eeg_data in student_eeg_streams:
                if self.platform.research_library:
                    result = self.platform.research_library.process_raw_eeg(
                        eeg_data, sampling_rate=256
                    )
                    engagement_levels.append(result["engagement"])
                else:
                    # Fallback calculation
                    engagement = sum(eeg_data) / len(eeg_data) / 30.0
                    engagement = max(0.1, min(0.9, engagement))
                    engagement_levels.append(engagement)

            # Calculate group engagement
            session.group_engagement = sum(engagement_levels) / len(engagement_levels)

            # Apply Equation 4: Experience Correlation Matrix
            synchrony_matrix = self._equation4_experience_correlation_matrix(
                experience_vector=engagement_levels,
                trait_changes=[0.1] * len(engagement_levels),  # Placeholder
            )

            session.synchrony_matrix = synchrony_matrix
            # Use numpy if available; otherwise use pure-Python mean
            if _HAS_NUMPY:
                session.synchrony_score = float(np.mean(synchrony_matrix))  # type: ignore[arg-type]
            else:
                session.synchrony_score = _safe_mean(synchrony_matrix)

            # Generate collaborative recommendations
            recommendations = self._generate_collaborative_recommendations(
                session.synchrony_score, engagement_levels
            )
            session.collaborative_recommendations = recommendations

            # Analyze teacher-student synchrony if teacher present
            if len(student_eeg_streams) > len(session.student_ids):
                teacher_eeg = student_eeg_streams[-1]  # Assume last is teacher
                teacher_engagement = engagement_levels[-1]

                # Calculate synchrony with each student
                for i, student_engagement in enumerate(engagement_levels[:-1]):
                    synchrony = self._calculate_pairwise_synchrony(
                        student_engagement, teacher_engagement
                    )
                    session.teacher_student_synchrony[session.student_ids[i]] = (
                        synchrony
                    )

            logger.info(f"Group synchrony analysis complete: {session_id}")
            logger.info(f"Mean synchrony: {session.synchrony_score:.3f}")
            logger.info(f"Group engagement: {session.group_engagement:.3f}")

            return {
                "session_id": session_id,
                "synchrony_score": session.synchrony_score,
                "group_engagement": session.group_engagement,
                "individual_engagement": dict(
                    zip(session.student_ids, engagement_levels)
                ),
                "recommendations": session.collaborative_recommendations,
                "teacher_student_synchrony": session.teacher_student_synchrony,
            }

        except Exception as e:
            logger.error(f"Group synchrony analysis failed: {e}")
            raise

    def _equation4_experience_correlation_matrix(
        self, experience_vector: List[float], trait_changes: List[float]
    ) -> List[List[float]]:
        """
        Equation 4: Experience Correlation Matrix

        Analyzes inter-individual brain synchrony for group learning
        C(i,j) = corr(E_i, E_j) × (1 + ΔT_i × ΔT_j)

        where:
        - E_i, E_j: Experience/engagement vectors for students i,j
        - ΔT_i, ΔT_j: Trait changes over time
        - corr(): Pearson correlation coefficient
        """
        n_students = len(experience_vector)
        correlation_matrix = [
            [0.0 for _ in range(n_students)] for _ in range(n_students)
        ]

        # Calculate pairwise correlations
        for i in range(n_students):
            for j in range(n_students):
                if i == j:
                    correlation_matrix[i][j] = 1.0  # Perfect self-correlation
                else:
                    # Simplified correlation (in production: full Pearson correlation)
                    correlation = self._calculate_correlation(
                        experience_vector[i], experience_vector[j]
                    )

                    # Apply trait change modulation
                    trait_modulation = 1 + (trait_changes[i] * trait_changes[j])

                    correlation_matrix[i][j] = correlation * trait_modulation

        # Ensure matrix is bounded
        for i in range(n_students):
            for j in range(n_students):
                correlation_matrix[i][j] = max(-1.0, min(1.0, correlation_matrix[i][j]))

        logger.info("Equation 4 applied: Experience correlation matrix computed")
        return correlation_matrix

    def _calculate_pairwise_synchrony(
        self, engagement1: float, engagement2: float
    ) -> float:
        """Calculate synchrony between two individuals"""
        # Simple synchrony measure (in production: more sophisticated analysis)
        synchrony = 1.0 - abs(engagement1 - engagement2)
        return max(0.0, min(1.0, synchrony))

    def _calculate_correlation(self, x: float, y: float) -> float:
        """Calculate simple correlation coefficient"""
        # Simplified correlation for demo (in production: use proper statistical correlation)
        return 1.0 - abs(x - y)  # Simple inverse distance correlation

    def _generate_collaborative_recommendations(
        self, synchrony_score: float, engagement_levels: List[float]
    ) -> List[str]:
        """
        Generate recommendations based on group synchrony analysis
        """
        recommendations = []

        if synchrony_score < self.synchrony_thresholds["low"]:
            recommendations.append(
                "🔄 Group synchrony is low - suggest collaborative activities"
            )
            recommendations.append(
                "👥 Pair students with complementary engagement levels"
            )
            recommendations.append("🎯 Introduce group problem-solving exercises")

        elif synchrony_score < self.synchrony_thresholds["moderate"]:
            recommendations.append("📈 Moderate synchrony - encourage peer teaching")
            recommendations.append("💬 Add discussion-based activities")

        elif synchrony_score >= self.synchrony_thresholds["high"]:
            recommendations.append(
                "✅ Excellent group synchrony - maintain current approach"
            )
            recommendations.append("🚀 Consider advanced collaborative challenges")

        # Individual engagement recommendations
        low_engagement_count = sum(1 for e in engagement_levels if e < 0.6)
        if low_engagement_count > len(engagement_levels) * 0.3:
            recommendations.append(
                "⚠️ Multiple students showing low engagement - consider break or content adjustment"
            )

        return recommendations

    async def end_group_session(self, session_id: str) -> Dict:
        """
        Complete group hyperscanning session

        Returns comprehensive group analysis
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Group session {session_id} not found")

        duration_minutes = (datetime.now() - session.start_time).total_seconds() / 60

        summary = {
            "session_id": session_id,
            "duration_minutes": duration_minutes,
            "students_count": len(session.student_ids),
            "final_synchrony_score": session.synchrony_score,
            "average_group_engagement": session.group_engagement,
            "recommendations": session.collaborative_recommendations,
            "teacher_student_synchrony": session.teacher_student_synchrony,
            "synchrony_trend": "stable",  # Would track over time in production
            "learning_outcome_prediction": self._predict_learning_outcomes(session),
        }

        logger.info("=" * 80)
        logger.info(f"GROUP SESSION COMPLETE: {session_id}")
        logger.info(f"Duration: {duration_minutes:.1f} minutes")
        logger.info(f"Students: {len(session.student_ids)}")
        logger.info(f"Final Synchrony: {session.synchrony_score:.3f}")
        logger.info(f"Average Engagement: {session.group_engagement:.3f}")
        logger.info("=" * 80)

        # Remove from active sessions
        del self.active_sessions[session_id]

        return summary

    def _predict_learning_outcomes(self, session: HyperscanningSession) -> str:
        """Predict learning outcomes based on synchrony analysis"""
        synchrony = session.synchrony_score
        engagement = session.group_engagement

        if synchrony > 0.7 and engagement > 0.75:
            return "Excellent - High collaborative learning potential"
        elif synchrony > 0.5 and engagement > 0.6:
            return "Good - Effective group learning"
        elif synchrony > 0.3 or engagement > 0.5:
            return "Moderate - Some collaborative benefits"
        else:
            return "Limited - Consider individual-focused activities"


# Enhanced NeuroChat-style adaptation (extends existing platform)
class EnhancedNeuroChatAdapter:
    """
    Enhanced NeuroChat-style conversational adaptation

    Builds on existing platform with advanced conversational strategies
    """

    def __init__(self, platform: NeuroadaptiveLearningPlatform):
        self.platform = platform
        self.conversation_history: List[Dict] = []

        # Conversational adaptation strategies
        self.strategies = {
            "simplify": {
                "complexity_reduction": 0.3,
                "interaction_increase": 2.0,
                "pacing_slow": 0.7,
                "examples_add": True,
            },
            "intensify": {
                "complexity_increase": 0.2,
                "challenge_add": True,
                "pacing_fast": 1.3,
                "depth_increase": True,
            },
            "maintain": {"stability_focus": True},
            "redirect": {
                "topic_shift": True,
                "engagement_boost": True,
                "question_frequency": 3.0,
            },
        }

        logger.info("💬 Enhanced NeuroChat Adapter initialized")

    async def adapt_conversational_strategy(
        self, session_id: str, eeg_data: List[float], current_topic_complexity: float
    ) -> Dict:
        """
        Adapt conversational strategy based on neural state

        Matches MIT's NeuroChat approach: "when engagement dips, the system
        modifies its conversational strategy, adjusting response complexity,
        pacing, and level of interactivity"
        """
        session = self.platform.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Get current neural state
        if self.platform.research_library:
            neural_state = self.platform.research_library.process_raw_eeg(
                eeg_data, sampling_rate=256
            )
            engagement = neural_state["engagement"]
            focus = neural_state["focus"]
            stress = neural_state["stress"]
        else:
            engagement = sum(eeg_data) / len(eeg_data) / 30.0
            engagement = max(0.1, min(0.9, engagement))
            focus = engagement * 0.85
            stress = 0.3

        # Determine adaptation strategy
        strategy_name = self._select_conversational_strategy(
            engagement, focus, stress, current_topic_complexity
        )

        strategy = self.strategies[strategy_name]

        # Apply conversational adaptations
        adaptations = {
            "strategy": strategy_name,
            "response_complexity": self._calculate_response_complexity(
                current_topic_complexity, strategy
            ),
            "pacing_modifier": strategy.get(
                "pacing_slow", strategy.get("pacing_fast", 1.0)
            ),
            "interaction_level": strategy.get("interaction_increase", 1.0),
            "question_frequency": strategy.get("question_frequency", 1.0),
            "examples_include": strategy.get("examples_add", False),
            "challenge_elements": strategy.get("challenge_add", False),
            "topic_shift_suggested": strategy.get("topic_shift", False),
            "engagement_boost_techniques": strategy.get("engagement_boost", False),
        }

        # Store in conversation history
        self.conversation_history.append(
            {
                "timestamp": datetime.now(),
                "engagement": engagement,
                "strategy": strategy_name,
                "adaptations": adaptations,
            }
        )

        logger.info(f"💬 NeuroChat adaptation: {strategy_name}")
        logger.info(f"   Engagement: {engagement:.3f} | Strategy: {strategy_name}")

        return adaptations

    def _select_conversational_strategy(
        self, engagement: float, focus: float, stress: float, topic_complexity: float
    ) -> str:
        """Select optimal conversational strategy"""

        # Critical disengagement
        if engagement < 0.4:
            return "redirect"

        # Low engagement
        elif engagement < 0.6:
            if stress > 0.6:
                return "simplify"  # High stress + low engagement = simplify
            else:
                return "redirect"  # Low stress = try redirect first

        # High engagement, low focus
        elif engagement > 0.75 and focus < 0.6:
            return "redirect"  # Need to recapture attention

        # High engagement and focus
        elif engagement > 0.8 and focus > 0.7:
            if topic_complexity < 0.7:  # Room to increase challenge
                return "intensify"
            else:
                return "maintain"

        # Moderate engagement
        else:
            return "maintain"

    def _calculate_response_complexity(
        self, current_complexity: float, strategy: Dict
    ) -> float:
        """Calculate new response complexity"""
        if "complexity_reduction" in strategy:
            new_complexity = current_complexity * (1 - strategy["complexity_reduction"])
        elif "complexity_increase" in strategy:
            new_complexity = current_complexity * (1 + strategy["complexity_increase"])
        else:
            new_complexity = current_complexity

        return max(0.1, min(1.0, new_complexity))


async def main():
    """Enhanced main function with advanced features"""

    print(
        """
================================================================================
                                                                               
   L.I.F.E. NEUROADAPTIVE LEARNING PLATFORM                        
   Advanced Features: NeuroChat + Nocturnal + Hyperscanning       
                                                                               
   Real-Time EEG-Based Personalized Learning                      
   Copyright 2025 - Sergio Paya Borrull                           
                                                                               
================================================================================
    """
    )

    # Initialize platform
    platform = NeuroadaptiveLearningPlatform()

    # Initialize advanced features
    nocturnal_optimizer = NocturnalLearningOptimizer(platform)
    hyperscanning = MultiStudentHyperscanning(platform)
    neurochat_adapter = EnhancedNeuroChatAdapter(platform)

    print("\n[INFO] Advanced Features Initialized:")
    print("   [OK] Nocturnal Research Mode")
    print("   [OK] Multi-Student Hyperscanning")
    print("   [OK] Enhanced NeuroChat Adaptation")

    # Run demonstration session
    print("\n[DEMO] Running 60-second demonstration of neuroadaptive learning...\n")
    await platform.run_demo_session(duration_seconds=60)

    # Demonstrate nocturnal optimization (simulated)
    print("\n[OPT] Testing Nocturnal Optimization...")
    if nocturnal_optimizer.is_low_activity_period():
        result = await nocturnal_optimizer.optimize_during_sleep()
        if result:
            print(
                f"   [SUCCESS] Optimization complete: {result.performance_improvement:.1%} improvement"
            )
        else:
            print(
                "   [INFO] No optimization needed or low-activity period not detected"
            )

    # Demonstrate hyperscanning (simulated)
    print("\n[HYSCAN] Testing Multi-Student Hyperscanning...")
    group_session_id = await hyperscanning.start_group_session(
        "DEMO-GROUP-001", ["STUDENT-001", "STUDENT-002", "STUDENT-003"]
    )

    # Simulate group EEG data
    group_eeg_data = [
        [0.7 + random.uniform(-0.1, 0.1) for _ in range(256)],  # Student 1
        [0.6 + random.uniform(-0.1, 0.1) for _ in range(256)],  # Student 2
        [0.8 + random.uniform(-0.1, 0.1) for _ in range(256)],  # Student 3
    ]

    synchrony_result = await hyperscanning.analyze_group_synchrony(
        group_session_id, group_eeg_data
    )

    print(f"   [RESULT] Group synchrony: {synchrony_result['synchrony_score']:.3f}")
    print(f"   [RESULT] Group engagement: {synchrony_result['group_engagement']:.3f}")

    group_summary = await hyperscanning.end_group_session(group_session_id)
    print(
        f"   [RESULT] Session complete: {group_summary['learning_outcome_prediction']}"
    )

    # Demonstrate NeuroChat adaptation
    print("\n[CHAT] Testing Enhanced NeuroChat Adaptation...")
    session_id = await platform.start_learning_session(
        "NEUROCHAT-DEMO",
        IndividualTraits(
            cognitive_style="visual",
            curiosity=0.8,
            resilience=0.7,
            openness=0.9,
            focus_duration=25.0,
            preferred_complexity="medium",
            learning_pace="moderate",
        ),
    )

    # Simulate conversational adaptation
    demo_eeg = [0.5 + random.uniform(-0.1, 0.1) for _ in range(256)]  # Low engagement
    chat_adaptation = await neurochat_adapter.adapt_conversational_strategy(
        session_id, demo_eeg, current_topic_complexity=0.6
    )

    print(f"   [ADAPT] Strategy: {chat_adaptation['strategy']}")
    print(
        f"   [ADAPT] Response complexity: {chat_adaptation['response_complexity']:.2f}"
    )
    print(f"   [ADAPT] Pacing modifier: {chat_adaptation['pacing_modifier']:.2f}")

    await platform.end_learning_session(session_id)

    print("\n[SUCCESS] All advanced features demonstrated!")
    print(f"\nLog file: {os.path.join(LOG_DIR, 'neuroadaptive_learning_*.log')}")


if __name__ == "__main__":
    asyncio.run(main())
