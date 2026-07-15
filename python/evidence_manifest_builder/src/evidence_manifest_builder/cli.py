"""CLI for evidence folder manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evidence_manifest_builder.manifest import (
    build_manifest,
    load_manifest,
    verify_manifest,
    write_manifest,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-manifest-builder",
        description="Build or verify SHA-256 manifests for a local evidence directory.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Create a manifest for a directory")
    build.add_argument("root", type=Path)
    build.add_argument("--out", type=Path, required=True)
    build.add_argument("--text", action="store_true", help="Write text instead of JSON")

    verify = sub.add_parser("verify", help="Verify a directory against a manifest")
    verify.add_argument("root", type=Path)
    verify.add_argument("--manifest", type=Path, required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            manifest = build_manifest(args.root)
            write_manifest(manifest, args.out, as_json=not args.text)
            print(json.dumps({"file_count": manifest["file_count"], "out": str(args.out)}))
            return 0
        if args.command == "verify":
            manifest = load_manifest(args.manifest)
            ok, problems = verify_manifest(args.root, manifest)
            if ok:
                print("OK")
                return 0
            for problem in problems:
                print(problem)
            return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
