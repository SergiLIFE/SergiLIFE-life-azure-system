#!/usr/bin/env python3
"""
L.I.F.E Platform - Experience Collection Pipeline
Converts platform events into L.I.F.E experiences for continuous learning

This module implements Phase 2 of the L.I.F.E integration, creating a pipeline
that captures platform interactions and converts them into learning experiences
for autonomous optimization and self-improvement.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List
from uuid import uuid4

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ExperienceTraits:
    """Traits that define the characteristics of an experience"""

    novelty: float  # 0.0 to 1.0 - How new/unique this experience is
    emotional_salience: float  # 0.0 to 1.0 - Emotional impact/importance
    complexity: float  # 0.0 to 1.0 - Cognitive complexity required
    relevance: float  # 0.0 to 1.0 - Relevance to current goals
    outcome_value: float = 0.5  # Success/failure value of the experience

    def calculate_learning_potential(self) -> float:
        """Calculate the learning potential of this experience"""
        # Higher novelty, complexity, and relevance increase learning potential
        # Emotional salience acts as a multiplier
        base_potential = (
            self.novelty * 0.4 + self.complexity * 0.3 + self.relevance * 0.3
        )
        emotional_multiplier = 1.0 + (self.emotional_salience * 0.5)
        return min(base_potential * emotional_multiplier, 1.0)


@dataclass
class IndividualTraits:
    """Individual characteristics that affect learning"""

    cognitive_style: str  # "active", "reflective", "pragmatic", "theorist"
    curiosity: float  # 0.0 to 1.0 - Drive to explore and learn
    resilience: float  # 0.0 to 1.0 - Ability to recover from failures
    openness: float  # 0.0 to 1.0 - Willingness to try new approaches
    learning_preference: str = "experiential"  # Learning style preference


@dataclass
class LearningOutcome:
    """Result of processing an experience through L.I.F.E algorithm"""

    experience_id: str
    learning_gain: float  # Amount learned from this experience
    confidence: float  # Confidence in the learning
    applied_optimizations: List[str]
    performance_improvement: float
    timestamp: datetime
    next_actions: List[str]


class LIFEEntity:
    """L.I.F.E learning entity with autonomous optimization capabilities"""

    def __init__(self, traits: IndividualTraits):
        self.traits = traits
        self.experience_buffer: List[Dict[str, Any]] = []
        self.research_buffer: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.performance_history: List[float] = []
        self.is_active = False

    async def process_experience(self, experience: ExperienceTraits) -> LearningOutcome:
        """Process an experience and generate learning outcomes"""
        experience_id = str(uuid4())

        try:
            # Calculate base learning gain based on experience traits and individual traits
            learning_potential = experience.calculate_learning_potential()

            # Individual traits modify learning effectiveness
            trait_multiplier = self._calculate_trait_multiplier(experience)

            # Final learning gain
            learning_gain = learning_potential * trait_multiplier

            # Determine optimizations to apply based on experience type
            optimizations = self._determine_optimizations(experience)

            # Calculate expected performance improvement
            performance_improvement = (
                learning_gain * 0.15
            )  # Conservative improvement estimate

            # Generate next actions based on learning
            next_actions = self._generate_next_actions(experience, learning_gain)

            # Create learning outcome
            outcome = LearningOutcome(
                experience_id=experience_id,
                learning_gain=learning_gain,
                confidence=min(learning_gain * self.traits.curiosity, 1.0),
                applied_optimizations=optimizations,
                performance_improvement=performance_improvement,
                timestamp=datetime.now(),
                next_actions=next_actions,
            )

            # Store in knowledge base
            self.knowledge_base[experience_id] = {
                "experience": asdict(experience),
                "outcome": asdict(outcome),
                "context": {"processing_time": datetime.now()},
            }

            logger.info(
                f"🧠 Experience processed: {learning_gain:.4f} learning gain, "
                f"{len(optimizations)} optimizations identified"
            )

            return outcome

        except Exception as e:
            logger.error(f"❌ Experience processing error: {e}")
            return LearningOutcome(
                experience_id=experience_id,
                learning_gain=0.0,
                confidence=0.0,
                applied_optimizations=[],
                performance_improvement=0.0,
                timestamp=datetime.now(),
                next_actions=["retry_processing"],
            )

    def _calculate_trait_multiplier(self, experience: ExperienceTraits) -> float:
        """Calculate how individual traits affect learning from this experience"""
        # Curiosity enhances learning from novel experiences
        curiosity_bonus = self.traits.curiosity * experience.novelty * 0.3

        # Resilience helps learn from failures (low outcome_value)
        resilience_bonus = 0.0
        if experience.outcome_value < 0.5:
            resilience_bonus = (
                self.traits.resilience * (1.0 - experience.outcome_value) * 0.2
            )

        # Openness enhances learning from complex experiences
        openness_bonus = self.traits.openness * experience.complexity * 0.2

        base_multiplier = 0.7  # Base learning effectiveness
        return base_multiplier + curiosity_bonus + resilience_bonus + openness_bonus

    def _determine_optimizations(self, experience: ExperienceTraits) -> List[str]:
        """Determine what optimizations to apply based on experience"""
        optimizations = []

        # High novelty suggests need for exploration
        if experience.novelty > 0.7:
            optimizations.extend(["explore_alternatives", "expand_knowledge_base"])

        # High complexity suggests need for simplification
        if experience.complexity > 0.8:
            optimizations.extend(["simplify_process", "break_into_steps"])

        # Low outcome value (failure) suggests need for improvement
        if experience.outcome_value < 0.4:
            optimizations.extend(["analyze_failure_patterns", "adjust_strategy"])

        # High relevance suggests priority optimization
        if experience.relevance > 0.8:
            optimizations.extend(["prioritize_learning", "immediate_application"])

        return optimizations

    def _generate_next_actions(
        self, experience: ExperienceTraits, learning_gain: float
    ) -> List[str]:
        """Generate next actions based on learning outcome"""
        actions = []

        # High learning gain suggests confidence to act
        if learning_gain > 0.7:
            actions.extend(["apply_immediately", "share_learning"])

        # Medium learning gain suggests need for validation
        elif learning_gain > 0.4:
            actions.extend(["validate_learning", "gradual_application"])

        # Low learning gain suggests need for more experience
        else:
            actions.extend(["gather_more_data", "seek_alternative_approach"])

        # Always include reflection for high-salience experiences
        if experience.emotional_salience > 0.6:
            actions.append("reflect_on_experience")

        return actions

    async def optimize_learning(self) -> Dict[str, Any]:
        """Optimize learning strategy based on accumulated experiences"""
        logger.info("🔧 Optimizing learning strategy...")

        try:
            if len(self.research_buffer) < 10:
                logger.info(
                    "📊 Insufficient data for optimization, continuing collection"
                )
                return {
                    "status": "collecting_data",
                    "buffer_size": len(self.research_buffer),
                }

            # Analyze patterns in research buffer
            patterns = self._analyze_experience_patterns()

            # Optimize learning parameters based on patterns
            optimizations = self._optimize_parameters(patterns)

            # Clear processed experiences from buffer
            processed_count = len(self.research_buffer)
            self.research_buffer.clear()

            logger.info(
                f"✅ Learning optimization complete: {processed_count} experiences processed"
            )

            return {
                "status": "optimized",
                "processed_experiences": processed_count,
                "patterns_found": len(patterns),
                "optimizations_applied": len(optimizations),
                "optimization_details": optimizations,
            }

        except Exception as e:
            logger.error(f"❌ Learning optimization error: {e}")
            return {"status": "error", "error": str(e)}

    def _analyze_experience_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in accumulated experiences"""
        patterns = {
            "high_learning_contexts": [],
            "low_learning_contexts": [],
            "successful_optimizations": [],
            "failed_optimizations": [],
        }

        for entry in self.research_buffer:
            gain = entry.get("gain", 0)
            exp = entry.get("exp", {})

            # Identify high-learning contexts
            if gain > 0.7:
                patterns["high_learning_contexts"].append(
                    {
                        "novelty": exp.get("novelty", 0),
                        "complexity": exp.get("complexity", 0),
                        "relevance": exp.get("relevance", 0),
                    }
                )

            # Identify low-learning contexts
            elif gain < 0.3:
                patterns["low_learning_contexts"].append(
                    {
                        "novelty": exp.get("novelty", 0),
                        "complexity": exp.get("complexity", 0),
                        "relevance": exp.get("relevance", 0),
                    }
                )

        return patterns

    def _optimize_parameters(self, patterns: Dict[str, Any]) -> List[str]:
        """Optimize learning parameters based on identified patterns"""
        optimizations = []

        # If high-learning contexts show consistent patterns, enhance them
        if patterns["high_learning_contexts"]:
            avg_novelty = sum(
                ctx["novelty"] for ctx in patterns["high_learning_contexts"]
            ) / len(patterns["high_learning_contexts"])
            if avg_novelty > 0.7:
                optimizations.append("increase_novelty_seeking")

        # If low-learning contexts show problems, address them
        if patterns["low_learning_contexts"]:
            avg_complexity = sum(
                ctx["complexity"] for ctx in patterns["low_learning_contexts"]
            ) / len(patterns["low_learning_contexts"])
            if avg_complexity > 0.8:
                optimizations.append("reduce_complexity_threshold")

        return optimizations

    def start(self) -> None:
        """Start the L.I.F.E entity background processes"""
        self.is_active = True
        logger.info("🧠 L.I.F.E Entity activated for continuous learning")

    def stop(self) -> None:
        """Stop the L.I.F.E entity background processes"""
        self.is_active = False
        logger.info("🛑 L.I.F.E Entity deactivated")


