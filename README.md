# Mini IT & Cyber Projects

| Field | Value |
|-------|-------|
| **Status** | Active Development |
| **Purpose** | Monorepo for small, high-quality defensive utilities and learning tools |
| **Author** | Muhanad Ghurab |

## Why a monorepo

Small scripts do not each deserve a separate GitHub repository. This structure prevents portfolio spam while keeping projects testable and documented.

## Projects

| Project | Language | Status | Path |
|---------|----------|--------|------|
| File Hash Verifier | Python 3.12+ | Functional Prototype | [`python/file_hash_verifier`](python/file_hash_verifier) |
| Log Summary Utility | Python 3.12+ | Functional Prototype | [`python/log_summary`](python/log_summary) |
| IOC Text Extractor | Python 3.12+ | Functional Prototype | [`python/ioc_text_extractor`](python/ioc_text_extractor) |
| Evidence Manifest Builder | Python 3.12+ | Functional Prototype | [`python/evidence_manifest_builder`](python/evidence_manifest_builder) |
| RBAC Simulator | Java 17+ | Functional Prototype | [`java/rbac-simulator`](java/rbac-simulator) |

## Safety

- Defensive / educational use only
- No credential theft, malware, persistence, phishing, or exploitation tooling
- No scanning of networks you do not own
- Each tool README includes a defensive-use statement and limitations

## Structure

```text
mini-it-cyber-projects/
├── python/
│   ├── file_hash_verifier/
│   ├── log_summary/
│   ├── ioc_text_extractor/
│   └── evidence_manifest_builder/
├── java/
│   └── rbac-simulator/
├── docs/
└── README.md
```

## Testing

```bash
python -m pip install -e "python/file_hash_verifier[dev]"
python -m pytest python/file_hash_verifier/tests -q
python -m pip install -e "python/log_summary[dev]"
python -m pytest python/log_summary/tests -q
python -m pip install -e "python/ioc_text_extractor[dev]"
python -m pytest python/ioc_text_extractor/tests -q
python -m pip install -e "python/evidence_manifest_builder[dev]"
python -m pytest python/evidence_manifest_builder/tests -q

# Java (requires JDK 17+)
cd java/rbac-simulator && mvn test
```

GitHub Actions runs Python and Java tests.

## License

MIT — original code by Muhanad Ghurab.

## Contact

- https://github.com/MuhanadGhurab
- muhanadghurab@gmail.com
