#!/usr/bin/env python3
"""
Test script to check syntax issues in the L.I.F.E. file
"""
import ast
import sys


def check_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        print("✅ Syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        print(f"Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    file_path = r"e:\NEW FOLDER X L.I.F.E\Letters\experimentP2L.I.F.E Learning Individually from Experience Theory Algorithm Code 2025 Copyright Sergio Paya Borrull. All rights Reserved 3-1.py"
    check_syntax(file_path)    check_syntax(file_path)