#!/usr/bin/env python3
"""
L.I.F.E. Theory Platform - Device Configuration System
Multi-device EEG/VR integration for educational institutions

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EEGDeviceType(Enum):
    """Supported EEG device types"""

    EMOTIV_EPOC = "emotiv_epoc"
    EMOTIV_INSIGHT = "emotiv_insight"
    MUSE_2 = "muse_2"
    MUSE_S = "muse_s"
    OPENBCI_GANGLION = "openbci_ganglion"
    OPENBCI_CYTON = "openbci_cyton"
    NEUROSKY_MINDWAVE = "neurosky_mindwave"
    ANT_NEURO_EEGO = "ant_neuro_eego"
    G_USBAMP = "g_usbamp"
    BIOSEMI_ACTIVETWO = "biosemi_activetwo"


class VRDeviceType(Enum):
    """Supported VR device types"""

    OCULUS_RIFT_S = "oculus_rift_s"
    OCULUS_QUEST_2 = "oculus_quest_2"
    OCULUS_QUEST_3 = "oculus_quest_3"
    HTC_VIVE = "htc_vive"
    HTC_VIVE_PRO = "htc_vive_pro"
    PLAYSTATION_VR = "playstation_vr"
    VALVE_INDEX = "valve_index"
    VARJO_AERO = "varjo_aero"
    PICO_4 = "pico_4"
    APPLE_VISION_PRO = "apple_vision_pro"


@dataclass
class EEGDeviceConfig:
    """EEG device configuration"""

    device_type: EEGDeviceType
    channels: int
    sampling_rate: int  # Hz
    resolution: int  # bits
    impedance_check: bool
    wireless: bool
    battery_life: int  # hours
    sdk_available: bool
    clinical_grade: bool
    price_range: str
    setup_complexity: str  # "easy", "medium", "complex"


@dataclass
class VRDeviceConfig:
    """VR device configuration"""

    device_type: VRDeviceType
    resolution_per_eye: tuple
    refresh_rate: int  # Hz
    field_of_view: int  # degrees
    tracking_type: str  # "inside-out", "outside-in", "mixed"
    controllers: bool
    hand_tracking: bool
    eye_tracking: bool
    wireless: bool
    pc_required: bool
    price_range: str
    setup_complexity: str


class DeviceCompatibilityManager:
    """Manages device compatibility and integration"""

    def __init__(self):
        self.eeg_configs = self._initialize_eeg_configs()
        self.vr_configs = self._initialize_vr_configs()
        self.institution_recommendations = (
            self._initialize_institution_recommendations()
        )

    def _initialize_eeg_configs(self) -> Dict[EEGDeviceType, EEGDeviceConfig]:
        """Initialize EEG device configurations"""
        return {
            EEGDeviceType.EMOTIV_EPOC: EEGDeviceConfig(
                device_type=EEGDeviceType.EMOTIV_EPOC,
                channels=14,
                sampling_rate=256,
                resolution=16,
                impedance_check=True,
                wireless=True,
                battery_life=12,
                sdk_available=True,
                clinical_grade=False,
                price_range="$400-600",
                setup_complexity="medium",
            ),
            EEGDeviceType.EMOTIV_INSIGHT: EEGDeviceConfig(
                device_type=EEGDeviceType.EMOTIV_INSIGHT,
                channels=5,
                sampling_rate=256,
                resolution=16,
                impedance_check=False,
                wireless=True,
                battery_life=9,
                sdk_available=True,
                clinical_grade=False,
                price_range="$300-400",
                setup_complexity="easy",
            ),
            EEGDeviceType.MUSE_2: EEGDeviceConfig(
                device_type=EEGDeviceType.MUSE_2,
                channels=4,
                sampling_rate=256,
                resolution=12,
                impedance_check=False,
                wireless=True,
                battery_life=10,
                sdk_available=True,
                clinical_grade=False,
                price_range="$200-300",
                setup_complexity="easy",
            ),
            EEGDeviceType.OPENBCI_CYTON: EEGDeviceConfig(
                device_type=EEGDeviceType.OPENBCI_CYTON,
                channels=8,
                sampling_rate=250,
                resolution=24,
                impedance_check=True,
                wireless=True,
                battery_life=26,
                sdk_available=True,
                clinical_grade=True,
                price_range="$500-700",
                setup_complexity="complex",
            ),
            EEGDeviceType.G_USBAMP: EEGDeviceConfig(
                device_type=EEGDeviceType.G_USBAMP,
                channels=16,
                sampling_rate=38400,
                resolution=24,
                impedance_check=True,
                wireless=False,
                battery_life=0,
                sdk_available=True,
                clinical_grade=True,
                price_range="$8000-12000",
                setup_complexity="complex",
            ),
        }

    def _initialize_vr_configs(self) -> Dict[VRDeviceType, VRDeviceConfig]:
        """Initialize VR device configurations"""
        return {
            VRDeviceType.OCULUS_QUEST_2: VRDeviceConfig(
                device_type=VRDeviceType.OCULUS_QUEST_2,
                resolution_per_eye=(1832, 1920),
                refresh_rate=90,
                field_of_view=100,
                tracking_type="inside-out",
                controllers=True,
                hand_tracking=True,
                eye_tracking=False,
                wireless=True,
                pc_required=False,
                price_range="$300-400",
                setup_complexity="easy",
            ),
            VRDeviceType.OCULUS_QUEST_3: VRDeviceConfig(
                device_type=VRDeviceType.OCULUS_QUEST_3,
                resolution_per_eye=(2064, 2208),
                refresh_rate=120,
                field_of_view=110,
                tracking_type="inside-out",
                controllers=True,
                hand_tracking=True,
                eye_tracking=False,
                wireless=True,
                pc_required=False,
                price_range="$500-650",
                setup_complexity="easy",
            ),
            VRDeviceType.HTC_VIVE_PRO: VRDeviceConfig(
                device_type=VRDeviceType.HTC_VIVE_PRO,
                resolution_per_eye=(1440, 1700),
                refresh_rate=90,
                field_of_view=110,
                tracking_type="outside-in",
                controllers=True,
                hand_tracking=False,
                eye_tracking=True,
                wireless=False,
                pc_required=True,
                price_range="$1200-1500",
                setup_complexity="complex",
            ),
            VRDeviceType.VALVE_INDEX: VRDeviceConfig(
                device_type=VRDeviceType.VALVE_INDEX,
                resolution_per_eye=(1440, 1600),
                refresh_rate=144,
                field_of_view=130,
                tracking_type="outside-in",
                controllers=True,
                hand_tracking=False,
                eye_tracking=False,
                wireless=False,
                pc_required=True,
                price_range="$1000-1300",
                setup_complexity="complex",
            ),
            VRDeviceType.APPLE_VISION_PRO: VRDeviceConfig(
                device_type=VRDeviceType.APPLE_VISION_PRO,
                resolution_per_eye=(3660, 3200),
                refresh_rate=90,
                field_of_view=120,
                tracking_type="inside-out",
                controllers=False,
                hand_tracking=True,
                eye_tracking=True,
                wireless=True,
                pc_required=False,
                price_range="$3500-4000",
                setup_complexity="medium",
            ),
        }

    def _initialize_institution_recommendations(self) -> Dict[str, Dict[str, List]]:
        """Initialize device recommendations by institution type"""
        return {
            "k12_school": {
                "eeg_devices": [
                    EEGDeviceType.MUSE_2,
                    EEGDeviceType.EMOTIV_INSIGHT,
                    EEGDeviceType.NEUROSKY_MINDWAVE,
                ],
                "vr_devices": [VRDeviceType.OCULUS_QUEST_2, VRDeviceType.PICO_4],
                "reasons": [
                    "Easy setup and maintenance",
                    "Student-friendly interfaces",
                    "Affordable for classroom deployment",
                    "Robust and durable for student use",
                ],
            },
            "university": {
                "eeg_devices": [
                    EEGDeviceType.EMOTIV_EPOC,
                    EEGDeviceType.OPENBCI_CYTON,
                    EEGDeviceType.ANT_NEURO_EEGO,
                ],
                "vr_devices": [
                    VRDeviceType.OCULUS_QUEST_3,
                    VRDeviceType.HTC_VIVE_PRO,
                    VRDeviceType.VALVE_INDEX,
                ],
                "reasons": [
                    "Research-grade data quality",
                    "SDK availability for student projects",
                    "Expandable and configurable",
                    "Good balance of cost and features",
                ],
            },
            "research_lab": {
                "eeg_devices": [
                    EEGDeviceType.G_USBAMP,
                    EEGDeviceType.BIOSEMI_ACTIVETWO,
                    EEGDeviceType.ANT_NEURO_EEGO,
                    EEGDeviceType.OPENBCI_CYTON,
                ],
                "vr_devices": [
                    VRDeviceType.HTC_VIVE_PRO,
                    VRDeviceType.VALVE_INDEX,
                    VRDeviceType.VARJO_AERO,
                ],
                "reasons": [
                    "Clinical-grade precision",
                    "High sampling rates",
                    "Publication-quality data",
                    "Advanced eye tracking capabilities",
                ],
            },
            "clinic": {
                "eeg_devices": [
                    EEGDeviceType.G_USBAMP,
                    EEGDeviceType.ANT_NEURO_EEGO,
                    EEGDeviceType.EMOTIV_EPOC,
                ],
                "vr_devices": [VRDeviceType.OCULUS_QUEST_2, VRDeviceType.HTC_VIVE_PRO],
                "reasons": [
                    "FDA-compliant options available",
                    "Patient safety certifications",
                    "Medical-grade data quality",
                    "Easy sanitization protocols",
                ],
            },
        }

    def get_device_recommendations(
        self, institution_type: str, budget_range: str = "medium"
    ) -> Dict[str, Any]:
        """Get device recommendations for institution type and budget"""
        if institution_type not in self.institution_recommendations:
            raise ValueError(f"Unsupported institution type: {institution_type}")

        recommendations = self.institution_recommendations[institution_type]

        # Filter by budget
        budget_filters = {
            "low": {"eeg_max": 500, "vr_max": 600},
            "medium": {"eeg_max": 1500, "vr_max": 1500},
            "high": {"eeg_max": 15000, "vr_max": 4000},
        }

        budget_filter = budget_filters.get(budget_range, budget_filters["medium"])

        # Get detailed recommendations
        eeg_recommendations = []
        for device_type in recommendations["eeg_devices"]:
            config = self.eeg_configs.get(device_type)
            if config:
                # Simple price parsing (would be more sophisticated in production)
                price_str = config.price_range.replace("$", "").replace(",", "")
                max_price = int(price_str.split("-")[-1])

                if max_price <= budget_filter["eeg_max"]:
                    eeg_recommendations.append(
                        {
                            "device": config,
                            "suitability_score": self._calculate_suitability_score(
                                config, institution_type, "eeg"
                            ),
                            "pros": self._get_device_pros(config),
                            "cons": self._get_device_cons(config),
                            "setup_requirements": self._get_setup_requirements(config),
                        }
                    )

        vr_recommendations = []
        for device_type in recommendations["vr_devices"]:
            config = self.vr_configs.get(device_type)
            if config:
                price_str = config.price_range.replace("$", "").replace(",", "")
                max_price = int(price_str.split("-")[-1])

                if max_price <= budget_filter["vr_max"]:
                    vr_recommendations.append(
                        {
                            "device": config,
                            "suitability_score": self._calculate_suitability_score(
                                config, institution_type, "vr"
                            ),
                            "pros": self._get_device_pros(config),
                            "cons": self._get_device_cons(config),
                            "setup_requirements": self._get_setup_requirements(config),
                        }
                    )

        # Sort by suitability score
        eeg_recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        vr_recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)

        return {
            "institution_type": institution_type,
            "budget_range": budget_range,
            "eeg_recommendations": eeg_recommendations,
            "vr_recommendations": vr_recommendations,
            "integration_notes": self._get_integration_notes(institution_type),
            "deployment_timeline": self._get_deployment_timeline(institution_type),
            "training_requirements": self._get_training_requirements(institution_type),
        }

    def _calculate_suitability_score(
        self, config: Any, institution_type: str, device_category: str
    ) -> float:
        """Calculate suitability score for device/institution combination"""
        score = 0.5  # Base score

        # Institution-specific scoring
        if institution_type == "k12_school":
            if config.setup_complexity == "easy":
                score += 0.3
            elif config.setup_complexity == "medium":
                score += 0.1
            else:
                score -= 0.2

            if device_category == "eeg" and config.wireless:
                score += 0.2

        elif institution_type == "university":
            if config.sdk_available:
                score += 0.2
            if device_category == "eeg" and config.clinical_grade:
                score += 0.1

        elif institution_type == "research_lab":
            if device_category == "eeg" and config.clinical_grade:
                score += 0.3
            if device_category == "eeg" and config.sampling_rate > 1000:
                score += 0.2
            if device_category == "vr" and config.eye_tracking:
                score += 0.2

        elif institution_type == "clinic":
            if device_category == "eeg" and config.clinical_grade:
                score += 0.4
            if config.setup_complexity == "easy":
                score += 0.1

        return min(1.0, max(0.0, score))

    def _get_device_pros(self, config: Any) -> List[str]:
        """Get device advantages"""
        pros = []

        if hasattr(config, "wireless") and config.wireless:
            pros.append("Wireless operation for freedom of movement")

        if hasattr(config, "sdk_available") and config.sdk_available:
            pros.append("SDK available for custom development")

        if hasattr(config, "clinical_grade") and config.clinical_grade:
            pros.append("Clinical-grade data quality")

        if hasattr(config, "setup_complexity") and config.setup_complexity == "easy":
            pros.append("Easy setup and configuration")

        if hasattr(config, "hand_tracking") and config.hand_tracking:
            pros.append("Natural hand interaction")

        if hasattr(config, "eye_tracking") and config.eye_tracking:
            pros.append("Advanced eye tracking capabilities")

        return pros

    def _get_device_cons(self, config: Any) -> List[str]:
        """Get device limitations"""
        cons = []

        if hasattr(config, "pc_required") and config.pc_required:
            cons.append("Requires powerful PC for operation")

        if hasattr(config, "setup_complexity") and config.setup_complexity == "complex":
            cons.append("Complex setup and calibration required")

        if hasattr(config, "clinical_grade") and not config.clinical_grade:
            cons.append("Not suitable for clinical research")

        if hasattr(config, "impedance_check") and not config.impedance_check:
            cons.append("No impedance checking for electrode quality")

        # Price-based cons
        if hasattr(config, "price_range"):
            if (
                "$1000" in config.price_range
                or "$2000" in config.price_range
                or "$3000" in config.price_range
            ):
                cons.append("High initial investment cost")

        return cons

    def _get_setup_requirements(self, config: Any) -> Dict[str, Any]:
        """Get setup requirements for device"""
        requirements = {
            "space_needed": "Varies by device",
            "technical_expertise": (
                config.setup_complexity
                if hasattr(config, "setup_complexity")
                else "medium"
            ),
            "additional_hardware": [],
            "software_requirements": [],
            "training_time": "2-4 hours",
        }

        if hasattr(config, "pc_required") and config.pc_required:
            requirements["additional_hardware"].append(
                "High-performance PC with VR-ready GPU"
            )

        if hasattr(config, "tracking_type") and config.tracking_type == "outside-in":
            requirements["additional_hardware"].append("Lighthouse base stations")
            requirements["space_needed"] = "Minimum 2m x 2m tracking area"

        if hasattr(config, "sdk_available") and config.sdk_available:
            requirements["software_requirements"].append(
                "Device SDK and development tools"
            )

        return requirements

    def _get_integration_notes(self, institution_type: str) -> List[str]:
        """Get integration notes for institution type"""
        notes = {
            "k12_school": [
                "Consider classroom management software integration",
                "Ensure devices are student-proof and durable",
                "Plan for teacher training and ongoing support",
                "Implement age-appropriate content filtering",
            ],
            "university": [
                "Integrate with existing learning management systems",
                "Provide student access to raw data for projects",
                "Consider multi-user scheduling systems",
                "Plan for research collaboration features",
            ],
            "research_lab": [
                "Ensure compatibility with existing analysis software",
                "Plan for data export in standard formats (BIDS, EDF+)",
                "Consider synchronization with other lab equipment",
                "Implement proper data archival systems",
            ],
            "clinic": [
                "Ensure HIPAA compliance for patient data",
                "Integrate with electronic health records (EHR)",
                "Plan for proper device sanitization protocols",
                "Consider patient comfort and accessibility",
            ],
        }

        return notes.get(institution_type, [])

    def _get_deployment_timeline(self, institution_type: str) -> Dict[str, str]:
        """Get deployment timeline for institution type"""
        timelines = {
            "k12_school": {
                "planning": "2-4 weeks",
                "procurement": "4-8 weeks",
                "installation": "1-2 weeks",
                "training": "2-3 weeks",
                "pilot_testing": "2-4 weeks",
                "full_deployment": "2-3 weeks",
            },
            "university": {
                "planning": "4-6 weeks",
                "procurement": "6-12 weeks",
                "installation": "2-3 weeks",
                "training": "3-4 weeks",
                "pilot_testing": "4-6 weeks",
                "full_deployment": "3-4 weeks",
            },
            "research_lab": {
                "planning": "6-8 weeks",
                "procurement": "8-16 weeks",
                "installation": "3-4 weeks",
                "training": "4-6 weeks",
                "validation": "6-8 weeks",
                "full_deployment": "2-3 weeks",
            },
            "clinic": {
                "planning": "8-12 weeks",
                "regulatory_review": "12-24 weeks",
                "procurement": "8-16 weeks",
                "installation": "2-3 weeks",
                "staff_training": "4-6 weeks",
                "patient_pilot": "8-12 weeks",
                "full_deployment": "4-6 weeks",
            },
        }

        return timelines.get(institution_type, timelines["university"])

    def _get_training_requirements(self, institution_type: str) -> Dict[str, Any]:
        """Get training requirements for institution type"""
        training = {
            "k12_school": {
                "target_audience": ["Teachers", "IT staff", "Administrative staff"],
                "training_modules": [
                    "Basic device operation",
                    "Student safety protocols",
                    "Troubleshooting common issues",
                    "Data privacy and security",
                ],
                "duration": "8-12 hours total",
                "format": "Hybrid (online + hands-on)",
                "ongoing_support": "Monthly check-ins, online resources",
            },
            "university": {
                "target_audience": [
                    "Faculty",
                    "Graduate students",
                    "Lab managers",
                    "IT staff",
                ],
                "training_modules": [
                    "Advanced device configuration",
                    "Research methodology integration",
                    "Data analysis workflows",
                    "SDK and development tools",
                    "Student supervision protocols",
                ],
                "duration": "16-24 hours total",
                "format": "Workshop-based with certification",
                "ongoing_support": "Quarterly workshops, research collaboration",
            },
            "research_lab": {
                "target_audience": [
                    "Principal investigators",
                    "Research staff",
                    "Technicians",
                ],
                "training_modules": [
                    "Clinical-grade data collection",
                    "Advanced signal processing",
                    "Statistical analysis methods",
                    "Publication-quality reporting",
                    "Equipment maintenance",
                ],
                "duration": "32-40 hours total",
                "format": "Intensive certification program",
                "ongoing_support": "Annual recertification, expert consultation",
            },
            "clinic": {
                "target_audience": [
                    "Clinicians",
                    "Technologists",
                    "Nurses",
                    "IT staff",
                ],
                "training_modules": [
                    "Clinical protocols and procedures",
                    "Patient safety and comfort",
                    "Medical device regulations",
                    "Data security and HIPAA compliance",
                    "Quality assurance procedures",
                ],
                "duration": "24-32 hours total",
                "format": "Clinical certification with practical assessment",
                "ongoing_support": "Continuing education credits, expert support",
            },
        }

        return training.get(institution_type, training["university"])

    def generate_deployment_report(
        self, institution_type: str, budget_range: str = "medium"
    ) -> str:
        """Generate comprehensive deployment report"""
        recommendations = self.get_device_recommendations(
            institution_type, budget_range
        )

        report = f"""
