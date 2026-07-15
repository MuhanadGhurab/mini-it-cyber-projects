from __future__ import annotations

from pathlib import Path

from log_summary.cli import main
from log_summary.summarizer import summarize_log


def test_summarize(tmp_path: Path) -> None:
    log = tmp_path / "app.log"
    log.write_text(
        "\n".join(
            [
                "2026-07-15 INFO started",
                "2026-07-15 WARN disk space low",
                "2026-07-15 ERROR failed backup",
                "2026-07-15 CRITICAL service down",
                "noise without level",
            ]
        ),
        encoding="utf-8",
    )
    counts = summarize_log(log)
    assert counts["INFO"] == 1
    assert counts["WARN"] == 1
    assert counts["ERROR"] == 1
    assert counts["CRITICAL"] == 1


def test_cli_json(tmp_path: Path, capsys) -> None:
    log = tmp_path / "app.log"
    log.write_text("INFO hi\n", encoding="utf-8")
    assert main([str(log), "--json"]) == 0
    out = capsys.readouterr().out
    assert '"INFO": 1' in out
