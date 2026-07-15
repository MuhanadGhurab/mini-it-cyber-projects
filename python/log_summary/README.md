# Log Summary Utility

Summarize severity counts from plain-text log files for quick triage practice.

## Purpose

Give IT/security practitioners a small defensive tool to scan exported logs for `ERROR`, `WARN`, `INFO`, and `CRITICAL` style tokens without uploading data to external services.

## Usage

```bash
python -m pip install -e ".[dev]"
python -m log_summary ./sample.log
python -m log_summary ./sample.log --json
```

## Testing

```bash
python -m pytest -q
```

## Safety

- Local files only
- No remote collection
- Does not claim full SIEM capability
