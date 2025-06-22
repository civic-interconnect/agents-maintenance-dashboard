# DEVELOPER.md

## Setup

First, fork the repo. Git clone your repo to your machine. Open project repo in VS Code.
Open a terminal (commands are for PowerShell).

```powershell
git clone https://github.com/civic-interconnect/app-agents.git
cd app-agents
py -m venv .venv
.\.venv\Scripts\activate
py src\setup\init_venv.py
app-agents prep-code
app-agents fetch-status
app-agents serve-app
```

or serve with:

```powershell
cd docs
py -m http.server 8000
```

Visit: <http://localhost:8000>

## Releasing New Version

After verifying changes:

```powershell
app-agents bump-version 1.0.3 1.0.4
app-agents release
```

## Publishing to PyPI

Requires valid PyPI token:

```powershell
py -m build
py -m twine upload dist/*
```

## Test Web App Locally

```powershell
cd docs
py -m http.server 8000
```

Visit: <http://localhost:8000>
