"""Local log severity counter."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

LEVEL_PATTERN = re.compile(
    r"\b(CRITICAL|ERROR|WARN(?:ING)?|INFO|DEBUG)\b",
    re.IGNORECASE,
)


def summarize_log(path: Path) -> Counter[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    counts: Counter[str] = Counter()
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = LEVEL_PATTERN.search(line)
            if not match:
                continue
            level = match.group(1).upper()
            if level == "WARNING":
                level = "WARN"
            counts[level] += 1
    return counts
