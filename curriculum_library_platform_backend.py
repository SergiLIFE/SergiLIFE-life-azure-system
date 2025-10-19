"""
L.I.F.E. Education Platform - Curriculum Library Backend
========================================================

Copyright 2025 - Sergio Paya Borrull
Platform Resource: Internal curriculum management system for 156 countries
NOT FOR USER USE - Backend infrastructure only

This Python library manages:
- Multi-level education data (Primary, K-12, Special Ed, University)
- 156 country curriculum metadata
- Automated data validation and updates
- Export to JavaScript/JSON for frontend consumption
- Database integrity checks
"""

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EducationLevel(Enum):
    """Education level classifications"""

    PRIMARY = "primary"
    K12 = "k12"
    SPECIAL_EDUCATION = "special_education"
    UNIVERSITY = "university"


class Region(Enum):
    """Geographic regions for 156 countries"""

    AFRICA = "africa"
    ASIA = "asia"
    EUROPE = "europe"
    NORTH_AMERICA = "north_america"
    SOUTH_AMERICA = "south_america"
    OCEANIA = "oceania"
    MIDDLE_EAST = "middle_east"


class UniversityDegreeLevel(Enum):
    """University degree classifications"""

    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    DOCTORAL = "doctoral"
    PROFESSIONAL = "professional"


@dataclass
class PrimaryEducation:
    """Primary education curriculum structure"""

    grades: str  # e.g., "1-6", "1-5"
    age_range: str  # e.g., "6-11", "5-10"
    core_subjects: List[str]
    languages: List[str]
    learning_focus: str  # e.g., "foundational literacy and numeracy"
    assessment_type: str  # e.g., "continuous", "standardized"

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class K12Education:
    """K-12 comprehensive education structure"""

    grades: str  # e.g., "K-12", "1-12"
    elementary_subjects: List[str]
    middle_school_subjects: List[str]
    high_school_subjects: List[str]
    stem_programs: List[str]
    arts_programs: List[str]
    ap_ib_available: bool
    vocational_tracks: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SpecialEducation:
    """Special education programs and support"""

    available_programs: List[str]  # autism, learning disabilities, gifted, etc.
    support_services: List[str]  # speech therapy, occupational therapy, etc.
    inclusion_model: str  # "full inclusion", "partial", "separate"
    individualized_plans: bool  # IEP/504 equivalent
    assistive_technology: List[str]
    specialized_schools: bool

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class UniversityProgram:
    """University degree program information"""

    degree_type: str  # BA, BS, MA, MS, PhD, etc.
    field_of_study: str
    duration_years: float
    language_of_instruction: List[str]
    level: UniversityDegreeLevel

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["level"] = self.level.value
        return data


@dataclass
class UniversityEducation:
    """University-level education structure"""

    undergraduate_degrees: List[UniversityProgram]
    graduate_degrees: List[UniversityProgram]
    doctoral_programs: List[UniversityProgram]
    professional_degrees: List[UniversityProgram]  # MD, JD, etc.
    top_universities: List[Dict[str, str]]  # [{name, ranking, specialization}]
    research_focus: List[str]
    international_students_welcome: bool

    def to_dict(self) -> Dict:
        return {
            "undergraduate_degrees": [
                deg.to_dict() for deg in self.undergraduate_degrees
            ],
            "graduate_degrees": [deg.to_dict() for deg in self.graduate_degrees],
            "doctoral_programs": [deg.to_dict() for deg in self.doctoral_programs],
            "professional_degrees": [
                deg.to_dict() for deg in self.professional_degrees
            ],
            "top_universities": self.top_universities,
            "research_focus": self.research_focus,
            "international_students_welcome": self.international_students_welcome,
        }


