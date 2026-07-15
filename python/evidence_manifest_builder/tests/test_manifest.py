from __future__ import annotations

from pathlib import Path

from evidence_manifest_builder.cli import main
from evidence_manifest_builder.manifest import build_manifest, verify_manifest


def test_build_and_verify(tmp_path: Path) -> None:
    root = tmp_path / "pack"
    root.mkdir()
    (root / "a.txt").write_text("alpha\n", encoding="utf-8")
    (root / "nested").mkdir()
    (root / "nested" / "b.txt").write_text("beta\n", encoding="utf-8")
    manifest = build_manifest(root)
    assert manifest["file_count"] == 2
    ok, problems = verify_manifest(root, manifest)
    assert ok and not problems


def test_cli_detects_tamper(tmp_path: Path) -> None:
    root = tmp_path / "pack"
    root.mkdir()
    target = root / "a.txt"
    target.write_text("alpha\n", encoding="utf-8")
    manifest_path = tmp_path / "m.json"
    assert main(["build", str(root), "--out", str(manifest_path)]) == 0
    target.write_text("changed\n", encoding="utf-8")
    assert main(["verify", str(root), "--manifest", str(manifest_path)]) == 2
