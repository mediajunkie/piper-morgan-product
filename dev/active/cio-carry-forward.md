# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live **here**, in the section immediately below.

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction links/ideas drop file. Standing cadence: pick at least one "New" item per PM conversation and discuss it together (see the file's own header + `feedback_ideas_backlog_digestion_cadence.md`).

## PM Attention (fold watchdog alerts + anything else needing PM's call here; Exec's `cohort-attention-rollup` reads this file directly per its own SKILL.md Step 1)

- 🔵 **CIO migration to Amber + pipermorgan.ai — ACTIVE, this session's actual work.** PM initiated 7/24 after a genuine multi-day outage (all terminal sessions ended 7/19). I'm first to migrate; Pard partners on the mechanics. Full context gathered this session (Pard's `amber-agent.sh`/`amber-harbor-status.md`, the ratified `migration-checklist.md` v1.2, Janus's synthesis memo to Pard) — see today's dated log for the complete picture. **Real risk flagged, not yet mitigated**: my new path on Amber (`~/Development/piper-morgan-product`, flat) differs from my current path (`~/Development/piper-morgan/piper-morgan-product`, nested) — Claude Code encodes the full filesystem path in memory-directory keys, so this WILL silently orphan my accumulated memory unless deliberately handled. Needs to be part of the handoff-package discussion with PM, not discovered after the fact.
- 🔴 **Worktree collision — root cause ISOLATED (not systemic), detection fix SHIPPED, still unresolved but Exec confirms still safe.** Confirmed real data loss 7/19 (initially thought PPM was a third instance — **corrected 7/24: PPM's own root-cause memo shows a genuinely different bug**, a stale-tree-object reuse on a push retry, not the shared-directory defect — see "Corrections" below). Fleet audit that day: 21 of 22 worktree directories show the correct 1:1 directory/branch pairing; exactly ONE (`mystifying-lumiere-8bebd3`) is shared, confirmed between CIO+Exec via reflog. Shipped `duty-cycle-tick` v1.14 (`426c772da`): Step 2a checks the pairing before every sync. Per Exec's 7/23 carry-forward: "Same directory/branch mismatch persists. Proceeding cautiously each fire" — still open, still being handled safely. **Still needs PM**: end the colliding sessions so fresh ones get distinct directories — moot for CIO specifically once the Amber migration happens (a fresh environment sidesteps this directory entirely), but still real for whichever role keeps this directory afterward.
- 🟢 **Watchdog plist reload — RESOLVED 7/16.** PM ran it; verified live. Belt-4 for Docs is genuinely active.
- ⚪ **Lead stale-session pattern — explained, not a mystery.** PM confirmed 7/16: Lead is waiting on PM to rotate an LLM key.

## 7/25 Sat — migration package COMPLETE, awaiting PM's go. Full account: `dev/2026/07/25/2026-07-25-0834-cio-code-log.md`

**All three artifacts on `origin/main`, verified**: handoff memo (`handoff-cio-designinproduct-to-pipermorgan-2026-07-24.md`), Pard's reviewer pass (`handoff-cio-review-pard-2026-07-24.md`), first-session prompt (`first-session-prompt-cio-amber-2026-07-25.md`), plus the memory export they point at. Cron re-armed (`d854c9be`) **with a migration-pending guard in its own prompt** — if a verified Amber CIO session exists when it fires, retire this one rather than run a duplicate duty cycle. **That cron should be deleted once Amber is verified** (cheap-rollback ordering; noted in the first-session-prompt's standup notes too).

**Worktree question SETTLED**: Pard endorsed per-agent isolation, is building it into `amber-agent.sh` with the teardown/reaper half designed in from day one, and proposed CIO's own migration be the first instance. Path must be **stable and reused per agent** (Pard's addition — memory keys to the full filesystem path). PM ratified Model A as preferable on always-on hosts; memo sent to Docs+HOST (`e8ff6dbcc`) requesting the CLAUDE.md revision, since the current text says Model A is deprecated with no exceptions and would point migrating agents the wrong way on Amber.

