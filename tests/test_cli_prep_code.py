"""
tests/test_cli_prep_code.py

"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from app_agents.cli.cli import app

runner = CliRunner()


@patch("app_agents.cli.prep_code.subprocess.run")
@patch("app_agents.cli.prep_code.init_venv.main")
def test_cli_prep_code(mock_init_venv, mock_subprocess_run):
    # Quick-fail if essential script is missing
    required_file = Path("src/app_agents/cli/prep_code.py")
    if not required_file.exists():
        pytest.fail(f"Required file not found: {required_file}")

    # Set up mocks
    mock_subprocess_run.return_value = MagicMock(returncode=0)
    mock_init_venv.return_value = MagicMock(returncode=0)

    result = runner.invoke(app, ["prep-code"])

    # Print CLI output for diagnostics
    print("CLI output:\n", result.output)

    assert result.exit_code == 0
    assert "Formatting code with Ruff..." in result.output
    assert "Linting and fixing issues with Ruff..." in result.output

    # Allow either subprocess.run or init_venv to be triggered
    if not mock_init_venv.called and not mock_subprocess_run.called:
        pytest.fail("Expected subprocess.run or init_venv.run to be called.")
