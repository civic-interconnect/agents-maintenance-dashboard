"""
tests/test_cli_bump_version.py

Test the `bump-version` command in app_agents.cli.cli using an isolated filesystem.
"""

from pathlib import Path

from typer.testing import CliRunner

from app_agents.cli.cli import app

runner = CliRunner()


def test_cli_bump_version_in_isolated_fs():
    old_version = "0.1.0"
    new_version = "0.2.0"

    with runner.isolated_filesystem():
        # Create mock files with old version
        for filename in ["VERSION", "README.md", "pyproject.toml", "setup.cfg"]:
            Path(filename).write_text(f"Version: {old_version}\n")

        # Run bump-version
        result = runner.invoke(app, ["bump-version", old_version, new_version])

        assert result.exit_code == 0
        assert "Updated VERSION" in result.output

        # Confirm replacement occurred
        for filename in ["VERSION", "README.md", "pyproject.toml", "setup.cfg"]:
            content = Path(filename).read_text()
            assert new_version in content
            assert old_version not in content
