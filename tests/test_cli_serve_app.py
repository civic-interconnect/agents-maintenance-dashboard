from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from app_agents.cli.cli import app

runner = CliRunner()


@patch("app_agents.cli.serve_app.subprocess.run")
def test_cli_serve_app(mock_subprocess_run):
    # Set up mocks
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    with runner.isolated_filesystem():
        Path("docs").mkdir()
        Path("docs/index.html").write_text("<html><body>Test</body></html>")

        result = runner.invoke(app, ["serve-app"])
        print("CLI output:\n", result.output)

        assert result.exit_code == 0
        assert "Serving app at http://localhost:8000" in result.output

        if not mock_subprocess_run.called:
            pytest.fail("Expected subprocess.run to be called.")
