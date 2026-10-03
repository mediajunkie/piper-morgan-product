---
currency_claim: none
currency_claim_reason: "Rewritten at the end of every substantive fire (multiple times/day) — a
  max_age_days check would either be trivially satisfied or would need an implausibly short
  window. Declared honest per check-refresh-promises.py's --state-files mode (found ungapped/
  undeclared 2026-09-12, PPM's own seat, same self-audit pattern CXO/CIO/Exec ran this week) —
  see the prose 'Last rewritten' timestamp at the top of this file for the actual live claim."
---

# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)

**★ THIRD-QUEUE-SOURCE CRITERIA LINE (adopted 2026-09-22, per v1.33's ruling; `--limit` bug fixed
2026-09-23 13:22)** — run at every START/WATCH, not just when remembered:
```bash
gh issue list --repo mediajunkie/piper-morgan-product --milestone MVP --state open --limit 500 --json number --jq '.[].number' | sort -n | uniq > /tmp/list1.txt
grep -oE '#[0-9]{4}' dev/active/mvp-epic-order-2026-09-09.md | tr -d '#' | sort -n | uniq > /tmp/list2.txt
comm -23 /tmp/list1.txt /tmp/list2.txt   # every MVP-open issue NOT mentioned in the epic-order file
```
⚠️ **`--limit 500` is REQUIRED** — `gh issue list` silently defaults to `--limit 30` with no
warning (live bug 2026-09-22 to 2026-09-23 13:22, since fixed and re-verified clean). **Must be
`#[0-9]{4}` (4-digit only)**, not `#[0-9]+` — the looser regex catches informal prose references
("cousin #3") and false-positives. Any non-empty output = a real MVP item with no epic home; read
each issue before placing. State the denominator when reporting.

**Last rewritten**: 2026-10-03 06:33 PT (START).

**Mechanism state**: LaunchAgent cadence (`:33` past 6,9,12,15,18,21) stable since 2026-10-02
15:33 migration — `CronList` correctly "No scheduled jobs," no cron-management ritual needed.
`sprint-truth.py` per-seat baseline (CIO's fix) fully landed — reads `sprint-truth-MVP.ppm.json`,
delta header correctly names "baseline: ppm's run."

**Phase3 destination-ruling thread (DISCOVERY/ANALYSIS/TRUST/MEMORY, 13 rows) — fully CLOSED,
13/13 agreed** (2026-10-03 06:33): the one standing technical finding (D1, `session_activity_query`
scoped to current-session-only, can't answer "our last session") was conceded in full by both CXO
and Arch after they independently re-read the handler source. Arch generalized the lesson
(destination scope must match ask scope, not just topic) and named the bar for if this op is ever
considered for a `read_floor`-style wave. Nothing further owed.

**Housekeeping**: Arch fixed a main-red mailbox-filename-length incident (#1616) affecting a copy
in `ppm/read/`; regenerated PPM's own MANIFEST per the ask.

**Board hygiene**: 0 unmilestoned, 0 gap, denominator 28 — clean every fire since 2026-10-01.

**No externally-blocked items. No other open threads.**
