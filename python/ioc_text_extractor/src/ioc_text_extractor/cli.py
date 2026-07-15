"""CLI for defensive IOC text extraction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ioc_text_extractor.extract import KIND_PATTERNS, extract_from_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ioc-text-extractor",
        description="Extract candidate IOC patterns from a local text file (defensive use).",
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--kinds",
        default=",".join(KIND_PATTERNS),
        help="Comma-separated kinds: ipv4,domain,url,email,md5,sha1,sha256",
    )
    args = parser.parse_args(argv)

    kinds = {part.strip().lower() for part in args.kinds.split(",") if part.strip()}
    try:
        results = extract_from_file(args.path, kinds)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
        return 0

    if not results:
        print("No IOC patterns found.")
        return 0

    for kind in sorted(results):
        for value in results[kind]:
            print(f"{kind}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
