# Windows Event Triage Report

Source: `lab_events.csv`

## Defensive-use notice

Lab/export triage only. Not a SIEM replacement.

**Total parsed events:** 8

## Counts by Event ID

| Event ID | Count | Label |
|----------|------:|-------|
| 4624 | 2 | Successful logon |
| 4625 | 3 | Failed logon |
| 4688 | 1 | Process creation |
| 4740 | 1 | Account locked out |
| 9999 | 1 | Unknown / unlisted |

## Top usernames

- `lab-user1` — 4
- `lab-admin` — 3
- `lab-service` — 1

## Top source IPs

- `10.10.30.20` — 5
- `10.10.10.10` — 1

## Suspicious pattern summary

- Event `4625` (Failed logon): 3
- Event `4740` (Account locked out): 1

## Unknown / unlisted Event IDs

- `9999` — 1

## Timeline summary (first events chronologically)

| Time | Event ID | Label | User | Source IP |
|------|----------|-------|------|-----------|
| 2026-07-15T08:14:01Z | 4624 | Successful logon | lab-user1 | 10.10.30.20 |
| 2026-07-15T08:14:05Z | 4625 | Failed logon | lab-user1 | 10.10.30.20 |
| 2026-07-15T08:14:06Z | 4625 | Failed logon | lab-user1 | 10.10.30.20 |
| 2026-07-15T08:14:07Z | 4625 | Failed logon | lab-admin | 10.10.30.20 |
| 2026-07-15T08:14:20Z | 4740 | Account locked out | lab-user1 | 10.10.30.20 |
| 2026-07-15T08:15:00Z | 4624 | Successful logon | lab-admin | 10.10.10.10 |
| 2026-07-15T08:15:30Z | 4688 | Process creation | lab-admin | - |
| 2026-07-15T08:16:00Z | 9999 | Unknown / unlisted | lab-service | - |
