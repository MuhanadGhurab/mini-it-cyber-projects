"""CLI for defensive Windows event export triage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from windows_event_triage_helper.triage import (
    load_events,
    render_markdown,
    summarize_events,
    write_csv_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="windows-event-triage-helper",
        description=(
            "Summarize exported Windows Event Log CSV/JSON for lab-only defensive triage. "
            "Does not connect to live systems."
        ),
    )
    parser.add_argument("path", type=Path, help="Path to .csv or .json export")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    parser.add_argument("--markdown-out", type=Path, help="Write Markdown report")
    parser.add_argument("--csv-out", type=Path, help="Write Event ID counts CSV")
    args = parser.parse_args(argv)

    try:
        rows = load_events(args.path)
        summary = summarize_events(rows)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.markdown_out:
        args.markdown_out.write_text(
            render_markdown(summary, args.path.name),
            encoding="utf-8",
        )
    if args.csv_out:
        write_csv_summary(summary, args.csv_out)

    if args.json:
        print(json.dumps(summary.to_dict(), indent=2))
    else:
        print(render_markdown(summary, args.path.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
