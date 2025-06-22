"""
fetch_status.py

Update application data files for Civic Interconnect agents.

This command runs update scripts or functions responsible for refreshing
data files (e.g., JSON, YAML) used by the application.

Intended for manual or scheduled use to ensure data freshness.
"""

import typer

from setup import fetch_status

app = typer.Typer(help="Update local JSON and structured data files.")


@app.command("fetch-status")
def main():
    """
    Run update tasks to refresh app data.
    """
    typer.echo("Fetching agent status data...")
    try:
        fetch_status.main()
        typer.echo("Fetch status complete.")
    except Exception as e:
        typer.echo(f"Error during fetch-status: {e}")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    main()
