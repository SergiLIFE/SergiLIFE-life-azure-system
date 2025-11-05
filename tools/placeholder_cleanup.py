import argparse
import os
import sys
import re
from datetime import datetime
from pathlib import Path

TOKEN = ""
REPLACEMENTS = {
    # Common language tags broken by the token removal
    "```bash": "```bash",
}

EXCLUDE_DIRS = {
    ".git", "venv", ".venv", "node_modules", "__pycache__", "dist", "build",
    "logs", "quarantine"
}

TEXT_EXTS = {
    ".md", ".txt", ".py", ".ps1", ".psm1", ".yml", ".yaml", ".json", ".sh", ".bat", ".cmd"
}


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS


def clean_text(text: str) -> tuple[str, int]:
    """Remove placeholder token and apply small quality fixes.
    Returns (cleaned_text, num_replacements).
    """
    count = text.count(TOKEN)
    if count:
        text = text.replace(TOKEN, "")
    # Small heuristics for common breakages after token removal
    for bad, good in REPLACEMENTS.items():
        if bad in text:
            text = text.replace(bad, good)
    return text, count


def backup_file(src: Path, quarantine_dir: Path) -> Path:
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{src.name}.{ts}.bak"
    dst = quarantine_dir / backup_name
    dst.write_bytes(src.read_bytes())
    return dst


def process_file(path: Path, dry_run: bool, quarantine_dir: Path, logs_dir: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"path": str(path), "status": "skip", "reason": f"read-error: {e}"}

    cleaned, n = clean_text(raw)
    if n == 0:
        return {"path": str(path), "status": "no-op", "matches": 0}

    if dry_run:
        return {"path": str(path), "status": "preview", "matches": n}

    # Write mode: backup then overwrite
    try:
        backup_path = backup_file(path, quarantine_dir)
        path.write_text(cleaned, encoding="utf-8")
        return {"path": str(path), "status": "updated", "matches": n, "backup": str(backup_path)}
    except Exception as e:
        return {"path": str(path), "status": "error", "reason": str(e)}


def walk_and_process(root: Path, dry_run: bool, target_file: str | None) -> list[dict]:
    results = []
    quarantine_dir = root / "quarantine"
    logs_dir = root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    if target_file:
        path = (root / target_file).resolve()
        if not path.exists():
            return [{"path": str(path), "status": "skip", "reason": "not-found"}]
        if not is_text_file(path):
            return [{"path": str(path), "status": "skip", "reason": "non-text"}]
        results.append(process_file(path, dry_run, quarantine_dir, logs_dir))
        return results

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for name in filenames:
            p = Path(dirpath) / name
            if not is_text_file(p):
                continue
            results.append(process_file(p, dry_run, quarantine_dir, logs_dir))
    return results


def write_report(results: list[dict], logs_dir: Path, dry_run: bool) -> Path:
    updated = [r for r in results if r.get("status") in {"updated", "preview"}]
    total_matches = sum(r.get("matches", 0) for r in updated)
    mode = "DRY-RUN" if dry_run else "WRITE"
    report_path = logs_dir / f"placeholder_cleanup_{mode.lower()}.txt"

    lines = [
        f"Placeholder cleanup report ({mode})",
        f"Token: {TOKEN}",
        f"Files impacted: {len(updated)}",
        f"Total matches: {total_matches}",
        "",
    ]
    for r in sorted(updated, key=lambda x: x.get("matches", 0), reverse=True):
        line = f"{r.get('matches', 0):5d} | {r.get('status'):8s} | {r.get('path')}"
        if r.get("backup"):
            line += f" | backup: {r['backup']}"
        lines.append(line)

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Remove placeholder tokens from files and back up originals.")
    parser.add_argument("--path", dest="target_file", help="Specific file path relative to repo root", default=None)
    parser.add_argument("--write", action="store_true", help="Apply changes (default is dry-run)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    results = walk_and_process(root, dry_run=not args.write, target_file=args.target_file)

    logs_dir = root / "logs"
    report = write_report(results, logs_dir, dry_run=not args.write)

    impacted = [r for r in results if r.get("status") in {"updated", "preview"}]
    print(f"Cleanup complete. Mode: {'DRY-RUN' if not args.write else 'WRITE'} | Files impacted: {len(impacted)} | Report: {report}")


if __name__ == "__main__":
    main()
