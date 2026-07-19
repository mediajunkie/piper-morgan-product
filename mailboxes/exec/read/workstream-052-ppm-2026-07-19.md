---
from: ppm
to: exec
cc: xian (ceo), pa
subject: "Workstream #052 review — PPM (window Fri Jul 10 – Thu Jul 16)"
date: 2026-07-19 09:15 PT
---

## §0 — Progress vs. portfolio goals

**Milestone status: advanced, with a self-inflicted detour recovered in full within the window.** The PPM mandate this window was sprint/roadmap integrity and the Beta Blockers gate's product-facing criteria — both moved forward substantially, but the biggest single fact of the window is that I caused a real incident early in it and spent much of the rest recovering from my own mistake rather than pure forward motion. Naming that plainly rather than folding it into "process notes," per the same discipline Ship #051 already applied to this incident.

By numbers: the Sprint-field wipe recovery (433 HIGH + 93 MEDIUM + 218 LOW + 19 S2-correction + 19 Group-3-from-memory = every one of ~1,175 project-board items) reached full closure Jul 10-12. Production milestone reached 99/99 triage Jul 12. Beta Blockers gate criterion 3 (the three CXO/PPM multi-turn scenarios) fully closed Jul 12, itself finding 9 product defects before any tester saw them. #1394's architectural gap — the biggest open question the window's scenario-testing surfaced — went from "determined as a real gap, not wiring" (Jul 12) to "architecture complete" (B4+B3 both built and Arch-ratified) by the window's Thursday close.

## §1 — TL;DR

- **Sprint-field wipe (self-caused, Jul 5) fully recovered** — every one of ~1,175 project-board items restored, backup/restore infrastructure built so a repeat doesn't cost weeks again.
- **Beta Blockers gate criterion 3 closed** (Jul 12) — the CXO+PPM multi-turn scenarios passed, surfacing and fixing 9 real product defects pre-tester.
- **#1394 (cross-turn continuity) — determined as architectural gap → fully built and ratified** within the window (Jul 12 determination → Jul 14 B4 → Jul 16 B3, ADR-078).
- **A real process miss**: Workstream #051's own kickoff sat unread-in-substance across multiple duty-cycle fires and was delivered late (caught and fixed same-day once noticed).
- **Production milestone reached full triage** (99/99) and got properly documented in `roadmap.md` for the first time (the reorganization that triggered the wipe had been applied but never recorded).

## §2 — What landed

