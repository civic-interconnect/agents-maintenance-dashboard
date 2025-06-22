"""
app_agents.__main__

Entrypoint for running the CLI with:

py -m app_agents
python -m app_agents
python3 -m app_agents

Usage depends on your operating system and Python installation.
"""

from app_agents.cli.cli import app

if __name__ == "__main__":
    app()
