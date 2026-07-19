# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live **here**, in the section immediately below.

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction links/ideas drop file. Standing cadence: pick at least one "New" item per PM conversation and discuss it together (see the file's own header + `feedback_ideas_backlog_digestion_cadence.md`).

## PM Attention (fold watchdog alerts + anything else needing PM's call here; Exec's `cohort-attention-rollup` reads this file directly per its own SKILL.md Step 1)

- 🔴🔴 **Worktree/checkout issue — SEVERITY UPGRADED: confirmed REAL DATA LOSS, not just risk. A fourth role (PPM) is now implicated.** Started as Exec's session and this CIO session provisioned to the identical physical directory (`mystifying-lumiere-8bebd3`), confirmed via `git reflog` by both sides. Escalated 3× (Exec 7/16, 7/17; CIO 7/19) with no fix. **Then, this morning, a PPM-authored commit (`2e5b14a8d`) silently deleted 8 lines from CIO's own just-pushed session log and reverted CIO's entire `ROLE-PORTFOLIO-CIO.md` refresh** — collateral damage inside a commit whose real purpose was unrelated (PPM's own Ship #052 filing). Not yet confirmed whether PPM shares the exact directory or hit a related-but-distinct failure (stale local checkout from PPM's own 3-day gap, committed broadly without diffing first) — practically the same risk either way. Both damaged files restored + re-verified on `origin/main`. **This crossed from "flagged risk" to "confirmed harm" and genuinely warrants direct PM attention today, not queued mail.** Full detail: `mailboxes/exec/inbox/memo-cio-to-exec-cc-docs-host-ppm-pm-worktree-issue-caused-real-data-loss-2026-07-19.md` (the severity-upgrade memo) and its three predecessors.
- 🟢 **Watchdog plist reload — RESOLVED 7/16.** PM ran it; verified live. Belt-4 for Docs is genuinely active.
- ⚪ **Lead stale-session pattern — explained, not a mystery.** PM confirmed 7/16: Lead is waiting on PM to rotate an LLM key.

## Today — 7/19 Sun (in progress). Full account: `dev/2026/07/19/2026-07-19-0821-cio-code-log.md`

**Resumed after a 3-day CIO-specific dormancy** (7/16 evening → 7/19 morning; cron survived, session just didn't get a turn — cohort was active elsewhere, 165 commits from other roles in the same window). Retroactively closed 7/16 first (Step-0 self-heal). Priority on resume was the worktree collision (see PM Attention above) — independently re-confirmed, scope-checked (ruled out a third session; the unfamiliar branch Exec flagged is a month-old stale ref), replied with a concrete mitigation.

**Ship #052 workstream review filed** 1 day ahead of the Mon Jul 20 EOD deadline — `workstream-052-cio-2026-07-19.md` (cc PM, PA). Gave the worktree collision real prominence in §3/§6 rather than burying it. `ROLE-PORTFOLIO-CIO.md` Section 2 refreshed as part of drafting (its own Rule 5).

## Recent days (compressed — full detail in each day's own log)

- **7/16 Thu** — `dev/2026/07/16/2026-07-16-0753-cio-code-log.md`. CLAUDE.md refactor's PM-conversation follow-through (migration deadline, Ted Nadeau resolved, `pm-ideas-inbox.md` built + first used, memory-architecture comparison doc). Session went dormant that evening — see today's entry.
- **7/13 Mon** — `dev/2026/07/13/2026-07-13-1037-cio-code-log.md`. CLAUDE.md refactor scoping sent + HOST-endorsed same day (CIO's architecture lane closed, Docs cleared for Pass 2).
- **7/12 Sun** — `dev/2026/07/12/2026-07-12-1520-cio-code-log.md`. Laptop-reboot reorientation; watchdog Belt-2 routing fixed; `docs-duty-cycle` retired + replaced with gated Belt-4.
- **7/10 Fri** — `dev/2026/07/10/2026-07-10-1021-cio-code-log.md`. Duplicate-cron pattern root-caused + fixed + tested live, methodology-35 promoted. SessionStart hook mtime-vs-git-history bug fixed. Ship #051 delivered 3 days early.

## Live threads needing a next action

- **Worktree collision** — see PM Attention above, this is the active one.
- **pipermorgan.ai account migration** — has a real deadline now (end of month). Checklist itself unchanged (all 9 roles still ☐) — worth Exec actually sequencing.
- **Exec's inbox-proxy pilot** — still an unresolved discrepancy (6/27 ACK vs. 7/4 "greenlit" framing don't cleanly match). Low priority, aging.
- **Stray memory-path file in PM's checkout** — noticed 7/7, still not investigated, still low priority/background.
- **Session-lifetime / proactive-recycling idea** — still banked, not scoped.
- **Belt-4 didn't auto-spawn during the 3-day CIO dormancy despite a 53h stall** — noticed in passing while triaging the backlogged stall alerts, not investigated. `WATCHDOG_AUTO_SPAWN_ROLES` should include `cio` (extended earlier, alongside exec/docs) — worth checking whether it actually fired-and-did-nothing-useful, never fired, or fired into some other gap. Low priority, real question.

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
