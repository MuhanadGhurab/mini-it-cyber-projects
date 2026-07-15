from __future__ import annotations

from pathlib import Path

from ioc_text_extractor.cli import main
from ioc_text_extractor.extract import extract_from_text


def test_extract_patterns() -> None:
    text = (
        "host 10.10.30.20 contacted example-malware.test "
        "via https://example-malware.test/a "
        "hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 "
        "mail analyst@lab.local"
    )
    found = extract_from_text(text)
    assert "10.10.30.20" in found["ipv4"]
    assert "example-malware.test" in [d.lower() for d in found["domain"]]
    assert found["sha256"]
    assert found["url"]
    assert found["email"]


def test_cli_json(tmp_path: Path, capsys) -> None:
    sample = tmp_path / "note.txt"
    sample.write_text("see 10.10.20.10\n", encoding="utf-8")
    assert main([str(sample), "--json", "--kinds", "ipv4"]) == 0
    out = capsys.readouterr().out
    assert "10.10.20.10" in out
