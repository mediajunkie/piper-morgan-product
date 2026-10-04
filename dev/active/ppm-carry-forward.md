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

**Last rewritten**: 2026-10-04 06:50 PT (START).

**Mechanism state**: LaunchAgent cadence (`:33` past 6,9,12,15,18,21) stable since 2026-10-02
15:33 migration — `CronList` correctly "No scheduled jobs," no cron-management ritual needed.
`sprint-truth.py` per-seat baseline (CIO's fix) fully landed — reads `sprint-truth-MVP.ppm.json`,
delta header correctly names "baseline: ppm's run."

**Phase3 destination-ruling thread (DISCOVERY/ANALYSIS/TRUST/MEMORY, 13 rows) — fully CLOSED,
13/13 agreed, verified live** (2026-10-03 09:33): D1 (`session_activity_query` scope) is now
shipped in the rail description and measured correct on the served model. C1 ("threats to our
timeline") settled at ANALYSIS/`analyze_blockers` after CXO reversed back to PPM's original call,
citing Lead's served-model measurement + CXO's own internal consistency. Zero outstanding
disagreement. Nothing further owed.

**Sprint goal (locked 2026-10-03, Exec relaying PM)**: week ending Thu 10-08 = finish epic 0 Phase 3
deletions for every list with a live wave; Lead owns; plan for FOUR days of capacity (quota ~exhausted Wed
~14:10). PPM holds nothing on the critical path (acked to Exec 12:3x). Standing posture: turn any
PPM/CXO destination-ruling request same-fire, verify against `action_registry.py` + handler docstrings.
Seat is now Sonnet 5.5.

**Housekeeping**: Arch fixed a main-red mailbox-filename-length incident (#1616) affecting a copy
in `ppm/read/`; regenerated PPM's own MANIFEST per the ask.

**Board hygiene**: MVP denominator **30** (6 SB / 2 IP / 3 IR / 19 PB; 1225 done). 18:33 placed `#1925`
+ `#1926` (MVP, board-added, epic 0 entries). `#1924` closed by Lead. 0 unmilestoned, 0 gap. Recurring:
Phase-3-lane issues land with no milestone/board (5 this week); sprint-truth's "NOT ON THE BOARD" line is
the tell, and Lead was sent an FYI (no action owed). Each fire: milestone MVP -> `gh project item-add 1`
-> set Status Product Backlog (id `e7d1c990`, project `PVT_kwHOADE-8s4A-JwA`) -> epic-order entry.

**ROUTING CHANGE (Exec broadcast 2026-10-03 17:28, PM ruling)**: PM's mailbox is retired. NEVER write to
`mailboxes/xian (ceo)/`; PM is not in `to:`/`cc:` of anything. Needs PM -> address to `exec` and name which
of the three conditions (decision only PM can make / relayed PM ruling / PM would contradict) in the
subject. The 09-11 cc-PM rule is retired.

**Frozen beta-gate standard (Spec ask, PM-endorsed idea)**: proposed doc written
(`docs/internal/planning/beta-gate-standard.md`, v0.1, 4 classes incl. my added golden-path blocker).
Replied to Spec; decision memo to Exec (cc-condition (a)): ratify, retire parallel records
(Sprint-field / `beta:*` labels / beta-blockers.md tables), and date-the-design-partner-invite vs date-beta.
**Status 10-04 06:33**: Exec acked; decisions 1+2 are on PM's rollup (blocked on xian), decision 3 waits on Lead's Epic 0 estimate (Exec requested it). Nothing for PPM to do until a ruling lands.
**Watch for**: PM's ruling via Exec. If ratified, PPM runs the one-time pass over the 30 open MVP issues
(read each body; board edits need PM confirmation) and starts the weekly admissions-by-class line in the
rollup. Ask Lead for a remaining Epic 0 wave estimate if PM wants to commit to 10-30. R1's "48 created"
premise is a mislabeled-TSV artifact (told Spec); do not reuse those TSVs as creation counts.

**No externally-blocked items.** Only open thread: the gate-standard ruling above (PM-gated, via Exec).
