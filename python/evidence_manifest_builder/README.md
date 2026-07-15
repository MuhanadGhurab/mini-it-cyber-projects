# Evidence Manifest Builder

Build and verify SHA-256 manifests for local evidence folders (lab exports, notes, sanitized screenshots).

| Status | Functional Prototype |
|--------|----------------------|

## Defensive-use statement

Intended for integrity tracking of files you own. Does not upload data, does not access remote systems, and does not collect credentials.

## Purpose

Create a portable evidence pack manifest so transferred lab artifacts can be checked for accidental modification.

## Features

- Recursive SHA-256 hashing
- Stable relative path ordering
- JSON or text manifest output
- Compare mode against an existing manifest

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
python -m evidence_manifest_builder build samples/evidence_pack --out samples/manifest.json
python -m evidence_manifest_builder verify samples/evidence_pack --manifest samples/manifest.json
```

### Sample text output

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  notes/readme.txt
...
```

## Testing

```bash
python -m pytest -q
```

## Limitations

- Not a chain-of-custody legal tool
- Does not sign manifests
- Does not encrypt evidence
- Binary identity only — content sensitivity still requires human review before publishing

## Author

Muhanad Ghurab
