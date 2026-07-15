"""CLI entrypoint for file hash verification."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from file_hash_verifier.hasher import hash_file, normalize_algo, verify_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-hash-verifier",
        description="Compute or verify SHA-256/SHA-512 digests for local files.",
    )
    parser.add_argument(
        "--algo",
        default="sha256",
        help="Hash algorithm: sha256 (default) or sha512",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    hash_cmd = sub.add_parser("hash", help="Print the digest for a file")
    hash_cmd.add_argument("path", type=Path)

    verify_cmd = sub.add_parser("verify", help="Compare file digest to an expected value")
    verify_cmd.add_argument("path", type=Path)
    verify_cmd.add_argument("expected")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        algo = normalize_algo(args.algo)
        if args.command == "hash":
            print(hash_file(args.path, algo))
            return 0
        if args.command == "verify":
            ok = verify_file(args.path, args.expected, algo)
            if ok:
                print("MATCH")
                return 0
            print("MISMATCH")
            return 2
        parser.error(f"Unknown command: {args.command}")
        return 1
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
