#!/usr/bin/env python3
r"""
Emoji Sanitizer (Windows-friendly)

Removes emoji and common decorative symbols from file contents and optionally
renames files/folders to ASCII-only names. Designed for Windows-first repos.

Usage examples (cmd.exe):
    python tools\emoji_sanitizer.py --dry-run
    python tools\emoji_sanitizer.py --write
    python tools\emoji_sanitizer.py --write --rename

By default, scans the workspace root (this script's grandparent) and processes
text files with common source/doc extensions. Skips .git, .venv and typical
dependency folders.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from typing import Iterable, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))


# Broad emoji + symbols ranges (covers most UI emoji and dingbats) as numeric codepoints
EMOJI_RANGES: Tuple[Tuple[int, int], ...] = (
    (0x1F300, 0x1F5FF),  # Misc Symbols & Pictographs
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F680, 0x1F6FF),  # Transport & Map
    (0x1F700, 0x1F77F),
    (0x1F780, 0x1F7FF),
    (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF),
    (0x1FA00, 0x1FA6F),
    (0x1FA70, 0x1FAFF),
    (0x2700, 0x27BF),  # Dingbats
    (0x2600, 0x26FF),  # Misc Symbols
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2300, 0x23FF),  # Misc Technical
    (0x1F1E6, 0x1F1FF),  # Regional indicator symbols (flags)
)

# Variation Selectors and joiners often used with emoji
ZWJ = "\u200d"
VS16 = "\ufe0f"
VS15 = "\ufe0e"
ZEROWIDTHS = [ZWJ, VS16, VS15, "\u200b", "\u2060"]


DEFAULT_EXTENSIONS = {
    ".py",
    ".bat",
    ".cmd",
    ".ps1",
    ".sh",
    ".md",
    ".txt",
    ".html",
    ".htm",
    ".css",
    ".js",
    ".json",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
}

SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__"}


def is_text_file(path: str, allowed_ext: Iterable[str]) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in allowed_ext


def _is_emoji_cp(cp: int) -> bool:
    for a, b in EMOJI_RANGES:
        if a <= cp <= b:
            return True
    return False


def strip_emojis(text: str) -> str:
    # Remove emoji codepoints by numeric range match
    cleaned_chars: List[str] = []
    for ch in text:
        cp = ord(ch)
        if _is_emoji_cp(cp):
            continue
        cleaned_chars.append(ch)
    cleaned = "".join(cleaned_chars)
    # Remove common zero-width/variation selectors
    for zw in ZEROWIDTHS:
        cleaned = cleaned.replace(zw, "")
    return cleaned


def sanitize_filename(name: str) -> str:
    # Normalize to ASCII-only by removing diacritics and non-ASCII
    norm = unicodedata.normalize("NFKD", name)
    ascii_name = norm.encode("ascii", "ignore").decode("ascii")
    # Remove characters invalid in Windows filenames
    ascii_name = re.sub(r"[<>:\\/\|\?\*]", "-", ascii_name)
    # Collapse runs of spaces/dashes
    ascii_name = re.sub(r"[\s\-]+", " ", ascii_name).strip()
    return ascii_name or "file"


def walk_files(root: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            yield os.path.join(dirpath, f)


def process_files(
    root: str, *, write: bool, rename: bool, exts: Iterable[str]
) -> Tuple[List[str], List[Tuple[str, str]], List[str]]:
    modified: List[str] = []
    renamed: List[Tuple[str, str]] = []
    errors: List[str] = []

    for path in walk_files(root):
        try:
            rel = os.path.relpath(path, root)
            if is_text_file(path, exts):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    original = f.read()
                cleaned = strip_emojis(original)
                if cleaned != original:
                    modified.append(rel)
                    if write:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(cleaned)

            if rename:
                dirname, basename = os.path.split(path)
                new_basename = strip_emojis(basename)
                new_basename = sanitize_filename(new_basename)
                if new_basename != basename:
                    new_path = os.path.join(dirname, new_basename)
                    if write:
                        # Ensure we don't overwrite an existing file unintentionally
                        if not os.path.exists(new_path):
                            os.rename(path, new_path)
                            renamed.append((rel, os.path.relpath(new_path, root)))
                        else:
                            # If collision, append a numeric suffix
                            base, ext = os.path.splitext(new_basename)
                            i = 1
                            candidate = new_path
                            while os.path.exists(candidate):
                                candidate = os.path.join(dirname, f"{base}_{i}{ext}")
                                i += 1
                            os.rename(path, candidate)
                            renamed.append((rel, os.path.relpath(candidate, root)))
                    else:
                        renamed.append((rel, os.path.relpath(new_path, root)))

        except Exception as e:
            errors.append(f"{rel}: {e}")

    return modified, renamed, errors


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Remove emojis from files and optionally rename them to ASCII-only names."
    )
    p.add_argument(
        "--root", default=REPO_ROOT, help="Root directory to scan (default: repo root)"
    )
    p.add_argument(
        "--write", action="store_true", help="Apply changes (otherwise dry-run)"
    )
    p.add_argument(
        "--rename", action="store_true", help="Also rename files/folders to ASCII-only"
    )
    p.add_argument(
        "--exts",
        nargs="*",
        default=sorted(DEFAULT_EXTENSIONS),
        help="File extensions to include (default: common text types)",
    )
    args = p.parse_args(argv)

    print("Emoji Sanitizer")
    print("================")
    print(f"Root: {os.path.abspath(args.root)}")
    print(f"Mode: {'WRITE' if args.write else 'DRY-RUN'} | Rename: {args.rename}")
    print(f"Extensions: {', '.join(args.exts)}")

    modified, renamed, errors = process_files(
        args.root,
        write=args.write,
        rename=args.rename,
        exts=set(e.lower() for e in args.exts),
    )

    print("")
    print(f"Files with content changes: {len(modified)}")
    for m in modified[:50]:
        print(f"  * {m}")
    if len(modified) > 50:
        print(f"  ... and {len(modified)-50} more")

    print("")
    print(f"Files renamed: {len(renamed)}")
    for old, new in renamed[:50]:
        print(f"  * {old} -> {new}")
    if len(renamed) > 50:
        print(f"  ... and {len(renamed)-50} more")

    if errors:
        print("")
        print(f"Errors: {len(errors)}")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more")

    print("")
    if not args.write:
        print("DRY RUN complete. Re-run with --write to apply changes.")
    else:
        print("Sanitization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
