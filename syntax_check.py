#!/usr/bin/env python3
"""
Simple syntax checker for L.I.F.E. algorithm

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import ast
import sys


def check_syntax(file_path):
    """Check Python file syntax"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        # Parse the AST
        ast.parse(source)
        print(f"✅ Syntax check passed for {file_path}")
        return True

    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}:")
        print(f"  Line {e.lineno}: {e.text}")
        print(f"  {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False


if __name__ == "__main__":
    file_path = r"c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
    success = check_syntax(file_path)
    sys.exit(0 if success else 1)
