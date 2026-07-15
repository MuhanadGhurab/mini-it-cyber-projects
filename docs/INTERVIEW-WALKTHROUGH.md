# Interview Walkthrough — Mini IT & Cyber Projects

Honest talking points for the defensive toolset.

## 1. IOC Text Extractor

**What it does:** Reads a local text/log file and extracts candidate IOC patterns (IPv4, domains, URLs, hashes, emails).

**Inputs:** Text files you are authorized to analyze (lab notes, exported alerts).

**Outputs:** Line-oriented `kind: value` lists or JSON.

**Defensive angle:** Speeds indicator collection without visiting remote hosts or scraping credentials.

**Limitation:** Heuristics produce false positives; it does not score maliciousness.

## 2. Evidence Manifest Builder

**What it does:** Builds a SHA-256 manifest for a folder and verifies later integrity.

**Inputs:** A local evidence directory.

**Outputs:** JSON or text digests; verify mode reports missing/mismatch/unexpected files.

**Defensive angle:** Protects lab exports from silent modification during transfer/archive.

**Limitation:** Not a legal chain-of-custody or signing product.

## 3. Windows Event Triage Helper

**What it does:** Summarizes exported Windows Event Log CSV/JSON by Event ID, usernames, source IPs, suspicious IDs, and a short timeline; can emit Markdown/CSV reports.

**Inputs:** Offline exports only — no live Event Log API, no remote WMI/RPC.

**Outputs:** Markdown report, optional counts CSV, optional JSON.

**Defensive angle:** Supports failed-logon and account-change drills in `lab.local` without requiring a SIEM license for learning.

**Limitation:** Field-name mapping is best-effort; unknown Event IDs are listed, not rejected.

## 4. How these tools stay defensive

- Local file IO only
- No network clients
- No credential harvesting
- Explicit privacy warnings for published samples
- Sample data uses fictional `lab-*` accounts and RFC1918 addresses

## 5. How tests prove behavior

| Tool | What tests cover |
|------|------------------|
| IOC extractor | Pattern extraction and CLI JSON mode |
| Manifest builder | Build/verify + tamper detection |
| Event triage helper | CSV/JSON parse, empty file, unknown IDs, Markdown/CSV outputs |

Pytest runs in GitHub Actions alongside the Java RBAC simulator CI job.

## 6. How this supports SOC / IT security work

These utilities mirror small analyst chores: collect indicators, preserve evidence integrity, and summarize authentication noise. They are **learning aids**, not replacements for enterprise SOC platforms.

## Still planned

- Password-policy helper for lab exports
- CSV asset inventory validator
- Optional educational game after quality gates remain green