class PlatformExperienceCollector:
    """Collects platform interactions and converts them to L.I.F.E experiences"""

    def __init__(self, cosmos_client=None):
        self.cosmos_client = cosmos_client
        self.life_entity = LIFEEntity(
            traits=IndividualTraits(
                cognitive_style="active",
                curiosity=0.8,
                resilience=0.7,
                openness=0.9,
                learning_preference="experiential",
            )
        )
        self.experience_queue: List[Dict[str, Any]] = []
        self.processing_stats = {
            "total_experiences": 0,
            "successful_processing": 0,
            "learning_gain_total": 0.0,
            "optimizations_applied": 0,
        }

    async def start_collection(self) -> None:
        """Start the experience collection and processing pipeline"""
        self.life_entity.start()
        logger.info("📡 Platform Experience Collector started")

        # Start background processing
        processing_tasks = [
            asyncio.create_task(self._process_experience_queue()),
            asyncio.create_task(self._periodic_optimization()),
            asyncio.create_task(self._metrics_reporting()),
        ]

        try:
            await asyncio.gather(*processing_tasks)
        except Exception as e:
            logger.error(f"❌ Experience collection error: {e}")
        finally:
            self.life_entity.stop()

    async def collect_platform_interaction(self, event_data: Dict[str, Any]) -> None:
        """Convert platform events into L.I.F.E experiences and process them"""
        try:
            # Calculate experience characteristics based on event data
            experience = ExperienceTraits(
                novelty=self._calculate_novelty(event_data),
                emotional_salience=self._calculate_salience(event_data),
                complexity=self._calculate_complexity(event_data),
                relevance=1.0 if event_data.get("critical", False) else 0.5,
                outcome_value=event_data.get("success_rate", 0.5),
            )

            # Process through L.I.F.E entity
            learning_outcome = await self.life_entity.process_experience(experience)

            # Store in research buffer for batch optimization
            self.life_entity.research_buffer.append(
                {
                    "exp": asdict(experience),
                    "gain": learning_outcome.learning_gain,
                    "timestamp": datetime.now(),
                    "context": event_data,
                    "outcome": asdict(learning_outcome),
                }
            )

            # Update processing statistics
            self.processing_stats["total_experiences"] += 1
            self.processing_stats["successful_processing"] += 1
            self.processing_stats[
                "learning_gain_total"
            ] += learning_outcome.learning_gain
            self.processing_stats["optimizations_applied"] += len(
                learning_outcome.applied_optimizations
            )

            # Trigger immediate optimization if buffer is full
            if len(self.life_entity.research_buffer) >= 100:
                optimization_result = await self.life_entity.optimize_learning()
                logger.info(
                    f"🔄 Batch optimization triggered: {optimization_result.get('status')}"
                )

            # Apply immediate optimizations if confidence is high
            if learning_outcome.confidence > 0.8:
                await self._apply_immediate_optimizations(learning_outcome)

            logger.debug(
                f"📊 Experience collected: {learning_outcome.learning_gain:.4f} gain, "
                f"{learning_outcome.confidence:.2%} confidence"
            )

        except Exception as e:
            logger.error(f"❌ Platform interaction collection error: {e}")

    async def collect_tab_interaction(self, tab_data: Dict[str, Any]) -> None:
        """Specialized collection for tab interactions"""
        try:
            # Enhance tab event data with UI-specific context
            enhanced_data = {
                **tab_data,
                "interaction_type": "ui_tab",
                "critical": tab_data.get("is_core_functionality", False),
                "success_rate": tab_data.get("response_time_ms", 200)
                < 150,  # Success if < 150ms
                "complexity_indicators": {
                    "javascript_errors": tab_data.get("js_errors", 0),
                    "css_load_failures": tab_data.get("css_failures", 0),
                    "user_retries": tab_data.get("retry_count", 0),
                },
            }

            await self.collect_platform_interaction(enhanced_data)

        except Exception as e:
            logger.error(f"❌ Tab interaction collection error: {e}")

    async def collect_eeg_processing_event(self, eeg_data: Dict[str, Any]) -> None:
        """Specialized collection for EEG processing events"""
        try:
            # Enhance EEG event data with neural processing context
            enhanced_data = {
                **eeg_data,
                "interaction_type": "neural_processing",
                "critical": True,  # EEG processing is always critical
                "success_rate": eeg_data.get("accuracy", 0.95),
                "complexity_indicators": {
                    "latency_ms": eeg_data.get("processing_latency_ms", 1.0),
                    "signal_quality": eeg_data.get("signal_quality", 0.9),
                    "channel_count": eeg_data.get("channels", 64),
                },
            }

            await self.collect_platform_interaction(enhanced_data)

        except Exception as e:
            logger.error(f"❌ EEG processing event collection error: {e}")

    def _calculate_novelty(self, event_data: Dict[str, Any]) -> float:
        """Calculate novelty score for an event"""
        try:
            # Base novelty on event type frequency and characteristics
            interaction_type = event_data.get("interaction_type", "unknown")

            # New interaction types have high novelty
            known_types = [
                "ui_tab",
                "neural_processing",
                "user_input",
                "system_response",
            ]
            if interaction_type not in known_types:
                return 0.9

            # Error conditions increase novelty
            if event_data.get("error_occurred", False):
                return 0.7

            # Unusual performance metrics increase novelty
            response_time = event_data.get("response_time_ms", 100)
            if response_time > 500:  # Unusually slow
                return 0.6

            return 0.3  # Default low novelty for routine interactions

        except Exception as e:
            logger.error(f"❌ Novelty calculation error: {e}")
            return 0.2  # Conservative default

    def _calculate_salience(self, event_data: Dict[str, Any]) -> float:
        """Calculate emotional salience (importance) of an event"""
        try:
            salience = 0.3  # Base salience

            # Critical events have high salience
            if event_data.get("critical", False):
                salience += 0.4

            # Failures increase salience
            if event_data.get("success_rate", 1.0) < 0.5:
                salience += 0.3

            # User impact increases salience
            affected_users = event_data.get("affected_users", 0)
            if affected_users > 0:
                salience += min(affected_users / 100.0, 0.3)  # Max 0.3 bonus

            return min(salience, 1.0)

        except Exception as e:
            logger.error(f"❌ Salience calculation error: {e}")
            return 0.3  # Conservative default

    def _calculate_complexity(self, event_data: Dict[str, Any]) -> float:
        """Calculate cognitive complexity of an event"""
        try:
            complexity = 0.2  # Base complexity

            # Multiple simultaneous failures increase complexity
            complexity_indicators = event_data.get("complexity_indicators", {})

            if isinstance(complexity_indicators, dict):
                error_count = sum(
                    v
                    for k, v in complexity_indicators.items()
                    if "error" in k.lower() and isinstance(v, (int, float))
                )
                complexity += min(error_count / 10.0, 0.4)  # Max 0.4 from errors

                # High latency increases complexity
                latency = complexity_indicators.get("latency_ms", 0)
                if latency > 100:
                    complexity += min(
                        (latency - 100) / 1000.0, 0.3
                    )  # Max 0.3 from latency

            # Multi-component events increase complexity
            if event_data.get("components_affected", 1) > 1:
                complexity += 0.2

            return min(complexity, 1.0)

        except Exception as e:
            logger.error(f"❌ Complexity calculation error: {e}")
            return 0.4  # Conservative default

    async def _process_experience_queue(self) -> None:
        """Background processing of experience queue"""
        logger.info("🔄 Experience queue processor started")

        while True:
            try:
                if self.experience_queue:
                    # Process queued experiences
                    while self.experience_queue:
                        event_data = self.experience_queue.pop(0)
                        await self.collect_platform_interaction(event_data)

                # Brief pause before next processing cycle
                await asyncio.sleep(1.0)

            except Exception as e:
                logger.error(f"❌ Experience queue processing error: {e}")
                await asyncio.sleep(5.0)

    async def _periodic_optimization(self) -> None:
        """Periodic optimization trigger"""
        logger.info("⚡ Periodic optimization scheduler started")

        while True:
            try:
                # Trigger optimization every 10 minutes
                await asyncio.sleep(600)

                if len(self.life_entity.research_buffer) >= 10:
                    optimization_result = await self.life_entity.optimize_learning()
                    logger.info(
                        f"🔄 Periodic optimization: {optimization_result.get('status')}"
                    )

            except Exception as e:
                logger.error(f"❌ Periodic optimization error: {e}")
                await asyncio.sleep(60)

    async def _metrics_reporting(self) -> None:
        """Periodic metrics reporting"""
        logger.info("📊 Metrics reporting scheduler started")

        while True:
            try:
                # Report metrics every 5 minutes
                await asyncio.sleep(300)

                avg_learning_gain = self.processing_stats["learning_gain_total"] / max(
                    self.processing_stats["successful_processing"], 1
                )

                logger.info(
                    f"📈 Experience Collection Metrics: "
                    f"{self.processing_stats['total_experiences']} total, "
                    f"{avg_learning_gain:.4f} avg gain, "
                    f"{self.processing_stats['optimizations_applied']} optimizations"
                )

            except Exception as e:
                logger.error(f"❌ Metrics reporting error: {e}")
                await asyncio.sleep(60)

    async def _apply_immediate_optimizations(self, outcome: LearningOutcome) -> None:
        """Apply immediate optimizations for high-confidence learning"""
        try:
            for optimization in outcome.applied_optimizations:
                if optimization == "apply_immediately":
                    # Immediate application of learned optimization
                    logger.info(f"⚡ Immediate optimization applied: {optimization}")
                elif optimization == "prioritize_learning":
                    # Increase priority of similar future experiences
                    logger.info(f"📈 Learning prioritization updated: {optimization}")

        except Exception as e:
            logger.error(f"❌ Immediate optimization error: {e}")