# L.I.F.E. Theory Platform Deployment Report

## Institution Type: {institution_type.replace('_', ' ').title()}
## Budget Range: {budget_range.title()}

### Executive Summary
This report provides comprehensive device recommendations and deployment guidance for implementing the L.I.F.E. Theory Platform in your {institution_type.replace('_', ' ')} environment.

### Recommended EEG Devices
"""

        for i, rec in enumerate(recommendations["eeg_recommendations"][:3], 1):
            device = rec["device"]
            report += f"""
#### {i}. {device.device_type.value.replace('_', ' ').title()}
- **Suitability Score:** {rec['suitability_score']:.2f}/1.00
- **Channels:** {device.channels}
- **Sampling Rate:** {device.sampling_rate} Hz
- **Price Range:** {device.price_range}
- **Setup Complexity:** {device.setup_complexity.title()}
- **Clinical Grade:** {'Yes' if device.clinical_grade else 'No'}

**Advantages:**
{chr(10).join(f"• {pro}" for pro in rec['pros'])}

**Considerations:**
{chr(10).join(f"• {con}" for con in rec['cons'])}
"""

        report += "\n### Recommended VR Devices\n"

        for i, rec in enumerate(recommendations["vr_recommendations"][:3], 1):
            device = rec["device"]
            report += f"""
