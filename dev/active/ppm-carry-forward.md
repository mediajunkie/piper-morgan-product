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

**Last rewritten**: 2026-10-05 15:55 PT (15:33 WORK).

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

**Frozen beta-gate standard: RATIFIED by PM 2026-10-05** (relayed by Exec 08:58). **v2 measured pass written and sent 09:55**
(`docs/internal/planning/beta-gate-pass-2026-10-05.md`, comment-verified; v1's "10 stay" count is SUPERSEDED, it read bodies only).
**31 open at 09:46; 31/31 bodies + threads read; `Gate class:` in 0/31.** 4 firm gate (#1889 #1913 #1595 #1386) / 5 need PM ruling
(#1735 #1852 #1907 #1886 #1925) / 4 gate-work-landed close-or-split (#1930 #1885 #1880 #1867) / 6 epic-0 evidence (#1579 #1623 #1771 #1783
#1843 #1860) / 12 Production (#1522 #1625 #1632 #1698 #1817 #1832 #1891 #1911 #1915 #1916 #1917 #1931). Non-Epic-0 gate = 3 to 7.
Range 10-23 / 10-30 conditional on 4 named unknowns (#1889 size, Lead, Wed 10-07; PM rulings, Wed 10-07; #1386 re-run duration,
PPM+CXO, Wed 10-07 sizing; Phase 3 tail, Lead, Thu 10-08 21:59). Confirm-or-move Fri 10-09. Slip rule drafted (Exec a+b, my c/symmetry/brake)
with ledger baseline in pass doc + standard; PM must edit and yes. **PM sprint ruling (via Exec 09:40): verify against the MVP milestone;
no labels; NO board/Sprint-field/label edits from PPM** (my 09:41 retire-labels/Sprint ask is superseded). `beta-blockers.md` bannered SUPERSEDED (done).
**HOLD: no board/milestone edits until Exec relays PM's yes.** On the yes, order: close #1930, #1885; split+close #1880 (residue 3 to
Production, confirm deploy), #1867 (Arch); milestone-move the 12 and (after corpus-row check, unverified) the 6; rewrite #1386 body;
apply PM's bucket-B rulings; file #1735 learning-loop follow-up if option C/Production. Then start the weekly admissions-by-class line
in the rollup (baseline 31 open at ratification, 0 admitted/closed since 10-03). R7 sent to Spec (cc Exec) and folded into the pass doc.
**PM-needs list sent to Exec 09:55**: class-4 v0.2, what the invite names (Slack/Google), Google OAuth audience, 5 rulings, #1852 console
keystrokes, #1913 answers, slip rule. **Watch for**: Exec's relay; Arch's ruling on #1867/#1886; Lead's #1889 sizing; decision-3 re-plan trigger
(gate grows, or Epic 0 tranche slips past 10-14). Later lane item (Exec's): after milestone moves Sprint values diverge; PM-confirmed cleanup.
R1's "48 created" premise is a mislabeled-TSV artifact (told Spec); do not reuse those TSVs.

Main CI green (success 16:32Z 10-05, verified 09:38 PDT; `--branch main` query returned a stale 09-13 run once, re-query without it was current).

**12:33 fire**: PM CONFIRMED slip rule (a)+(b) in his form (Exec, decisions.log); my (c)/symmetry/brake still proposed (rollup v41 decision 6). Board unchanged (31, 0 gap, no new admissions). Answered Exec on assignee: no written rule, 23/31 are `mediajunkie`, 8 unassigned all in my pass; proposed gate-issue assignment = PPM, build = Lead; field untouched, held; will own a tracking issue if PM says yes. Added v18.10 pointer to roadmap.md; **full roadmap fold (#1644 open half) due after Fri 10-09 confirm-or-move**, blocked on PM gate rulings (told Docs).

**15:33 fire**: PM said YES (13:15, via Exec): PPM owns assigning gate issues; Lead build work. Mechanism answered: Assignee stays `mediajunkie` (1787/1787 issues), role lives in `Owner:` body line, no board/label edit. Rule filed **#1940** (Ongoing). **BLOCKED: classifier denied my board-placement of #1940 and assignee-set on the 8 unassigned (#1931 #1930 #1925 #1917 #1916 #1915 #1913 #1911); neither ran.** Told Exec it's a permission setting. **Next fire: if allowed, (1) `gh project item-add` + Product Backlog for #1940, (2) `--add-assignee mediajunkie` on the 8, (3) re-count unassigned.** Do not touch the 23. Backfill `Owner:` on gate issues only, after PM reviews #1940.

**Externally blocked**: the board-edit yes (PM via Exec) gates the applying of the pass; nothing else.
