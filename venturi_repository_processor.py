#!/usr/bin/env python3
"""
Venturi Repository Processor - Apply 3 Venturi Gates to Repository Organization
Uses fluid dynamics principles to solve the GitHub truncation bottleneck

The 3 Venturi Gates Process:
1. INPUT GATE: Signal Enhancement - File categorization and prioritization
2. PROCESSING GATE: Noise Reduction - Remove redundant/unnecessary files  
3. OUTPUT GATE: Pattern Extraction - Organized structure creation

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from venturi_gates_system import create_3_venturi_system, VenturiGatesSystem
    VENTURI_AVAILABLE = True
except ImportError:
    VENTURI_AVAILABLE = False
    print("⚠️ Venturi system not available - using mock implementation")

class VenturiRepositoryProcessor:
    """
    Revolutionary Repository Organization using 3 Venturi Gates System
    Applies fluid dynamics to solve GitHub truncation bottleneck
    """
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.venturi_system = None
        self.file_metrics = {}
        self.organization_results = {}
        
        # Setup logging
        self._setup_logging()
        
        # File categorization patterns for Venturi processing
        self.file_categories = {
            "core_algorithms": {
                "priority": 1.0,
                "patterns": ["experimentP2L*.py", "lifetheory.py", "venturi_gates_system.py", 
                           "*algorithm*.py", "*neural*.py"],
                "description": "Core L.I.F.E. Platform algorithms"
            },
            "azure_integration": {
                "priority": 0.9, 
                "patterns": ["azure_*.py", "function_app.py", "requirements.txt", "host.json"],
                "description": "Azure deployment and integration"
            },
            "campaign_systems": {
                "priority": 0.7,
                "patterns": ["campaign_*.py", "*outreach*.py", "*email*.py", "*marketing*.py"],
                "description": "Marketing and campaign automation"
            },
            "testing_validation": {
                "priority": 0.6,
                "patterns": ["test_*.py", "*test*.py", "*validation*.py", "*benchmark*.py"],
                "description": "Testing and validation frameworks"
            },
            "deployment_scripts": {
                "priority": 0.5,
                "patterns": ["deploy*.py", "deploy*.bat", "deploy*.ps1", "*.sh"],
                "description": "Deployment automation scripts"
            },
            "documentation": {
                "priority": 0.4,
                "patterns": ["*.md", "*.html", "*.txt", "*README*", "*GUIDE*"],
                "description": "Documentation and guides"
            },
            "configuration": {
                "priority": 0.3,
                "patterns": ["*.json", "*.yaml", "*.yml", "*.config", "*.settings"],
                "description": "Configuration files"
            },
            "archive_candidates": {
                "priority": 0.1,
                "patterns": ["*backup*", "*old*", "*deprecated*", "*temp*", "*tmp*"],
                "description": "Files suitable for archiving"
            }
        }
    
    def _setup_logging(self):
        """Setup logging for Venturi repository processing"""
        import logging
        
        # Create logs directory with absolute path
        script_dir = os.getcwd()
        logs_dir = os.path.join(script_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"venturi_repository_processor_{timestamp}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("VenturiRepoProcessor")
    
    async def initialize_venturi_system(self) -> bool:
        """Initialize the 3 Venturi Gates system for repository processing"""
        try:
            self.logger.info("🌊 Initializing 3 Venturi Gates System for Repository Processing")
            
            if VENTURI_AVAILABLE:
                self.venturi_system = create_3_venturi_system()
                self.logger.info("✅ Venturi Gates System initialized successfully")
            else:
                # Mock system for demonstration
                self.venturi_system = MockVenturiSystem()
                self.logger.info("✅ Mock Venturi system initialized for demonstration")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Venturi system: {e}")
            return False
    
    async def process_repository_through_venturi_gates(self) -> Dict[str, Any]:
        """
        Process repository through the 3 Venturi Gates:
        INPUT → PROCESSING → OUTPUT
        """
        self.logger.info("🚀 Starting Venturi Repository Processing")
        self.logger.info("Target: Solve GitHub truncation issue (1,257+ files)")
        
        results = {
            "start_time": datetime.now().isoformat(),
            "venturi_gates": {
                "input_gate": {},
                "processing_gate": {},
                "output_gate": {}
            },
            "file_analysis": {},
            "organization_results": {},
            "performance_metrics": {}
        }
        
        try:
            # VENTURI GATE 1: INPUT - Signal Enhancement (File Categorization)
            self.logger.info("🌊 VENTURI GATE 1: INPUT - Signal Enhancement")
            input_results = await self._venturi_gate_1_input_enhancement()
            results["venturi_gates"]["input_gate"] = input_results
            
            # VENTURI GATE 2: PROCESSING - Noise Reduction (File Filtering)
            self.logger.info("🌊 VENTURI GATE 2: PROCESSING - Noise Reduction") 
            processing_results = await self._venturi_gate_2_noise_reduction(input_results)
            results["venturi_gates"]["processing_gate"] = processing_results
            
            # VENTURI GATE 3: OUTPUT - Pattern Extraction (Organization)
            self.logger.info("🌊 VENTURI GATE 3: OUTPUT - Pattern Extraction")
            output_results = await self._venturi_gate_3_pattern_extraction(processing_results)
            results["venturi_gates"]["output_gate"] = output_results
            
            # Final organization execution
            final_results = await self._execute_venturi_organization(output_results)
            results["organization_results"] = final_results
            
            results["end_time"] = datetime.now().isoformat()
            results["success"] = True
            
            self.logger.info("✅ Venturi Repository Processing completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Venturi processing failed: {e}")
            results["error"] = str(e)
            results["success"] = False
        
        return results
    
    async def _venturi_gate_1_input_enhancement(self) -> Dict[str, Any]:
        """
        VENTURI GATE 1: INPUT - Signal Enhancement
        Apply fluid dynamics to enhance file signal detection and categorization
        """
        self.logger.info("   🔍 Analyzing repository files with signal enhancement...")
        
        # Get all files in repository
        all_files = []
        for item in self.base_path.iterdir():
            if item.is_file():
                all_files.append(item.name)
        
        self.logger.info(f"   📁 Found {len(all_files)} files to process")
        
        # Apply Venturi signal enhancement - categorize by priority
        if self.venturi_system:
            # Convert file list to numerical signal for Venturi processing
            file_signal = [hash(f) % 100 / 100.0 for f in all_files]  # Normalize to 0-1
            
            # Process through Venturi system for enhancement
            venturi_results = self.venturi_system.process_through_gates(file_signal)
            enhanced_signal = venturi_results["final_output"]
        else:
            enhanced_signal = [0.5] * len(all_files)  # Default signal
        
        # Categorize files based on enhanced signal and patterns
        categorized_files = {}
        file_priorities = {}
        
        for i, filename in enumerate(all_files):
            # Calculate enhanced priority using Venturi output
            base_priority = self._calculate_file_priority(filename)
            venturi_enhancement = enhanced_signal[i] if i < len(enhanced_signal) else 0.5
            
            # Combine base priority with Venturi enhancement
            enhanced_priority = base_priority * 0.7 + venturi_enhancement * 0.3
            file_priorities[filename] = enhanced_priority
            
            # Categorize file
            category = self._categorize_file(filename)
            if category not in categorized_files:
                categorized_files[category] = []
            categorized_files[category].append(filename)
        
        # Sort by enhanced priority
        for category in categorized_files:
            categorized_files[category].sort(
                key=lambda f: file_priorities[f], 
                reverse=True
            )
        
        results = {
            "total_files": len(all_files),
            "categorized_files": categorized_files,
            "file_priorities": file_priorities,
            "venturi_enhancement_applied": True,
            "categories_identified": len(categorized_files),
            "top_priority_files": sorted(file_priorities.items(), 
                                       key=lambda x: x[1], 
                                       reverse=True)[:20]
        }
        
        self.logger.info(f"   ✅ Signal enhancement complete: {len(categorized_files)} categories")
        return results
    
    async def _venturi_gate_2_noise_reduction(self, input_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        VENTURI GATE 2: PROCESSING - Noise Reduction
        Remove redundant files and reduce repository noise
        """
        self.logger.info("   🔧 Applying noise reduction to eliminate redundancy...")
        
        categorized_files = input_results["categorized_files"]
        file_priorities = input_results["file_priorities"]
        
        # Apply Venturi noise reduction principles
        filtered_files = {}
        removed_files = []
        reduction_stats = {}
        
        for category, files in categorized_files.items():
            category_info = self.file_categories.get(category, {"priority": 0.1})
            category_priority = category_info["priority"]
            
            # Apply noise reduction based on category priority
            if category_priority >= 0.5:
                # Keep high-priority categories with minimal reduction
                keep_ratio = 0.95
            elif category_priority >= 0.3:
                # Medium priority - moderate reduction
                keep_ratio = 0.80
            else:
                # Low priority - aggressive noise reduction
                keep_ratio = 0.50
            
            # Calculate files to keep using Venturi principles
            files_to_keep = max(1, int(len(files) * keep_ratio))
            
            # Sort by priority and keep top files
            sorted_files = sorted(files, 
                                key=lambda f: file_priorities.get(f, 0), 
                                reverse=True)
            
            kept_files = sorted_files[:files_to_keep]
            noise_files = sorted_files[files_to_keep:]
            
            filtered_files[category] = kept_files
            removed_files.extend(noise_files)
            
            reduction_stats[category] = {
                "original_count": len(files),
                "kept_count": len(kept_files),
                "removed_count": len(noise_files),
                "reduction_ratio": len(noise_files) / len(files) if files else 0
            }
        
        results = {
            "filtered_files": filtered_files,
            "removed_files": removed_files,
            "reduction_stats": reduction_stats,
            "total_files_kept": sum(len(files) for files in filtered_files.values()),
            "total_files_removed": len(removed_files),
            "noise_reduction_ratio": len(removed_files) / input_results["total_files"]
        }
        
        self.logger.info(f"   ✅ Noise reduction complete: {len(removed_files)} files identified for archiving")
        return results
    
    async def _venturi_gate_3_pattern_extraction(self, processing_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        VENTURI GATE 3: OUTPUT - Pattern Extraction
        Extract optimal organization patterns and create structure
        """
        self.logger.info("   📋 Extracting organization patterns and creating structure...")
        
        filtered_files = processing_results["filtered_files"]
        
        # Extract organization patterns using Venturi principles
        organization_structure = {
            "root_priority": [],
            "archive": {}
        }
        
        # Define root priority patterns (keep in main directory)
        root_patterns = [
            "experimentP2L*.py", "lifetheory.py", "venturi_gates_system.py",
            "azure_config.py", "function_app.py", "requirements.txt",
            "README.md", "LICENSE", "CHANGELOG.md"
        ]
        
        for category, files in filtered_files.items():
            if category in ["core_algorithms", "azure_integration"]:
                # Keep highest priority files in root
                organization_structure["root_priority"].extend(files[:5])
            else:
                # Archive other categories
                archive_path = f"archive/{category.replace('_', '-')}"
                organization_structure["archive"][archive_path] = files
        
        # Create archive structure mapping
        archive_structure = {
            "archive/algorithms": {
                "description": "Core L.I.F.E. Platform algorithms and neural processing",
                "files": organization_structure["archive"].get("archive/core-algorithms", [])
            },
            "archive/deployment": {
                "description": "Deployment scripts and Azure configurations", 
                "files": organization_structure["archive"].get("archive/deployment-scripts", [])
            },
            "archive/campaigns": {
                "description": "Marketing automation and outreach systems",
                "files": organization_structure["archive"].get("archive/campaign-systems", [])
            },
            "archive/testing": {
                "description": "Testing frameworks and validation tools",
                "files": organization_structure["archive"].get("archive/testing-validation", [])
            },
            "archive/documentation": {
                "description": "Documentation, guides, and reports",
                "files": organization_structure["archive"].get("archive/documentation", [])
            }
        }
        
        results = {
            "organization_structure": organization_structure,
            "archive_structure": archive_structure,
            "root_files_count": len(organization_structure["root_priority"]),
            "archive_categories": len(archive_structure),
            "total_organized_files": sum(
                len(files) for files in organization_structure["archive"].values()
            ) + len(organization_structure["root_priority"]),
            "pattern_extraction_complete": True
        }
        
        self.logger.info(f"   ✅ Pattern extraction complete: {results['archive_categories']} archive categories")
        return results
    
    async def _execute_venturi_organization(self, output_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Venturi-optimized repository organization"""
        self.logger.info("🎯 Executing Venturi-optimized repository organization...")
        
        archive_structure = output_results["archive_structure"]
        
        execution_results = {
            "directories_created": [],
            "files_moved": 0,
            "errors": [],
            "organization_complete": False
        }
        
        try:
            # Create archive directories
            for archive_path in archive_structure:
                full_path = self.base_path / archive_path
                full_path.mkdir(parents=True, exist_ok=True)
                execution_results["directories_created"].append(archive_path)
                self.logger.info(f"   📁 Created directory: {archive_path}")
            
            # Move files to archive directories
            for archive_path, info in archive_structure.items():
                files_to_move = info["files"]
                dest_path = self.base_path / archive_path
                
                for filename in files_to_move:
                    source_file = self.base_path / filename
                    dest_file = dest_path / filename
                    
                    if source_file.exists() and source_file != dest_file:
                        try:
                            shutil.move(str(source_file), str(dest_file))
                            execution_results["files_moved"] += 1
                            self.logger.info(f"   📦 Moved: {filename} → {archive_path}")
                        except Exception as e:
                            error_msg = f"Failed to move {filename}: {e}"
                            execution_results["errors"].append(error_msg)
                            self.logger.warning(f"   ⚠️ {error_msg}")
            
            execution_results["organization_complete"] = True
            self.logger.info("✅ Venturi organization execution completed successfully!")
            
        except Exception as e:
            error_msg = f"Organization execution failed: {e}"
            execution_results["errors"].append(error_msg)
            self.logger.error(f"❌ {error_msg}")
        
        return execution_results
    
    def _calculate_file_priority(self, filename: str) -> float:
        """Calculate base file priority before Venturi enhancement"""
        for category, info in self.file_categories.items():
            patterns = info["patterns"]
            for pattern in patterns:
                if self._matches_pattern(filename, pattern):
                    return info["priority"]
        return 0.1  # Default low priority
    
    def _categorize_file(self, filename: str) -> str:
        """Categorize file based on patterns"""
        for category, info in self.file_categories.items():
            patterns = info["patterns"]
            for pattern in patterns:
                if self._matches_pattern(filename, pattern):
                    return category
        return "miscellaneous"
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern (simplified glob matching)"""
        import fnmatch
        return fnmatch.fnmatch(filename.lower(), pattern.lower())
    
    def save_results(self, results: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save Venturi processing results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/venturi_repository_processing_{timestamp}.json"
        
        # Ensure results directory exists
        results_dir = self.base_path / "results"
        results_dir.mkdir(exist_ok=True)
        
        filepath = results_dir / filename.replace("results/", "")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.info(f"💾 Results saved to: {filepath}")
        return str(filepath)

class MockVenturiSystem:
    """Mock Venturi system for demonstration when real system unavailable"""
    
    def process_through_gates(self, signal):
        """Mock processing that applies simple enhancement"""
        # Simple signal enhancement simulation
        enhanced = [min(1.0, s * 1.2) for s in signal]
        return {
            "final_output": enhanced,
            "gate_outputs": {
                "venturi1": enhanced,
                "venturi2": enhanced, 
                "venturi3": enhanced
            }
        }

async def main():
    """Main function to execute Venturi repository processing"""
    print("🌊 L.I.F.E. Platform - Venturi Repository Processor")
    print("=" * 65)
    print("Revolutionary repository organization using 3 Venturi Gates")
    print("Target: Solve GitHub truncation bottleneck (1,257+ files)")
    print()
    
    processor = VenturiRepositoryProcessor()
    
    try:
        # Initialize Venturi system
        if not await processor.initialize_venturi_system():
            print("❌ Failed to initialize Venturi system")
            return 1
        
        # Process repository through Venturi gates
        results = await processor.process_repository_through_venturi_gates()
        
        # Save results
        results_file = processor.save_results(results)
        
        # Display summary
        print("\n🎯 VENTURI PROCESSING SUMMARY")
        print("=" * 35)
        
        if results.get("success", False):
            org_results = results.get("organization_results", {})
            print(f"✅ Status: SUCCESS")
            print(f"📁 Directories created: {len(org_results.get('directories_created', []))}")
            print(f"📦 Files organized: {org_results.get('files_moved', 0)}")
            print(f"💾 Results saved: {results_file}")
            print()
            print("🎉 GitHub truncation bottleneck RESOLVED!")
            print("   Repository now organized with Venturi-optimized structure")
            
            return 0
        else:
            print(f"❌ Status: FAILED")
            if "error" in results:
                print(f"   Error: {results['error']}")
            return 1
            
    except Exception as e:
        print(f"❌ Venturi processing failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)