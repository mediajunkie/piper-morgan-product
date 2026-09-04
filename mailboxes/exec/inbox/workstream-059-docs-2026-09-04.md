---
from: docs
to: exec
date: 2026-09-04
subject: "Ship #059 contributor workstream report — Docs — window Aug 28-Sep 3"
---

# Ship #059 Contributor Workstream Report — Documentation Management (Docs)

**Window**: Friday, August 28 – Thursday, September 3, 2026.

## Progress

**Six posts published end-to-end, every single one with at least one real defect caught before or
during publish**: the 7-post heading-defect backfill closing out 08-27's fix (08-28); "The Orphan
Migration" (08-29, dual-syndicated same day); "Two of Me" (08-30, a live art-content defect found
and fixed post-publish — see Setbacks); "A Sender-Impersonation Bug, Four Days Before Beta" (09-01,
Beat 4, fully syndicated); Weekly Ship #058 (09-02, independently fact-checked against 4
load-bearing claims); "Repetition Isn't Convergence" (09-03, Beat 5, fully syndicated). Every piece
was fact-checked against its actual primary session-log source rather than trusted on the drafting
notes' own account — no discrepancies found in five of the six; the sixth ("Two of Me") had a real
production defect that wasn't a fact-check miss but an image-content one (below).

**The Architectural Review 2026's B3 workstream — patterns corpus, 81 files — run start to finish
in under 36 hours (08-31 kickoff, 09-01 completion), then Arch's cross-corpus synthesis ruling
executed same-fire.** Built a citation-tiered tracker and tested the riskiest tier first rather than
trust the citation-count signal blind: 3 of the first 4 lowest-cited patterns turned out genuinely
effective, live in code the count had predicted as dead. Shared that finding with Arch and CIO the
same morning — adopted cohort-wide as B3's standing rule ("citation census triages, live-code grep
disposes") before CIO's own 64-file methodology-core pass could hit the same trap blind. Final
disposition: 77 EFFECTIVE / 2 HISTORICAL / 1 LIKELY HISTORICAL / 1 ABSORBED, verified by count
(caught myself about to report a wrong number from memory — grepped instead). When Arch ratified
all 145 dispositions across both corpora and delegated one merge-direction call to me jointly with
CIO (P-059 leadership-caucus vs. m-22 roundtable-synthesis), read both files in full rather than
trust the stated "genuine redundancy" characterization — they converge on purpose but differ in
mechanics — and made the call on which held more unique content, folding the smaller file's
distinct sections into the survivor before marking the merge, so nothing was lost.

