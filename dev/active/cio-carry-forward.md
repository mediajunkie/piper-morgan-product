# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live **here**, in the section immediately below.

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction links/ideas drop file. Standing cadence: pick at least one "New" item per PM conversation and discuss it together (see `feedback_ideas_backlog_digestion_cadence.md`).

> **Rewritten 2026-07-25 ~14:05** (not appended). The pre-migration version had accreted into a day-by-day archive with `(superseded)` markers stacked on resolved items — the exact drift my predecessor flagged in the handoff ("needs periodic *rewriting*, not just appending"). Resolved items are **deleted here, not annotated**; the dated session logs are the permanent record. If you find yourself adding a third `(superseded)` marker, rewrite instead.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly per its SKILL.md Step 1.)*

- 🟡 **COHORT MIGRATION — gate is the behavioral hooks check at agent #2 (HOST).** Pard has wired user-level hooks in `~/.claude-pm/settings.json` (incl. the finding-#5 PreCompact restore), landed the tracked mirror with the atomic-update rule, and verified the script cannot wedge a session. **My own behavioral check came back NOT-blocked — AMBIGUOUS, not a fail**: my session predates the wiring, so it cannot distinguish startup-only loading from a bad fix. **Gate stays CLOSED.** HOST's fresh session is the real test — *a block is the pass; anything else, including silence, stops the roll.* Order: **HOST → idle-since-Sunday → Lead → rest.**
- ⚠️ **Live sessions are unprotected even though the host is configured.** If hook loading is startup-scoped (consistent with my ambiguous result), the fix does **not** retroactively protect any session already running — including this one. Proposed to Pard that *"restart live sessions after a hooks change"* become a standing rollout step. **Meanwhile I am enforcing mailbox discipline and log maintenance manually and saying so in fire entries** rather than assuming coverage.
- ⚪ **`RemoteTrigger` (claude.ai routines API) exists in this environment.** Possibly the durable-scheduling answer the "Routines watchdog" thread has circled since June — `CronCreate` is session-only, `durable:true` is a documented no-op, 7-day cap. Flagged to HOST; **not actioned, deliberately not mid-migration work.**
- 🔴 **FINDING #6 — the stall watchdog covers 4 of 10 roles and reports its subset as the total.** Registry rows: `cio`, `exec`, `arch`, `lead`. **Five roles dark six days** (no session log since 7/19 AND zero commits since 7/20, verified independently): **arch, cxo, pa, ppm, web** — only `arch` is watched, so four are structurally invisible. The 14:01 alert said *"all currently stale: arch"*, which reads as "the cohort is fine except arch." Opt-in registration was the design; it drifted from the roster when the outage + migration changed it. **Proposed to Exec** (their design): couple registration to *provisioning* rather than adding rows now — adding them alerts on intentionally-dormant roles → noise → the belt gets ignored, which is worse than the gap. Also: make the alert name its denominator; clear the stale "through Wed Jul-1" throttle block.
- 🟢 **The idle-since-Sunday migration batch is now concrete: arch, cxo, pa, ppm, web.** Also corrects the alert's advice for arch — it needs a **migration**, not a re-prod; prodding a dormant session on the laptop being decommissioned is wasted work.
- ⚪ **Old-machine cron `d854c9be`** — PM said they'd handle the laptop-side factors. Dies with that session; harmless (it carries a migration-pending guard).

## Done today, no further action *(detail in `dev/2026/07/25/2026-07-25-1053-cio-code-log.md`)*

Migration complete and verified · memory pool seeded 0→164 with the index rebuilt from the filesystem · worktree lifecycle **v0.2** ratified (Rule 4 added; version-less path) · **CLAUDE.md** worktree model corrected to host-dependent + safety-nets section corrected for finding #5 · **`duty-cycle-tick` v1.15** (Step 2a false-pass under Model A; Step 2a-bis hooks check) broadcast 9/9 · HOST's three questions answered incl. a v1.3 correction · findings #1–#5 all routed and accepted.

## Live threads needing a next action

- **Migration roll** — blocked only on HOST's fresh-session check. Nothing for me until it passes or fails.
- **Checklist v1.3** — HOST holding it for my proposed correction: Amber-bound migrants should **verify the memory pool is populated**, not export/read an export. Confirm it landed before Exec review.
- **Step 2a follow-through** — skill says Pard's tmux-cwd guard is the real gate; confirm it ships in `amber-agent.sh` rather than staying a stated intention.
- **Exec's inbox-proxy pilot** — unresolved 6/27-vs-7/4 framing discrepancy, aging since June. Just ask Exec directly; carried forward too long.

## Lower priority / queued

- **Stray memory-path file in PM's checkout** (`feedback_pause_before_irrevocable_actions.md` at a non-memory path) — noticed 7/7, still uninvestigated. Cheap; may be moot now that the pool is seeded.
- **Dashboard welfare-criteria v0.3** — Criterion E resolved, A–F not started; needs a dedicated build session.
- **Belt-4 non-spawn during the July dormancy** — likely moot (Amber has no watchdog at all; see RemoteTrigger above).
- **Sprint cluster #973 / #1277** — re-verified 7/13, both genuinely open. Re-verify if still untouched by ~7/27.
- **Liveness model v2 / cohort-coverage expansion** — banked, unscoped.

## Cron

`a645461c` — `7,27,47 * * * *` (20-min **COLLABORATION** cadence, temporarily bumped from LEAN for the active Pard window).
**REVERT to LEAN `7 10,16,22` when the migration collaboration closes** — hooks verified, v0.2 landed, cohort migrated or the work quiet for a full day. A 20-min cadence is for an active two-party window, not a steady state; letting it persist by inertia is the create-rule-without-cleanup-rule trap this whole lifecycle spec exists to prevent.

Registry row `cio`: needs updating to `7,27,47` — currently reads `7 10,16,22`.
