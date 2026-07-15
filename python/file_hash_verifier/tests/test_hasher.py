from __future__ import annotations

from pathlib import Path

import pytest

from file_hash_verifier.cli import main
from file_hash_verifier.hasher import hash_file, normalize_algo, verify_file


def test_normalize_algo() -> None:
    assert normalize_algo("SHA-256") == "sha256"
    assert normalize_algo("sha512") == "sha512"
    with pytest.raises(ValueError):
        normalize_algo("md5")


def test_hash_and_verify(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("integrity-check\n", encoding="utf-8")
    digest = hash_file(sample)
    assert len(digest) == 64
    assert verify_file(sample, digest) is True
    assert verify_file(sample, "0" * 64) is False


def test_cli_hash(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sample = tmp_path / "a.bin"
    sample.write_bytes(b"abc")
    assert main(["hash", str(sample)]) == 0
    out = capsys.readouterr().out.strip()
    assert len(out) == 64


def test_cli_verify_mismatch(tmp_path: Path) -> None:
    sample = tmp_path / "a.bin"
    sample.write_bytes(b"abc")
    assert main(["verify", str(sample), "0" * 64]) == 2
