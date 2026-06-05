---
from: PA (Piper Alpha)
to: CEO (xian)
cc: Lead Developer
date: 2026-05-23
subject: M2 convergence memo v2 — CORRECTION: 18 open issues on project board, not 3; revised scope analysis
priority: standard — supersedes v1 (`memo-pa-to-ceo-cc-lead-m2-sprint-convergence-read-2026-05-23.md`)
response-requested: at your cadence
in-reply-to: memo-pa-to-ceo-cc-lead-m2-sprint-convergence-read-2026-05-23.md
---

# M2 convergence v2 — correction memo

## The error in v1

v1 reported 3 open M2 issues. The actual count from PM's project-board filter is **18**. Root cause: my `gh issue list --label "M2,M2g,..."` query used comma-separated labels (which don't OR in gh CLI), and most of the 18 issues aren't tagged with M2-sub-epic labels at all — they carry generic labels (`enhancement`, `architecture`, `priority: low`) plus GitHub Milestone "MVP" + project-board status fields. The authoritative grouping is the project board, which requires `read:project` scope I don't have. That's a real PA-visibility gap; flagging at the bottom as something to address structurally.

**v1's "structural M2 close mid-next-week (May 26-27)" claim was wrong.** It was a 6x undercount.

## The corrected scope (18 open issues per project board)

| # | Title | Labels | Convergence-gating? |
|---|---|---|---|
| **In active work** | | | |
| #1089 | KG-PRIVACY-FILTER | enhancement, priority:low, architecture, M2g | YES (Increment 1 of 5 shipped today `b5270c203`; ~2-2.5 hr remaining) |
| **MEM cluster (4)** | | | |
| #972 | MEM-TEMPORAL — temporal validity fields | enhancement | Yes (queued) |
| #973 | MEM-CACHE-AUDIT — stable vs dynamic layers | enhancement, architecture | Yes (PM-ratified ship-now-as-prep May 19; Phase 1 at Lead's cadence) |
| #974 | MEM-EVAL — session-end memory evaluation | enhancement | Yes (queued) |
| #975 | MEM-DELTA — delta-since-last-session context | enhancement | Yes (queued) |
| **WIRE-* superseded (4)** | | | |
| #692 | WIRE-SLACK: blocker detection | — | Likely close-on-cleanup (#1041 WIRE-TRIAGE disposition was "superseded-by-floor-migration") |
| #693 | WIRE-STANDUP: workflow settings | — | Likely close-on-cleanup |
| #694 | WIRE-GITHUB-LLM: issue generator LLM call | — | Likely close-on-cleanup |
| #695 | WIRE-GITHUB-CMD: GitHub command integration | — | Likely close-on-cleanup |
| **Test-infra follow-ups (4)** | | | |
| #989 | CANONICAL-FIXTURES — warmed-up user fixture | enhancement, priority:low | Defer / M2-discovered |
| #993 | SCORER-VOCABULARY — AAXT taxonomy adoption | enhancement, priority:low | Defer / M2-discovered |
| #994 | TEST-PATHOLOGICAL-TAGS — expected-pass vs known-pathological | enhancement, priority:low | Defer / M2-discovered |
| #995 | FABRICATION-PROBES — standalone absence probes | enhancement, priority:low | Defer / M2-discovered |
| **M2d UAT + UI (2)** | | | |
| #1047 | M2D-UAT — manual browser-smoke + a11y + perf verification | enhancement, UX | **YES — gate-shaped** (verifies M2d shipped surfaces) |
| #1050 | STANDUP-ACTIVE-REPOS — full active-repos resolution | enhancement, component:ui | Yes (Lead Dev lane) |
| **Epic / tracker (2)** | | | |
| #472 | EPIC Slack Integration TDD Gaps | — | Tracker-shaped (umbrella; some child issues closed; needs disposition) |
| #1016 | ARCH-DESIGN: LLM-touch boundary principle | architecture, epic, M2g | Tracker-shaped (implementation #1017 closed May 15) |
| **Tech-debt P3 (1)** | | | |
| #1082 | NOTION-TEST-REWRITE — against notion-client lib | priority:low, technical-debt | Defer |

## Revised convergence vector

**Close-gating issues** (the ones that genuinely need to land before M2 declares done):

- #1089 (in flight; ~2-2.5 hr stated, runs at Lead's piecemeal cadence)
- #972, #974, #975 (MEM cluster — 3 issues queued after #973's Phase 1; need Lead Dev sequencing)
- #1047 (M2D-UAT — manual verification gate; not yet scheduled per my read)
- #1050 (STANDUP-ACTIVE-REPOS)
- Disposition needed on #472 + #1016 (epics — close vs. carry as living trackers)
- Disposition needed on #692-695 (WIRE-* superseded — close cleanly or defer)

**Net**: ~8 close-gating items (could be as few as 6 if #472 and #1016 disposition as carry-trackers). That's ~3 hr of remaining build (#1089) + however long the MEM cluster takes (Lead Dev estimate needed — could be 1-2 days or 1+ week depending on scope) + the UAT + STANDUP + dispositions.

**Realistic structural M2 close**: **end of May or into early-June**, not mid-next-week. Matches your "Jun/Jul beta" intuition cleanly.

## What v1 still has right

The non-count parts of v1 hold up:

1. **Year-anniversary beta (May 27/28) is not plausible** — reinforced, not weakened, by the corrected count
2. **Run 10 canonical retest is still the missing quality-gate data point** — last Run 9 May 13 at 69.8% vs ≥75% north star; no Run 10 since despite 15+ closures
3. **Phase A Gemma simulation harness status unknown** — alpha-catch-22 reframe substrate; not visibly in flight; needs Lead Dev disposition
4. **M3-M5 are downstream** — placements landed May 5 but no shipping; "much less onerous" per PM but undated

## Two structural takeaways for PA's lane

1. **GitHub Milestone + Project board are the authoritative M2 surface, not labels.** The label-based view I queried is a partial reflection. I'm requesting `read:project` scope at next session so this gap closes structurally — see chat for the ask.
2. **The MEM cluster is a real load-bearing M2 surface** I'd missed framing. PM ratified #973 ship-now-as-prep May 19, but #972 / #974 / #975 are in the same family and aren't actively in flight per Lead's recent logs. Worth a Lead Dev sequencing call.

## Cross-references

- **v1 memo (superseded)**: `dev/active/pa-m2-convergence-memo-2026-05-23.md` and inbox copies
- **Project board** (authoritative; PA can't query without `read:project`): https://github.com/orgs/mediajunkie/projects/...
- **GitHub Milestone "MVP"** (dueOn 2026-05-27): query `gh issue list --milestone MVP --state open` (returns 30 — superset that includes some non-M2 work)
- **Other cross-refs**: see v1 memo

— PA, 2026-05-23 ~10:00 AM PT (correction filed ~30 min after v1)
