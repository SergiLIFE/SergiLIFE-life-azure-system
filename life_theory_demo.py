"""
L.I.F.E. Theory Demonstration - Learning Individually from Experience
Copyright 2025 - Sergio Paya Borrull

Interactive demonstration of the L.I.F.E. (Learning Individually from Experience)
theory and algorithm implementation. This demo showcases the core principles
of neuroadaptive learning through real-time EEG processing and adaptive
algorithms.

The demonstration includes:
- Real-time EEG signal processing simulation
- Adaptive learning algorithm visualization
- Performance metrics and KPI tracking
- Interactive learning scenarios
"""

import asyncio
import json
import logging
import random
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class EEGMetrics:
    """EEG signal metrics"""

    timestamp: datetime
    alpha_power: float
    beta_power: float
    theta_power: float
    delta_power: float
    signal_quality: float
    attention_level: float
    cognitive_load: float


@dataclass
class LearningOutcome:
    """Learning outcome metrics"""

    timestamp: datetime
    learning_stage: str
    performance_score: float
    adaptation_rate: float
    knowledge_retention: float
    neural_efficiency: float
    cognitive_gain: float


@dataclass
class LIFEDemonstration:
    """L.I.F.E. theory demonstration session"""

    session_id: str
    start_time: datetime
    current_stage: str
    total_learning_time: float
    cumulative_performance: float
    adaptation_events: int
    neural_states_visited: List[str]