#### {i}. {device.device_type.value.replace('_', ' ').title()}
- **Suitability Score:** {rec['suitability_score']:.2f}/1.00
- **Resolution per Eye:** {device.resolution_per_eye[0]} x {device.resolution_per_eye[1]}
- **Refresh Rate:** {device.refresh_rate} Hz
- **Price Range:** {device.price_range}
- **Setup Complexity:** {device.setup_complexity.title()}
- **PC Required:** {'Yes' if device.pc_required else 'No'}

**Advantages:**
{chr(10).join(f"• {pro}" for pro in rec['pros'])}

**Considerations:**
{chr(10).join(f"• {con}" for con in rec['cons'])}
"""

        report += f"""
### Deployment Timeline
{chr(10).join(f"• **{phase.replace('_', ' ').title()}:** {duration}" for phase, duration in recommendations['deployment_timeline'].items())}

### Integration Considerations
{chr(10).join(f"• {note}" for note in recommendations['integration_notes'])}

### Training Requirements
- **Target Audience:** {', '.join(recommendations['training_requirements']['target_audience'])}
- **Total Duration:** {recommendations['training_requirements']['duration']}
- **Format:** {recommendations['training_requirements']['format']}
- **Ongoing Support:** {recommendations['training_requirements']['ongoing_support']}

