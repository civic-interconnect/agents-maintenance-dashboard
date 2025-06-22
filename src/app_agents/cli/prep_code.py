"""
prep_code.py

Format, lint, and test Civic Interconnect apps.

Runs:
- Ruff format
- Ruff lint with --fix
- Pre-commit hooks (twice)
- Unit tests via pytest

Reinstalls environment if pyproject.toml or requirements.txt changed since .venv.
"""

import subprocess
from pathlib import Path

import typer

from setup import init_venv

app = typer.Typer(help="Prepare code by formatting, linting, and testing.")


def should_reinstall():
    venv_dir = init_venv.get_venv_dir()
    if not venv_dir.exists():
        return True

    venv_time = venv_dir.stat().st_mtime
    for f in ["pyproject.toml", "requirements.txt", "poetry.lock"]:
        p = Path(f)
        if p.exists() and p.stat().st_mtime > venv_time:
            return True
    return False


@app.command("prep-code")
def main():
    typer.echo("Checking virtual environment...")
    reinstall = should_reinstall()
    init_venv.main(reinstall=reinstall)

    typer.echo("Formatting code with Ruff...")
    subprocess.run(["ruff", "format", "."], check=True)

    typer.echo("Linting and fixing issues with Ruff...")
    subprocess.run(["ruff", "check", ".", "--fix"], check=True)

    typer.echo("Running pre-commit hooks (1st pass, allow fixes)...")
    subprocess.run(["pre-commit", "run", "--all-files"], check=False)

    typer.echo("Running pre-commit hooks (2nd pass, verify clean)...")
    subprocess.run(["pre-commit", "run", "--all-files"], check=True)

    typer.echo("Running unit tests...")
    subprocess.run(["pytest", "tests"], check=True)

    typer.echo("Code is formatted, linted, and tested.")


if __name__ == "__main__":
    main()
