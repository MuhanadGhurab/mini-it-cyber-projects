"""Parse and summarize exported Windows event rows (CSV/JSON)."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from windows_event_triage_helper.catalog import EVENT_CATALOG, SUSPICIOUS_IDS

REQUIRED_HINTS = ("EventID", "event_id", "Id")


@dataclass
class TriageSummary:
    total_events: int = 0
    by_event_id: Counter[int] = field(default_factory=Counter)
    top_usernames: Counter[str] = field(default_factory=Counter)
    top_source_ips: Counter[str] = field(default_factory=Counter)
    unknown_event_ids: Counter[int] = field(default_factory=Counter)
    suspicious_hits: Counter[int] = field(default_factory=Counter)
    timeline: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_events": self.total_events,
            "by_event_id": {
                str(k): {"count": v, "label": EVENT_CATALOG.get(k, "Unknown / unlisted")}
                for k, v in sorted(self.by_event_id.items())
            },
            "top_usernames": self.top_usernames.most_common(10),
            "top_source_ips": self.top_source_ips.most_common(10),
            "unknown_event_ids": dict(sorted(self.unknown_event_ids.items())),
            "suspicious_hits": {
                str(k): {"count": v, "label": EVENT_CATALOG.get(k, "Unknown / unlisted")}
                for k, v in sorted(self.suspicious_hits.items())
            },
            "timeline": self.timeline[:50],
        }


def _normalize_key(row: dict[str, Any]) -> dict[str, Any]:
    return {str(k).strip().lower(): v for k, v in row.items()}


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _pick(row: dict[str, Any], *names: str) -> str | None:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return str(row[name]).strip()
    return None


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    if path.stat().st_size == 0:
        return []

    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "Events" in data:
            data = data["Events"]
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list of event objects")
        return [_normalize_key(item) for item in data if isinstance(item, dict)]

    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            return [_normalize_key(row) for row in reader]

    raise ValueError("Supported formats: .csv or .json")


def summarize_events(rows: list[dict[str, Any]], timeline_limit: int = 50) -> TriageSummary:
    summary = TriageSummary()
    ordered: list[tuple[str, dict[str, Any]]] = []

    for row in rows:
        event_id = _as_int(_pick(row, "eventid", "event_id", "id"))
        if event_id is None:
            continue
        summary.total_events += 1
        summary.by_event_id[event_id] += 1
        if event_id not in EVENT_CATALOG:
            summary.unknown_event_ids[event_id] += 1
        if event_id in SUSPICIOUS_IDS:
            summary.suspicious_hits[event_id] += 1

        user = _pick(
            row,
            "targetusername",
            "target_user",
            "username",
            "accountname",
            "account_name",
        )
        if user and user.upper() not in {"-", "N/A"}:
            summary.top_usernames[user] += 1

        source_ip = _pick(row, "ipaddress", "sourceip", "source_ip", "ip_address")
        if source_ip and source_ip not in {"-", "::1"}:
            summary.top_source_ips[source_ip] += 1

        when = _pick(row, "timecreated", "time", "timestamp", "utc_time") or ""
        ordered.append(
            (
                when,
                {
                    "time": when,
                    "event_id": event_id,
                    "label": EVENT_CATALOG.get(event_id, "Unknown / unlisted"),
                    "user": user or "",
                    "source_ip": source_ip or "",
                },
            )
        )

    ordered.sort(key=lambda item: item[0])
    summary.timeline = [item[1] for item in ordered[:timeline_limit]]
    return summary


def render_markdown(summary: TriageSummary, source_name: str) -> str:
    data = summary.to_dict()
    lines = [
        "# Windows Event Triage Report",
        "",
        f"Source: `{source_name}`",
        "",
        "## Defensive-use notice",
        "",
        "Lab/export triage only. Not a SIEM replacement.",
        "",
        f"**Total parsed events:** {data['total_events']}",
        "",
        "## Counts by Event ID",
        "",
        "| Event ID | Count | Label |",
        "|----------|------:|-------|",
    ]
    for event_id, meta in data["by_event_id"].items():
        lines.append(f"| {event_id} | {meta['count']} | {meta['label']} |")

    lines.extend(["", "## Top usernames", ""])
    if data["top_usernames"]:
        for name, count in data["top_usernames"]:
            lines.append(f"- `{name}` — {count}")
    else:
        lines.append("- None found")

    lines.extend(["", "## Top source IPs", ""])
    if data["top_source_ips"]:
        for ip, count in data["top_source_ips"]:
            lines.append(f"- `{ip}` — {count}")
    else:
        lines.append("- None found")

    lines.extend(["", "## Suspicious pattern summary", ""])
    if data["suspicious_hits"]:
        for event_id, meta in data["suspicious_hits"].items():
            lines.append(f"- Event `{event_id}` ({meta['label']}): {meta['count']}")
    else:
        lines.append("- No catalogued suspicious Event IDs in this export")

    if data["unknown_event_ids"]:
        lines.extend(["", "## Unknown / unlisted Event IDs", ""])
        for event_id, count in data["unknown_event_ids"].items():
            lines.append(f"- `{event_id}` — {count}")

    lines.extend(["", "## Timeline summary (first events chronologically)", ""])
    if data["timeline"]:
        lines.append("| Time | Event ID | Label | User | Source IP |")
        lines.append("|------|----------|-------|------|-----------|")
        for item in data["timeline"]:
            lines.append(
                f"| {item['time']} | {item['event_id']} | {item['label']} | "
                f"{item['user']} | {item['source_ip']} |"
            )
    else:
        lines.append("_No timeline rows_")

    lines.append("")
    return "\n".join(lines)


def write_csv_summary(summary: TriageSummary, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["event_id", "count", "label"])
        for event_id, count in sorted(summary.by_event_id.items()):
            writer.writerow([event_id, count, EVENT_CATALOG.get(event_id, "Unknown / unlisted")])