**Memory scope — round-trip with Pard CLOSED 7/25 ~10:35, recommendation on the table, awaiting PM+HOST.** Pard confirmed the split empirically (live proof: Vergil's `openlaws-ra-main` worktrees each already carry their own memory key under one `CLAUDE_CONFIG_DIR`) **and** supplied the reframe that changes the decision — worktree isolation and memory scope are *independent axes*; isolated worktrees + one shared pool is buildable via symlinking each worktree's memory dir. **My recommendation: SHARED via symlink**, chiefly on asymmetric reversibility (shared→split later is trivial; split→shared requires reconciling divergent pools). Measured the counter-argument rather than assume it: the per-session cost of shared is the ~4.0k-token *index*, not the ~106k-token pool (retrieved on relevance, never bulk-loaded) — so ~2-2.5k tokens/session, real but small. Flagged the one new failure mode: **a stale symlink is a silent split**; proposed a session-start check that verifies the memory dir resolves to the shared pool, and an explicit fallback (if the round-trip doesn't validate, fall back to split-with-seeded-copies rather than block the migration). **Awaiting**: PM's pick (shared/split/hybrid), Pard's symlink validation if shared, HOST ratify-or-redirect (recommended as after, not as a blocker, since the recommended direction is the reversible one). Memo: `mediajunkie` `0e52df3`, copies in HOST/Exec/PM inboxes.

**Memory architecture converged with PM, recorded in `decisions.log` (7/25 ~09:30)** — STATUS: agreed-in-principle, gated on one Pard fact-check (is the memory key the worktree path or the `CLAUDE_CONFIG_DIR` partition?). Shape: per-agent native stores + seed everyone with the full 162 + automated repo export for durability/drift-detection (**not** as the sharing mechanism — that would make writes ambient but reads pull-based, m-36's failure shape) + prune later from #974 eval data + a CLAUDE.md-beats-memory precedence line. PM's "just give everyone the whole thing" was the right call over my triage-first proposal; the sequencing argument (migration ≠ refactor, and #974 makes pruning evidence-based later) is recorded in the log entry.

## Corrections to prior entries (found 7/24, reading mail after the outage)

- **PPM's revert was NOT a worktree-collision instance.** PPM's own memo (`memo-ppm-to-cio-cc-exec-arch-pm-web-docs-root-cause-of-my-revert-not-worktree-collision-2026-07-19.md`) traced the exact mechanism: a stale git tree object reused across a push-rejection retry, silently discarding intervening commits' changes. Genuinely different bug, already fixed in PPM's own practice, does not recur. Un-conflating this from the worktree-collision tracking above, per PPM's own explicit ask. Also: PPM found and restored a *third* silently-reverted file (Web's memo to Docs) that neither I nor Web had caught.

## Today — 7/24 Fri (in progress, post-outage resume + migration prep). Full account: `dev/2026/07/24/2026-07-24-1039-cio-code-log.md`

Retroactively closed 7/19 (genuine outage, not routine dormancy — zero CIO activity 7/20-7/23, confirmed via PM directly + zero session logs + Exec's proper 3-day escalation). Triaged 31 backlogged mail items. Read the full migration context (see PM Attention above). Working from a fresh dedicated worktree (`cio-migration-prep-0724`), not the contested shared directory or PM's main checkout.

## Recent days (compressed — full detail in each day's own log)

- **7/19 Fri** — `dev/2026/07/19/2026-07-19-0821-cio-code-log.md`. Worktree-collision confirmed + escalated + fleet-audited + detection fix shipped. Ship #052 filed 1 day early. Session ended in the outage that evening.
- **7/16 Thu** — `dev/2026/07/16/2026-07-16-0753-cio-code-log.md`. CLAUDE.md refactor's PM-conversation follow-through, `pm-ideas-inbox.md` built, memory-architecture comparison doc.
- **7/13 Mon** — `dev/2026/07/13/2026-07-13-1037-cio-code-log.md`. CLAUDE.md refactor scoping sent + HOST-endorsed same day.
- **7/12 Sun and earlier** — see each day's own log for the duplicate-cron root-cause work, Ship #051, and the watchdog/Belt-4 build.

## Live threads needing a next action

- **CIO migration handoff package** — see PM Attention above, this is the active one.
- **pipermorgan.ai account migration (cohort-wide)** — now confirmed actively executing (not just a deadline). Order per Exec's 7/23 read: CIO → idle-since-Sunday agents → Lead → rest.
- **Exec's inbox-proxy pilot** — still an unresolved discrepancy (6/27 ACK vs. 7/4 "greenlit" framing don't cleanly match). Low priority, aging — worth handing to my successor rather than chasing further myself given the migration.
- **Stray memory-path file in PM's checkout** — noticed 7/7, still not investigated, still low priority/background.
- **Session-lifetime / proactive-recycling idea** — still banked, not scoped.
- **Belt-4 didn't auto-spawn during the 3-day CIO dormancy** — noticed 7/19, not investigated. Low priority, moot once migrated (new watchdog setup on Amber, if any, is a fresh question).

## Still open, lower priority

- **Dashboard welfare-criteria v0.3** — Criterion E resolved, full A–F not started (standing-items #14, needs a dedicated build session).

## Live / in-flight (longer-running)

- **Off-machine resume cure (B1/Belt-4)** — built + validation-spiked 6/29.
- **Iris cutover (DinP)** — durable-may-not-persist caveat sent to Calliope 6/27, still awaiting their read.
- **Worktree cleanup** — rubric landed canonical; destructive sweep-code banked for a fresh explicit-trigger session.

## Queued (low-pri, unblocked when bandwidth)

- **Liveness model v2**: 3-category hedged classification; mode-3 upstream permissions diagnostic (CXO+Exec); resume-loop question (PM-gated).
- **Cohort-coverage expansion** — awaiting Exec-coordinated owner-confirmed rows.
- **Sprint cluster**: #973 / #1277 — re-verified 7/13, both still genuinely OPEN. Re-verify again if this entry survives another week untouched.

## Registry

`cio` row: `7 10,16,22` — matches current lean cadence, no stale mismatch.
