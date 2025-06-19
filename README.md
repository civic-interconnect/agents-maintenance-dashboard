# agents-maintenance-dashboard


> Agent Status Dashboard for Civic Interconnect

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/civic-interconnect/agents-maintenance-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-maintenance-dashboard/actions/workflows/main.yml/badge.svg)](https://github.com/civic-interconnect/agents-maintenance-dashboard/actions)

**Live Dashboard:** [View Live Site](https://civic-interconnect.github.io/agents-maintenance-dashboard/)

GitHub Pages dashboard displaying Civic Interconnect Agent status, commit info, schema sources, and success indicators.

## Local development

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip uninstall civic-lib -y
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements-dev.txt --timeout 100 --no-cache-dir
pre-commit install
py scripts/main.py
```

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

First: Update these files to the new version:

1. VERSION file
2. README.md (update version badge)

Then run the following:

```shell
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
ruff check . --fix
pre-commit run --all-files

# Optional: delete existing tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# State, commit, create the release tag, and push
git add .
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
```

## Test Web App Locally

```powershell
cd docs
py -m http.server 8000
```

Visit: <http://localhost:8000>

[View Live Site](https://civic-interconnect.github.io/agents-maintenance-dashboard/)

![Screenshot of Civic Interconnect Dashboard](images/screenshot.png)
