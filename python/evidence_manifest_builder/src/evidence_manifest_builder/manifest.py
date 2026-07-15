"""Hash a directory tree into a stable integrity manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

_CHUNK = 1024 * 1024


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(_CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    entries: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        entries.append({"path": rel, "sha256": hash_file(path)})
    return {
        "algorithm": "sha256",
        "root_name": root.name,
        "file_count": len(entries),
        "files": entries,
    }


def write_manifest(manifest: dict[str, Any], destination: Path, as_json: bool = True) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if as_json:
        destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return
    lines = [f"{item['sha256']}  {item['path']}" for item in manifest["files"]]
    destination.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json" or text.lstrip().startswith("{"):
        data = json.loads(text)
        if not isinstance(data, dict) or "files" not in data:
            raise ValueError("Invalid JSON manifest structure")
        return data
    files: list[dict[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        if not rel:
            raise ValueError(f"Invalid manifest line: {line}")
        files.append({"path": rel, "sha256": digest.lower()})
    return {"algorithm": "sha256", "files": files, "file_count": len(files)}


def verify_manifest(root: Path, manifest: dict[str, Any]) -> tuple[bool, list[str]]:
    expected = {item["path"]: item["sha256"].lower() for item in manifest["files"]}
    actual_manifest = build_manifest(root)
    actual = {item["path"]: item["sha256"] for item in actual_manifest["files"]}
    problems: list[str] = []
    for path, digest in sorted(expected.items()):
        if path not in actual:
            problems.append(f"missing: {path}")
        elif actual[path] != digest:
            problems.append(f"mismatch: {path}")
    for path in sorted(set(actual) - set(expected)):
        problems.append(f"unexpected: {path}")
    return (not problems), problems