@dataclass
class CountryCurriculum:
    """Complete curriculum data for one country"""

    country: str
    region: Region
    country_code: str  # ISO 3166-1 alpha-2
    primary: PrimaryEducation
    k12: K12Education
    special_education: SpecialEducation
    university: UniversityEducation
    official_languages: List[str]
    education_system_type: str  # e.g., "centralized", "decentralized"
    compulsory_education_years: int
    literacy_rate: float  # percentage
    status: str  # "Active", "Updating", "Under Review"
    last_update: str  # ISO date format

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export"""
        return {
            "country": self.country,
            "region": self.region.value,
            "country_code": self.country_code,
            "primary": self.primary.to_dict(),
            "k12": self.k12.to_dict(),
            "special_education": self.special_education.to_dict(),
            "university": self.university.to_dict(),
            "official_languages": self.official_languages,
            "education_system_type": self.education_system_type,
            "compulsory_education_years": self.compulsory_education_years,
            "literacy_rate": self.literacy_rate,
            "status": self.status,
            "last_update": self.last_update,
        }


class CurriculumLibraryBackend:
    """
    Backend platform resource for managing global curriculum database

    INTERNAL USE ONLY - Not exposed to frontend users
    """

    def __init__(self):
        self.curriculum_data: List[CountryCurriculum] = []
        self.data_directory = os.path.join(os.path.dirname(__file__), "curriculum_data")
        os.makedirs(self.data_directory, exist_ok=True)
        logger.info("Curriculum Library Backend initialized")

    def add_country(self, curriculum: CountryCurriculum) -> bool:
        """Add or update country curriculum data"""
        try:
            # Check if country already exists
            existing_idx = None
            for idx, curr in enumerate(self.curriculum_data):
                if curr.country == curriculum.country:
                    existing_idx = idx
                    break

            if existing_idx is not None:
                self.curriculum_data[existing_idx] = curriculum
                logger.info(f"Updated curriculum for {curriculum.country}")
            else:
                self.curriculum_data.append(curriculum)
                logger.info(f"Added curriculum for {curriculum.country}")

            return True
        except Exception as e:
            logger.error(f"Error adding country {curriculum.country}: {str(e)}")
            return False

    def get_country(self, country_name: str) -> Optional[CountryCurriculum]:
        """Retrieve curriculum data for specific country"""
        for curr in self.curriculum_data:
            if curr.country.lower() == country_name.lower():
                return curr
        return None

    def get_countries_by_region(self, region: Region) -> List[CountryCurriculum]:
        """Get all countries in a specific region"""
        return [curr for curr in self.curriculum_data if curr.region == region]

    def validate_database(self) -> Dict[str, any]:
        """Validate database integrity and completeness"""
        validation_results = {
            "total_countries": len(self.curriculum_data),
            "countries_by_region": {},
            "missing_data": [],
            "outdated_entries": [],
            "validation_errors": [],
        }

        # Count by region
        for region in Region:
            count = len(self.get_countries_by_region(region))
            validation_results["countries_by_region"][region.value] = count

        # Check for missing or incomplete data
        for curr in self.curriculum_data:
            try:
                # Check if essential data is present
                if not curr.primary.core_subjects:
                    validation_results["missing_data"].append(
                        f"{curr.country}: No primary subjects"
                    )

                if not curr.university.undergraduate_degrees:
                    validation_results["missing_data"].append(
                        f"{curr.country}: No university programs"
                    )

                # Check if data is outdated (older than 1 year)
                last_update = datetime.fromisoformat(curr.last_update)
                if (datetime.now() - last_update).days > 365:
                    validation_results["outdated_entries"].append(curr.country)

            except Exception as e:
                validation_results["validation_errors"].append(
                    f"{curr.country}: {str(e)}"
                )

        logger.info(
            f"Database validation complete: {validation_results['total_countries']} countries"
        )
        return validation_results

    def export_to_json(self, output_path: str) -> bool:
        """Export entire database to JSON file"""
        try:
            data = [curr.to_dict() for curr in self.curriculum_data]
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported database to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return False

    def export_to_javascript(self, output_path: str) -> bool:
        """Export database as JavaScript array for frontend integration"""
        try:
            data = [curr.to_dict() for curr in self.curriculum_data]
            js_content = f"// Auto-generated by Curriculum Library Backend\n"
            js_content += f"// Generated: {datetime.now().isoformat()}\n"
            js_content += f"// Total Countries: {len(data)}\n\n"
            js_content += f"const globalCurriculumDatabase = "
            js_content += json.dumps(data, indent=2, ensure_ascii=False)
            js_content += ";\n"

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(js_content)

            logger.info(f"Exported JavaScript to {output_path}")
            return True
        except Exception as e:
            logger.error(f"JavaScript export failed: {str(e)}")
            return False

    def import_from_json(self, input_path: str) -> bool:
        """Import database from JSON file"""
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.curriculum_data.clear()
            for country_data in data:
                # Reconstruct CountryCurriculum objects
                curriculum = self._dict_to_curriculum(country_data)
                if curriculum:
                    self.curriculum_data.append(curriculum)

            logger.info(
                f"Imported {len(self.curriculum_data)} countries from {input_path}"
            )
            return True
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            return False

    def _dict_to_curriculum(self, data: Dict) -> Optional[CountryCurriculum]:
        """Convert dictionary back to CountryCurriculum object"""
        try:
            # Reconstruct nested objects
            primary = PrimaryEducation(**data["primary"])
            k12 = K12Education(**data["k12"])
            special_ed = SpecialEducation(**data["special_education"])

            # Reconstruct university programs
            university_data = data["university"]
            undergrad = [
                UniversityProgram(
                    **{**prog, "level": UniversityDegreeLevel(prog["level"])}
                )
                for prog in university_data["undergraduate_degrees"]
            ]
            grad = [
                UniversityProgram(
                    **{**prog, "level": UniversityDegreeLevel(prog["level"])}
                )
                for prog in university_data["graduate_degrees"]
            ]
            doctoral = [
                UniversityProgram(
                    **{**prog, "level": UniversityDegreeLevel(prog["level"])}
                )
                for prog in university_data["doctoral_programs"]
            ]
            professional = [
                UniversityProgram(
                    **{**prog, "level": UniversityDegreeLevel(prog["level"])}
                )
                for prog in university_data["professional_degrees"]
            ]

            university = UniversityEducation(
                undergraduate_degrees=undergrad,
                graduate_degrees=grad,
                doctoral_programs=doctoral,
                professional_degrees=professional,
                top_universities=university_data["top_universities"],
                research_focus=university_data["research_focus"],
                international_students_welcome=university_data[
                    "international_students_welcome"
                ],
            )

            return CountryCurriculum(
                country=data["country"],
                region=Region(data["region"]),
                country_code=data["country_code"],
                primary=primary,
                k12=k12,
                special_education=special_ed,
                university=university,
                official_languages=data["official_languages"],
                education_system_type=data["education_system_type"],
                compulsory_education_years=data["compulsory_education_years"],
                literacy_rate=data["literacy_rate"],
                status=data["status"],
                last_update=data["last_update"],
            )
        except Exception as e:
            logger.error(f"Error reconstructing curriculum: {str(e)}")
            return None

    def generate_statistics(self) -> Dict[str, any]:
        """Generate comprehensive statistics about the database"""
        stats = {
            "total_countries": len(self.curriculum_data),
            "by_region": {},
            "education_systems": {},
            "average_literacy_rate": 0,
            "university_programs_total": 0,
            "special_ed_coverage": 0,
            "languages": set(),
        }

        literacy_sum = 0
        special_ed_count = 0

        for curr in self.curriculum_data:
            # Region counts
            region_name = curr.region.value
            stats["by_region"][region_name] = stats["by_region"].get(region_name, 0) + 1

            # Education system types
            sys_type = curr.education_system_type
            stats["education_systems"][sys_type] = (
                stats["education_systems"].get(sys_type, 0) + 1
            )

            # Literacy
            literacy_sum += curr.literacy_rate

            # University programs
            stats["university_programs_total"] += (
                len(curr.university.undergraduate_degrees)
                + len(curr.university.graduate_degrees)
                + len(curr.university.doctoral_programs)
                + len(curr.university.professional_degrees)
            )

            # Special education
            if curr.special_education.available_programs:
                special_ed_count += 1

            # Languages
            stats["languages"].update(curr.official_languages)

        if len(self.curriculum_data) > 0:
            stats["average_literacy_rate"] = literacy_sum / len(self.curriculum_data)
            stats["special_ed_coverage"] = (
                special_ed_count / len(self.curriculum_data)
            ) * 100

        stats["languages"] = list(stats["languages"])

        return stats


# Platform initialization function
def initialize_curriculum_backend() -> CurriculumLibraryBackend:
    """
    Initialize the curriculum library backend system

    PLATFORM RESOURCE - Internal use only
    """
    logger.info("=" * 60)
    logger.info("L.I.F.E. Education Platform - Curriculum Library Backend")
    logger.info("Initializing backend resource for 156-country database")
    logger.info("=" * 60)

    backend = CurriculumLibraryBackend()
    return backend


if __name__ == "__main__":
    # This runs only for backend maintenance and testing
    print("=" * 60)
    print("L.I.F.E. Curriculum Library Backend - Platform Resource")
    print("=" * 60)
    print("\nThis is a backend infrastructure component.")
    print("Not for direct user interaction.")
    print("\nCapabilities:")
    print("✓ Manage 156-country education database")
    print("✓ Multi-level education structure (Primary, K-12, Special Ed, University)")
    print("✓ Data validation and integrity checks")
    print("✓ Export to JSON/JavaScript for frontend consumption")
    print("✓ Automated updates and maintenance")
    print("\nStatus: Platform resource initialized")
