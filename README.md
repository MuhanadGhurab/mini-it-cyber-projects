# Mini IT & Cyber Projects

| Field | Value |
|-------|-------|
| **Status** | Active Development |
| **Purpose** | Monorepo for small, high-quality defensive utilities and learning tools |
| **Author** | Muhanad Ghurab |

## Why a monorepo

Small scripts do not each deserve a separate GitHub repository. This structure prevents portfolio spam while keeping projects testable and documented.

## Projects in this milestone

| Project | Language | Status | Path |
|---------|----------|--------|------|
| File Hash Verifier | Python 3.12+ | Functional Prototype | [`python/file_hash_verifier`](python/file_hash_verifier) |
| Log Summary Utility | Python 3.12+ | Functional Prototype | [`python/log_summary`](python/log_summary) |
| RBAC Simulator | Java 17+ | Functional Prototype | [`java/rbac-simulator`](java/rbac-simulator) |

## Safety

- Defensive / educational use only
- No credential theft, malware, persistence, phishing, or exploitation tooling
- No scanning of networks you do not own

## Structure

```text
mini-it-cyber-projects/
├── python/
│   ├── file_hash_verifier/
│   └── log_summary/
├── java/
│   └── rbac-simulator/
├── docs/
└── README.md
```

## Testing

```bash
# Python
python -m pip install -e "python/file_hash_verifier[dev]"
python -m pytest python/file_hash_verifier/tests -q
python -m pip install -e "python/log_summary[dev]"
python -m pytest python/log_summary/tests -q

# Java (requires JDK 17+)
cd java/rbac-simulator && mvn test
```

GitHub Actions runs Python tests and Java tests with a provisioned JDK.

## License

MIT — original code by Muhanad Ghurab.

## Contact

- https://github.com/MuhanadGhurab
- muhanadghurab@gmail.com