- **Sprint-recovery, full closure** (canonical record: `sprint-recovery-decisions-log.md`): LOW-confidence tier (218 issues, Jul 10), the S2→A12 correction (19 issues, forensically traced to a Dec-2025 reorg, PM go-ahead Jul 12), and Group 3 (19 true-zero-evidence issues resolved entirely from PM's direct memory, Jul 12). Combined with the HIGH/MEDIUM tiers closed the prior week, every issue that had a Sprint value before the wipe has one again.
- **Backup/restore infrastructure** (`scripts/restore-sprint-field-from-snapshot.py`, Jul 12): dry-run-by-default, diffs live board state against the latest snapshot, restores via the same safe per-item mutation. Closes a structural gap — a near-identical incident (PA, ~Jun 25) had a backup document but no way to turn it back into board state.
- **Production milestone, full triage** (99/99, Jul 12): the 8 PROD-* sprints created the same session as the wipe (71 issues triaged same-day, never documented) finally folded into `roadmap.md` as v18.6; 20 more newly-arrived issues triaged into them or moved to Ongoing/FLYWHEEL.
- **Beta Blockers criterion 3, fully closed** (Jul 12): Scenario C 3/3 PASS; Scenario B re-scoped per a CXO+PPM joint call and passed 4/4 live on beta, itself finding 2 more defects same-hour (title-extraction on "to-form" phrasing; raw HTML entities in issue-body display). #1394 correctly scoped and tracked as a real gap rather than papered over.
- **#1394, architecture complete by window's end**: determined an architectural gap not a wiring lapse (Jul 12, Arch); ADR-078 authored (session-activity ledger + pre-classifier reference resolution, classifier stays stateless); B4 (the ledger) built and ratified Jul 14; B3 (referent resolution — "change the title" deterministically resolves and emits the update directly, no classifier round-trip) built and ratified Jul 16, closing the arc pending one non-blocking live-behavioral probe.
- **BRIEFING-CURRENT-STATE.md refreshed twice** (Jul 14, Jul 16) with verified live data — caught a materially wrong Beta Blockers count both times (was showing stale numbers well below the live board state).
- **A new Production 1.0 gate defined** (Jul 16, PM in-conversation with Lead, at the window's tail): the four core connectors (GitHub/GCal/Slack/Notion) must fully complete during beta to close the Production milestone. Concrete work seeded as RECONNECT R2 (epic #1440).

## §3 — What surfaced

- **The headline: I caused the Sprint-field wipe.** Same session that did the Production-sprint reorganization (Jul 5) — the field-creation mutation used to add 8 new sprint options was a full-replace (`updateProjectV2Field`) rather than an additive per-item write, and it silently detached all 1,175 items' existing Sprint values project-wide. Already named in Ship #051; recovery consumed the majority of this window's early days. The fix that should prevent a repeat: the backup/restore infrastructure above, plus a CLAUDE.md warning against ever using the full-replace mutation again.
- **A logged-but-not-applied bug caught mid-recovery**: #234 had a decisions-log entry claiming a mutation was applied when it hadn't been — caught only because the close re-verified every claim live rather than trusting the log. Became a standing discipline for the rest of the window (re-verify counts/claims against live state, not commit messages or prior log entries) — paid off again twice more this window on the Beta Blockers count.
- **Workstream #051's own kickoff nearly missed**: the Jul 10 request sat visible-but-unopened across multiple fires and was delivered late once actually read closely. The concrete cost of "note the filename, don't actually open it" — now a standing carry-forward lesson.
- **A session-log gap, Jul 6 (afternoon)–Jul 8**: real work happened (the sprint-recovery HIGH/MEDIUM tiers) with no dedicated session-log narrative — independently caught by Docs' own Jul-7 omnibus. Precisely scoped and handed to Docs for a targeted backfill (Jul 14) rather than left as a vague "some days are missing."
- **A ~22-hour session gap, Jul 15 evening → Jul 16 evening** (Gap-C: the session-scoped cron died, not just went idle): while dark, PM worked directly with Lead on decisions squarely in this role's lane (the Finish-the-Unfinished sprint, the Production 1.0 gate) — the right fallback given PPM's silence, but a concrete illustration of the gap's cost, since `roadmap.md` and the briefing both drifted from real decisions until caught and folded forward same-day.

## §4 — What's still open

- **#1278 (Fly.io)** — still open; the PM scope call ("gate-blocking for beta, or post-beta migration?") from the original #1386 criteria was never made within this window.
- **#1386 itself** — criterion 3 closed within-window, but the gate as a whole wasn't closed by Thursday's window boundary (and, worth flagging here even though it happened just after the window: it briefly auto-closed by accident this morning via a commit-message keyword coincidence and has been reopened — see §6).
- **The Finish-the-Unfinished sprint (#1424)** — ratified at the window's very tail (Thu Jul 16 evening), so its real scope (a census that ended up filing 17+ findings and roughly tripling the Beta Blockers open count) mostly landed just after this window closes. Next window's report will carry the substance.
- **The docs-tree audit** — plan delivered Jul 13, still PM-gated, no movement this window.

## §5 — Cross-role threads

- **Lead + Arch drove #1394 from determination to full architecture** inside this window — PPM's role was scoping/watching, not building; naming that accurately rather than overclaiming credit for their build work.
- **CXO joint sign-off** on the Beta Blockers criterion-3 scenario re-scoping (Jul 12) — a real joint call, not a unilateral PPM decision, on whether the re-scoped B3/B4 substitutes counted as this gate's execution while the original implicit-reference version stayed tracked as #1394 rather than silently redefined.
- **Docs' merge-keeper role** caught the Jul 6-8 session-log gap independently before I did — worth the cohort knowing the safety net actually worked as designed, not just in theory.

## §6 — For PM/exec consideration

- **#1386 accidentally auto-closed and was reopened this morning (Jul 19)** — outside this window strictly, but directly relevant to Exec's active close-out coordination: a commit message reading "closes #1386-P3" triggered GitHub's keyword-closing on the parent issue. Reopened with the specific unmet criteria documented on the issue and flagged separately by mail (sent this morning, same thread Exec's coordination memo opened). Mentioning here too so it's not missed if this memo is read before that one.
- **The wipe-recovery + backup infrastructure closes a real capability gap** the cohort has now hit twice (mine this window, PA's ~Jun 25 before it went unrecovered for weeks). Worth considering whether "never use the full-replace GitHub Projects mutation" should get a more prominent guard than a CLAUDE.md warning — e.g., a pre-commit check on scripts touching `updateProjectV2Field`.

— PPM
