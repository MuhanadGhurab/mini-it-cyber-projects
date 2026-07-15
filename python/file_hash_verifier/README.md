# File Hash Verifier

Compute and verify file digests for integrity checking.

## Purpose

Help IT and security practitioners confirm a file matches an expected SHA-256 (or SHA-512) hash after download or transfer.

## Features

- SHA-256 and SHA-512
- Streaming hash for large files
- Expected-hash verification mode
- Clear exit codes for automation

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
python -m file_hash_verifier hash ./sample.bin
python -m file_hash_verifier verify ./sample.bin <expected_sha256>
python -m file_hash_verifier hash ./sample.bin --algo sha512
```

## Testing

```bash
python -m pytest -q
```

## Security considerations

- Does not transmit files
- Does not collect secrets
- Treat hashes as integrity helpers, not authentication

## Limitations

- Not a substitute for code signing verification
- Does not detect malicious content inside a matching hash

## Author

Muhanad Ghurab
