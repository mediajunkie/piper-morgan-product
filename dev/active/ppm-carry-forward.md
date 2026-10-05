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

**Last rewritten**: 2026-10-05 09:41 PT (09:33 WORK).

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

**Board hygiene**: MVP denominator **31** (6 SB / 2 IP / 3 IR / 20 PB; 1229 done). `#1933`, `#1926` closed by Lead. `#1934` (guard hardening) and `#1936` (requirements.lock uninstallable, filed by Pard; MVP-flagged by criteria line, I moved it to Ongoing 21:3x as infra) placed Ongoing + board, verified by 21:3x sprint-truth. 10-04 09:4x placed `#1930`
+ `#1931` (MVP, board-added, epic 0 entry) and `#1927` (tooling, Ongoing + board). Filed `#1932` (Production). 0 unmilestoned, 0 gap. Recurring:
Phase-3-lane issues land with no milestone/board (5 this week); sprint-truth's "NOT ON THE BOARD" line is
the tell, and Lead was sent an FYI (no action owed). Each fire: milestone MVP -> `gh project item-add 1`
-> set Status Product Backlog (id `e7d1c990`, project `PVT_kwHOADE-8s4A-JwA`) -> epic-order entry.

**ROUTING CHANGE (Exec broadcast 2026-10-03 17:28, PM ruling)**: PM's mailbox is retired. NEVER write to
`mailboxes/xian (ceo)/`; PM is not in `to:`/`cc:` of anything. Needs PM -> address to `exec` and name which
of the three conditions (decision only PM can make / relayed PM ruling / PM would contradict) in the
subject. The 09-11 cc-PM rule is retired.

**Frozen beta-gate standard: RATIFIED by PM 2026-10-05** (relayed by Exec 08:58). Pass done and written
(`docs/internal/planning/beta-gate-pass-2026-10-05.md`, 31 bodies read): **10 stay (#1885 #1735 #1889 #1880 #1852 #1913
#1907 #1386 #1595 #1925), 1 closes (#1930), 6 epic-0 evidence (#1579 #1623 #1771 #1783 #1843 #1860), 2 held for Arch
(#1867 #1886), 12 to Production (#1522 #1625 #1632 #1698 #1817 #1832 #1891 #1911 #1915 #1916 #1917 #1931).**
Standard now carries R7's per-surface section. **HOLD: no board/milestone/label edits until Exec relays that PM said yes**
(decision memo sent 09:41: board-edit yes, class-4 clarification, Google OAuth audience call). On the yes, order:
close #1930; milestone-move the 12 + (after corpus-row check, unverified) the 6; file #1735 learning-loop follow-up
(Production); rewrite #1386 body (still says Beta Blockers sprint / Fly artifact); retire parallel records. Then start the
weekly admissions-by-class line in the rollup (baseline: 31 open at ratification, 0 admitted/closed since 10-03).
R7 sent to Spec (cc Exec). Decision-3 recommendation (design partners by Fri 10-23, outer 10-30) is with Exec.
**Watch for**: Exec's relay; Arch's ruling on #1867/#1886; re-plan trigger for decision-3 if the gate list grows or Epic 0's
tranche slips past 10-14. R1's "48 created" premise is a mislabeled-TSV artifact (told Spec); do not reuse those TSVs.

Main CI green (success 16:32Z 10-05, verified 09:38 PDT; `--branch main` query returned a stale 09-13 run once, re-query without it was current).

**Externally blocked**: the board-edit yes (PM via Exec) gates the applying of the pass; nothing else.
