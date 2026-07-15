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
| Windows Event Triage Helper | Python 3.12+ | Functional Prototype | [`python/windows_event_triage_helper`](python/windows_event_triage_helper) |
| RBAC Simulator | Java 17+ | Functional Prototype | [`java/rbac-simulator`](java/rbac-simulator) |

Interview talking points: [`docs/INTERVIEW-WALKTHROUGH.md`](docs/INTERVIEW-WALKTHROUGH.md)

## Safety

- Defensive / educational use only
- No credential theft, malware, persistence, phishing, or exploitation tooling
- No scanning of networks you do not own
- No live Windows Event Log connections from the triage helper
- Each tool README includes a defensive-use statement and limitations

## Testing

```bash
for proj in file_hash_verifier log_summary ioc_text_extractor evidence_manifest_builder windows_event_triage_helper; do
  python -m pip install -e "python/${proj}[dev]"
  python -m pytest "python/${proj}/tests" -q
done

# Java (requires JDK 17+)
cd java/rbac-simulator && mvn test
```

## License

MIT — original code by Muhanad Ghurab.

## Contact

- https://github.com/MuhanadGhurab
- muhanadghurab@gmail.com
