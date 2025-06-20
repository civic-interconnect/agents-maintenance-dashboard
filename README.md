# agents-maintenance-dashboard


> Agent Status Dashboard for Civic Interconnect

[![Version](https://img.shields.io/badge/version-v1.0.1-blue)](https://github.com/civic-interconnect/agents-maintenance-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-maintenance-dashboard/actions/workflows/app.yml/badge.svg)](https://github.com/civic-interconnect/agents-maintenance-dashboard/actions)

**Live Dashboard:** [View Live Site](https://civic-interconnect.github.io/agents-maintenance-dashboard/)

GitHub Pages dashboard displaying Civic Interconnect Agent status, commit info, schema sources, and success indicators.

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Local Development

See [REF_DEV.md](./REF_DEV.md). Then:

```shell
py scripts/main.py
```

## Test Web App Locally

```powershell
cd docs
py -m http.server 8000
```

Visit: <http://localhost:8000>

[View Live Site](https://civic-interconnect.github.io/agents-maintenance-dashboard/)

![Screenshot of Civic Interconnect Dashboard](images/screenshot.png)
