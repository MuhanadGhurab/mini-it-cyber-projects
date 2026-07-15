"""CLI for local log severity summaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from log_summary.summarizer import summarize_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="log-summary",
        description="Count severity tokens in a local log file.",
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON object")
    args = parser.parse_args(argv)

    try:
        counts = summarize_log(args.path)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    order = ["CRITICAL", "ERROR", "WARN", "INFO", "DEBUG"]
    payload = {level: counts.get(level, 0) for level in order}
    payload["TOTAL_MATCHED"] = sum(payload.values())

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
