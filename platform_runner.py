#!/usr/bin/env python3
"""
Simple runner for L.I.F.E. Neuroadaptive Learning Platform
Outputs results to file for Azure Cloud Shell compatibility
"""

import os
import subprocess
import sys


def run_and_capture(command, description):
    """Run a command and capture output to file"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )

        # Write output to file
        with open(f"{description.replace(' ', '_')}_output.txt", "w") as f:
            f.write(f"Command: {command}\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\nSTDERR:\n")
            f.write(result.stderr)

        print(f"Output written to {description.replace(' ', '_')}_output.txt")
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"Command timed out: {description}")
        return False
    except Exception as e:
        print(f"Error running {description}: {e}")
        return False


def main():
    print("L.I.F.E. Platform Runner")
    print("=" * 50)

    # Test Python version
    run_and_capture("python --version", "Python Version Check")

    # Run test platform
    success1 = run_and_capture("python test_platform.py", "Platform Test")

    # Run main platform
    success2 = run_and_capture(
        "python neuroadaptive_learning_platform.py", "Main Platform"
    )

    print("\nRunner complete!")
    print("Check the output files for results.")

    return success1 and success2


if __name__ == "__main__":
    main()
