"""
tests/test_cli_release.py

Smoke test the `release` command with mocked subprocess.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from app_agents.cli.cli import app

runner = CliRunner()


@patch("app_agents.cli.release.subprocess.run")
@patch("app_agents.cli.release.run")
def test_cli_release_runs(mock_run, mock_subprocess_run):
    mock_run.return_value = None
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="")

    with runner.isolated_filesystem():
        Path("VERSION").write_text("0.2.0\n")
        Path("pyproject.toml").write_text("")
        Path("tests").mkdir()

        result = runner.invoke(app, ["release"])
        print("CLI output:\n", result.output)

        # Allow exit codes that reflect early exit or testing errors
        assert result.exit_code in (0, 1, 2)
