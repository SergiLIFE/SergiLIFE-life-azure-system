"""
Python source cleaner and sanitizer.

Goals:
- Remove BOM and zero-width chars
- Normalize smart quotes and dashes
- Strip emojis and other non-text symbols
- Remove/control invalid control characters (keep \t\r\n)
- Comment out Git merge conflict markers
- Normalize whitespace/blank lines
- Optionally restrict to ASCII only
- Verify AST parseability

Designed for large files; operates line-by-line where possible.
"""
from __future__ import annotations

import argparse
import ast
import io
import os
import re
import sys
from typing import Iterable


# Unicode ranges for emoji and dingbats etc.
EMOJI_REGEX = re.compile(
    "[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0001F1E6-\U0001F1FF\U000024C2-\U0001F251]",
    flags=re.UNICODE,
)

# Zero-width and BOM
ZERO_WIDTH = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"]
ZERO_WIDTH_RE = re.compile("[" + "".join(ZERO_WIDTH) + "]")

# Control chars except tab/newline/carriage-return
CONTROL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

SMART_QUOTES = {
    "\u2018": "'",  # ‘
    "\u2019": "'",  # ’
    "\u201C": '"',  # “
    "\u201D": '"',  # ”
    "\u2032": "'",  # ′
    "\u2033": '"',  # ″
}

DASHES = {
    "\u2013": "-",  # –
    "\u2014": "-",  # —
    "\u2212": "-",  # −
}

NON_BREAKING_SPACE_RE = re.compile("\u00A0")

CONFLICT_MARKERS = (
    "<<<<<<< ",
    "=======",
    ">>>>>>> ",
)


def _normalize_line(line: str) -> str:
    # Remove zero-width and BOM
    line = ZERO_WIDTH_RE.sub("", line)
    # Replace non-breaking spaces
    line = NON_BREAKING_SPACE_RE.sub(" ", line)
    # Replace smart quotes and dashes
    for k, v in SMART_QUOTES.items():
        if k in line:
            line = line.replace(k, v)
    for k, v in DASHES.items():
        if k in line:
            line = line.replace(k, v)
    # Remove emojis
    line = EMOJI_REGEX.sub("", line)
    # Remove other control characters except tab/newline/CR
    line = CONTROL_RE.sub("", line)
    return line


def _comment_conflict_markers(line: str) -> str:
    stripped = line.lstrip()
    for marker in CONFLICT_MARKERS:
        if stripped.startswith(marker):
            # Prefix with '# ' preserving leading indentation
            prefix_len = len(line) - len(stripped)
            return line[:prefix_len] + "# " + stripped
    return line


def clean_source(text: str, max_blank_lines: int = 2, ascii_only: bool = False) -> str:
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out_lines: list[str] = []
    blank_run = 0
    for raw_line in text.split("\n"):
        line = _normalize_line(raw_line)
        line = _comment_conflict_markers(line)
        # Strip trailing whitespace
        line = line.rstrip()
        if ascii_only:
            # Best-effort ASCII: replace non-ASCII with space
            line = line.encode("ascii", errors="ignore").decode("ascii")
        if line.strip() == "":
            blank_run += 1
            if blank_run > max_blank_lines:
                continue
        else:
            blank_run = 0
        out_lines.append(line)
    cleaned = "\n".join(out_lines)
    # Ensure file ends with a single newline
    if not cleaned.endswith("\n"):
        cleaned += "\n"
    return cleaned


def verify_ast_parseable(text: str) -> tuple[bool, str | None]:
    try:
        ast.parse(text)
        return True, None
    except SyntaxError as e:
        # Provide a compact error report
        loc = f"line {e.lineno}, col {e.offset}"
        msg = f"SyntaxError at {loc}: {e.msg}"
        # Include a small excerpt if available
        if e.text:
            excerpt = e.text.strip().replace("\n", "\\n")
            msg += f" | excerpt: {excerpt}"
        return False, msg
    except Exception as e:
        return False, f"Non-syntax error during AST parse: {type(e).__name__}: {e}"


def _read_text(path: str) -> str:
    # Read with replacement to survive encoding glitches
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Clean and sanitize a Python source file.")
    p.add_argument("src", help="Source .py file path")
    p.add_argument("dst", nargs="?", help="Destination .py file path (defaults to src when --inplace)")
    p.add_argument("--inplace", action="store_true", help="Modify the source file in place")
    p.add_argument("--ascii-only", action="store_true", help="Drop all non-ASCII chars after normalization")
    p.add_argument("--max-blank-lines", type=int, default=2, help="Maximum consecutive blank lines to keep")
    p.add_argument("--verify-ast", action="store_true", help="Verify file parses with ast")
    p.add_argument("--report", help="Optional report file path for verification details")
    args = p.parse_args(list(argv) if argv is not None else None)

    if not os.path.exists(args.src):
        print(f"ERROR: Source not found: {args.src}", file=sys.stderr)
        return 2

    raw = _read_text(args.src)
    cleaned = clean_source(raw, max_blank_lines=args.max_blank_lines, ascii_only=args.ascii_only)

    if args.inplace:
        dst_path = args.src
    else:
        if not args.dst:
            print("ERROR: Provide destination path or use --inplace", file=sys.stderr)
            return 2
        dst_path = args.dst

    _write_text(dst_path, cleaned)

    ok, msg = True, None
    if args.verify_ast:
        ok, msg = verify_ast_parseable(cleaned)

    if args.report:
        report = io.StringIO()
        report.write(f"source: {args.src}\n")
        report.write(f"dest:   {dst_path}\n")
        report.write(f"ascii_only: {args.ascii_only}\n")
        report.write(f"verify_ast: {args.verify_ast}\n")
        report.write(f"result: {'OK' if ok else 'FAIL'}\n")
        if msg:
            report.write(f"details: {msg}\n")
        _write_text(args.report, report.getvalue())

    if args.verify_ast:
        if ok:
            print("AST verification: OK")
            return 0
        else:
            print("AST verification: FAIL")
            if msg:
                print(msg)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
