"""Pattern extractors for common IOC shapes in local text."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

IPV4_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
DOMAIN_RE = re.compile(
    r"\b(?!(?:\d+\.)+\d+\b)(?:[A-Za-z0-9-]+\.)+(?:test|invalid|example|local|com|net|org|info)\b",
    re.IGNORECASE,
)
MD5_RE = re.compile(r"\b[a-fA-F0-9]{32}\b")
SHA1_RE = re.compile(r"\b[a-fA-F0-9]{40}\b")
SHA256_RE = re.compile(r"\b[a-fA-F0-9]{64}\b")

KIND_PATTERNS: dict[str, re.Pattern[str]] = {
    "ipv4": IPV4_RE,
    "url": URL_RE,
    "email": EMAIL_RE,
    "domain": DOMAIN_RE,
    "md5": MD5_RE,
    "sha1": SHA1_RE,
    "sha256": SHA256_RE,
}


def extract_from_text(text: str, kinds: set[str] | None = None) -> dict[str, list[str]]:
    selected = kinds or set(KIND_PATTERNS)
    unknown = selected - set(KIND_PATTERNS)
    if unknown:
        raise ValueError(f"Unknown IOC kinds: {', '.join(sorted(unknown))}")

    found: dict[str, list[str]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)

    # Prefer longer hashes first to reduce double-counting overlaps in presentation
    order = ["url", "email", "sha256", "sha1", "md5", "ipv4", "domain"]
    for kind in order:
        if kind not in selected:
            continue
        for match in KIND_PATTERNS[kind].findall(text):
            value = match.rstrip(".,);]")
            key = value.lower() if kind in {"md5", "sha1", "sha256", "domain", "email"} else value
            if key in seen[kind]:
                continue
            seen[kind].add(key)
            found[kind].append(value)
    return dict(found)


def extract_from_file(path: Path, kinds: set[str] | None = None) -> dict[str, list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    text = path.read_text(encoding="utf-8", errors="replace")
    return extract_from_text(text, kinds)
