"""
scripts/main.py

This Python file fetches information from the various GitHub repositories of the Civic Interconnect agents,
compiles their statuses, and generates a JSON report that is saved to the `docs` directory.
It includes details such as the latest version, last commit date, action status, and report URLs
and key information from their most recent reports.

"""

import json
import requests
import yaml
from civic_lib_core import log_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.config_utils import load_version

from pathlib import Path

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
    try:
        response = requests.get(report_url)
        if response.status_code == 200:
            return yaml.safe_load(response.text)
        elif response.status_code == 404 and "schema-report.yaml" in report_url:
            # Try change-report.yaml instead
            fallback_url = report_url.replace(
                "schema-report.yaml", "change-report.yaml"
            )
            fallback_response = requests.get(fallback_url)
            if fallback_response.status_code == 200:
                return yaml.safe_load(fallback_response.text)
            else:
                logger.warning(
                    f"Fallback also failed: {fallback_url} (status {fallback_response.status_code})"
                )
        else:
            logger.warning(
                f"Could not fetch YAML report: {report_url} (status {response.status_code})"
            )
    except Exception as e:
        logger.error(f"Error fetching YAML report from {report_url}: {e}")
    return {}


def get_latest_action_status(repo):
    url = (
        f"https://api.github.com/repos/{ORG}/{repo}/actions/runs?branch=main&per_page=1"
    )
    response = requests.get(url)
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        if runs:
            conclusion = runs[0].get("conclusion", "in_progress")
            return (
                f"{conclusion.capitalize()}"
                if conclusion == "success"
                else f"{conclusion.capitalize()}"
            )
    return "unknown"


def get_latest_commit(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/commits/main"
    response = requests.get(url)
    if response.status_code == 200:
        commit = response.json()
        date = commit["commit"]["committer"]["date"]
        return date[:10]  # YYYY-MM-DD
    return "unknown"


def get_latest_tag(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/tags"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()[0]["name"]
    return "none"


def get_report_url(repo, commit_date):
    report_type = repo.replace("agents-monitor-", "")  # e.g., "mapping"
    filename = f"{commit_date}-{report_type}-report.yaml"
    path = f"reports/{commit_date}/{filename}"
    return f"https://raw.githubusercontent.com/{ORG}/{repo}/main/{path}"


def main():
    logger.info("===== Starting Dashboard Update =====")

    ROOT_DIR = Path(__file__).resolve().parent.parent
    logger.info(f"Root directory: {ROOT_DIR}")
    dashboard_version = load_version("VERSION")

    data = []

    for repo in AGENTS:
        version = get_latest_tag(repo)
        last_commit = get_latest_commit(repo)
        action_status = get_latest_action_status(repo)
        report_url = get_report_url(repo, last_commit)

        logger.info(
            f"{repo}: {version}, last_commit={last_commit}, status={action_status}"
        )
        report_data = fetch_yaml_report_data(report_url)

        agent_status = {
            "name": repo,
            "repo": f"https://github.com/{ORG}/{repo}",
            "version": version,
            "last_commit": last_commit,
            "action_status": action_status,
            "schema_source": "OpenStates"
            if "people" in repo or "bills" in repo
            else "OCD",
        }
        # Add YAML report information
        for key, value in report_data.items():
            if key not in ["version", "date"]:  # skip duplicate fields
                agent_status[key] = value

        data.append(agent_status)

    dashboard_status = {
        "dashboard_version": dashboard_version,
        "generated": today_utc_str(),
        "agents": data,
    }

    output_file = Path("docs/status.json")
    output_file.write_text(json.dumps(dashboard_status, indent=2))
    logger.info(f"Wrote status.json with {len(data)} agents to {output_file}")
    logger.info("===== Dashboard Update Complete =====")


if __name__ == "__main__":
    main()
