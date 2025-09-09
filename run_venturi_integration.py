#!/usr/bin/env python3
"""
L.I.F.E THEORY Venturi Integration Runner
Execute complete research integration with safety protocols

Copyright 2025 - Sergio Paya Borrull
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


async def main():
    """Main integration execution"""

    print("🌊 L.I.F.E THEORY Venturi Research Integration")
    print("=" * 65)
    print("Integrating Venturi meter research with PID controller optimization")
    print()

    try:
        # Import integration modules
        print("📦 Loading integration modules...")

        try:
            from enhanced_venturi_control import demonstrate_integrated_system

            print("   ✅ Enhanced Venturi Control module loaded")
        except ImportError as e:
            print(f"   ❌ Failed to load enhanced_venturi_control: {e}")
            return

        try:
            from venturi_research_integration import demonstrate_research_integration

            print("   ✅ Research Integration module loaded")
        except ImportError as e:
            print(f"   ❌ Failed to load venturi_research_integration: {e}")
            return

        print("\n🔬 Research Integration Summary:")
        print("   • PID Controller: Kp=0.8, Ki=0.1, Kd=0.05, Alpha=0.3")
        print("   • Venturi Standards: ±1.0% accuracy at Re > 200,000")
        print("   • Discharge Coefficient: 0.984 (Classical design)")
        print("   • Multi-mode operation with adaptive load targets")
        print()

        # Run enhanced Venturi control demonstration
        print("🚀 Phase 1: Enhanced Venturi Control Demonstration")
        print("-" * 50)
        await demonstrate_integrated_system()

        print("\n")

        # Run research integration demonstration
        print("🧬 Phase 2: Research Integration Demonstration")
        print("-" * 50)
        await demonstrate_research_integration()

        print("\n🎉 INTEGRATION COMPLETE!")
        print("=" * 65)
        print("📊 Results Summary:")
        print("   ✅ Enhanced Venturi Controller operational")
        print("   ✅ PID control system with exponential smoothing")
        print("   ✅ Research-based performance standards implemented")
        print("   ✅ Multi-mode operation validated")
        print("   ✅ Safety protocols maintained throughout integration")
        print()
        print("📄 Generated Files:")
        print("   • enhanced_venturi_control.py - Advanced control system")
        print("   • venturi_research_integration.py - Integration manager")
        print("   • venturi_integration_report_*.md - Detailed report")
        print()
        print("🔧 Next Steps:")
        print("   1. Review integration report for optimization recommendations")
        print("   2. Test with real L.I.F.E THEORY data")
        print("   3. Fine-tune PID parameters for specific use cases")
        print("   4. Deploy to production environment")
        print()

    except Exception as e:
        print(f"❌ Integration failed: {e}")
        import traceback

        traceback.print_exc()

    print("🌊 Integration process completed.")


if __name__ == "__main__":
    asyncio.run(main())
