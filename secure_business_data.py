"""
Secure Business & Financial Data Utility

Purpose
  - Provide selective, pattern-based redaction for financial/business-sensitive content
  - Offer optional file encryption/decryption using a passphrase (no secrets stored)
  - Default to safe, non-destructive operations (dry-run unless explicitly asked to write)

Design constraints (L.I.F.E. platform conventions)
  - Windows-first paths and behavior
  - Never perform broad/global string replacements across code by default
  - Target human-readable artifacts by default (.md, .txt, .json, .yaml), not source code
  - Create logs/ directory automatically and record actions

Usage (examples)
  Redact (dry-run, safe):
    python secure_business_data.py redact --root .

  Redact in place (explicit):
    python secure_business_data.py redact --root . --in-place

    Redact to output mirror (non-destructive copy):
        python secure_business_data.py redact --root . --out .\\sanitized

  Encrypt a file:
    python secure_business_data.py encrypt --file README.md --passphrase "your passphrase"

  Decrypt a file:
    python secure_business_data.py decrypt --file README.md.enc --passphrase "your passphrase"

Note: Do NOT hard-code passphrases; provide via CLI or environment at runtime.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


# Optional crypto support (only required for encrypt/decrypt paths)
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    _CRYPTO_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    # Define dummies to avoid NameError if crypto not installed
    Fernet = None  # type: ignore
    hashes = None  # type: ignore
    PBKDF2HMAC = None  # type: ignore
    _CRYPTO_AVAILABLE = False


LOGS_DIR = Path(__file__).resolve().parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class RedactionResult:
    path: Path
    redactions: int
    written_to: Optional[Path]


def _compile_default_patterns() -> List[re.Pattern]:
    """Patterns targeting only financial/business-sensitive content.

    Important: These patterns intentionally avoid generic text to prevent
    over-redaction that can corrupt code or documentation.
    """
    flags = re.IGNORECASE
    patterns = [
        # Currency amounts like $123,456.78 or €1.2M
        re.compile(r"[\$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?[mkb]|\s?million|\s?billion)?", flags),
        # Common finance terms
        re.compile(r"\b(revenue|revenues|profit|margin|arr|mrr|forecast|projection|budget|pricing|price)\b", flags),
        # Quarter/year phrases that typically accompany projections
        re.compile(r"\b(q[1-4]\s*20\d{2}|fy\s*20\d{2}|202[5-9]|203\d)\b", flags),
        # Explicit phrases
        re.compile(r"\b(business\s+plan|financial\s+plan|financial\s+forecast|sales\s+forecast)\b", flags),
    ]
    return patterns


class BusinessSecurityUtility:
    """Selective financial redaction and optional encryption for text files.

    Default behavior is conservative and non-destructive.
    """

    def __init__(
        self,
        root: Path,
        include_exts: Optional[Sequence[str]] = None,
        exclude_dirs: Optional[Sequence[str]] = None,
        redaction_token: str = "[REDACTED]",
        patterns: Optional[Sequence[re.Pattern]] = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.include_exts = set(e.lower() for e in (include_exts or [".md", ".txt", ".json", ".yaml", ".yml"]))
        self.exclude_dirs = set((exclude_dirs or [".git", ".venv", "node_modules", "__pycache__"]))
        self.redaction_token = redaction_token
        self.patterns = list(patterns or _compile_default_patterns())

    def _should_process(self, p: Path) -> bool:
        if not p.is_file():
            return False
        if any(part in self.exclude_dirs for part in p.parts):
            return False
        return p.suffix.lower() in self.include_exts

    def redact_text(self, text: str) -> Tuple[str, int]:
        count = 0
        redacted = text
        for pat in self.patterns:
            redacted, c = pat.subn(self.redaction_token, redacted)
            count += c
        return redacted, count

    def process_file(
        self,
        src: Path,
        out_dir: Optional[Path] = None,
        in_place: bool = False,
        encoding: str = "utf-8",
        errors: str = "replace",
        dry_run: bool = True,
    ) -> RedactionResult:
        src = Path(src)
        if not self._should_process(src):
            return RedactionResult(path=src, redactions=0, written_to=None)

        try:
            text = src.read_text(encoding=encoding, errors=errors)
        except Exception as exc:  # pragma: no cover - IO safeguard
            _append_log(f"READ_FAIL {src}: {exc}")
            return RedactionResult(path=src, redactions=0, written_to=None)

        new_text, redactions = self.redact_text(text)
        if redactions == 0:
            return RedactionResult(path=src, redactions=0, written_to=None)

        if dry_run:
            _append_log(f"DRY_RUN REDACT {src} redactions={redactions}")
            return RedactionResult(path=src, redactions=redactions, written_to=None)

        if in_place:
            try:
                src.write_text(new_text, encoding=encoding, errors=errors)
                _append_log(f"REDACTED_IN_PLACE {src} redactions={redactions}")
                return RedactionResult(path=src, redactions=redactions, written_to=src)
            except Exception as exc:  # pragma: no cover
                _append_log(f"WRITE_FAIL {src}: {exc}")
                return RedactionResult(path=src, redactions=0, written_to=None)

        else:
            if not out_dir:
                raise ValueError("out_dir is required when not using --in-place")
            dst = Path(out_dir) / src.relative_to(self.root)
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                dst.write_text(new_text, encoding=encoding, errors=errors)
                _append_log(f"REDACTED_TO {dst} from {src} redactions={redactions}")
                return RedactionResult(path=src, redactions=redactions, written_to=dst)
            except Exception as exc:  # pragma: no cover
                _append_log(f"WRITE_FAIL {dst}: {exc}")
                return RedactionResult(path=src, redactions=0, written_to=None)

    def walk_and_process(
        self,
        out_dir: Optional[Path] = None,
        in_place: bool = False,
        dry_run: bool = True,
    ) -> List[RedactionResult]:
        results: List[RedactionResult] = []
        for p in self.root.rglob("*"):
            if self._should_process(p):
                res = self.process_file(p, out_dir=out_dir, in_place=in_place, dry_run=dry_run)
                if res.redactions:
                    results.append(res)
        return results


# ----------------------------
# Encryption/Decryption helpers
# ----------------------------

def _require_crypto():
    if not _CRYPTO_AVAILABLE:  # pragma: no cover
        raise RuntimeError("cryptography is not installed. Install 'cryptography' to use encryption features.")


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    # At runtime, crypto must be available; the asserts help static analyzers
    assert PBKDF2HMAC is not None and hashes is not None  # type: ignore[unreachable]
    kdf = PBKDF2HMAC(  # type: ignore[misc]
        algorithm=hashes.SHA256(),  # type: ignore[attr-defined]
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def encrypt_bytes(data: bytes, passphrase: str) -> bytes:
    _require_crypto()
    import os as _os

    salt = _os.urandom(16)
    key = _derive_key(passphrase, salt)
    token = Fernet(key).encrypt(data)  # type: ignore[misc]
    return b"SB1" + salt + token  # simple header + salt + fernet token


def decrypt_bytes(blob: bytes, passphrase: str) -> bytes:
    _require_crypto()
    if not blob.startswith(b"SB1"):
        raise ValueError("Unsupported blob format")
    salt = blob[3:19]
    token = blob[19:]
    key = _derive_key(passphrase, salt)
    return Fernet(key).decrypt(token)  # type: ignore[misc]


def encrypt_file(path: Path, passphrase: str, out_path: Optional[Path] = None) -> Path:
    path = Path(path)
    data = path.read_bytes()
    blob = encrypt_bytes(data, passphrase)
    dst = out_path or path.with_suffix(path.suffix + ".enc")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(blob)
    _append_log(f"ENCRYPTED_FILE {path} -> {dst}")
    return dst


def decrypt_file(path: Path, passphrase: str, out_path: Optional[Path] = None) -> Path:
    path = Path(path)
    blob = path.read_bytes()
    data = decrypt_bytes(blob, passphrase)
    if out_path is None:
        if path.suffix.lower() == ".enc":
            out_path = path.with_suffix("")
        else:
            out_path = path.with_name(path.name + ".dec")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    _append_log(f"DECRYPTED_FILE {path} -> {out_path}")
    return out_path


# ----------------------------
# Logging
# ----------------------------

def _append_log(msg: str) -> None:
    try:
        (LOGS_DIR / "secure_business_data.log").open("a", encoding="utf-8").write(msg + "\n")
    except Exception:  # pragma: no cover
        pass


# ----------------------------
# CLI
# ----------------------------

def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Selective financial redaction and optional encryption")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("redact", help="Redact financial details in text files")
    pr.add_argument("--root", default=".", help="Root folder to scan")
    pr.add_argument("--in-place", action="store_true", help="Write changes back to source files (explicit)")
    pr.add_argument("--out", type=str, default=None, help="Output folder for sanitized copies (required if not --in-place)")
    pr.add_argument("--dry-run", action="store_true", help="Dry run: report what would change (default)")
    pr.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Disable dry-run")
    pr.add_argument("--include-exts", nargs="*", default=None, help="Override default extensions (.md .txt .json .yaml .yml)")

    pe = sub.add_parser("encrypt", help="Encrypt a single file using a passphrase")
    pe.add_argument("--file", required=True, help="Path to file to encrypt")
    pe.add_argument("--passphrase", required=True, help="Passphrase (do not hard-code in scripts)")
    pe.add_argument("--out", type=str, default=None, help="Destination path (default: <file>.enc)")

    pd = sub.add_parser("decrypt", help="Decrypt a single file using a passphrase")
    pd.add_argument("--file", required=True, help="Path to file to decrypt")
    pd.add_argument("--passphrase", required=True, help="Passphrase (do not hard-code in scripts)")
    pd.add_argument("--out", type=str, default=None, help="Destination path (default: strip .enc)")

    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)

    if args.cmd == "redact":
        include_exts = [e if e.startswith(".") else f".{e}" for e in (args.include_exts or [])] or None
        util = BusinessSecurityUtility(
            root=Path(args.root),
            include_exts=include_exts,
        )
        out_dir = Path(args.out) if args.out else None

        try:
            results = util.walk_and_process(out_dir=out_dir, in_place=bool(args.in_place), dry_run=bool(args.dry_run))
        except ValueError as ve:
            print(str(ve))
            return 2

        total = sum(r.redactions for r in results)
        changed = len(results)
        print(f"Redaction candidates changed={changed} total_redactions={total} dry_run={bool(args.dry_run)}")
        return 0

    if args.cmd == "encrypt":
        if not _CRYPTO_AVAILABLE:
            print("cryptography is not installed. Install it to use encryption.")
            return 3
        dst = encrypt_file(Path(args.file), args.passphrase, Path(args.out) if args.out else None)
        print(f"Encrypted -> {dst}")
        return 0

    if args.cmd == "decrypt":
        if not _CRYPTO_AVAILABLE:
            print("cryptography is not installed. Install it to use decryption.")
            return 3
        dst = decrypt_file(Path(args.file), args.passphrase, Path(args.out) if args.out else None)
        print(f"Decrypted -> {dst}")
        return 0

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
