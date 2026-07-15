"""Known defensive Event ID labels for lab triage."""

from __future__ import annotations

EVENT_CATALOG: dict[int, str] = {
    4624: "Successful logon",
    4625: "Failed logon",
    4634: "Logoff",
    4648: "Explicit credential logon",
    4672: "Special privileges assigned",
    4688: "Process creation",
    4697: "Service installed",
    4720: "User account created",
    4726: "User account deleted",
    4740: "Account locked out",
    7045: "Service installed (System)",
}

SUSPICIOUS_IDS = {4625, 4648, 4672, 4697, 4720, 4740, 7045}
