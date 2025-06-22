"""
release.py

Automate the release process for Civic Interconnect applications.

This script:
- Reads the version from the VERSION file
- Updates pre-commit hooks
- Installs the package in editable mode
- Formats and lints the code
- Runs pre-commit hooks twice (fix + verify)
- Runs unit tests if present
- Commits changes if any are staged
- Tags the commit and pushes to GitHub

Assumes version strings have already been updated using:
    app-agents bump-version OLD_VERSION NEW_VERSION
"""

import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="Run formatting, tests, and tagging to publish a release.")


def run(cmd: str, check: bool = True) -> None:
    """
    Run a shell command and echo it.
    """
    typer.echo(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        typer.echo(f"Command failed: {cmd}")
        raise typer.Exit(result.returncode)


@app.command("release")
def main() -> None:
    """
    Complete the release workflow for the current version.
    """
    version_path = Path("VERSION")
    if not version_path.exists():
        typer.echo("VERSION file not found.")
        raise typer.Exit(1)

    version = version_path.read_text().strip().lstrip("v")
    tag = f"v{version}"

    typer.echo(f"Releasing version {tag}...")

    try:
        # Update pre-commit hooks
        run("pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks")

        # Install editable package
        if Path("pyproject.toml").exists():
            run("python -m pip install -e .")
        else:
            typer.echo("pyproject.toml not found — skipping install.")

        # Format and lint
        run("ruff format .")
        run("ruff check . --fix")

        # Pre-commit: first pass may fix
        run("pre-commit run --all-files", check=False)

        # Stage changes
        run("git add .")

        # Pre-commit: second pass may still fix more
        run("pre-commit run --all-files", check=False)

        # Stage again
        run("git add .")

        # Final check must pass
        run("pre-commit run --all-files")

        # Run tests
        if Path("tests").exists():
            run("pytest")
        else:
            typer.echo("No tests/ folder — skipping tests.")

        # Git commit if changes staged
        run("git add .")
        result = subprocess.run("git diff --cached --quiet", shell=True)
        if result.returncode == 1:
            run(f'git commit -m "Release: {tag}"')
            run("git push origin main --force")
        else:
            typer.echo("No changes to commit.")

        # Handle existing tag
        result = subprocess.run(f"git tag --list {tag}", shell=True, capture_output=True, text=True)
        if tag in result.stdout:
            typer.echo(f"Tag {tag} already exists — replacing it.")
            run(f"git tag -d {tag}")
            run(f"git push --delete origin {tag}")

        # Tag and push
        run(f"git tag {tag}")
        run(f"git push origin {tag}")

        typer.echo(f"Release {tag} completed successfully.")
    except typer.Exit:
        typer.echo("Warning: Release process halted due to errors.")
        raise


if __name__ == "__main__":
    main()
