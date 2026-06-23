# Migration Wave Retrospective — June 2026 ("the whole crew home again")

**Author**: CIO (Chief Innovation Officer) · **Date**: 2026-06-19 · **Status**: COMPLETE
**Scope**: the June 2026 cohort migration — consolidating all agents back onto PM's main account, with bundled per-role model alignment, worktree-model standardization (Model A → Model B ephemeral), and duty-cycle standardization (CronCreate). PM-confirmed complete 2026-06-19: *"PPM migrated yesterday. The whole crew is home again."*

This is the first complete-wave retrospective. It exists because the wave was a multi-day, 11-agent coordinated operation that produced durable methodology — the lessons should outlive the wave, and the *next* migration (Klatch rouse; any future account move) should start from here.

---

## 1 · What the wave was

A coordinated migration of the full cohort onto a single account ("home"), one agent at a time, each via a two-prompt handoff. It bundled four changes per role:

1. **Account consolidation** — every agent back onto PM's main account.
2. **Model alignment** — each role set to its `role-model-map.md` (RATIFIED 6/13) tier (Opus for Arch/CIO/Exec/Lead; Sonnet for the rest; PA Sonnet).
3. **Worktree-model standardization** — Model A (dedicated `claude/{role}-cycle` worktrees) → **Model B ephemeral** (the auto-worktree per session). Model A fully deprecated, **zero carve-outs**.
4. **Duty-cycle standardization** — CronCreate windowed crons (the cohort standard), replacing the scheduled-task experiments.

## 2 · Timeline (authoritative — from plan-of-record §5)

