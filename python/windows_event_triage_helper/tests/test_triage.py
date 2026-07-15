from __future__ import annotations

from pathlib import Path

import pytest

from windows_event_triage_helper.cli import main
from windows_event_triage_helper.triage import (
    load_events,
    render_markdown,
    summarize_events,
)


SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_csv_parsing() -> None:
    rows = load_events(SAMPLES / "lab_events.csv")
    assert len(rows) == 8
    summary = summarize_events(rows)
    assert summary.total_events == 8
    assert summary.by_event_id[4625] == 3
    assert summary.top_usernames["lab-user1"] >= 1
    assert summary.top_source_ips["10.10.30.20"] >= 1
    assert summary.unknown_event_ids[9999] == 1
    assert 4625 in summary.suspicious_hits


def test_json_parsing() -> None:
    rows = load_events(SAMPLES / "lab_events.json")
    summary = summarize_events(rows)
    assert summary.by_event_id[4625] == 2
    assert summary.by_event_id[4720] == 1


def test_empty_file(tmp_path: Path) -> None:
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    rows = load_events(empty)
    summary = summarize_events(rows)
    assert summary.total_events == 0


def test_markdown_report() -> None:
    rows = load_events(SAMPLES / "lab_events.csv")
    summary = summarize_events(rows)
    md = render_markdown(summary, "lab_events.csv")
    assert "# Windows Event Triage Report" in md
    assert "4625" in md
    assert "Suspicious pattern summary" in md


def test_cli_writes_outputs(tmp_path: Path) -> None:
    md_out = tmp_path / "report.md"
    csv_out = tmp_path / "counts.csv"
    assert (
        main(
            [
                str(SAMPLES / "lab_events.csv"),
                "--markdown-out",
                str(md_out),
                "--csv-out",
                str(csv_out),
                "--json",
            ]
        )
        == 0
    )
    assert md_out.exists() and "Event ID" in md_out.read_text(encoding="utf-8")
    assert csv_out.exists() and "4625" in csv_out.read_text(encoding="utf-8")


def test_unknown_format(tmp_path: Path) -> None:
    bad = tmp_path / "notes.txt"
    bad.write_text("nope", encoding="utf-8")
    with pytest.raises(ValueError):
        load_events(bad)
