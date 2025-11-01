"""
Runner script to clean the attached experimentP2L source file and place a sanitized
version into the repository under src/experimentP2L/.

This does not push to Git; it only writes the cleaned file and can stage/commit locally.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DEST_DIR = os.path.join(REPO_ROOT, "src", "experimentP2L")
DEST_PATH = os.path.join(DEST_DIR, "experimentP2L_theory_2025_v3_1_clean.py")
REPORT_PATH = os.path.join(DEST_DIR, "experimentP2L_theory_2025_v3_1_clean.report.txt")


def run_cleaner(src_path: str, dest_path: str, report_path: str) -> int:
    cleaner = os.path.join(REPO_ROOT, "tools", "python_source_cleaner.py")
    if not os.path.exists(cleaner):
        print(f"Cleaner not found: {cleaner}", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    cmd = [
        sys.executable,
        cleaner,
        src_path,
        dest_path,
        "--verify-ast",
        "--report",
        report_path,
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)


def maybe_git_stage_and_commit(dest_path: str, message: str) -> None:
    # Best-effort local stage+commit; no push here.
    try:
        subprocess.check_call(["git", "add", dest_path], cwd=REPO_ROOT)
        subprocess.check_call(["git", "commit", "-m", message], cwd=REPO_ROOT)
    except subprocess.CalledProcessError as e:
        print(f"Git stage/commit skipped or failed: {e}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean and stage experimentP2L source")
    ap.add_argument(
        "--src",
        required=True,
        help="Absolute path to the original attached .py file (e.g., E:\\... .py)",
    )
    ap.add_argument(
        "--no-commit",
        action="store_true",
        help="Do not attempt local git commit after cleaning",
    )
    args = ap.parse_args()

    src_path = os.path.abspath(args.src)
    if not os.path.exists(src_path):
        print(f"ERROR: Source not found: {src_path}", file=sys.stderr)
        return 2

    rc = run_cleaner(src_path, DEST_PATH, REPORT_PATH)
    if rc != 0:
        print("Cleaning completed with issues. See report:", REPORT_PATH)
        return rc

    print("Cleaned file written to:", DEST_PATH)
    print("Report:", REPORT_PATH)

    if not args.no_commit:
        maybe_git_stage_and_commit(
            DEST_PATH,
            "chore(clean): sanitized experimentP2L file (AST-verified)",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
