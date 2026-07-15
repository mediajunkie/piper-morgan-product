---
from: ppm
to: exec
cc: xian (ceo), pa
subject: "Workstream #051 — PPM (window Fri Jul 3 – Thu Jul 9)"
date: 2026-07-14 ~7:55 PM PT
---

# Workstream #051 — PPM

**Late submission, filed 2026-07-14.** The kickoff asked for Mon Jul 13 EOD; I missed it — my session went stale mid-afternoon Jul 13 (a genuine multi-hour gap, not a choice) and I didn't resurface until this evening. Sending now in case there's still time to fold it in; if not, at least the record is straight for next time. Sourced against `origin/main` commit history for the window (not memory alone) — timestamps below are verified, not recalled.

## §0 — Progress vs. portfolio goals

**Mixed: advanced, with a significant self-inflicted incident in the middle of the window.**

The window opens with clean triage work (Jul 3-5) that built the 25-issue Beta Blockers sprint — the actual beta-gate. That's real portfolio progress: without that triage, there's no scoped sprint for Lead to execute against. Lead's execution then drove it from 25 to 10 open issues by end-of-window (Jul 7-8), which is the milestone that matters most this cycle.

But mid-window (Jul 5, evening), I caused the incident that defined the rest of the window: adding 8 new Production-sprint options to the GitHub Projects Sprint field via a full-replace mutation, which silently wiped the Sprint-field assignment for all ~1175 items on the board — project-wide, no undo, no version history. I own this fully; it was my mutation. Recovery consumed the majority of my capacity from that point through Jul 9 (and, past this window's boundary, through Jul 12): 433 HIGH-confidence + 93 MEDIUM-confidence sprint assignments reconstructed and reapplied by end of window (Jul 6), with the LOW-confidence tier (218 issues) launched Jul 9. The full effort — all 744 recoverable issues plus a 19-issue true-zero-evidence set resolved entirely from PM's direct memory — didn't close out until Jul 12, past this window.

**Net**: the portfolio's actual gate (Beta Blockers) advanced well. A real, severe process failure happened on my watch and cost real time and trust. Both are true; neither cancels the other.

## §1 — TL;DR

- Beta Blockers sprint triaged from scratch (Jul 3-5): M3-Quality/Health/Security + RECONNECT swept issue-by-issue, 25 issues landed in the sprint, milestone ground-truth audit caught 16 discrepancies before Lead started building.
- **Caused the Sprint-field wipe** (Jul 5 evening): a full-replace `updateProjectV2Field` mutation detached all ~1175 items' Sprint values project-wide, no API-level undo.
- Recovery: 433 HIGH-confidence + 93 MEDIUM-confidence assignments reconstructed and verified live by end-of-window (Jul 6); LOW-confidence tier (218 issues) launched Jul 9.
- Roadmap folded twice with PM ratification: v18.3 (Jul 3, RECONNECT WS-2 drain) and v18.4 (Jul 4, Beta Blockers sprint introduced, MVP-milestone-as-beta-gate made explicit, Aug 1 date dropped).
- **Session-log discipline broke down Jul 6 (afternoon) through Jul 8** — real work happened (verifiable via commits) but wasn't captured in a proper dated session log; Docs' Jul-7 omnibus flagged PPM as absent. Recovering by Jul 9.

## §2 — What landed

- **Beta Blockers sprint built** (Jul 3-5): swept M3-Quality (7 issues → 4 Production/3 gate), M3-Health (9 → all Production, PM: fine for Lead to cherry-pick idle-time), M3-Security (4 Production/3 gate, split from #358), RECONNECT (35 reviewed, 29 already closed, 6 → Production). Milestone ground-truth audit (Jul 5) cross-checked every open MVP issue against the Beta Blockers list rather than trusting Sprint-field tags — caught 16 discrepancies, resolved 3 → Beta Blockers, 4 → Production, 9 → a new **Ongoing** milestone (FLYWHEEL/SKUNK work that had never been in the triage sequence at all).
- **Roadmap v18.3** (Jul 3, PM-ratified): RECONNECT WS-2 buildable scope drained.
- **Roadmap v18.4** (Jul 4, PM-ratified): Beta Blockers sprint formally introduced (12 hard gates, no theme); MVP milestone = beta gate made explicit (beta ships when the milestone clears, not on a calendar date); Aug 1 target dropped as unrealistic; RECONNECT connector status corrected (PAT/keychain fallback works today — RECONNECT is an architecture migration, not a broken-connector fix).
- **Sprint-field wipe incident**, full account and root cause in `dev/2026/07/05/2026-07-05-0000-ppm-code-sonnet-log.md`: `updateProjectV2Field`'s `singleSelectOptions` argument is a full replace, not additive, and the API rejects `optionId` in the input — there's no ID-preserving path. Documented as a CRITICAL warning in CLAUDE.md same-day.
- **Sprint-field recovery, HIGH + MEDIUM tiers** (through Jul 6): 433 HIGH-confidence assignments (closedAt-vs-calendar cross-reference, Bike-outliner direct links, inchworm-map matching, explicit Tier-1 document mentions) applied and individually re-verified against the live board — zero discrepancies. 93 MEDIUM-confidence issues classified by calendar cross-check outcome for PM's review.
- **LOW-confidence tier launched** (Jul 9): 218-issue reconciliation artifact built and published for PM's systematic review (this window's final action — the tier didn't close until Jul 10, past the boundary).
- **#1235 resolved** (Jul 3-4): a Sprint-field move PM hadn't authorized got reverted by Lead, escalated to PM, and cleared per PM's ruling — same underlying fragility (informal moves without confirmation) that the wipe incident later made unmissable.
- **#1366 (PIPER.user.md unscoped-config leak)** tracked, not owned: Lead + Arch did the actual decomposition and Component A build; PPM received status copies.

## §3 — What surfaced

- **The wipe itself is the headline finding**: a Projects v2 custom field's option-list mutation can silently destroy project-wide data with no warning, no undo, and no version history exposed via the API. This wasn't a one-off — a near-identical incident had already happened to a different agent (PA) ~10 days earlier (~Jun 25) and was never actually recovered, just documented. That's the deeper pattern: a real, prior instance of exactly this damage sat unrepaired for a week and a half, and I nearly repeated the "the analysis exists, therefore the problem is solved" mistake before catching myself mid-recovery.
- **Doing the analysis is not the same as doing the work.** PA's Jun 27 CSV reconstruction (1146 rows, 265 with a proposed value) had zero rows ever applied back to GitHub. Naming this precisely mattered — it's why this window's recovery insisted on applying and re-verifying against the live board at every step, not just producing another document.
- **Session-log discipline broke down under crisis load.** The wipe and its recovery consumed enough attention that proper dated session logging lapsed for roughly 2.5 days (Jul 6 afternoon through Jul 8) even though real, substantial work was happening and is fully reconstructable from commits. Docs' Jul-7 omnibus caught this independently. This window's honest lesson: a crisis is exactly when logging discipline matters most, not when it's safest to let slip.
- **Full-replace-vs-additive is a class of risk, not a one-off**: any GitHub Projects v2 mutation that looks like a small addition (add an option, add a field) needs to be checked for whether the underlying API call is actually additive or requires resubmitting — and silently destroying — the complete prior state.

## §4 — What's still open (crosses past this window)

- **The full sprint-recovery effort didn't close until Jul 12** (past this window): LOW tier (218) + a 19-issue Sprint-field data-quality correction (S2, found to have dissolved into another sprint via a Dec-2025 reorg, never actually executed) + 19 true-zero-evidence issues resolved entirely from PM's memory. A restore script (`scripts/restore-sprint-field-from-snapshot.py`) now exists so a third incident wouldn't cost another week.
- **Production milestone reached full triage (99/99)** on Jul 12, also past this window — 8 new PROD-* sprints created as part of the reorganization that caused the wipe, most of their assignments applied same-day, but never folded into roadmap.md until Jul 12 (now v18.6).
- **#1216 flag from the milestone audit** (Jul 5): honest-provenance data-model gap, initially flagged as a possible Beta Blocker candidate. Resolved past this window — shipped a beta-safe interim fix and closed Jul 7; full fix scoped as its own Production-milestone issue (#1377).

## §6 — For PM/exec consideration

The wipe is the thing worth naming plainly in the Ship narrative if this window gets covered at all: I made a mistake that destroyed real data across the whole board, and the week that followed was substantially about earning back a baseline most other windows get for free. PM's own framing at the time (an au pair who dropped the baby; competence at routine tasks doesn't transfer to irreversible ones) is the honest register for this, not a softened one. The recovery held up — every reconstructed assignment was independently re-verified, nothing was papered over — but the cost was real and shouldn't be narrated as a clean week.

— PPM, 2026-07-14
