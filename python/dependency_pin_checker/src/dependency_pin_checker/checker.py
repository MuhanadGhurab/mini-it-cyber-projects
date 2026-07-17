"""Scan common dependency manifests for unpinned or overly loose versions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REQ_LINE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*([^\s#]*)")


@dataclass(frozen=True)
class Finding:
    file: str
    package: str
    specifier: str
    issue: str


def _check_req_specifier(spec: str) -> str | None:
    if not spec:
        return "unpinned (no version)"
    if "*" in spec or spec.strip() in {">", ">=", "<", "<=", "~="}:
        return "wildcard or incomplete specifier"
    if spec.startswith(">=") and "==" not in spec and "," not in spec:
        # allow ranges but flag bare lower-bounds as loose for supply-chain hygiene
        return "loose lower-bound only"
    return None


def scan_requirements(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or raw.startswith("-"):
            continue
        m = REQ_LINE.match(raw)
        if not m:
            continue
        name, spec = m.group(1), m.group(2)
        issue = _check_req_specifier(spec)
        if issue:
            findings.append(Finding(str(path), name, spec or "(none)", issue))
    return findings


def scan_package_json(path: Path) -> list[Finding]:
    data = json.loads(path.read_text(encoding="utf-8"))
    findings: list[Finding] = []
    for section in ("dependencies", "devDependencies", "optionalDependencies"):
        deps = data.get(section) or {}
        for name, spec in deps.items():
            s = str(spec)
            if s.startswith("^") or s.startswith("~") or s == "*" or "x" in s.lower():
                findings.append(Finding(str(path), name, s, "range/wildcard pin"))
            elif not s or s == "latest":
                findings.append(Finding(str(path), name, s or "(none)", "unpinned"))
    return findings


def scan_path(target: Path) -> list[Finding]:
    findings: list[Finding] = []
    if target.is_file():
        files = [target]
    else:
        files = list(target.rglob("requirements*.txt")) + list(target.rglob("package.json"))
    for path in files:
        if path.name.startswith("package.json"):
            findings.extend(scan_package_json(path))
        else:
            findings.extend(scan_requirements(path))
    return findings
