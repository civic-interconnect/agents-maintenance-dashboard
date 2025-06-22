"""
fetch_status.py

Fetches GitHub metadata and YAML report data for Civic Interconnect agents,
then compiles a unified dashboard status report.

This script:
- Queries GitHub for the latest tags, commit dates, and Actions status.
- Attempts to retrieve the latest YAML report from each agent repository.
- Aggregates all results into a single JSON structure.
- Writes the output to `docs/status.json` for dashboard use.

Usage:
    python src/setup/fetch_status.py

Dependencies:
    - civic_lib_core (for logging, versioning, date utilities)
    - requests, PyYAML

Safe to run multiple times. Each run refreshes live GitHub and report data.
"""

import json
from pathlib import Path

import requests
import yaml
from civic_lib_core import log_utils
from civic_lib_core.config_utils import load_version
from civic_lib_core.date_utils import today_utc_str

log_utils.init_logger()
logger = log_utils.logger

ORG = "civic-interconnect"
AGENTS = [
    "agents-monitor-schema",
    "agents-monitor-mapping",
    "agents-monitor-bills",
    "agents-monitor-people",
]


def fetch_yaml_report_data(report_url):
    """Attempt to download and parse a YAML report from a known URL."""
    try:
        response = requests.get(report_url)
        if response.status_code == 200:
            return yaml.safe_load(response.text) or {}
        if response.status_code == 404 and "schema-report.yaml" in report_url:
            fallback_url = report_url.replace("schema-report.yaml", "change-report.yaml")
            fallback_response = requests.get(fallback_url)
            if fallback_response.status_code == 200:
                return yaml.safe_load(fallback_response.text) or {}
            logger.warning(
                f"Fallback also failed: {fallback_url} ({fallback_response.status_code})"
            )
        else:
            logger.warning(f"Could not fetch YAML report: {report_url} ({response.status_code})")
    except Exception as e:
        logger.error(f"Error fetching YAML report from {report_url}: {e}")
    return {}


def get_latest_action_status(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/actions/runs?branch=main&per_page=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs:
                return runs[0].get("conclusion", "in_progress").capitalize()
    except Exception as e:
        logger.error(f"Error getting Actions status for {repo}: {e}")
    return "Unknown"


def get_latest_commit(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/commits/main"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["commit"]["committer"]["date"][:10]
    except Exception as e:
        logger.error(f"Error getting latest commit for {repo}: {e}")
    return "Unknown"


def get_latest_tag(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/tags"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            tags = response.json()
            if tags:
                return tags[0]["name"]
    except Exception as e:
        logger.error(f"Error getting tag for {repo}: {e}")
    return "None"


def get_report_url(repo, commit_date):
    report_type = repo.replace("agents-monitor-", "")
    filename = f"{commit_date}-{report_type}-report.yaml"
    return f"https://raw.githubusercontent.com/{ORG}/{repo}/main/reports/{commit_date}/{filename}"


def normalize_key(key):
    return key.strip().replace(" ", "_").lower()


def main():
    logger.info("===== Starting Dashboard Update =====")

    try:
        dashboard_version = load_version("VERSION")
    except Exception as e:
        logger.error(f"Failed to load dashboard version: {e}")
        dashboard_version = "unknown"

    data = []

    for repo in AGENTS:
        version = get_latest_tag(repo)
        last_commit = get_latest_commit(repo)
        action_status = get_latest_action_status(repo)
        report_url = get_report_url(repo, last_commit)

        logger.info(f"{repo}: version={version}, commit={last_commit}, status={action_status}")
        report_data = fetch_yaml_report_data(report_url)

        agent_status = {
            "name": repo,
            "repo": f"https://github.com/{ORG}/{repo}",
            "version": version,
            "last_commit": last_commit,
            "action_status": action_status,
            "schema_source": "OpenStates" if any(k in repo for k in ["people", "bills"]) else "OCD",
            "report_url": report_url,
        }

        if report_data:
            for k, v in report_data.items():
                if k in ["version", "date"]:
                    continue
                norm_key = normalize_key(k)
                agent_status[norm_key] = v
        else:
            agent_status["note"] = "No report available."

        data.append(agent_status)

    dashboard_status = {
        "dashboard_version": dashboard_version,
        "generated": today_utc_str(),
        "agents": data,
    }

    output_path = Path("docs/status.json")
    try:
        output_path.write_text(json.dumps(dashboard_status, indent=2))
        logger.info(f"Wrote status.json with {len(data)} agents to {output_path}")
    except Exception as e:
        logger.error(f"Error writing output: {e}")

    logger.info("===== Dashboard Update Complete =====")


if __name__ == "__main__":
    main()