### Next Steps
1. Review and approve device recommendations
2. Finalize budget allocation
3. Begin procurement process
4. Schedule installation and training
5. Plan pilot testing phase

### Contact Information
For more information about L.I.F.E. Theory Platform deployment:
- Email: sergio@lifecoach-121.com
- Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb
- Website: lifecoach-121.com

---
*This report was generated by the L.I.F.E. Theory Platform Device Configuration System*
"""

        return report


async def main():
    """Demonstration of device configuration system"""
    print("🔧 L.I.F.E. Theory Platform - Device Configuration System")
    print("=" * 60)

    manager = DeviceCompatibilityManager()

    # Generate reports for different institution types
    institution_types = ["k12_school", "university", "research_lab", "clinic"]

    for institution in institution_types:
        print(f"\n📋 Generating report for {institution.replace('_', ' ').title()}...")

        # Generate recommendations
        recommendations = manager.get_device_recommendations(institution, "medium")

        print(f"\n🧠 EEG Device Recommendations:")
        for i, rec in enumerate(recommendations["eeg_recommendations"][:2], 1):
            device = rec["device"]
            print(f"  {i}. {device.device_type.value.replace('_', ' ').title()}")
            print(
                f"     Score: {rec['suitability_score']:.2f} | Price: {device.price_range}"
            )

        print(f"\n🥽 VR Device Recommendations:")
        for i, rec in enumerate(recommendations["vr_recommendations"][:2], 1):
            device = rec["device"]
            print(f"  {i}. {device.device_type.value.replace('_', ' ').title()}")
            print(
                f"     Score: {rec['suitability_score']:.2f} | Price: {device.price_range}"
            )

        # Save detailed report
        report = manager.generate_deployment_report(institution, "medium")
        filename = f"life_deployment_report_{institution}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"  📄 Detailed report saved: {filename}")

    print("\n" + "=" * 60)
    print("✅ Device configuration analysis complete!")
    print("📧 Contact sergio@lifecoach-121.com for deployment assistance")
    print("🌐 Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb")


if __name__ == "__main__":
    asyncio.run(main())
