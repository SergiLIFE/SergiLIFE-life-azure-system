#!/usr/bin/env python3
"""
MODULE 2: Reflective Depth Analyzer (RDA)
Gibbs Reflective Cycle Analysis for Metacognitive Assessment

STANDALONE DEMONSTRATION - NOT YET INTEGRATED
Created: October 6, 2025
Copyright 2025 - Sergio Paya Borrull

This module analyzes reflective learning text to assess depth of metacognitive processing
using the Gibbs Reflective Cycle framework (6 phases).
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ReflectiveDepthScore:
    """Scores for each phase of Gibbs Reflective Cycle"""

    description: float  # What happened?
    feelings: float  # What were you thinking/feeling?
    evaluation: float  # What was good/bad about the experience?
    analysis: float  # What sense can you make of it?
    conclusion: float  # What else could you have done?
    action_plan: float  # What will you do next time?
    overall_depth: float
    timestamp: str


class ReflectiveDepthAnalyzer:
    """
    Analyzes learner reflections using Gibbs Reflective Cycle framework

    Educational Value:
    - Promotes deeper learning through metacognition
    - Identifies students needing reflection coaching
    - Tracks development of critical thinking skills
    """

    def __init__(self):
        """Initialize with linguistic markers for each Gibbs phase"""
        self.phase_patterns = {
            "description": [
                r"\b(what|describe|explain|occurred|happened|event|situation|experience)\b",
                r"\b(when|where|who|did|action|took place)\b",
                r"\b(observed|noticed|saw|witnessed)\b",
            ],
            "feelings": [
                r"\b(feel|felt|feeling|emotion|emotional|react|reacted)\b",
                r"\b(happy|sad|angry|frustrated|excited|anxious|worried|confused)\b",
                r"\b(comfortable|uncomfortable|confident|uncertain)\b",
                r"\b(thought|thinking|believed|assumed)\b",
            ],
            "evaluation": [
                r"\b(good|bad|positive|negative|effective|ineffective)\b",
                r"\b(success|successful|failure|failed|worked|didn\'t work)\b",
                r"\b(advantage|disadvantage|strength|weakness)\b",
                r"\b(better|worse|improved|deteriorated)\b",
            ],
            "analysis": [
                r"\b(why|because|reason|cause|factor|influence)\b",
                r"\b(analyze|analysis|consider|reflect|examine)\b",
                r"\b(theory|concept|principle|knowledge|understand)\b",
                r"\b(relate|connection|link|pattern|theme)\b",
            ],
            "conclusion": [
                r"\b(conclude|conclusion|learned|learning|realize|realized)\b",
                r"\b(understand|understanding|insight|aware|awareness)\b",
                r"\b(different|differently|alternative|approach)\b",
                r"\b(overall|summary|general)\b",
            ],
            "action_plan": [
                r"\b(will|would|should|plan|intend|next time|future)\b",
                r"\b(improve|change|modify|adjust|develop)\b",
                r"\b(practice|try|attempt|implement|apply)\b",
                r"\b(goal|objective|aim|strategy|technique)\b",
            ],
        }

        # Weight adjustments for context
        self.context_weights = {
            "question_forms": 1.5,  # Questions indicate deeper thinking
            "first_person": 1.2,  # Personal engagement
            "comparative_lang": 1.3,  # Comparing options shows analysis
            "future_tense": 1.4,  # Action planning
        }

    def analyze(self, reflection_text: str) -> ReflectiveDepthScore:
        """
        Analyze reflection text and return Gibbs Cycle phase scores

        Args:
            reflection_text: Student's written reflection

        Returns:
            ReflectiveDepthScore with normalized scores for each phase
        """
        if not reflection_text or len(reflection_text.strip()) < 10:
            return self._empty_score()

        text_lower = reflection_text.lower()

        # Count markers for each phase
        phase_counts = {}
        for phase, patterns in self.phase_patterns.items():
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                count += len(matches)
            phase_counts[phase] = count

        # Apply context-based weighting
        weighted_counts = self._apply_contextual_weights(text_lower, phase_counts)

        # Normalize to 0-1 scale
        total_markers = sum(weighted_counts.values())
        if total_markers == 0:
            return self._empty_score()

        normalized_scores = {
            phase: count / total_markers for phase, count in weighted_counts.items()
        }

        # Calculate overall depth score
        # Higher weights for analysis, conclusion, and action planning
        depth_weights = {
            "description": 0.1,
            "feelings": 0.15,
            "evaluation": 0.15,
            "analysis": 0.25,
            "conclusion": 0.2,
            "action_plan": 0.15,
        }

        overall_depth = sum(
            normalized_scores[phase] * weight for phase, weight in depth_weights.items()
        )

        return ReflectiveDepthScore(
            description=normalized_scores["description"],
            feelings=normalized_scores["feelings"],
            evaluation=normalized_scores["evaluation"],
            analysis=normalized_scores["analysis"],
            conclusion=normalized_scores["conclusion"],
            action_plan=normalized_scores["action_plan"],
            overall_depth=overall_depth,
            timestamp=datetime.now().isoformat(),
        )

    def _apply_contextual_weights(
        self, text: str, phase_counts: Dict[str, int]
    ) -> Dict[str, float]:
        """Apply contextual weighting based on linguistic features"""
        weighted = phase_counts.copy()

        # Boost analysis if questions present
        if re.search(r"\?", text):
            weighted["analysis"] *= self.context_weights["question_forms"]

        # Boost feelings/action if first-person language
        first_person = len(re.findall(r"\b(i|my|me|myself)\b", text))
        if first_person > 3:
            weighted["feelings"] *= self.context_weights["first_person"]
            weighted["action_plan"] *= self.context_weights["first_person"]

        # Boost evaluation if comparative language
        if re.search(r"\b(better|worse|more|less|compared|versus)\b", text):
            weighted["evaluation"] *= self.context_weights["comparative_lang"]

        # Boost action_plan if future tense markers
        future_markers = len(re.findall(r"\b(will|going to|plan to|intend)\b", text))
        if future_markers > 0:
            weighted["action_plan"] *= self.context_weights["future_tense"]

        return weighted

    def _empty_score(self) -> ReflectiveDepthScore:
        """Return zero score for invalid input"""
        return ReflectiveDepthScore(
            description=0.0,
            feelings=0.0,
            evaluation=0.0,
            analysis=0.0,
            conclusion=0.0,
            action_plan=0.0,
            overall_depth=0.0,
            timestamp=datetime.now().isoformat(),
        )

    def get_feedback(self, score: ReflectiveDepthScore) -> Dict[str, str]:
        """
        Generate feedback for learner based on reflection depth

        Returns:
            Dictionary with overall assessment and specific recommendations
        """
        feedback = {
            "overall_assessment": "",
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": [],
        }

        # Overall assessment based on depth score
        if score.overall_depth > 0.7:
            feedback["overall_assessment"] = (
                "Excellent reflective depth! You demonstrate strong metacognitive skills."
            )
        elif score.overall_depth > 0.5:
            feedback["overall_assessment"] = (
                "Good reflection with room for deeper analysis."
            )
        elif score.overall_depth > 0.3:
            feedback["overall_assessment"] = (
                "Basic reflection present. Consider exploring your thinking more deeply."
            )
        else:
            feedback["overall_assessment"] = (
                "Limited reflection detected. Try to engage more deeply with your learning experience."
            )

        # Identify strengths (phases > 0.2)
        phase_names = {
            "description": "describing the experience",
            "feelings": "exploring your emotions and thoughts",
            "evaluation": "evaluating what worked well",
            "analysis": "analyzing why things happened",
            "conclusion": "drawing conclusions",
            "action_plan": "planning future actions",
        }

        for phase in [
            "description",
            "feelings",
            "evaluation",
            "analysis",
            "conclusion",
            "action_plan",
        ]:
            score_val = getattr(score, phase)
            if score_val > 0.2:
                feedback["strengths"].append(phase_names[phase])
            elif score_val < 0.1:
                feedback["areas_for_improvement"].append(phase_names[phase])

        # Specific recommendations
        if score.analysis < 0.15:
            feedback["recommendations"].append(
                "Try asking 'why' questions to deepen your analysis. "
                "Consider: Why did this happen? What factors influenced the outcome?"
            )

        if score.action_plan < 0.1:
            feedback["recommendations"].append(
                "Include specific action plans. "
                "Consider: What will you do differently next time? What's your next step?"
            )

        if score.feelings < 0.1:
            feedback["recommendations"].append(
                "Reflect on your emotions during the learning experience. "
                "Consider: How did you feel? What were you thinking?"
            )

        return feedback

    def batch_analyze(self, reflections: List[Dict[str, str]]) -> List[Dict]:
        """
        Analyze multiple reflections (e.g., class cohort)

        Args:
            reflections: List of dicts with 'user_id' and 'text' keys

        Returns:
            List of analysis results with scores and feedback
        """
        results = []

        for reflection in reflections:
            user_id = reflection.get("user_id", "unknown")
            text = reflection.get("text", "")

            score = self.analyze(text)
            feedback = self.get_feedback(score)

            results.append(
                {
                    "user_id": user_id,
                    "score": score.__dict__,
                    "feedback": feedback,
                    "text_length": len(text),
                    "timestamp": score.timestamp,
                }
            )

        return results

    def get_cohort_statistics(self, results: List[Dict]) -> Dict:
        """Calculate cohort-level statistics for instructor dashboard"""
        if not results:
            return {}

        overall_depths = [r["score"]["overall_depth"] for r in results]

        return {
            "cohort_size": len(results),
            "average_depth": sum(overall_depths) / len(overall_depths),
            "median_depth": sorted(overall_depths)[len(overall_depths) // 2],
            "high_performers": len([d for d in overall_depths if d > 0.7]),
            "need_support": len([d for d in overall_depths if d < 0.3]),
            "phase_averages": {
                "description": sum(r["score"]["description"] for r in results)
                / len(results),
                "feelings": sum(r["score"]["feelings"] for r in results) / len(results),
                "evaluation": sum(r["score"]["evaluation"] for r in results)
                / len(results),
                "analysis": sum(r["score"]["analysis"] for r in results) / len(results),
                "conclusion": sum(r["score"]["conclusion"] for r in results)
                / len(results),
                "action_plan": sum(r["score"]["action_plan"] for r in results)
                / len(results),
            },
        }


# ============================================================================
# DEMONSTRATION & TESTING
# ============================================================================


def demonstrate_reflective_depth_analyzer():
    """Demonstrate the Reflective Depth Analyzer with example reflections"""
    print("=" * 80)
    print("MODULE 2: Reflective Depth Analyzer - DEMONSTRATION")
    print("=" * 80)
    print()

    analyzer = ReflectiveDepthAnalyzer()

    # Example 1: High-quality reflection (all Gibbs phases present)
    print("Example 1: High-Quality Reflection")
    print("-" * 80)

    high_quality = """
    Today I participated in the group project discussion about climate change solutions.
    What happened was that we had to present our research findings, and I was responsible
    for the renewable energy section.
    
    I felt nervous at first because I wasn't sure if my research was thorough enough.
    However, as I started presenting, I became more confident when I saw my teammates
    nodding in agreement. I thought the data I collected was well-organized.
    
    The positive aspect was that our collaboration worked well, and everyone contributed
    equally. The presentation was effective because we divided the work clearly. However,
    one weakness was that we didn't rehearse enough beforehand, which made some transitions
    awkward.
    
    Why did this happen? I think it was because we underestimated the preparation time needed.
    The theory we learned about effective teamwork really applies here - clear communication
    and defined roles are crucial. I can now understand how important practice is for
    presentations.
    
    Overall, I learned that preparation is key to reducing anxiety and improving performance.
    I realize that my initial nervousness was largely due to lack of rehearsal rather than
    insufficient research.
    
    Next time, I will schedule at least two practice sessions before any major presentation.
    I plan to also create better transition slides to improve flow between sections.
    My goal is to feel more confident by being better prepared.
    """

    score1 = analyzer.analyze(high_quality)
    feedback1 = analyzer.get_feedback(score1)

    print("Reflection Text (truncated):")
    print(high_quality[:200] + "...\n")

    print("Gibbs Cycle Phase Scores:")
    print(f"  Description:  {score1.description:.3f}")
    print(f"  Feelings:     {score1.feelings:.3f}")
    print(f"  Evaluation:   {score1.evaluation:.3f}")
    print(f"  Analysis:     {score1.analysis:.3f}")
    print(f"  Conclusion:   {score1.conclusion:.3f}")
    print(f"  Action Plan:  {score1.action_plan:.3f}")
    print(f"  Overall Depth: {score1.overall_depth:.3f}")
    print()

    print("Feedback:")
    print(f"  Assessment: {feedback1['overall_assessment']}")
    if feedback1["strengths"]:
        print(f"  Strengths: {', '.join(feedback1['strengths'])}")
    if feedback1["recommendations"]:
        print("  Recommendations:")
        for rec in feedback1["recommendations"]:
            print(f"    - {rec}")
    print()
    print()

    # Example 2: Surface-level reflection (missing deeper phases)
    print("Example 2: Surface-Level Reflection")
    print("-" * 80)

    surface_level = """
    We had a group meeting today and discussed our project. Everyone showed up and
    we talked about what we need to do. The meeting went okay. We divided up the work
    and that was it.
    """

    score2 = analyzer.analyze(surface_level)
    feedback2 = analyzer.get_feedback(score2)

    print("Reflection Text:")
    print(surface_level)

    print("\nGibbs Cycle Phase Scores:")
    print(f"  Description:  {score2.description:.3f}")
    print(f"  Feelings:     {score2.feelings:.3f}")
    print(f"  Evaluation:   {score2.evaluation:.3f}")
    print(f"  Analysis:     {score2.analysis:.3f}")
    print(f"  Conclusion:   {score2.conclusion:.3f}")
    print(f"  Action Plan:  {score2.action_plan:.3f}")
    print(f"  Overall Depth: {score2.overall_depth:.3f}")
    print()

    print("Feedback:")
    print(f"  Assessment: {feedback2['overall_assessment']}")
    if feedback2["areas_for_improvement"]:
        print(
            f"  Areas for Improvement: {', '.join(feedback2['areas_for_improvement'])}"
        )
    if feedback2["recommendations"]:
        print("  Recommendations:")
        for rec in feedback2["recommendations"]:
            print(f"    - {rec}")
    print()
    print()

    # Example 3: Batch analysis (classroom scenario)
    print("Example 3: Classroom Cohort Analysis")
    print("-" * 80)

    cohort_reflections = [
        {"user_id": "student_001", "text": high_quality},
        {"user_id": "student_002", "text": surface_level},
        {
            "user_id": "student_003",
            "text": "I learned something new today. It was interesting.",
        },
        {
            "user_id": "student_004",
            "text": """
            I struggled with the assignment at first. Why was it so difficult? I think because
            the instructions weren't clear to me. Next time I will ask for clarification earlier.
            I learned that it's okay to ask questions when confused.
        """,
        },
    ]

    batch_results = analyzer.batch_analyze(cohort_reflections)
    cohort_stats = analyzer.get_cohort_statistics(batch_results)

    print(f"Cohort Size: {cohort_stats['cohort_size']} students")
    print(f"Average Reflection Depth: {cohort_stats['average_depth']:.3f}")
    print(f"High Performers (>0.7): {cohort_stats['high_performers']} students")
    print(f"Need Support (<0.3): {cohort_stats['need_support']} students")
    print()

    print("Phase Averages Across Cohort:")
    for phase, avg in cohort_stats["phase_averages"].items():
        print(f"  {phase.capitalize()}: {avg:.3f}")
    print()

    print("Individual Student Results:")
    for result in batch_results:
        print(
            f"  {result['user_id']}: Overall Depth = {result['score']['overall_depth']:.3f}"
        )
    print()

    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("INTEGRATION NOTES:")
    print("- Add ReflectiveDepthAnalyzer to LIFEAlgorithmCore class")
    print("- Call analyze() method when processing user reflections")
    print("- Store scores in learning_history for longitudinal tracking")
    print("- Use get_feedback() to provide real-time guidance to learners")
    print("- Use batch_analyze() for instructor dashboards")


if __name__ == "__main__":
    demonstrate_reflective_depth_analyzer()