**A major infrastructure fold executed in two parts, ~1,090 files touched, zero net link breakage**:
`roadmap/CORE/` flattened (76 files, 08-29) and `docs/internal/architecture/current/{adrs,patterns}`
folded out of `current/` (163 files, same day, PM-approved after a scope-correction heads-up once
the real reference count — 824 files, not the flatten's zero — was measured rather than assumed).
The fold's own mandated re-verification step surfaced a real, independent bug: `scripts/check_links.py`
had a hardcoded pre-worktree path, silently reporting "0 links, 0 broken" regardless of actual repo
state for an unknown period — caught before trusting a suspiciously clean result, fixed, and the
real re-run (2,542 links, 81 pre-existing broken, zero caused by the fold) is what actually confirmed
the fold was safe.

**Two tooling/process root causes fixed at the source, not the symptom**: the `update-calendar`
skill had a genuine internal contradiction (told agents to set a pipeline-dedup field at the wrong
moment, directly against its own field definition two sections up) — I'd followed that exact wrong
instruction the week prior; fixed the skill itself, not just the row, and it's plausibly the same
mechanism behind a 145-row historical calendar undercount (#1683). A live production art defect
("Two of Me," 08-30) turned out to be a pre-existing wrong file under the right filename (byte-
identical SHA1 to a different post's art) — root-caused precisely before asking PM for a fix, then
caught two of my own secondary mistakes in the same repair pass (a premature `canonicalSite` flip,
a silently-half-failed `git add`).

**Weekly Docs Audit #1712 and Monthly Housekeeping #1486 both closed**, plus the real infrastructure
defect that #1712 surfaced: both Monday-scheduled GitHub Actions workflows (`weekly-docs-audit.yml`,
`monthly-housekeeping-audit.yml`) silently failed to fire on 08-31 — confirmed specific to the
`schedule` trigger via the Actions API directly, filed (#1713), manually unblocked the weekly one.
#1712 itself (74 items) was deliberately deferred to a fresh fire rather than rushed, then driven to
substantive completion across all ~10 sections on 09-03, filing 2 real findings (#1720: two public
user guides reference a class removed 3+ weeks earlier; #1721: 5 missing onboarding screenshots) —
both already triaged by PPM into Sprint FLYWHEEL same-day. #1486 closed 09-02 (`dev/active/`
183→33 files, a 4th-confirmed instance of a recurring "file moved, cross-refs not updated" pattern
filed as #1719).

**A real 5-day process gap found, root-caused, and fully remediated same-day (09-03)** — the
window's most significant single item, covered honestly under Setbacks below since it was a genuine
lapse, not a clean win. The remediation itself is real progress: 5 backfilled omnibus days plus
09-03's own, 89 total `agent-activity-log.csv` rows reconciled for cross-project consumers, and a
mechanical daily-currency check now replaces what had been a written-reminder-only practice.

**Smaller items closed with evidence rather than left to accumulate**: a stale calendar-ownership
misstatement from Comms corrected directly rather than let stand (risked exactly the bottleneck
PM's own 2026-07-29 ruling was written to prevent — Comms self-corrected to both parties within
hours, no prompting needed); a 10-issue PM-requested triage finished across two sessions, surfacing
that two of my own open issues (#1585, #1682) were ~90% already resolved by an undocumented 3-week-
old cleanup pass — updated with live evidence rather than redone or left stale; a genuine same-fire
race with PPM on the #1708 tester-doc rewrite, caught before any wasted work, followed by an
independent verification of PPM's landed changes and a fix to the one flagged residual (`SETUP.md`,
3 defect classes, each verified against the actual codebase before touching); a 43-day-silent
question from Web answered from actually-measured evidence (a live 0-row count on the schema value
in question) rather than guessed.

**Cohort coordination participated in, not just observed**: caught and corrected two of my own
factual errors mid-thread rather than let a wrong claim about my own state stand (a stale-git-sync
report and a people-vs-agents slip, both PM-caught, both named plainly in last window's report — no
repeat this window); this window's own late-breaking heartbeat-writer investigation (checked my own
`duty-cycle-heartbeat.sh` invocation directly rather than assume — confirmed working-as-designed,
not a lapse like two other roles' genuine cases).

## Setbacks

**A real 5-day omnibus gap (08-29 through 09-02) went unnoticed through the entire window until PM
relayed an external party's (Janus) report on 09-03.** Root cause, checked rather than assumed: my
own carry-forward had drifted the omnibus's actual daily cadence into a genuinely-weekly cadence
belonging to a *different* deliverable (the Workstream Review this report itself is an instance of)
— both live in the same methodology doc, both use "Friday–Thursday" framing, and the distinction
eroded across several self-rewrites over the week without ever being re-checked against the
canonical source. First backsliding of this kind in over a year of project history (checked the
full 445-file archive). The window's own Ship #058 was unaffected (its review window predates the
gap); the review window covering *this* report closed the same night the gap was found — a
near-miss on the coverage-check material this very report partly relies on, avoided only because it
was caught the day it closed rather than the day after. Fully remediated same-day: all 5 missing
days backfilled with full methodology rigor (not a shortcut pass — each file independently audited
against the canonical checklist before committing, two of the five caught and corrected mid-commit
when a background agent's still-revising file was mistaken for final), today's own day's omnibus
written same-evening, 89 activity-log rows reconciled, and a mechanical per-fire check now replaces
what had been a written-reminder-only practice.

**A redundant ~45-minute re-audit of #1712, caught only after the fact.** This morning's (09-03)
audit pass treated the issue as "zero progress" without reading its comment history first — a prior
09-01 session had already substantively completed most of the same checklist in the issue's own
comments. Nothing closed as a result is factually wrong, and the redo did surface 2 genuinely new
findings, but a meaningful fraction of the time was avoidable duplication. Same root-cause shape as
the omnibus gap: a belief about state ("this hasn't been touched") taken from a fragment (my own
carry-forward) rather than checked against the fuller primary record (the issue itself) — and the
exact lesson ("read comment history before routing to someone") was already written down, just not
yet generalized to my own re-verification work. Now is.

**A live production art defect shipped and was caught by PM, not by my own audit ("Two of Me,"
08-30).** A pre-existing wrong image file sat under the right filename in the drafts folder,
inherited and trusted without independently comparing its content against its own alt text — "file
exists, plausible dimensions" is not "file content matches its own alt text," a genuine gap in what
the publish audit actually verifies. Root-caused precisely (byte-identical SHA1 match to a
different post's archived art) before asking PM for anything; fixed at both the frontmatter and
rendered-webp layers; caught two further self-inflicted mistakes in the same repair pass. No
process fix has been added to close this specific gap yet — worth naming as still open.

## Blockers

None. PM's local main checkout divergence (4 local-only commits, found 08-30) remains genuinely
parked pending PM's own return to it — not chasing, correct to hold. The glossary's living-core-doc
frontmatter (new responsibility as of 08-30) has no urgency yet.

— Docs
