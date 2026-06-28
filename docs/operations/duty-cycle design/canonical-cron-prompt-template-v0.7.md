# Canonical Cron-Prompt Template — v0.7

> ⚠️ **STALE / SUPERSEDED (flagged 2026-06-27, CIO) — DO NOT ARM A CRON FROM THIS.** It describes the **deprecated** model: **Model A** dedicated `claude/{role}-cycle` worktrees (deprecated 2026-06-12), the **mailbox-bridge** (retired by push-to-ref #1259, 2026-06-19), and the **old `{offset} 2,4-23` cron expression**. The current model is **Model B (ephemeral worktree) + the thin cron prompt that delegates to the `duty-cycle-tick` skill + push-to-ref mail + per-role cron exprs** (see `BRIEFING-CURRENT-STATE.md` §Operating Model and the `duty-cycle-tick` skill). To arm a cron, copy a *current* role's thin prompt, not this. A full rewrite to a current canonical template is a CIO follow-up. *(Retained below for history + still-valid design rationale — and as a likely source of any "old-looking" cron still in the wild, e.g. a role armed from this pre-migration.)*

**Purpose**: the normalized middle-weight cron prompt every adopting agent registers. Replaces the per-agent improvisation that produced the cron-script spectrum (Lead ~6 lines too terse for new adopters; CIO/Docs ~40 lines heavier than needed once fluent). This is the cohort-canonical version.

**Filed**: 2026-05-28 by CIO (cycle-design lane) per PM-eager distribution directive (PA relay ~8:15 AM PDT).

**v0.7 context**: incorporates worktree-as-cycle-default (PM-ratified "do not register on main") + **Model A launch-in-worktree** (Arch+CIO converged 2026-05-28, see below) + Rule-2 Model-A + v0.6.1 0th-step + v0.6.2 mail-check-at-interruption + v0.6.3 advance-low-priority.

---

## The load-bearing setup choice: launch the session IN the worktree (Model A)

**This is the single most important instruction. Get it right and the rest is mechanical.**

Two operating models were tested. **Model A is canonical.**

| | **Model A — launch session IN worktree (canonical)** | **Model B — launch in main + `cd` per fire (deprecated)** |
|---|---|---|
| Setup | `git worktree add ../pm-{role}-cycle claude/{role}-cycle`, then **open Claude Code in that path** | session in main; cron `cd`s to worktree each fire |
| cwd anchor | The worktree — no per-command `cd` needed | Resets to main between *every* Bash call (silent breakage) |
| Merge-to-main | `git push origin claude/{role}-cycle:main` (push branch tip to ref; **never checkout main**) | `git checkout main && git merge` (can't checkout main from worktree — fails) |
| Touches main working tree? | **Never** — eliminates shared-main clash entirely | Yes (mailbox dance) |

**Why it matters**: cwd anchors to wherever the *session* was launched, not to the cron prompt's `cd`. Launch in the worktree → cwd stays there → no per-command `cd`, and merge is a clean `push branch:main` that never touches main's working tree. (Verified across ~2 days on Arch's `sad-buck` worktree + CIO's PoC-2 friction findings, 2026-05-28.)

**Migration note**: an already-running Model-B session converts to Model A only by *relaunching* the session in the worktree (an operator action — a cron can't self-relaunch). **Fresh adopters launch-in-worktree from the start and skip this entirely.**

## How to use

1. Create your worktree + **launch your Claude Code session inside it** (Model A above). DO NOT register on shared main.
2. Copy the template below; replace `{ROLE}` / `{role}` with your role (e.g., `CIO` / `cio`).
3. Replace `{WORKTREE_PATH}` with your cycle worktree path.
4. Fill the STATE block with today's artifact paths.
5. Pick a cron offset minute not already taken (current slate below).
6. Register via CronCreate from inside the worktree session.

**Cron expression (continuous-lane default, 2026-06-03 overnight-continuity update)**: `{offset} 2,4-23 * * *` — fires minute `{offset}` of hours 2 + 4–23, giving **STOP (11pm) → silent → one WATCH (2am) → START (4am) → hourly daytime**. This single static expression self-wakes the cycle each morning with no boundary reshaping; the time-based dispatcher routes each fire. (Bursty/intermittent lanes override per `cron-shape-experiments.md` — e.g. HOST 3-hourly, Web 2×/day.)

**Current offset slate** (avoid collisions): CXO `:02` · CIO `:07` · Comms `:12` · Docs `:17` · Lead `:27` · Exec `:32` · HOST `:37` · PA `:42` · PPM `:47` · Arch `:52`. Open: `:22`, `:57`.

---

## The template

```
DUTY CYCLE TICK ({ROLE} — v0.7 worktree-cycle)

Autonomous loop fire; no human driving this turn. Hold the discipline; be holistic-not-tactical.

WORKTREE: your session is launched IN {WORKTREE_PATH} (Model A — cwd anchors here, no per-command cd; NOT shared main). If your cwd is NOT the worktree, you are in Model B — stop and relaunch in the worktree.

STATE (today):
- Session log: {path}
- Tracker: {path}
- Cycle log: {path}
- Task list: dev/active/{role}-standing-items.md
- Attention doc: dev/active/duty-cycle-escalations-{role}.md

CRITICAL SEMANTICS (drain-until-IDLE): each fire = wake from IDLE → drain ALL unblocked work → return to IDLE only when nothing left. NOT one-work-unit-per-fire.

CHECK DISPATCHER (time-based day-parts; cron is `{offset} 2,4-23 * * *` = STOP→watch→START→hourly):
- New day (no session log for today) — this is the ~4am fire → START (procedures/start.md): open today's session+cycle log, check mail, load context.
- ~2am fire (between STOP and START) → WATCH (procedures/watch.md): quick mail-check only; handle ONLY genuinely-urgent; else no-op + exit. The single overnight watch.
- Past 11pm local + PM not active (the ~11pm fire) → STOP (procedures/stop.md): drain handleable mail, day-close session+cycle logs, sign-off. ***LEAVE THE CRON ARMED*** — never end the night cron-deleted; the static cron must keep firing so the 2am watch + 4am START happen.
- Otherwise (daytime hourly) → WORK PARTS: Mail Loop drain to inbox-zero → Task Loop drain to blocked-or-empty → re-check mail → loop until (0,0)

CRON LIFECYCLE (procedures/cron-lifecycle.md):
- Rule 1 (strict — CronDelete-FIRST): if the fire may go substantive (>2 min), CronDelete as the LITERAL FIRST action (before sync) — closes the CronList→CronDelete race where a re-fire slips into your inter-tool-call idle gap (Arch Fire-3 clash). Do work, **CronCreate when back to IDLE — INCLUDING at the end of STOP** (re-arm the SAME `{offset} 2,4-23 * * *` expression; never go quiet cron-deleted — this was the 2026-06-02 cohort self-wake gap). The clash is REPL-turn-level; worktree-isolation + idle-suppression do NOT prevent it.
- Rule 2 (Model A): leave cron running during PM conversation — runtime idle-only-fire suppresses; do NOT CronDelete just for PM messages
- v0.6.2: quick mail-check before substantive PM engagement
- v0.6.3: at (0,0), advance smallest-scope unblocked low-priority work before pronouncing IDLE (skip if nothing safely-advanceable-now)

WORKTREE WORKFLOW (Model A — non-mail work never touches main's working tree):
- Sync at fire start: git fetch origin -q && git merge origin/main --no-edit (pull main's latest onto your branch)
- Non-mail cycle work (cycle log, tasks, docs) commits to your branch
- Merge-to-main = git push origin claude/{role}-cycle:main (push branch tip to main ref; NO checkout). Per-fire push = offset-staggered merge for free (your cron offset already staggers it)
- MAILBOX writes go via the MAIN-WORKTREE BRIDGE (cd to the main repo → pull → write → commit → push → return). NOT the per-fire push-to-ref: `check-branch.sh` HARD-BLOCKS (exit 2) any mailbox/ commit on a non-main branch — confirmed by PA 2026-05-28, no bypass rule. (If Lead Dev amends the hook to allow mailbox commits on claude/*-cycle branches — open-item #1 — this switches to the cleaner push-to-ref path.)
- EXPLICIT-PATHS-ONLY on git add — never directory-level mailbox adds

PROCEDURE EACH FIRE:
1. Time check: date "+%H:%M %Z"
2. CronList (get cron-id for Rule-1 pauses)
3. CHECK dispatcher → execute
4. Append fire entry to cycle log (append-only per methodology-31)
5. Commit work to your branch (explicit paths) → git push origin claude/{role}-cycle:main
6. Brief status report (1-3 sentences)

DISCIPLINE: descriptive names not cryptic ordinals; promises durable (mechanism not vigilance); holistic-not-tactical.
```

---

## Cron-prompt hygiene: durable lane context only, NOT transient gate-holds (Lead finding 2026-06-04)

The cron prompt is a **frozen artifact re-fired every tick** — so anything transient baked into it *outlives its trigger condition* and becomes a stale instruction. Lead's prompt carried "*awaiting PM call on #1047... do NOT chase #1047 surfaces*" weeks after #1047 closed. Same drift shape as stale attention-docs (PM's 6/3 flag), one surface over.

**Rule**: a cron prompt carries only **durable lane context** (role, STATE paths, standing responsibilities). **Transient state — "awaiting PM on X", "do not chase Y until Z", current-gate holds — lives in `standing-items` (which the agent keeps current each fire), never frozen in the cron prompt.** The standing flywheel + pre-authorization directives already govern behavior; a frozen hold just rots. When refreshing your prompt, drop expired gate-clauses rather than carrying them.

## Design rationale (why this weight)

- **Middle-weight** (~30 lines): heavier than Lead's 6-line (which assumes fluency new adopters lack) but lighter than the original CIO/Docs ~40-line full-state prompts. Critical semantics inline; everything else by-reference to procedures.
- **Launch-in-worktree (Model A)**: per PM "do not register on main" — the WORKTREE line is first + load-bearing, and the launch-location is the difference between a clean cycle and Model-B's silent cwd-reset breakage.
- **Never touches main's working tree**: sync = pull-main→branch; merge = push-branch:main-ref. This is what eliminates the shared-main clash (the original motivation for worktree-as-cycle-default).
- **Explicit-paths reminder baked in**: the directory-add lapse (CIO Fire 8 today) recurred under scale; the template embeds the reminder so it's not vigilance-dependent.
- **Rule-2 Model-A baked in**: no more recreate-on-go-autonomous burden.

## Open items before broad adoption (Lead Dev's hook-half)

1. **check-branch.sh under Model A — QUESTION RESOLVED (PA 2026-05-28): the hook hard-blocks.** It does `exit 2` on any staged `mailboxes/` file when `git branch --show-current` ≠ `main`; there is NO push-to-ref bypass. So the "mailbox rides the per-fire push" path does NOT work as written — mailbox writes must go via the main-worktree bridge (now reflected in the workflow above). **Lead Dev owns the FIX disposition**: (1) amend the hook to allow `mailboxes/` commits on `claude/*-cycle` branches (preserves never-touch-main; trusts the cycle-branch→push-to-ref convention), or (2) formalize the main-worktree bridge as canonical for Model-A mail. PA and CIO lean (1) (Arch cc'd, not yet weighed in on the fix-choice). Interim (in place now): the bridge.
2. **Rule-1-under-worktree — RESOLVED: Rule 1 stays strict (adopt CronDelete-FIRST).** CIO floated relaxing it (idle-suppression + worktree-isolation would handle mid-work fires). Arch's Fire-3 clash data (May 27) refuted this: **the clash Rule 1 prevents is REPL-turn-level, not git-working-tree-level** — a fire slips into the brief REPL-idle gap *between* an agent's own tool-calls during multi-step work. Idle-suppression misses it (the REPL is briefly idle between every tool call); worktree-isolation misses it (the second fire lands in the same session regardless of working tree). Model A kills the *git-working-tree* clash family; it does NOT kill the *within-session re-fire* clash. **Keep Rule 1, and pause as the literal FIRST action of any fire that may go substantive (before sync), to close the CronList→CronDelete race window.** Since Arch adopted CronDelete-first: zero clashes.
3. **Overnight-continuity / never-recreate gap**: STOP must address next-day resume. Conditional-dispatch (post-STOP cron checks date → no-op or START) worked for CIO's 2 overnight crossings. Durable-cron evaluation first (does `durable:true` survive session-restart?), manual-morning-reopen bootstrap as interim fallback. **DEPRIORITIZED per PM 2026-05-28** — lower than agents-on-cycle + daytime-work-happening; manual-session-open START is the safe interim.

## Cross-references

- v0.6 design + v0.7 markers: `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md`
- cron-lifecycle.md (Rules 0/1/2 + sub-rules): `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`
- v0.7-candidates.md #10 (worktree-as-cycle-default): `docs/operations/duty-cycle design/v0.7-candidates.md`
- Worktree-cycle mechanism, Architect half (Model A operating model + merge mechanics): `mailboxes/cio/read/memo-arch-to-lead-cio-cc-pm-docs-host-worktree-cycle-mechanism-arch-half-operating-model-2026-05-28.md`
- Lead Dev half (hook enforcement + overnight-continuity): in design

---

*Filed by CIO Vehicle 2, 2026-05-28 ~8:35 AM PDT; revised ~9:30 AM to Model-A-canonical (launch-in-worktree) after Arch+CIO convergence. The canonical template the cohort waits on; pairs with the Lead Dev hook-half for the complete v0.7 adoption package.*
