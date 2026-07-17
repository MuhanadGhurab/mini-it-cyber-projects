"""CLI for dependency pin checker."""

from __future__ import annotations

import argparse
from pathlib import Path

from dependency_pin_checker.checker import scan_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Defensive scan for unpinned/wildcard dependency declarations."
    )
    parser.add_argument("path", type=Path, help="File or directory to scan")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when findings exist (default: exit 0 after report)",
    )
    args = parser.parse_args(argv)
    findings = scan_path(args.path)
    if not findings:
        print("No loose dependency pins found.")
        return 0
    for f in findings:
        print(f"{f.file}: {f.package} {f.specifier} -> {f.issue}")
    print(f"Total findings: {len(findings)}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
