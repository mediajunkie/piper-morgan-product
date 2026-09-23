#!/usr/bin/env python3
"""belt-mechanical-reasoning-proxy.py — CIO's half of standing item 8a (joint belt classification
with Exec, due 2026-09-27, PM's model-tiering direction relayed by Pard 2026-09-22).

Classifies each role's origin/main commits in a date window into MECHANICAL (heartbeats, MANIFEST
regens, registry state-column bookkeeping, quiet-hold log entries) vs SUBSTANTIVE (everything else)
by commit-message shape. This is a rough proxy, not a precise measure — a commit MESSAGE shape is
not the same as the actual reasoning content of the work, and this week's numbers are inflated by
the reboot recovery, the fire-zero incident, and the usage-crisis response (all real commits, none
representative of an ordinary week's mechanical load). Report accordingly.

Combine with Exec's session-log read + the correction-/retraction- memo proxy for the actual
classification synthesis; this script is one input, not the answer.

Usage: scripts/belt-mechanical-reasoning-proxy.py --since 2026-09-20 --until 2026-09-23
       scripts/belt-mechanical-reasoning-proxy.py --since 2026-09-20 --until 2026-09-23 --role cio
       scripts/belt-mechanical-reasoning-proxy.py --since 2026-09-20 --until 2026-09-23 --include-incidents
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROLES = ["arch", "cio", "comms", "cxo", "docs", "exec", "host", "lead", "pa", "ppm", "web"]

# Commit-message shapes that are pure duty-cycle bookkeeping, not reasoning work.
MECHANICAL_PATTERNS = [
    r"^hb\(",  # hb(role): heartbeat marker
    r"^hb-last-invoked\(",  # suppressed-heartbeat marker
    r"MANIFEST regen",
    r"MANIFEST\.md",
    r"registry row --.*(re-arm|START confirmation|state.column)",
    r"registry\(.*\): re-arm",
    r"update last-pm-scan marker",
    r"cycle\(.*\): .*quiet hold",
]
MECHANICAL_RE = re.compile("|".join(MECHANICAL_PATTERNS), re.IGNORECASE)


# Commit-message prefixes that identify a role's own commit. Covers the observed conventions:
# "role:", "role(...)", "verb(role):", "verb(role ...)".
def role_pattern(role: str) -> re.Pattern:
    return re.compile(
        rf"(^{role}[:(]|\({role}[):])",
        re.IGNORECASE,
    )


# Known incident-spam windows to exclude by default: (start, end) as "YYYY-MM-DD HH:MM:SS" bounds,
# inclusive. Currently: the 2026-09-21 ~22:00 fire-zero hook-recursion incident, which alone
# produced 967 spurious hb(cio)/hb-last-invoked(cio) commits in about one hour — discovered WHILE
# building this script (2026-09-23), by running it once without exclusion and finding cio's window
# unusable: 982 of 1044 matched commits were incident noise, not duty-cycle activity, concentrated
# in a single hour. Verified via git log --pretty with per-hour bucketing before adding this
# exclusion — not assumed from the incident's known existence alone.
INCIDENT_WINDOWS = [
    ("2026-09-21 21:55:00", "2026-09-21 23:05:00"),
]


def in_incident_window(ts: str) -> bool:
    return any(start <= ts <= end for start, end in INCIDENT_WINDOWS)


def git_log(since: str, until: str) -> list[tuple[str, str, str]]:
    """Returns list of (hash, timestamp, subject)."""
    out = subprocess.run(
        [
            "git",
            "log",
            f"--since={since} 00:00",
            f"--until={until} 23:59",
            "--pretty=%H%x09%ad%x09%s",
            "--date=format:%Y-%m-%d %H:%M:%S",
            "origin/main",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    rows = []
    for line in out.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def classify(since: str, until: str, roles: list[str], exclude_incidents: bool) -> dict:
    all_commits = git_log(since, until)
    excluded = 0
    commits = []
    for h, ts, subject in all_commits:
        if exclude_incidents and in_incident_window(ts):
            excluded += 1
            continue
        commits.append((h, ts, subject))

    results = {}
    for role in roles:
        pat = role_pattern(role)
        mechanical = 0
        substantive = 0
        for _, _, subject in commits:
            if not pat.search(subject):
                continue
            if MECHANICAL_RE.search(subject):
                mechanical += 1
            else:
                substantive += 1
        total = mechanical + substantive
        ratio = (substantive / total) if total else None
        results[role] = {
            "mechanical": mechanical,
            "substantive": substantive,
            "total": total,
            "substantive_ratio": ratio,
        }
    return {
        "roles": results,
        "excluded_incident_commits": excluded,
        "total_commits_in_window": len(all_commits),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--since", required=True, help="YYYY-MM-DD, inclusive")
    ap.add_argument("--until", required=True, help="YYYY-MM-DD, inclusive")
    ap.add_argument("--role", help="single role; default all 11")
    ap.add_argument(
        "--include-incidents",
        action="store_true",
        help="do NOT exclude known incident-spam windows (see INCIDENT_WINDOWS) — for comparison only",
    )
    args = ap.parse_args()

    roles = [args.role] if args.role else ROLES
    out = classify(args.since, args.until, roles, exclude_incidents=not args.include_incidents)

    print(
        f"belt-mechanical-reasoning-proxy: window {args.since}..{args.until} (inclusive), "
        f"commit-message-shape classification, ROUGH PROXY not a precise measure"
    )
    print(
        f"total commits in window: {out['total_commits_in_window']}; "
        f"excluded as known incident spam: {out['excluded_incident_commits']}"
        + (" (--include-incidents: exclusion disabled)" if args.include_incidents else "")
    )
    print(f"{'role':<6} {'mechanical':>10} {'substantive':>11} {'total':>6} {'subst.ratio':>11}")
    for role in roles:
        r = out["roles"][role]
        ratio_str = f"{r['substantive_ratio']:.2f}" if r["substantive_ratio"] is not None else "n/a"
        print(
            f"{role:<6} {r['mechanical']:>10} {r['substantive']:>11} {r['total']:>6} {ratio_str:>11}"
        )

    print()
    print(
        "NOT a claim about reasoning DEPTH, only commit-message SHAPE. A role can produce one huge"
    )
    print("substantive commit or ten small ones and this counts them the same. Cross-check against")
    print("Exec's session-log read before drawing a conclusion from this alone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
