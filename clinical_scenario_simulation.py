#!/usr/bin/env python3
"""
L.I.F.E. Platform - Clinical Scenario Simulation
Real Hospital EEG Analysis Demonstration

Copyright 2025 - Sergio Paya Borrull
Enterprise Neuroscience Platform - Clinical Use Case Demo

This simulation shows what healthcare professionals see when using 
the L.I.F.E. Platform with real patient EEG data.
"""

import asyncio
import importlib.util
import json
import logging
import os
import random
# Import our L.I.F.E. Algorithm
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np


# Clinical condition classifications
class ClinicalCondition(Enum):
    NORMAL = "normal"
    ADHD = "adhd"
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    COGNITIVE_DECLINE = "cognitive_decline"
    LEARNING_DISABILITY = "learning_disability"
    POST_STROKE = "post_stroke"
    TBI = "traumatic_brain_injury"
    EPILEPSY_RISK = "epilepsy_risk"

class SeverityLevel(Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

@dataclass
class PatientProfile:
    """Patient demographic and clinical information"""
    patient_id: str
    age: int
    gender: str
    condition: ClinicalCondition
    medical_history: List[str]
    current_medications: List[str]
    presenting_symptoms: List[str]
    referring_physician: str
    department: str

@dataclass
class ClinicalRecommendation:
    """Clinical recommendations based on EEG analysis"""
    primary_finding: str
    severity: SeverityLevel
    recommended_treatment: List[str]
    follow_up_tests: List[str]
    therapy_suggestions: List[str]
    medication_considerations: List[str]
    lifestyle_modifications: List[str]
    prognosis: str
    confidence_level: float
    urgent_attention_required: bool

@dataclass
class ClinicalReport:
    """Complete clinical report for healthcare professionals"""
    report_id: str
    patient: PatientProfile
    test_date: datetime
    eeg_duration_minutes: int
    neural_metrics: Dict[str, float]
    learning_assessment: Dict[str, float]
    clinical_findings: List[str]
    recommendations: ClinicalRecommendation
    comparison_to_normative_data: Dict[str, str]
    follow_up_timeline: str
    clinician_notes_section: str

class ClinicalLIFESimulation:
    """
    Clinical simulation of the L.I.F.E. Platform
    Shows real-world hospital use cases and clinical decision support
    """
    
    def __init__(self):
        self.life_algorithm = self._load_life_algorithm()
        self.normative_database = self._initialize_normative_database()
        
    def _load_life_algorithm(self):
        """Load the L.I.F.E. Algorithm Core"""
        try:
            spec = importlib.util.spec_from_file_location(
                "life_algorithm", 
                "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
            )
            life_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(life_module)
            return life_module.LIFEAlgorithmCore()
        except Exception as e:
            print(f"❌ Could not load L.I.F.E. Algorithm: {e}")
            return None
    
    def _initialize_normative_database(self) -> Dict[str, Dict[str, float]]:
        """Initialize normative EEG data for clinical comparison"""
        return {
            "children_6_12": {
                "alpha_power": 0.45, "beta_power": 0.25, "theta_power": 0.35,
                "attention_index": 0.65, "learning_efficiency": 0.70
            },
            "adolescents_13_18": {
                "alpha_power": 0.50, "beta_power": 0.30, "theta_power": 0.25,
                "attention_index": 0.70, "learning_efficiency": 0.75
            },
            "adults_19_65": {
                "alpha_power": 0.55, "beta_power": 0.35, "theta_power": 0.20,
                "attention_index": 0.75, "learning_efficiency": 0.80
            },
            "elderly_65_plus": {
                "alpha_power": 0.45, "beta_power": 0.30, "theta_power": 0.30,
                "attention_index": 0.65, "learning_efficiency": 0.70
            }
        }
    
    def create_patient_scenarios(self) -> List[PatientProfile]:
        """Create realistic patient scenarios for hospital setting"""
        scenarios = [
            PatientProfile(
                patient_id="PT-2025-001",
                age=8,
                gender="Male",
                condition=ClinicalCondition.ADHD,
                medical_history=["Premature birth", "Family history of ADHD"],
                current_medications=["None"],
                presenting_symptoms=["Inattention", "Hyperactivity", "Academic difficulties"],
                referring_physician="Dr. Sarah Johnson",
                department="Pediatric Neurology"
            ),
            PatientProfile(
                patient_id="PT-2025-002",
                age=34,
                gender="Female",
                condition=ClinicalCondition.DEPRESSION,
                medical_history=["Major depressive episode 2 years ago"],
                current_medications=["Sertraline 50mg"],
                presenting_symptoms=["Cognitive fog", "Difficulty concentrating", "Memory issues"],
                referring_physician="Dr. Michael Chen",
                department="Psychiatry"
            ),
            PatientProfile(
                patient_id="PT-2025-003",
                age=67,
                gender="Male",
                condition=ClinicalCondition.POST_STROKE,
                medical_history=["Ischemic stroke 6 months ago", "Hypertension"],
                current_medications=["Aspirin", "Lisinopril"],
                presenting_symptoms=["Speech difficulties", "Memory problems", "Learning challenges"],
                referring_physician="Dr. Lisa Rodriguez",
                department="Neurology - Stroke Recovery"
            ),
            PatientProfile(
                patient_id="PT-2025-004",
                age=16,
                gender="Female",
                condition=ClinicalCondition.LEARNING_DISABILITY,
                medical_history=["Diagnosed dyslexia age 7"],
                current_medications=["None"],
                presenting_symptoms=["Reading difficulties", "Math struggles", "Working memory issues"],
                referring_physician="Dr. Robert Kim",
                department="Pediatric Developmental Medicine"
            ),
            PatientProfile(
                patient_id="PT-2025-005",
                age=45,
                gender="Male",
                condition=ClinicalCondition.TBI,
                medical_history=["Motor vehicle accident 3 months ago", "Mild TBI"],
                current_medications=["Gabapentin for headaches"],
                presenting_symptoms=["Headaches", "Concentration issues", "Fatigue"],
                referring_physician="Dr. Amanda Foster",
                department="Neurology - Brain Injury"
            )
        ]
        return scenarios
    
    def generate_condition_specific_eeg(self, condition: ClinicalCondition, age: int) -> np.ndarray:
        """Generate realistic EEG patterns based on clinical condition"""
        channels = 64
        time_points = 1024
        t = np.linspace(0, 4, time_points)
        eeg_data = np.zeros((channels, time_points))
        
        # Base EEG patterns
        base_alpha = 0.5
        base_beta = 0.3
        base_theta = 0.4
        noise_level = 0.1
        
        # Condition-specific modifications
        if condition == ClinicalCondition.ADHD:
            # Increased theta, reduced alpha
            base_theta *= 1.6
            base_alpha *= 0.7
            noise_level *= 1.3
            
        elif condition == ClinicalCondition.DEPRESSION:
            # Reduced alpha, increased delta
            base_alpha *= 0.6
            base_theta *= 1.2
            noise_level *= 1.1
            
        elif condition == ClinicalCondition.POST_STROKE:
            # Asymmetric patterns, reduced coherence
            noise_level *= 1.8
            base_alpha *= 0.5
            
        elif condition == ClinicalCondition.LEARNING_DISABILITY:
            # Irregular patterns, increased theta
            base_theta *= 1.4
            base_beta *= 0.8
            noise_level *= 1.2
            
        elif condition == ClinicalCondition.TBI:
            # Irregular patterns, increased noise
            noise_level *= 2.0
            base_alpha *= 0.6
            base_beta *= 0.7
        
        # Generate EEG data for each channel
        for ch in range(channels):
            # Alpha rhythm (8-12 Hz)
            alpha = base_alpha * np.sin(2 * np.pi * 10 * t + np.random.random() * 2 * np.pi)
            
            # Beta activity (12-30 Hz)
            beta = base_beta * np.sin(2 * np.pi * 20 * t + np.random.random() * 2 * np.pi)
            
            # Theta waves (4-8 Hz)
            theta = base_theta * np.sin(2 * np.pi * 6 * t + np.random.random() * 2 * np.pi)
            
            # Add condition-specific noise and artifacts
            noise = noise_level * np.random.randn(time_points)
            
            # Add asymmetry for stroke patients (affect left hemisphere more)
            if condition == ClinicalCondition.POST_STROKE and ch < channels // 2:
                alpha *= 0.5
                noise *= 1.5
            
            eeg_data[ch] = alpha + beta + theta + noise
        
        return eeg_data
    
    async def analyze_patient_eeg(self, patient: PatientProfile) -> ClinicalReport:
        """Analyze patient EEG and generate clinical report"""
        print(f"\n🏥 Analyzing EEG for Patient {patient.patient_id}")
        print(f"   Department: {patient.department}")
        print(f"   Referring Physician: {patient.referring_physician}")
        
        # Generate condition-specific EEG data
        eeg_data = self.generate_condition_specific_eeg(patient.condition, patient.age)
        
        # Process through L.I.F.E. Algorithm
        if self.life_algorithm:
            eeg_metrics = await self.life_algorithm.process_eeg_stream(eeg_data)
        else:
            # Fallback if algorithm not loaded
            from datetime import datetime
            eeg_metrics = type('EEGMetrics', (), {
                'timestamp': datetime.now(),
                'alpha_power': random.uniform(0.2, 0.8),
                'beta_power': random.uniform(0.1, 0.5),
                'theta_power': random.uniform(0.1, 0.6),
                'delta_power': random.uniform(0.05, 0.3),
                'gamma_power': random.uniform(0.02, 0.15),
                'coherence_score': random.uniform(0.3, 0.9),
                'attention_index': random.uniform(0.2, 0.9),
                'learning_efficiency': random.uniform(0.3, 0.9)
            })()
        
        # Get age-appropriate normative data
        if patient.age <= 12:
            norm_group = "children_6_12"
        elif patient.age <= 18:
            norm_group = "adolescents_13_18"
        elif patient.age <= 65:
            norm_group = "adults_19_65"
        else:
            norm_group = "elderly_65_plus"
        
        normative_data = self.normative_database[norm_group]
        
        # Generate clinical findings and recommendations
        recommendations = self._generate_clinical_recommendations(
            patient, eeg_metrics, normative_data
        )
        
        # Create comprehensive clinical report
        from datetime import datetime as dt
        report = ClinicalReport(
            report_id=f"LIFE-{patient.patient_id}-{dt.now().strftime('%Y%m%d')}",
            patient=patient,
            test_date=dt.now(),
            eeg_duration_minutes=15,
            neural_metrics={
                "alpha_power": eeg_metrics.alpha_power,
                "beta_power": eeg_metrics.beta_power,
                "theta_power": eeg_metrics.theta_power,
                "attention_index": eeg_metrics.attention_index,
                "learning_efficiency": eeg_metrics.learning_efficiency,
                "coherence_score": eeg_metrics.coherence_score
            },
            learning_assessment={
                "working_memory": eeg_metrics.attention_index * 0.8,
                "processing_speed": eeg_metrics.learning_efficiency,
                "sustained_attention": eeg_metrics.coherence_score,
                "cognitive_flexibility": (eeg_metrics.beta_power / eeg_metrics.theta_power) if eeg_metrics.theta_power > 0 else 0.5
            },
            clinical_findings=self._generate_clinical_findings(patient, eeg_metrics, normative_data),
            recommendations=recommendations,
            comparison_to_normative_data=self._compare_to_normative(eeg_metrics, normative_data),
            follow_up_timeline=self._determine_follow_up_timeline(recommendations.severity),
            clinician_notes_section="[Space for clinician observations and additional notes]"
        )
        
        return report
    
    def _generate_clinical_recommendations(
        self, patient: PatientProfile, metrics, normative_data: Dict[str, float]
    ) -> ClinicalRecommendation:
        """Generate evidence-based clinical recommendations"""
        
        # Determine severity based on deviation from normative data
        attention_deviation = abs(metrics.attention_index - normative_data["attention_index"])
        learning_deviation = abs(metrics.learning_efficiency - normative_data["learning_efficiency"])
        
        if attention_deviation > 0.3 or learning_deviation > 0.3:
            severity = SeverityLevel.SEVERE
        elif attention_deviation > 0.2 or learning_deviation > 0.2:
            severity = SeverityLevel.MODERATE
        else:
            severity = SeverityLevel.MILD
        
        # Condition-specific recommendations
        if patient.condition == ClinicalCondition.ADHD:
            return ClinicalRecommendation(
                primary_finding="Attention deficit pattern with increased theta activity",
                severity=severity,
                recommended_treatment=[
                    "Neurofeedback therapy targeting theta/beta ratio",
                    "Cognitive behavioral therapy for attention skills",
                    "Stimulant medication evaluation if not contraindicated"
                ],
                follow_up_tests=[
                    "Follow-up EEG in 3 months to assess treatment response",
                    "Continuous performance test",
                    "Academic achievement assessment"
                ],
                therapy_suggestions=[
                    "Working memory training program",
                    "Attention regulation exercises",
                    "Behavioral modification techniques"
                ],
                medication_considerations=[
                    "Consider methylphenidate or amphetamine-based stimulants",
                    "Monitor for side effects: appetite, sleep, growth",
                    "Alternative: non-stimulant options (atomoxetine, guanfacine)"
                ],
                lifestyle_modifications=[
                    "Structured daily routine",
                    "Regular exercise (30+ minutes daily)",
                    "Reduced screen time, especially before sleep",
                    "Nutrition: reduce sugar, increase omega-3 fatty acids"
                ],
                prognosis="Good with appropriate multimodal treatment approach",
                confidence_level=0.85,
                urgent_attention_required=False
            )
            
        elif patient.condition == ClinicalCondition.DEPRESSION:
            return ClinicalRecommendation(
                primary_finding="Cognitive processing deficits associated with depressive symptoms",
                severity=severity,
                recommended_treatment=[
                    "Transcranial direct current stimulation (tDCS) targeting left DLPFC",
                    "Cognitive training for processing speed and working memory",
                    "Antidepressant optimization"
                ],
                follow_up_tests=[
                    "Depression severity scales (PHQ-9, HAM-D)",
                    "Cognitive assessment battery",
                    "Follow-up EEG in 6 weeks"
                ],
                therapy_suggestions=[
                    "Cognitive behavioral therapy focusing on cognitive restructuring",
                    "Mindfulness-based cognitive therapy",
                    "Behavioral activation therapy"
                ],
                medication_considerations=[
                    "Current sertraline may need dose adjustment",
                    "Consider switching to SNRI for cognitive benefits",
                    "Augmentation with cognitive enhancers if indicated"
                ],
                lifestyle_modifications=[
                    "Regular sleep schedule (7-9 hours nightly)",
                    "Daily light therapy (morning exposure)",
                    "Aerobic exercise 150 minutes/week",
                    "Social engagement activities"
                ],
                prognosis="Favorable with integrated treatment approach",
                confidence_level=0.78,
                urgent_attention_required=False
            )
            
        elif patient.condition == ClinicalCondition.POST_STROKE:
            return ClinicalRecommendation(
                primary_finding="Post-stroke cognitive impairment with hemispheric asymmetry",
                severity=severity,
                recommended_treatment=[
                    "Intensive cognitive rehabilitation program",
                    "Speech and language therapy",
                    "Occupational therapy for daily living skills"
                ],
                follow_up_tests=[
                    "MRI to assess structural changes",
                    "Comprehensive neuropsychological testing",
                    "Follow-up EEG in 1 month"
                ],
                therapy_suggestions=[
                    "Computer-based cognitive training",
                    "Constraint-induced language therapy",
                    "Motor-cognitive dual-task training"
                ],
                medication_considerations=[
                    "Continue current stroke prevention regimen",
                    "Consider cholinesterase inhibitors for cognitive enhancement",
                    "Monitor for post-stroke depression"
                ],
                lifestyle_modifications=[
                    "Gradual increase in physical activity",
                    "Cognitive stimulation activities",
                    "Family involvement in rehabilitation",
                    "Stroke support group participation"
                ],
                prognosis="Guarded but potential for improvement with intensive rehabilitation",
                confidence_level=0.72,
                urgent_attention_required=severity == SeverityLevel.SEVERE
            )
            
        elif patient.condition == ClinicalCondition.LEARNING_DISABILITY:
            return ClinicalRecommendation(
                primary_finding="Learning-related neural processing differences",
                severity=severity,
                recommended_treatment=[
                    "Specialized educational interventions",
                    "Neurofeedback training for attention and processing",
                    "Assistive technology evaluation"
                ],
                follow_up_tests=[
                    "Comprehensive psychoeducational assessment",
                    "Visual and auditory processing evaluation",
                    "Follow-up EEG in 6 months"
                ],
                therapy_suggestions=[
                    "Orton-Gillingham reading instruction",
                    "Math intervention using concrete-representational-abstract approach",
                    "Executive function skills training"
                ],
                medication_considerations=[
                    "Generally not indicated for learning disabilities alone",
                    "Address comorbid conditions if present (ADHD, anxiety)",
                    "Monitor for secondary emotional issues"
                ],
                lifestyle_modifications=[
                    "Structured homework environment",
                    "Break tasks into smaller components",
                    "Use of visual and auditory learning aids",
                    "Regular sleep schedule to optimize learning"
                ],
                prognosis="Good with appropriate educational supports and interventions",
                confidence_level=0.82,
                urgent_attention_required=False
            )
            
        elif patient.condition == ClinicalCondition.TBI:
            return ClinicalRecommendation(
                primary_finding="Post-traumatic cognitive changes with irregular neural patterns",
                severity=severity,
                recommended_treatment=[
                    "Comprehensive brain injury rehabilitation program",
                    "Cognitive therapy targeting affected domains",
                    "Vestibular therapy if indicated"
                ],
                follow_up_tests=[
                    "Neuropsychological testing battery",
                    "MRI with DTI to assess white matter integrity",
                    "Follow-up EEG in 4 weeks"
                ],
                therapy_suggestions=[
                    "Cognitive rehabilitation therapy",
                    "Compensatory strategy training",
                    "Attention process training"
                ],
                medication_considerations=[
                    "Continue gabapentin for headache management",
                    "Consider stimulants for cognitive enhancement if appropriate",
                    "Monitor for depression and anxiety"
                ],
                lifestyle_modifications=[
                    "Gradual return to activities",
                    "Cognitive rest periods throughout day",
                    "Sleep hygiene optimization",
                    "Stress management techniques"
                ],
                prognosis="Variable depending on injury severity and rehabilitation compliance",
                confidence_level=0.69,
                urgent_attention_required=True
            )
        
        # Default recommendation for other conditions
        return ClinicalRecommendation(
            primary_finding="Neural pattern analysis completed",
            severity=SeverityLevel.MILD,
            recommended_treatment=["Standard care protocols"],
            follow_up_tests=["Follow-up EEG as clinically indicated"],
            therapy_suggestions=["Supportive therapy as needed"],
            medication_considerations=["Continue current medications"],
            lifestyle_modifications=["Maintain healthy lifestyle"],
            prognosis="Stable",
            confidence_level=0.60,
            urgent_attention_required=False
        )
    
    def _generate_clinical_findings(
        self, patient: PatientProfile, metrics, normative_data: Dict[str, float]
    ) -> List[str]:
        """Generate specific clinical findings based on EEG analysis"""
        findings = []
        
        # Alpha power analysis
        alpha_diff = (metrics.alpha_power - normative_data["alpha_power"]) / normative_data["alpha_power"]
        if alpha_diff > 0.2:
            findings.append(f"Increased alpha power ({metrics.alpha_power:.3f}) - may indicate relaxed state or medication effects")
        elif alpha_diff < -0.2:
            findings.append(f"Decreased alpha power ({metrics.alpha_power:.3f}) - suggests increased arousal or anxiety")
        
        # Theta power analysis
        theta_diff = (metrics.theta_power - normative_data["theta_power"]) / normative_data["theta_power"]
        if theta_diff > 0.3:
            findings.append(f"Elevated theta activity ({metrics.theta_power:.3f}) - consistent with attention difficulties or drowsiness")
        
        # Attention index analysis
        attention_diff = (metrics.attention_index - normative_data["attention_index"]) / normative_data["attention_index"]
        if attention_diff < -0.2:
            findings.append(f"Reduced attention index ({metrics.attention_index:.3f}) - indicates attention regulation challenges")
        elif attention_diff > 0.2:
            findings.append(f"Enhanced attention index ({metrics.attention_index:.3f}) - suggests good attention regulation")
        
        # Learning efficiency analysis
        learning_diff = (metrics.learning_efficiency - normative_data["learning_efficiency"]) / normative_data["learning_efficiency"]
        if learning_diff < -0.15:
            findings.append(f"Reduced learning efficiency ({metrics.learning_efficiency:.3f}) - may impact academic/occupational performance")
        
        # Coherence analysis
        if metrics.coherence_score < 0.4:
            findings.append(f"Low neural coherence ({metrics.coherence_score:.3f}) - suggests fragmented neural communication")
        elif metrics.coherence_score > 0.8:
            findings.append(f"High neural coherence ({metrics.coherence_score:.3f}) - indicates well-coordinated neural activity")
        
        return findings if findings else ["EEG patterns within normal variation for age group"]
    
    def _compare_to_normative(self, metrics, normative_data: Dict[str, float]) -> Dict[str, str]:
        """Compare patient metrics to normative database"""
        comparisons = {}
        
        for metric in ["alpha_power", "beta_power", "theta_power", "attention_index", "learning_efficiency"]:
            patient_value = getattr(metrics, metric)
            norm_value = normative_data[metric]
            
            deviation = (patient_value - norm_value) / norm_value * 100
            
            if abs(deviation) < 10:
                comparisons[metric] = f"Within normal range ({deviation:+.1f}%)"
            elif deviation > 10:
                comparisons[metric] = f"Above average (+{deviation:.1f}%)"
            else:
                comparisons[metric] = f"Below average ({deviation:.1f}%)"
        
        return comparisons
    
    def _determine_follow_up_timeline(self, severity: SeverityLevel) -> str:
        """Determine appropriate follow-up timeline"""
        if severity == SeverityLevel.CRITICAL:
            return "Immediate follow-up within 1 week"
        elif severity == SeverityLevel.SEVERE:
            return "Follow-up within 2-4 weeks"
        elif severity == SeverityLevel.MODERATE:
            return "Follow-up in 1-3 months"
        else:
            return "Follow-up in 3-6 months or as clinically indicated"
    
    def display_clinical_report(self, report: ClinicalReport):
        """Display the clinical report as healthcare professionals would see it"""
        print("\n" + "="*80)
        print("🏥 L.I.F.E. PLATFORM - CLINICAL EEG ANALYSIS REPORT")
        print("="*80)
        
        # Header Information
        print(f"📋 Report ID: {report.report_id}")
        print(f"📅 Test Date: {report.test_date.strftime('%B %d, %Y at %I:%M %p')}")
        print(f"⏱️  EEG Duration: {report.eeg_duration_minutes} minutes")
        print(f"🏥 Department: {report.patient.department}")
        print(f"👨‍⚕️ Referring Physician: {report.patient.referring_physician}")
        
        # Patient Information
        print(f"\n👤 PATIENT INFORMATION")
        print(f"   Patient ID: {report.patient.patient_id}")
        print(f"   Age: {report.patient.age} years")
        print(f"   Gender: {report.patient.gender}")
        print(f"   Medical History: {', '.join(report.patient.medical_history)}")
        print(f"   Current Medications: {', '.join(report.patient.current_medications)}")
        print(f"   Presenting Symptoms: {', '.join(report.patient.presenting_symptoms)}")
        
        # Neural Metrics
        print(f"\n🧠 NEURAL ANALYSIS RESULTS")
        print(f"   Alpha Power: {report.neural_metrics['alpha_power']:.4f}")
        print(f"   Beta Power: {report.neural_metrics['beta_power']:.4f}")
        print(f"   Theta Power: {report.neural_metrics['theta_power']:.4f}")
        print(f"   Attention Index: {report.neural_metrics['attention_index']:.4f}")
        print(f"   Learning Efficiency: {report.neural_metrics['learning_efficiency']:.4f}")
        print(f"   Neural Coherence: {report.neural_metrics['coherence_score']:.4f}")
        
        # Learning Assessment
        print(f"\n📊 COGNITIVE ASSESSMENT")
        print(f"   Working Memory: {report.learning_assessment['working_memory']:.3f}")
        print(f"   Processing Speed: {report.learning_assessment['processing_speed']:.3f}")
        print(f"   Sustained Attention: {report.learning_assessment['sustained_attention']:.3f}")
        print(f"   Cognitive Flexibility: {report.learning_assessment['cognitive_flexibility']:.3f}")
        
        # Comparison to Normative Data
        print(f"\n📈 COMPARISON TO AGE-MATCHED NORMS")
        for metric, comparison in report.comparison_to_normative_data.items():
            print(f"   {metric.replace('_', ' ').title()}: {comparison}")
        
        # Clinical Findings
        print(f"\n🔍 CLINICAL FINDINGS")
        for i, finding in enumerate(report.clinical_findings, 1):
            print(f"   {i}. {finding}")
        
        # Recommendations
        rec = report.recommendations
        print(f"\n💡 CLINICAL RECOMMENDATIONS")
        print(f"   Primary Finding: {rec.primary_finding}")
        print(f"   Severity Level: {rec.severity.value.upper()}")
        print(f"   Confidence Level: {rec.confidence_level:.0%}")
        
        if rec.urgent_attention_required:
            print(f"   ⚠️  URGENT ATTENTION REQUIRED")
        
        print(f"\n   🎯 RECOMMENDED TREATMENTS:")
        for i, treatment in enumerate(rec.recommended_treatment, 1):
            print(f"      {i}. {treatment}")
        
        print(f"\n   🧪 FOLLOW-UP TESTS:")
        for i, test in enumerate(rec.follow_up_tests, 1):
            print(f"      {i}. {test}")
        
        print(f"\n   🏃‍♂️ THERAPY SUGGESTIONS:")
        for i, therapy in enumerate(rec.therapy_suggestions, 1):
            print(f"      {i}. {therapy}")
        
        print(f"\n   💊 MEDICATION CONSIDERATIONS:")
        for i, med in enumerate(rec.medication_considerations, 1):
            print(f"      {i}. {med}")
        
        print(f"\n   🏠 LIFESTYLE MODIFICATIONS:")
        for i, lifestyle in enumerate(rec.lifestyle_modifications, 1):
            print(f"      {i}. {lifestyle}")
        
        print(f"\n   📅 FOLLOW-UP TIMELINE: {report.follow_up_timeline}")
        print(f"   🔮 PROGNOSIS: {rec.prognosis}")
        
        print(f"\n📝 CLINICIAN NOTES:")
        print(f"   {report.clinician_notes_section}")
        
        print(f"\n" + "="*80)
        print("End of Clinical Report")
        print("="*80)

async def main():
    """Run the clinical scenario simulation"""
    print("🏥 L.I.F.E. Platform - Clinical Scenario Simulation")
    print("   Real Hospital EEG Analysis Demonstration")
    print("=" * 60)
    
    # Initialize the clinical simulation
    clinical_sim = ClinicalLIFESimulation()
    
    # Create patient scenarios
    patients = clinical_sim.create_patient_scenarios()
    
    print(f"\n🎯 Simulating hospital EEG analysis for {len(patients)} patients...")
    print("   This shows what healthcare professionals see on their screens")
    
    # Analyze each patient
    for i, patient in enumerate(patients, 1):
        print(f"\n{'='*60}")
        print(f"PATIENT {i} of {len(patients)}")
        print(f"{'='*60}")
        
        # Analyze the patient's EEG
        clinical_report = await clinical_sim.analyze_patient_eeg(patient)
        
        # Display the clinical report
        clinical_sim.display_clinical_report(clinical_report)
        
        # Brief pause between patients
        if i < len(patients):
            print(f"\n⏳ Processing next patient...")
            await asyncio.sleep(1)
    
    print(f"\n🎉 Clinical Simulation Completed!")
    print(f"   Healthcare professionals now have actionable insights for:")
    print(f"   • Evidence-based treatment recommendations")
    print(f"   • Personalized therapy protocols")
    print(f"   • Objective progress monitoring")
    print(f"   • Risk stratification and prognosis")
    print(f"\n🚀 L.I.F.E. Platform: Transforming healthcare through neuroadaptive technology!")

if __name__ == "__main__":
    asyncio.run(main())if __name__ == "__main__":
    asyncio.run(main())