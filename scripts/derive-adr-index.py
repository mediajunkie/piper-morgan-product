#!/usr/bin/env python3
"""Derive the ADR index from ADR files' own Status headers.

B4 of the Architectural Review 2026 (closes #1455). The hand-maintained index drifted for months
(claimed "Superseded: 0" while 8+ ADRs carried corrected statuses; missing 9+ entries since June)
— the exact hand-maintained-surface class m-36/ADR-077/ADR-079 forbid. This generator makes the
index a DERIVED VIEW: the individual ADR files' Status lines are the single source of truth, and
the index is a build artifact.

B3 RULE (inherited from the corpus-disposition pass, Docs' day-1 finding, 2026-08-31): a citation
or status count TRIAGES — it orders where to look. It never DISPOSES. Do not use this index (or
any derived count) as sufficient evidence that a document is inert; check the live mechanism.

Usage: python3 scripts/derive-adr-index.py [--check]
  default: regenerate docs/internal/architecture/adrs/adr-index.md in place
  --check: exit 1 if the committed index differs from what would be generated (CI-able)
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ADR_DIR = REPO / "docs/internal/architecture/adrs"
OUT = ADR_DIR / "adr-index.md"


def extract(fp: Path):
    text = fp.read_text(errors="replace")
    m = re.match(r"adr-(\d{3})", fp.name)
    num = m.group(1) if m else "???"
    title = fp.stem
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hm = re.match(r"\s*#\s+(.+)$", line)
        if hm:
            title = hm.group(1).strip()
            break
    # Status: bold-inline form OR heading form
    s = re.search(r"^\*\*Status\*\*:\s*(.+)$", text, re.M)
    if not s:
        s = re.search(r"^##\s*Status\s*\n+([^\n#]+)", text, re.M)
    if s:
        status = s.group(1).strip()
    elif re.search(r"^#+\s*.{0,4}(DEPRECAT|SUPERSED)", text, re.M | re.I):
        status = "Superseded/Deprecated (via notice heading — no formal Status line)"
    else:
        status = "(no Status line — fix the ADR, not this index)"
    date_m = re.search(r"^\*\*Date\*\*:\s*(.+)$", text, re.M)
    date = date_m.group(1).strip() if date_m else ""
    return num, title, status, date, fp.name


def status_bucket(status: str) -> str:
    s = status.lower()
    if "supersed" in s:
        return "Superseded"
    if "deprecat" in s:
        return "Deprecated"
    if "dormant" in s:
        return "Dormant (Proposed, unratified)"
    if "historical" in s:
        return "Historical"
    if "proposed" in s:
        return "Proposed"
    if (
        "accepted" in s
        or "implemented" in s
        or "ratified" in s
        or "approved" in s
        or "complete" in s
    ):
        return "Accepted"
    if "draft" in s or s.startswith("v0."):
        return "Proposed"
    return "Other"


def generate() -> str:
    files = sorted(ADR_DIR.glob("adr-[0-9][0-9][0-9]-*.md"))
    rows = [extract(f) for f in files]
    buckets = {}
    for r in rows:
        buckets.setdefault(status_bucket(r[2]), []).append(r)
    order = [
        "Accepted",
        "Proposed",
        "Dormant (Proposed, unratified)",
        "Superseded",
        "Deprecated",
        "Historical",
        "Other",
    ]
    lines = []
    lines.append("# Architectural Decision Records (ADR) Index — DERIVED VIEW\n")
    lines.append(
        "> 🤖 **GENERATED FILE — DO NOT EDIT.** Regenerate with "
        "`python3 scripts/derive-adr-index.py`; verify with `--check`. The individual "
        "ADR files' own Status lines are the single source of truth; this index is a "
        "build artifact (Architectural Review 2026 workstream B4, closes #1455). Per the "
        "B3 rule: counts here TRIAGE, they never DISPOSE — check the live document "
        "before treating any status as the whole story.\n"
    )
    total = len(rows)
    missing = [
        n
        for n in range(0, max(int(r[0]) for r in rows) + 1)
        if f"{n:03d}" not in {r[0] for r in rows}
    ]
    lines.append(
        f"**Total ADR files**: {total} · **Numbering gaps (never filed)**: "
        f"{', '.join(f'{m:03d}' for m in missing) if missing else 'none'} · "
        f"**Counts by status**: "
        + " · ".join(f"{k}: {len(buckets[k])}" for k in order if k in buckets)
        + "\n"
    )
    for bucket in order:
        if bucket not in buckets:
            continue
        lines.append(f"\n## {bucket} ({len(buckets[bucket])})\n")
        for num, title, status, date, fname in buckets[bucket]:
            date_str = f" · {date}" if date else ""
            lines.append(f"- [{title}]({fname}) — {status}{date_str}")
    lines.append("")
    return "\n".join(lines)


def main():
    content = generate()
    if "--check" in sys.argv:
        current = OUT.read_text() if OUT.exists() else ""
        if current != content:
            print(
                "DERIVED-INDEX DRIFT: committed adr-index.md differs from generated view. "
                "Run scripts/derive-adr-index.py. (This check measured the index file against "
                "the ADR corpus at HEAD — nothing else.)"
            )
            sys.exit(1)
        print(f"adr-index.md matches generated view ({content.count(chr(10))} lines).")
        return
    OUT.write_text(content)
    print(f"wrote {OUT.relative_to(REPO)}: {content.count(chr(10))} lines")


if __name__ == "__main__":
    main()
