"""
Build deployment_package.zip for Azure Functions config-zip deployment.
Selects core modules and requirements. Run with Python 3 on Windows or Linux.
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "deployment_package.zip"

INCLUDE = [
    "azure_functions_workflow.py",
    "azure_functions_config.py",
    "clinical_validation_framework.py",
    "eeg_iothub_stream.py",
    "kpi_monitor.py",
    "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
]

REQS = [
    "requirements.txt",
    "azure_functions_requirements.txt",
]


def add_file(zf: zipfile.ZipFile, path: Path, arcname: str):
    if path.exists():
        zf.write(path, arcname)


def main():
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in INCLUDE:
            add_file(zf, ROOT / name, name)
        # Include requirements file fallback
        for req in REQS:
            p = ROOT / req
            if p.exists():
                add_file(zf, p, req)
                break
    print(f"[OK] Built: {OUT}")


if __name__ == "__main__":
    main()
