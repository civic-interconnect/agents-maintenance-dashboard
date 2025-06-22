"""
scripts/init_venv.py

Install Civic Interconnect project dependencies into an existing `.venv`.

This script:
- Verifies `.venv` exists and is not empty
- Installs required and dev dependencies via `pyproject.toml`
- Installs pre-commit hooks

Does NOT create or activate the virtual environment.
"""

import os
import subprocess
import sys
from pathlib import Path

__all__ = ["main", "get_venv_dir"]

VENV_DIR = Path(".venv")


def get_venv_dir():
    """Return the absolute path to the `.venv` directory."""
    return VENV_DIR.resolve()


def run(cmd, shell=False):
    print(f"Run: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    subprocess.run(cmd, shell=shell, check=True)


def verify_venv():
    """Ensure .venv exists and has a Python binary."""
    if not VENV_DIR.exists():
        print("Error: .venv directory not found.")
        sys.exit(1)

    python_bin = (
        VENV_DIR / "Scripts" / "python.exe" if os.name == "nt" else VENV_DIR / "bin" / "python"
    )

    if not python_bin.exists():
        print(f"Error: Python not found in {python_bin}")
        sys.exit(1)

    return python_bin


def install_dependencies(python_bin):
    """Install pip, runtime dependencies, and pre-commit hooks."""

    # Upgrade base tools
    run([
        str(python_bin),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "setuptools",
        "wheel",
        "--prefer-binary",
    ])

    # Install runtime deps from pyproject.toml (non-editable, no dev extras)
    run([
        str(python_bin),
        "-m",
        "pip",
        "install",
        ".[dev]",
        "--timeout",
        "100",
        "--no-cache-dir",
        "--prefer-binary",
    ])

    # Optionally install dev requirements separately
    req_file = Path("requirements-dev.txt")
    if req_file.exists():
        run([
            str(python_bin),
            "-m",
            "pip",
            "install",
            "-r",
            str(req_file),
            "--timeout",
            "100",
            "--no-cache-dir",
        ])

    # Finally install pre-commit if available
    try:
        run([str(python_bin), "-m", "pre_commit", "install"])
    except subprocess.CalledProcessError:
        print("Skipped pre-commit installation — not installed?")


def main(reinstall=False):
    print("Verifying virtual environment...")
    python_bin = verify_venv()

    print("Installing dependencies...")
    install_dependencies(python_bin)

    print("Environment setup complete.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Setup failed: {e}")
        sys.exit(1)
