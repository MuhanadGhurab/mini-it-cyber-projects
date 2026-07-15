"""File hashing helpers for integrity verification."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

Algo = Literal["sha256", "sha512"]

_CHUNK = 1024 * 1024


def normalize_algo(name: str) -> Algo:
    key = name.strip().lower()
    if key in {"sha256", "sha-256"}:
        return "sha256"
    if key in {"sha512", "sha-512"}:
        return "sha512"
    raise ValueError(f"Unsupported algorithm: {name}. Use sha256 or sha512.")


def hash_file(path: Path, algo: Algo = "sha256") -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    digest = hashlib.new(algo)
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(_CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected: str, algo: Algo = "sha256") -> bool:
    cleaned = expected.strip().lower()
    if not cleaned or any(ch not in "0123456789abcdef" for ch in cleaned):
        raise ValueError("Expected hash must be a hexadecimal digest.")
    actual = hash_file(path, algo)
    return actual == cleaned