async def main():
    """Main function to demonstrate experience collection"""
    logger.info("🧠 L.I.F.E Platform Experience Collector Demo")

    # Initialize experience collector
    collector = PlatformExperienceCollector()

    # Simulate platform events for demonstration
    async def simulate_platform_events():
        """Simulate various platform events"""
        events = [
            {
                "interaction_type": "ui_tab",
                "tab_name": "dashboard",
                "response_time_ms": 125,
                "success_rate": 0.98,
                "user_satisfaction": 0.92,
            },
            {
                "interaction_type": "neural_processing",
                "accuracy": 0.9825,
                "processing_latency_ms": 0.37,
                "signal_quality": 0.94,
                "critical": True,
            },
            {
                "interaction_type": "ui_tab",
                "tab_name": "analytics",
                "response_time_ms": 850,  # Slow response
                "js_errors": 2,
                "retry_count": 1,
                "success_rate": 0.65,
            },
        ]

        for event in events:
            await collector.collect_platform_interaction(event)
            await asyncio.sleep(1)

    try:
        # Start collection in background
        collection_task = asyncio.create_task(collector.start_collection())

        # Simulate events
        await simulate_platform_events()

        # Let it run for a bit
        await asyncio.sleep(10)

    except KeyboardInterrupt:
        logger.info("🛑 Demonstration stopped by user")
    finally:
        logger.info("✅ Experience collection demonstration complete")


if __name__ == "__main__":
    asyncio.run(main())
