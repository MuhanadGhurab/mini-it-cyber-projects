# Windows Event Triage Helper

Defensive helper for summarizing **exported** Windows Event Log data (CSV or JSON).

| Status | Functional Prototype |
|--------|----------------------|

## Defensive-use statement

- Local files only
- Intended for personal lab exports (`lab.local`) and authorized training data
- Does **not** connect to live Event Log services, remote hosts, or credentials stores
- Not offensive tooling, persistence, evasion, or exploitation

## Privacy warning

Event exports can contain usernames, hostnames, and IPs. Sanitize before publishing outputs. Prefer fictional lab accounts (`lab-user1`) and RFC1918 addresses in samples.

## Purpose

Accelerate triage during lab incident drills by counting Event IDs, highlighting suspicious patterns, and producing Markdown/CSV summaries.

## Example Event IDs (catalogued)

4624, 4625, 4634, 4648, 4672, 4688, 4697, 4720, 4726, 4740, 7045

Unknown IDs are counted under “unknown / unlisted” without failing the run.

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
python -m windows_event_triage_helper samples/lab_events.csv
python -m windows_event_triage_helper samples/lab_events.json --json
python -m windows_event_triage_helper samples/lab_events.csv \
  --markdown-out samples/sample_report.md \
  --csv-out samples/sample_counts.csv
```

## Testing

```bash
python -m pytest -q
```

## Limitations

- Heuristic field name matching (`TargetUserName`, `IpAddress`, etc.)
- Not a full forensic timeline engine
- Does not validate whether activity is malicious
- Does not replace a SIEM or EDR console

## Author

Muhanad Ghurab