class LIFEDemonstrationEngine:
    """Engine for running L.I.F.E. theory demonstrations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Demonstration state
        self.current_demo: Optional[LIFEDemonstration] = None
        self.eeg_history: List[EEGMetrics] = []
        self.learning_history: List[LearningOutcome] = []

        # L.I.F.E. algorithm parameters
        self.learning_stages = [
            "exploration",
            "pattern_recognition",
            "skill_acquisition",
            "mastery",
            "innovation",
        ]

        self.neural_states = [
            "curious",
            "focused",
            "challenged",
            "overwhelmed",
            "confident",
            "frustrated",
            "enlightened",
        ]

    async def start_demonstration(
        self, scenario: str = "adaptive_learning"
    ) -> LIFEDemonstration:
        """Start a new L.I.F.E. demonstration session"""
        session_id = f"life_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.current_demo = LIFEDemonstration(
            session_id=session_id,
            start_time=datetime.now(),
            current_stage="exploration",
            total_learning_time=0.0,
            cumulative_performance=0.0,
            adaptation_events=0,
            neural_states_visited=[],
        )

        self.logger.info(f"Started L.I.F.E. demonstration: {session_id}")
        return self.current_demo

    async def simulate_eeg_stream(self, duration_seconds: int = 60) -> List[EEGMetrics]:
        """Simulate real-time EEG data stream"""
        eeg_data = []
        start_time = datetime.now()

        self.logger.info(f"Starting EEG simulation for {duration_seconds} seconds...")

        for i in range(duration_seconds):
            # Simulate realistic EEG patterns
            timestamp = start_time + timedelta(seconds=i)

            # Base EEG patterns with realistic variations
            alpha_base = 25 + random.uniform(-5, 5)  # Relaxation
            beta_base = 20 + random.uniform(-3, 3)  # Active thinking
            theta_base = 15 + random.uniform(-2, 2)  # Memory/dreaming
            delta_base = 10 + random.uniform(-1, 1)  # Deep sleep

            # Add learning-induced variations
            learning_factor = min(1.0, i / 30)  # Learning progression
            alpha_power = alpha_base * (1 + learning_factor * 0.3)
            beta_power = beta_base * (1 + learning_factor * 0.5)
            theta_power = theta_base * (1 + learning_factor * 0.2)
            delta_power = delta_base * (1 - learning_factor * 0.1)

            # Calculate derived metrics
            total_power = alpha_power + beta_power + theta_power + delta_power
            signal_quality = 0.85 + random.uniform(-0.1, 0.1)  # 85-95% quality

            # Attention level based on alpha/beta ratio
            attention_level = min(1.0, beta_power / max(alpha_power, 0.1))

            # Cognitive load based on beta/theta ratio
            cognitive_load = min(1.0, beta_power / max(theta_power, 0.1))

            eeg = EEGMetrics(
                timestamp=timestamp,
                alpha_power=round(alpha_power, 2),
                beta_power=round(beta_power, 2),
                theta_power=round(theta_power, 2),
                delta_power=round(delta_power, 2),
                signal_quality=round(signal_quality, 3),
                attention_level=round(attention_level, 3),
                cognitive_load=round(cognitive_load, 3),
            )

            eeg_data.append(eeg)
            self.eeg_history.append(eeg)

            # Small delay to simulate real-time streaming
            await asyncio.sleep(0.1)

        self.logger.info(f"EEG simulation completed: {len(eeg_data)} data points")
        return eeg_data

    async def run_adaptive_learning_cycle(
        self, eeg_data: List[EEGMetrics]
    ) -> List[LearningOutcome]:
        """Run the adaptive learning cycle based on EEG data"""
        learning_outcomes = []

        current_stage_index = 0
        cumulative_performance = 0.0
        adaptation_events = 0

        self.logger.info("Starting adaptive learning cycle...")

        for i, eeg in enumerate(eeg_data):
            # Determine current learning stage based on progress
            progress_factor = min(1.0, i / len(eeg_data))
            stage_index = min(
                len(self.learning_stages) - 1,
                int(progress_factor * len(self.learning_stages)),
            )
            current_stage = self.learning_stages[stage_index]

            # Calculate performance based on attention and cognitive load
            base_performance = (
                eeg.attention_level * 0.6 + (1 - eeg.cognitive_load) * 0.4
            )
            performance_score = base_performance * (0.7 + progress_factor * 0.3)

            # Adaptation rate based on neural state changes
            adaptation_rate = 0.1 + (eeg.signal_quality - 0.8) * 0.5

            # Knowledge retention improves with learning progress
            knowledge_retention = 0.6 + progress_factor * 0.4

            # Neural efficiency based on power distribution
            total_power = (
                eeg.alpha_power + eeg.beta_power + eeg.theta_power + eeg.delta_power
            )
            neural_efficiency = min(1.0, total_power / 100)

            # Cognitive gain based on learning stage advancement
            cognitive_gain = performance_score * (1 + stage_index * 0.2)

            # Check for adaptation events (significant changes)
            if (
                i > 0
                and abs(performance_score - cumulative_performance / max(i, 1)) > 0.2
            ):
                adaptation_events += 1

            cumulative_performance += performance_score

            outcome = LearningOutcome(
                timestamp=eeg.timestamp,
                learning_stage=current_stage,
                performance_score=round(performance_score, 3),
                adaptation_rate=round(adaptation_rate, 3),
                knowledge_retention=round(knowledge_retention, 3),
                neural_efficiency=round(neural_efficiency, 3),
                cognitive_gain=round(cognitive_gain, 3),
            )

            learning_outcomes.append(outcome)
            self.learning_history.append(outcome)

            # Update demonstration state
            if self.current_demo:
                self.current_demo.current_stage = current_stage
                self.current_demo.total_learning_time = (
                    datetime.now() - self.current_demo.start_time
                ).total_seconds()
                self.current_demo.cumulative_performance = cumulative_performance / (
                    i + 1
                )
                self.current_demo.adaptation_events = adaptation_events

                # Track neural states
                neural_state = self._determine_neural_state(eeg)
                if neural_state not in self.current_demo.neural_states_visited:
                    self.current_demo.neural_states_visited.append(neural_state)

        self.logger.info(
            f"Adaptive learning cycle completed: {len(learning_outcomes)} outcomes"
        )
        return learning_outcomes

    def _determine_neural_state(self, eeg: EEGMetrics) -> str:
        """Determine neural state based on EEG metrics"""
        if eeg.attention_level > 0.8 and eeg.cognitive_load < 0.3:
            return "focused"
        elif eeg.alpha_power > eeg.beta_power and eeg.cognitive_load < 0.4:
            return "curious"
        elif eeg.beta_power > 30 and eeg.cognitive_load > 0.6:
            return "challenged"
        elif eeg.cognitive_load > 0.8:
            return "overwhelmed"
        elif eeg.attention_level > 0.7 and eeg.signal_quality > 0.9:
            return "confident"
        elif eeg.theta_power > eeg.alpha_power:
            return "frustrated"
        else:
            return "enlightened"

    async def run_interactive_scenario(
        self, scenario_type: str = "skill_acquisition"
    ) -> Dict[str, Any]:
        """Run an interactive learning scenario"""
        self.logger.info(f"Starting interactive scenario: {scenario_type}")

        # Start demonstration
        demo = await self.start_demonstration(scenario_type)

        # Simulate EEG stream
        eeg_data = await self.simulate_eeg_stream(duration_seconds=30)

        # Run learning cycle
        learning_outcomes = await self.run_adaptive_learning_cycle(eeg_data)

        # Generate scenario results
        results = {
            "scenario": scenario_type,
            "demonstration": asdict(demo),
            "eeg_metrics_count": len(eeg_data),
            "learning_outcomes_count": len(learning_outcomes),
            "final_performance": (
                learning_outcomes[-1].performance_score if learning_outcomes else 0
            ),
            "total_adaptation_events": demo.adaptation_events,
            "neural_states_explored": len(demo.neural_states_visited),
            "learning_efficiency": self._calculate_learning_efficiency(
                learning_outcomes
            ),
        }

        # Export results
        await self._export_scenario_results(results)

        return results

    def _calculate_learning_efficiency(self, outcomes: List[LearningOutcome]) -> float:
        """Calculate overall learning efficiency"""
        if not outcomes:
            return 0.0

        # Efficiency based on performance improvement over time
        initial_performance = outcomes[0].performance_score
        final_performance = outcomes[-1].performance_score
        improvement_rate = (final_performance - initial_performance) / max(
            len(outcomes), 1
        )

        # Factor in adaptation events (more adaptations = more efficient learning)
        adaptation_factor = min(1.0, len(outcomes) / 100)  # Normalize

        efficiency = (
            final_performance * 0.7 + improvement_rate * 0.2 + adaptation_factor * 0.1
        )
        return max(0.0, min(1.0, efficiency))

    async def _export_scenario_results(self, results: Dict[str, Any]):
        """Export scenario results to file"""
        filename = f"life_demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.info(f"Scenario results exported to {filename}")

    async def demonstrate_life_principles(self) -> Dict[str, Any]:
        """Demonstrate core L.I.F.E. principles through multiple scenarios"""
        self.logger.info("Starting comprehensive L.I.F.E. principles demonstration...")

        scenarios = [
            "exploratory_learning",
            "skill_acquisition",
            "problem_solving",
            "creative_thinking",
            "adaptive_reasoning",
        ]

        all_results = {}

        for scenario in scenarios:
            self.logger.info(f"Running scenario: {scenario}")
            result = await self.run_interactive_scenario(scenario)
            all_results[scenario] = result

            # Brief pause between scenarios
            await asyncio.sleep(1)

        # Aggregate results
        summary = {
            "demonstration_type": "comprehensive_life_principles",
            "scenarios_run": len(scenarios),
            "total_eeg_data_points": sum(
                r["eeg_metrics_count"] for r in all_results.values()
            ),
            "total_learning_outcomes": sum(
                r["learning_outcomes_count"] for r in all_results.values()
            ),
            "average_final_performance": np.mean(
                [r["final_performance"] for r in all_results.values()]
            ),
            "total_adaptation_events": sum(
                r["total_adaptation_events"] for r in all_results.values()
            ),
            "average_learning_efficiency": np.mean(
                [r["learning_efficiency"] for r in all_results.values()]
            ),
            "scenario_results": all_results,
            "life_principles_demonstrated": [
                "Individual Learning Pace Adaptation",
                "Experience-Based Knowledge Building",
                "Neural State-Aware Teaching",
                "Real-time Performance Optimization",
                "Cognitive Load Management",
            ],
        }

        # Export comprehensive results
        filename = (
            f"life_principles_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(filename, "w") as f:
            json.dump(summary, f, indent=2, default=str)

        self.logger.info(f"Comprehensive L.I.F.E. principles demonstration completed")
        return summary

    def get_demonstration_history(self) -> Dict[str, Any]:
        """Get history of all demonstration data"""
        return {
            "eeg_history": [
                asdict(eeg) for eeg in self.eeg_history[-100:]
            ],  # Last 100 readings
            "learning_history": [
                asdict(outcome) for outcome in self.learning_history[-50:]
            ],  # Last 50 outcomes
            "current_demo": asdict(self.current_demo) if self.current_demo else None,
        }


async def main():
    """Main demonstration function"""
    print("L.I.F.E. Theory Demonstration")
    print("Learning Individually from Experience")
    print("=" * 75)
    print("Copyright 2025 - Sergio Paya Borrull")
    print()

    engine = LIFEDemonstrationEngine()

    try:
        # Run comprehensive demonstration
        print("Running comprehensive L.I.F.E. principles demonstration...")
        results = await engine.demonstrate_life_principles()

        print("\nDemonstration Summary:")
        print(f"   Scenarios Completed: {results['scenarios_run']}")
        print(f"   EEG Data Points: {results['total_eeg_data_points']}")
        print(f"   Learning Outcomes: {results['total_learning_outcomes']}")
        print(f"   Average Performance: {results['average_final_performance']:.3f}")
        print(f"   Adaptation Events: {results['total_adaptation_events']}")
        print(f"   Learning Efficiency: {results['average_learning_efficiency']:.3f}")

        print("\nL.I.F.E. Principles Demonstrated:")
        for principle in results["life_principles_demonstrated"]:
            print(f"   - {principle}")

        print("\nResults exported to JSON files")
        print("L.I.F.E. Theory demonstration completed successfully!")

    except Exception as e:
        print(f"Demonstration failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