| Order | Role | Migrated | Model | Phase |
|---|---|---|---|---|
| 1 | **PA** | 6/11 | Sonnet | Pioneer — thin-prompt exemplar; bundled model change; clean |
| 2 | **Exec** | 6/12 | Opus | Self-migrated lead — **hit the variant-preservation trap** (→ m-41 Proven); its diagnostic memo drove the wave's fixes |
| 3 | **Lead Dev** | 6/12 | Opus | Self-authored handoff with §6 tacit knowledge (**the wave's best exemplar**); proved no Model-A exception needed |
| 4 | **CIO** | 6/12 | Opus | Account-move only; **then supervised the rest of the wave** |
| 5 | **HOST** | 6/13 | Sonnet | First CIO-supervised migration |
| 6 | **Comms** | 6/14 | Sonnet | |
| 7 | **Docs** | 6/14 | Sonnet | Merge-keeper — migrated mid-order so the safety net stayed live |
| 8 | **Web** | 6/17 | Sonnet | |
| 9 | **Arch** | 6/17 | Opus (no change) | |
| 10 | **CXO** | 6/18 | Sonnet | |
| 11 | **PPM** | 6/18 | Sonnet | **Last of the wave** — completes the migration |

**Span**: 6/11 → 6/18 (~8 days). **Two phases**: pioneers/leads self-migrated (PA, Exec, Lead, CIO), then CIO drafted each pair + supervised the remainder (HOST → PPM).

## 3 · What worked

- **One-at-a-time, supervised.** No parallel migrations. Each role got a dedicated, reviewed handoff/bootstrap pair before PM fired it. Zero migrations had to be redone.
- **The two-prompt structure.** Handoff-half (what to carry: live threads, cron, lane specifics) + bootstrap-half (re-anchor: role identity, canonical patterns, report-back). Clean separation of "what's in flight" from "who you are."
- **Verify-the-pair-before-firing caught currency drift.** Verifying Arch's pair caught two stale lines today's changes had created (a deprecated escalations-doc pointer; a "being built" watcher that was already live). The pair-review step is where migration-day surprises get pre-empted.
- **The supervisor migrated early (4th) then drove the rest.** CIO migrating before supervising meant the supervisor had lived the process — every downstream pair encoded a lesson the supervisor had hit personally (e.g., the §5 variant trap → the plan-of-record-wins rule baked into HOST's pair).
- **The continuity infra held under real stress** (see §6).

## 4 · What we learned (methodology instances)

- **m-41 — Mechanism Displaces Unreferenced Discipline / the variant-preservation trap.** Exec (6/12) preserved its predecessor's *stale operating-model variant* (a dedicated worktree the cohort had deprecated). This was the **founding instance** that drove m-41 to Proven. CIO hit a sibling instance (its bootstrap §5 pointed at the stale worktree model). **Cure, codified into every subsequent pair**: a **MIGRATION INTENT preamble** — *"do not preserve the predecessor's operating-model variant; the plan-of-record wins any conflict."* Force-by-constraint, not vigilance.
- **methodology-29 — pattern formation via imitation.** The wave propagated thin-prompt + windowed-cron + one-place-logging by each migrated agent imitating the prior one's pair. The discipline spread structurally, not by broadcast.
- **No Model-A exception is needed — proven, not assumed.** Lead Dev (whose dev-server binds a worktree path — the one plausible exception) determined empirically that the ephemeral worktree nests inside the main checkout, so `find_dotenv()` walks up and finds main's env. The nested-walk-up property generalizes → **zero carve-outs**. A would-be exception was retired by evidence.
- **The cron is the fragile part, and it's session-only.** Every migration had to re-arm the cron because CronCreate jobs die with the session. This recurred enough that it became a **load-bearing rule** in the codified format (cron-as-literal-CONSTANT) and motivated the freeze-watcher.

## 5 · Durable artifacts produced

- **`migration-prompt-format.md`** (6/18) — the wave's instinct-extracted handoff/bootstrap pattern, promoted to a *designed, reusable template*. Two load-bearing rules named: **cron-as-literal-CONSTANT** + the **inherited-blocked-task slot**. **Validated cross-project by Janus** (it transferred to a different substrate — local-cron, state-in-files — with only context-fitting). This is the single most reusable output of the wave.
- **`duty-cycle-registry.tsv` + the launchd freeze-watcher** — per-role liveness thresholds + Gap-C cures (active→silent AND closed→never-restarted). Now watches all migrated cycling roles.
- **The escalations-fold** (skill v1.13) — removed the per-role escalations-doc surface; PM-attention items ride the carry-forward. A simplification the wave surfaced as redundant.
- **`role-model-map.md`** (RATIFIED 6/13) — the per-role model tiering the wave applied.
- **Plan-of-record §5** — the live migration tracker (now to be marked COMPLETE).

## 6 · The battery-outage coda — the continuity infra tested, and it held

The day after the wave completed (6/18 afternoon), a **battery outage** (~10:17–17:00) killed sessions and crons cohort-wide — an unplanned, real-world stress test of exactly the continuity infrastructure the wave standardized. Outcome: **it held.**
- Sessions resumed; **no work was lost** (CXO confirmed; CIO confirmed).
- The **retroactive day-close self-heal** worked (6/18 had no STOP → closed cleanly at the next START).
- The outage **exposed one honest boundary**: the on-machine freeze-watcher dies *with* the machine, so it can't alert during a machine-death (only after return). Documented in the freeze-check header; the off-machine Routines watchdog ($70/mo, PM-deferred) is the cure for that class — a captured data point, not yet a re-raise.

The wave didn't just consolidate accounts — it left behind continuity infra robust enough to survive a cohort-wide hardware outage with zero lost work the very next day. That's the validation that matters.

## 7 · Forward recommendations

1. **Klatch inherits the format.** When Klatch is roused, hand them `migration-prompt-format.md` (already queued) + a pointer to this retro. They get the designed template, not the instinct version we had to learn the hard way.
2. **The format is now canonical for any future migration** — account moves, model changes, tool migrations. Start from the template; don't re-derive.
3. **Get all cycling roles into the freeze-registry.** It currently watches cio/exec/arch/cxo/ppm. The other cycling roles (host/comms/docs/web/pa/lead) should be added so the liveness net covers the whole cohort.
4. **Revisit the off-machine watcher only on a recurrence trigger** — outages recurring or costing work. One no-harm outage is a data point, not a mandate.
5. **Retire the in-wave runbook precursor** in plan-of-record §5 in favor of the codified format (the §5 list is now historical).

---

*Prepared by CIO, 2026-06-19. Source artifacts on origin/main: plan-of-record §5 · `migration-prompt-format.md` · m-41 (Proven) · the per-role migration pairs (`dev/active/{role}-{migration-handoff,bootstrap-brief}-*.md`) · CXO battery-outage report · the duty-cycle-registry + freeze-watcher.*
