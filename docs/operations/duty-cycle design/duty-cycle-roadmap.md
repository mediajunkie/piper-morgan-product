# Duty-Cycle Roadmap — version arc + horizon research

**Owner**: CIO. **Created**: 2026-06-06 (PM-directed, after the `/loop` assessment surfaced Routines as a horizon enabler). **Companion to**: `v0.7-candidates.md` (near-term refinements), `loop-vs-cron-assessment-2026-06-06.md`, `cron-shape-experiments.md`.

This doc holds **forward-looking** duty-cycle direction — distinct from `v0.7-candidates.md` (incremental refinements to the *current local* design). Roadmap = where the system is *headed* across major versions.

---

## The governing lens: build-vs-ride (platform-commodification evaluation)

Every duty-cycle roadmap decision runs through one recurring question PM named (2026-06-06):

> *Each time the harness improves, has the platform commodified something we built by hand — and at what point does it make sense to stop maintaining ours and ride their surface, building new things on top?*

The recurring finding: the platform ships a **generic/easy version** that often lacks the **sophistication of the hand-built one** — the same way we build something under-the-hood that they later wrap a UI around for non-programmers. Neither "always ride" nor "never ride" is right; **each release needs the comparison.** The `/loop` assessment (2026-06-06) is the canonical worked example: `/loop` commodified scheduling, but it's a thin wrapper that doesn't match our Rule-1/Rule-2/cohort-clock sophistication → keep ours, but *Routines* (the deeper surface) is worth riding for the gap we can't close ourselves.

*(Candidate to formalize as a methodology entry — "Platform-Commodification Evaluation" — if the comparison keeps recurring per release. Sibling of m-34 cohort-discipline-as-moat + the platform-laps-you/value-chain-climbing lens. Flagged, not yet built.)*

## Version arc

| Version | Theme | State |
|---|---|---|
| v0.1–v0.6 | design iteration (cron-bind-to-IDLE, PM-presence-pause, drain-to-IDLE) | done |
| **v0.7** | **cohort adoption** — worktree Model A, overnight continuity, cron-shape-fit, thin-job-prompt skill | **current (stabilizing)** |
| **v1.0** | the local system, stable + documented — *PM's basic working method.* Thin-prompt skill cohort-wide; possibly the methodology-dream-cycle. The thing we lock before reaching for the cloud. | near |
| **v2.0 — "the airlift"** | **cloud-native** — sessions run server-side in cloud branches, laptop-independent, smoother recovery. Removes the session-alive ceiling entirely. | horizon (research-when-ready) |

**Sequencing principle (PM 2026-06-06)**: *get the local system working first* (we have it; it's the basic method) → lock v1.0 → *then* research the v2 airlift when ready. Do NOT jump to cloud now.

---

## Horizon item 1 — Routines as a watchdog for the brittle local system (nearer-term spike)

**The idea (PM 2026-06-06)**: a cloud Routine as a **helper/watchdog** that *sustains* the local duty cycle — could it intervene, nudge, restart, or trigger something that's stalled out? This is the bridge between v1 (local) and v2 (cloud): keep running locally, but add a cloud safety net.

**Why it's compelling**: our uncloseable-from-a-prompt gaps are the **session-alive ceiling** (suspend-not-destroy — laptop sleeps → session dies → no fires) AND — bigger — **Gap C: compaction silently kills session-scoped crons** (PA verified 2026-06-07; `durable:true` is a no-op here, so no flag fixes it). A server-side Routine doesn't depend on the local session at all, so it's the natural watchdog for both. **Gap C makes this load-bearing, not optional** (see `procedures/cron-lifecycle.md` Gap C): a dead cron can't self-report, so an *external* liveness monitor is the only detector for the silent-compaction-stop class. Paired agent-side floor: SessionStart-re-arm (self-heals on next resume; PA piloting).

**Open research questions (the spike must answer)**:
1. **Detection** — can a Routine detect a *stalled/dead* local cohort? Signal candidates: no new commits to `origin/main` from a role's branch in N hours; a cycle log that stopped mid-day; mailbox sitting undrained. (All git/mailbox-observable server-side.)
2. **Intervention — the hard part.** A cloud Routine almost certainly *cannot relaunch a local laptop session* directly. So the realistic interventions are:
   - **(a) Alert** — Routine detects staleness → notifies PM ("CIO went dark at 14:00, no fires since") so PM manually reopens. Low-risk, high-value, probably buildable now.
   - **(b) Server-side fallback fire** — if the Routine itself has repo + mailbox access headless, it could run a *minimal* fire server-side (drain mail, commit) to maintain continuity while the local session is down. Bigger lift; overlaps with v2.
3. **Access/auth/cost** — does a headless Routine get the repo (git push to main), the worktree, the mailbox, keychain creds? What's the auth model? Per-run cost?

**Disposition**: **FEASIBILITY CONFIRMED 2026-06-07** (`routines-watchdog-feasibility-2026-06-07.md`) — Routines are cloud-persistent + headless + clone the repo + push to `claude/`-prefixed branches (matches our convention) + git-commit-recency is the alive-signal. The open questions (headless repo access? auth? git+Slack?) all resolved YES. **Alert-only watchdog moved from "spike-worthy" to "buildable, ~4-6hr, ~$70/mo, pending PM go."** Start with (a) alert-only (cures Gap-C *detection*; pairs with the v1.3 agent-side self-heal which reduces the dark-window). (b) fallback-fire is a later design pass. **PM decision queued** (build? thresholds? Slack-only?) — see `duty-cycle-escalations-cio.md`.

## Horizon item 2 — v2.0 "the airlift" (cloud-native cohort)

**The idea (PM 2026-06-06)**: the whole duty cycle runs **in the cloud, not locally** — all ~11 sessions running in cloud branches, still coordinating around each other, **less dependent on PM's laptop being on**, and with **smoother recovery** when something fails.

**What it would buy**:
- Removes the session-alive ceiling entirely (no laptop dependency).
- Smoother recovery (cloud restart vs. manual reopen).
- True 24/7 cohort autonomy.

**What it would require figuring out (research-when-ready — NOT now)**:
- How do N cloud sessions run in branches and **competently function around each other** — the same coordination the local worktree + mailbox-on-main + explicit-paths discipline solves locally? Does that discipline port to cloud, or need rework?
- Recovery semantics — what does "smoother recovery" actually look like server-side?
- The Routines/server-side execution substrate (item 1's findings feed this).
- Cost at 11-agents-×-continuous-cloud.
- What migrates vs. what stays (the m-34 migrate-vs-stays taxonomy applied to our own infrastructure).

**Disposition**: explicit **horizon** item. PM: "obviously we're not going to jump to that right away... research this idea... when we're ready." Sequenced *after* v1.0 locks. Item 1 (watchdog spike) is the natural on-ramp — and the 2026-06-07 Routines research **answered the load-bearing question YES**: a Routine *can* clone our repo, read the mailbox, commit, and push headless (the watchdog's fallback-fire tier (B) is literally a server-side duty-cycle fire). So **v2 is no longer hypothetical** — the substrate exists; the remaining v2 work is the coordination model (collision-avoidance + per-run checkpoint since each Routine run is a fresh clone with no persistent sandbox state) + cost-at-11-agents. Item 1's fallback-fire tier is the concrete first taste.

---

## Roadmap review cadence

Revisit on each material harness release (the build-vs-ride lens), at v1.0 lock, and when item-1 spike findings land. CIO maintains; folds into the methodology corpus + Ship narratives as items advance.
