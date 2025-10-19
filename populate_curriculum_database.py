"""
L.I.F.E. Education Platform - Database Population Script
==========================================================

PLATFORM RESOURCE - Backend infrastructure script
Populates the 156-country curriculum database with comprehensive education data

Copyright 2025 - Sergio Paya Borrull
Internal use only - Not exposed to users
"""

import os
import sys
from datetime import datetime

from curriculum_library_platform_backend import (
    CountryCurriculum,
    CurriculumLibraryBackend,
    K12Education,
    PrimaryEducation,
    Region,
    SpecialEducation,
    UniversityDegreeLevel,
    UniversityEducation,
    UniversityProgram,
)


def create_usa_curriculum() -> CountryCurriculum:
    """Example: United States comprehensive curriculum"""

    primary = PrimaryEducation(
        grades="K-5",
        age_range="5-11",
        core_subjects=[
            "Mathematics",
            "English Language Arts",
            "Science",
            "Social Studies",
        ],
        languages=["English", "Spanish (bilingual programs)"],
        learning_focus="Common Core standards, literacy, numeracy, social-emotional learning",
        assessment_type="Continuous assessment + standardized state tests",
    )

    k12 = K12Education(
        grades="K-12",
        elementary_subjects=[
            "Math",
            "ELA",
            "Science",
            "Social Studies",
            "PE",
            "Art",
            "Music",
        ],
        middle_school_subjects=[
            "Algebra",
            "Geometry",
            "Biology",
            "Chemistry",
            "US History",
            "World History",
            "Foreign Languages",
        ],
        high_school_subjects=[
            "Calculus",
            "Statistics",
            "Physics",
            "AP Sciences",
            "Literature",
            "Composition",
            "Economics",
            "Government",
        ],
        stem_programs=[
            "AP Computer Science",
            "Engineering",
            "Robotics",
            "Data Science",
        ],
        arts_programs=[
            "Visual Arts",
            "Performing Arts",
            "Music Theory",
            "Digital Media",
        ],
        ap_ib_available=True,
        vocational_tracks=["CTE Programs", "Dual Enrollment", "Trade Certifications"],
    )

    special_ed = SpecialEducation(
        available_programs=[
            "Learning Disabilities",
            "Autism Spectrum",
            "Gifted & Talented",
            "ADHD Support",
            "Speech/Language",
            "Emotional Support",
        ],
        support_services=[
            "IEP",
            "504 Plans",
            "Speech Therapy",
            "Occupational Therapy",
            "Behavioral Interventions",
            "Assistive Technology",
        ],
        inclusion_model="Full inclusion with resource support",
        individualized_plans=True,
        assistive_technology=[
            "Text-to-Speech",
            "Speech-to-Text",
            "Visual Supports",
            "Adaptive Equipment",
        ],
        specialized_schools=True,
    )

    university = UniversityEducation(
        undergraduate_degrees=[
            UniversityProgram(
                "BA",
                "Liberal Arts",
                4.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
            UniversityProgram(
                "BS",
                "Computer Science",
                4.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
            UniversityProgram(
                "BS",
                "Engineering",
                4.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
            UniversityProgram(
                "BBA",
                "Business Administration",
                4.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
            UniversityProgram(
                "BSN", "Nursing", 4.0, ["English"], UniversityDegreeLevel.UNDERGRADUATE
            ),
        ],
        graduate_degrees=[
            UniversityProgram(
                "MA", "Education", 2.0, ["English"], UniversityDegreeLevel.GRADUATE
            ),
            UniversityProgram(
                "MS", "Data Science", 2.0, ["English"], UniversityDegreeLevel.GRADUATE
            ),
            UniversityProgram(
                "MBA",
                "Business Administration",
                2.0,
                ["English"],
                UniversityDegreeLevel.GRADUATE,
            ),
            UniversityProgram(
                "MS", "Engineering", 2.0, ["English"], UniversityDegreeLevel.GRADUATE
            ),
        ],
        doctoral_programs=[
            UniversityProgram(
                "PhD",
                "Computer Science",
                5.0,
                ["English"],
                UniversityDegreeLevel.DOCTORAL,
            ),
            UniversityProgram(
                "PhD", "Engineering", 5.0, ["English"], UniversityDegreeLevel.DOCTORAL
            ),
            UniversityProgram(
                "EdD",
                "Educational Leadership",
                4.0,
                ["English"],
                UniversityDegreeLevel.DOCTORAL,
            ),
        ],
        professional_degrees=[
            UniversityProgram(
                "MD", "Medicine", 4.0, ["English"], UniversityDegreeLevel.PROFESSIONAL
            ),
            UniversityProgram(
                "JD", "Law", 3.0, ["English"], UniversityDegreeLevel.PROFESSIONAL
            ),
        ],
        top_universities=[
            {
                "name": "MIT",
                "ranking": "1",
                "specialization": "Engineering, Computer Science",
            },
            {
                "name": "Stanford",
                "ranking": "2",
                "specialization": "Technology, Business",
            },
            {
                "name": "Harvard",
                "ranking": "3",
                "specialization": "Law, Medicine, Business",
            },
        ],
        research_focus=[
            "AI/ML",
            "Biotechnology",
            "Quantum Computing",
            "Renewable Energy",
        ],
        international_students_welcome=True,
    )

    return CountryCurriculum(
        country="United States",
        region=Region.NORTH_AMERICA,
        country_code="US",
        primary=primary,
        k12=k12,
        special_education=special_ed,
        university=university,
        official_languages=["English"],
        education_system_type="Decentralized (state-controlled)",
        compulsory_education_years=12,
        literacy_rate=99.0,
        status="Active",
        last_update=datetime.now().date().isoformat(),
    )


def create_uk_curriculum() -> CountryCurriculum:
    """United Kingdom comprehensive curriculum"""

    primary = PrimaryEducation(
        grades="1-6 (Key Stage 1-2)",
        age_range="5-11",
        core_subjects=[
            "English",
            "Mathematics",
            "Science",
            "Computing",
            "History",
            "Geography",
        ],
        languages=["English"],
        learning_focus="National Curriculum, SATs assessments, phonics",
        assessment_type="SATs at Key Stage 2, continuous teacher assessment",
    )

    k12 = K12Education(
        grades="1-13 (Reception to A-Levels)",
        elementary_subjects=[
            "English",
            "Maths",
            "Science",
            "History",
            "Geography",
            "Art",
            "Music",
            "PE",
        ],
        middle_school_subjects=[
            "Mathematics",
            "English",
            "Sciences",
            "Languages",
            "Humanities",
            "Technology",
        ],
        high_school_subjects=["GCSE subjects", "A-Level subjects", "BTEC options"],
        stem_programs=[
            "Computer Science",
            "Engineering",
            "Triple Science",
            "Further Maths",
        ],
        arts_programs=["Drama", "Music", "Art & Design", "Media Studies"],
        ap_ib_available=True,
        vocational_tracks=["BTEC", "Apprenticeships", "T-Levels"],
    )

    special_ed = SpecialEducation(
        available_programs=[
            "SEN Support",
            "Autism",
            "Dyslexia",
            "ADHD",
            "Gifted Support",
        ],
        support_services=[
            "EHCP (Education Health Care Plan)",
            "SEN Coordinators",
            "Speech Therapy",
        ],
        inclusion_model="Inclusive with specialist units",
        individualized_plans=True,
        assistive_technology=["Read&Write", "Visual aids", "Communication devices"],
        specialized_schools=True,
    )

    university = UniversityEducation(
        undergraduate_degrees=[
            UniversityProgram(
                "BA",
                "Arts & Humanities",
                3.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
            UniversityProgram(
                "BSc", "Science", 3.0, ["English"], UniversityDegreeLevel.UNDERGRADUATE
            ),
            UniversityProgram(
                "BEng",
                "Engineering",
                3.0,
                ["English"],
                UniversityDegreeLevel.UNDERGRADUATE,
            ),
        ],
        graduate_degrees=[
            UniversityProgram(
                "MA", "Master of Arts", 1.0, ["English"], UniversityDegreeLevel.GRADUATE
            ),
            UniversityProgram(
                "MSc",
                "Master of Science",
                1.0,
                ["English"],
                UniversityDegreeLevel.GRADUATE,
            ),
        ],
        doctoral_programs=[
            UniversityProgram(
                "PhD", "Philosophy", 3.0, ["English"], UniversityDegreeLevel.DOCTORAL
            ),
        ],
        professional_degrees=[
            UniversityProgram(
                "MBBS", "Medicine", 5.0, ["English"], UniversityDegreeLevel.PROFESSIONAL
            ),
        ],
        top_universities=[
            {"name": "Oxford", "ranking": "1", "specialization": "All fields"},
            {"name": "Cambridge", "ranking": "2", "specialization": "All fields"},
            {"name": "Imperial College", "ranking": "3", "specialization": "STEM"},
        ],
        research_focus=["Medicine", "Engineering", "AI", "Climate Science"],
        international_students_welcome=True,
    )

    return CountryCurriculum(
        country="United Kingdom",
        region=Region.EUROPE,
        country_code="GB",
        primary=primary,
        k12=k12,
        special_education=special_ed,
        university=university,
        official_languages=["English"],
        education_system_type="Centralized with devolution",
        compulsory_education_years=11,
        literacy_rate=99.0,
        status="Active",
        last_update=datetime.now().date().isoformat(),
    )


def populate_sample_countries(backend: CurriculumLibraryBackend):
    """
    Populate backend with sample countries

    PLATFORM RESOURCE - This function generates database content
    In production, would include all 156 countries
    """

    print("\n" + "=" * 60)
    print("Populating Curriculum Database - Platform Resource")
    print("=" * 60)

    # Add sample countries
    countries_to_add = [
        create_usa_curriculum(),
        create_uk_curriculum(),
        # Additional 154 countries would be added here in production
    ]

    for curriculum in countries_to_add:
        success = backend.add_country(curriculum)
        if success:
            print(f"✓ Added {curriculum.country} ({curriculum.region.value})")
        else:
            print(f"✗ Failed to add {curriculum.country}")

    print(f"\nTotal countries in database: {len(backend.curriculum_data)}")

    # Validate database
    print("\n" + "-" * 60)
    print("Validating Database Integrity...")
    print("-" * 60)
    validation = backend.validate_database()
    print(f"Total Countries: {validation['total_countries']}")
    print(f"By Region: {validation['countries_by_region']}")
    if validation["missing_data"]:
        print(f"Missing Data: {validation['missing_data']}")
    if validation["validation_errors"]:
        print(f"Errors: {validation['validation_errors']}")

    # Generate statistics
    print("\n" + "-" * 60)
    print("Database Statistics")
    print("-" * 60)
    stats = backend.generate_statistics()
    print(f"Total Countries: {stats['total_countries']}")
    print(f"Total University Programs: {stats['university_programs_total']}")
    print(f"Average Literacy Rate: {stats['average_literacy_rate']:.1f}%")
    print(f"Special Education Coverage: {stats['special_ed_coverage']:.1f}%")
    print(f"Languages Supported: {len(stats['languages'])}")

    return backend


def export_for_platform(backend: CurriculumLibraryBackend, output_dir: str):
    """Export database for platform frontend consumption"""

    print("\n" + "=" * 60)
    print("Exporting for Platform Integration")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)

    # Export to JSON
    json_path = os.path.join(output_dir, "curriculum_database.json")
    if backend.export_to_json(json_path):
        print(f"✓ Exported JSON: {json_path}")

    # Export to JavaScript
    js_path = os.path.join(output_dir, "curriculum_database.js")
    if backend.export_to_javascript(js_path):
        print(f"✓ Exported JavaScript: {js_path}")

    print("\n✅ Database ready for platform integration")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("L.I.F.E. Education Platform - Curriculum Database Population")
    print("PLATFORM RESOURCE - Backend Infrastructure")
    print("=" * 70)

    # Initialize backend
    backend = CurriculumLibraryBackend()

    # Populate with sample data
    backend = populate_sample_countries(backend)

    # Export for platform
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "curriculum_data")
    export_for_platform(backend, output_dir)

    print("\n" + "=" * 70)
    print("✅ Database Population Complete")
    print("=" * 70)
    print("\nBackend resource ready for platform use.")
    print("Frontend HTML file can import from: curriculum_data/curriculum_database.js")
    print("\nBackend resource ready for platform use.")
    print("Frontend HTML file can import from: curriculum_data/curriculum_database.js")
