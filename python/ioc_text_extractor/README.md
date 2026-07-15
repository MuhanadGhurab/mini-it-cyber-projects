# IOC Text Extractor

Defensive helper that extracts common indicator patterns from local text or log exports.

| Status | Functional Prototype |
|--------|----------------------|

## Defensive-use statement

Use only on text you are authorized to analyze (lab notes, your exports, public threat reports you downloaded). This tool does **not** scan networks, harvest credentials, or contact remote hosts.

## Purpose

Pull candidate IOCs from unstructured text so analysts can triage faster during lab exercises.

## Supported patterns

- IPv4 addresses
- Domains (simple heuristic)
- URLs
- MD5 / SHA-1 / SHA-256 hex digests
- Emails (often sensitive — review before sharing)

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
python -m ioc_text_extractor samples/sample_alert.txt
python -m ioc_text_extractor samples/sample_alert.txt --json
python -m ioc_text_extractor samples/sample_alert.txt --kinds ipv4,sha256,domain
```

### Sample output

```text
ipv4: 10.10.30.20
domain: example-malware.test
sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
url: https://example-malware.test/payload
```

## Testing

```bash
python -m pytest -q
```

## Limitations

- Heuristic parsers produce false positives (version strings, etc.)
- Does not enrich or score reputation
- Does not validate that a string is malicious
- Emails may be personal data — sanitize before publishing

## Author

Muhanad Ghurab
