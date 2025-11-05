import os
import sys
from typing import List, Tuple

# Windows-first path handling; no secrets used
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
REPORT_PATH = os.path.join(LOGS_DIR, "placeholder_audit.txt")

TOKEN = ""

# Considered text file extensions for scanning
TEXT_EXTS = {
    ".md", ".markdown", ".txt", ".py", ".ps1", ".psm1", ".psd1",
    ".bat", ".cmd", ".sh", ".ps", ".yml", ".yaml", ".json", ".ini", ".cfg", ".conf",
    ".toml", ".csv", ".tsv", ".html", ".css", ".js", ".ts"
}

# Skip very large files and known binary folders
SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules", ".azure", ".idea", ".vscode"
}

MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB safety cap


def is_text_like(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in TEXT_EXTS


def scan_file_for_token(path: str) -> Tuple[int, List[Tuple[int, str]]]:
    """
    Return (count, contexts) where contexts is a list of (line_number, context_str)
    context_str includes up to 1 line before and after.
    """
    try:
        size = os.path.getsize(path)
        if size > MAX_FILE_BYTES:
            return 0, []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return 0, []

    matches: List[int] = []
    for idx, line in enumerate(lines):
        if TOKEN in line:
            matches.append(idx)

    if not matches:
        return 0, []

    contexts: List[Tuple[int, str]] = []

    # Collapse contiguous or near-by matches to clusters and provide a compact context
    last_idx = -10
    for idx in matches:
        if idx - last_idx <= 1:
            # Too close to previous, skip to avoid spamming
            last_idx = idx
            continue
        start = max(0, idx - 1)
        end = min(len(lines), idx + 2)
        snippet = "".join(lines[start:end]).rstrip()
        contexts.append((idx + 1, snippet))
        last_idx = idx

    return len(matches), contexts


def main() -> int:
    os.makedirs(LOGS_DIR, exist_ok=True)

    findings = []
    total_matches = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        # prune dirs in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            full = os.path.join(root, name)
            if not is_text_like(full):
                continue
            c, ctx = scan_file_for_token(full)
            if c:
                rel = os.path.relpath(full, ROOT_DIR)
                findings.append((rel, c, ctx))
                total_matches += c

    findings.sort(key=lambda x: x[1], reverse=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as rep:
        rep.write("Placeholder Audit Report\n")
        rep.write("Token: %s\n" % TOKEN)
        rep.write("Root: %s\n" % ROOT_DIR)
        rep.write("Total files with matches: %d\n" % len(findings))
        rep.write("Total matches: %d\n" % total_matches)
        rep.write("\n=== Top offenders (by match count) ===\n\n")
        for rel, cnt, ctxs in findings:
            rep.write(f"- {rel}  (matches: {cnt})\n")
        rep.write("\n=== Detailed contexts ===\n\n")
        for rel, cnt, ctxs in findings:
            rep.write(f"## {rel} (matches: {cnt})\n")
            for ln, snippet in ctxs:
                rep.write(f"  - line {ln}:\n")
                rep.write(snippet)
                rep.write("\n\n")

    print(f"Audit complete. Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
