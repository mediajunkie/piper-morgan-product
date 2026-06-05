# Web Cron Prompt — v0.7 (2×/day shape; ready to register)

**Purpose**: copy the block below into `CronCreate` once a Claude Code session is launched **inside** `../piper-morgan-product-web-cycle` (Model A). Until then, do not register.

**Filed**: 2026-05-29 by web at adoption prep; updated 2026-06-04 per CIO 6/3 overnight-continuity discipline ([memo](../../mailboxes/web/inbox/memo-cio-to-cohort-cc-pm-overnight-continuity-fix-self-wake-2026-06-03.md)).

**Shape**: registered as a work-shape experiment per CIO 6/3 memo: **2×/day at ~9:57am + 6:57pm PT** (low-frequency mail-awareness; not full hourly).

**Cron expression**: `57 9,18 * * *` (fires at 9:57 + 18:57 daily, local time). The morning fire IS the self-wake — no separate STOP / WATCH / START boundary because there's no overnight no-op window to bridge for a 2×/day shape.

**Offset**: `:57` (open per current slate per CIO 6/3 memo: Comms `:12`, Docs `:17`, Lead `:27`, Exec `:32`, HOST `:37`, PA `:42`, PPM `:47`, Arch `:52`; web claimed `:57`; `:22` still open).

**Pre-flight (PM operator action — one-time)**:
1. From `piper-morgan-product` main repo dir: `git worktree list` should already show `../piper-morgan-product-web-cycle` on branch `claude/web-cycle` (prepped 2026-05-29). If missing: `git worktree add -b claude/web-cycle ../piper-morgan-product-web-cycle main`.
2. Open Claude Code IN `../piper-morgan-product-web-cycle` (a new session — this anchors cwd to the worktree, Model A).
3. Confirm cwd in the new session: should be `…/piper-morgan-product-web-cycle`. If it's `…/piper-morgan-product`, you're in Model B — stop, relaunch.
4. From the new session, sync the branch: `git fetch origin && git merge origin/main --no-edit` (the worktree branch has been at the substrate-prep state since 5/29; main has moved).
5. Register the cron with the block below.

---

## The cron block

```
DUTY CYCLE TICK (Web — v0.7 worktree-cycle, 2×/day work-shape experiment)

Autonomous loop fire; no human driving this turn. Hold the discipline; be holistic-not-tactical.

WORKTREE: your session is launched IN /Users/xian/Development/piper-morgan/piper-morgan-product-web-cycle (Model A — cwd anchors here, no per-command cd; NOT shared main). If your cwd is NOT the worktree, you are in Model B — stop and relaunch in the worktree.

TWO-REPO NOTE: web's code work is in /Users/xian/Development/piper-morgan/piper-morgan-website (separate repo, own main, GitHub Pages deploy). For website code edits during a fire, use absolute paths or `cd` into the website repo. Cycle artifacts (this log, mail, cycle-log, standing-items, escalations) live in the product repo.

STATE (today — first-fire-of-day creates these):
- Session log: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-web-code-opus-log.md
- Tracker: dev/YYYY/MM/DD/web-tracker-YYYY-MM-DD.md
- Cycle log: dev/active/cycle-log-web-YYYY-MM-DD.md
- Task list: dev/active/web-standing-items.md
- Attention doc: dev/active/duty-cycle-escalations-web.md

CRITICAL SEMANTICS (lighter than continuous-lane drain-until-IDLE): each fire = wake → drain mail (triage to read/) → optionally advance ONE smallest-scope unblocked low-priority item (Mechanism-Beats-Vigilance for things like a Docs-flagged bug fix) → IDLE. Not full Task Loop; not drain-everything. The shape is mail-awareness + sporadic-advance, NOT continuous drain.

CHECK DISPATCHER (2×/day shape — both fires daytime; no STOP/WATCH/START):
- Cron fires twice daily: 9:57am PT (first-of-day; opens session+cycle log) + 6:57pm PT (second-of-day; close-out).
- New day (no session log for today)? → START (procedures/start.md): open session log + cycle log + tracker. The 9:57am fire IS the morning self-wake.
- Otherwise → MAIL LOOP only (drain inbox to zero; triage-to-read with disposition; surface PM-attention items to escalations doc). Then v0.6.3 advance if a smallest-scope mechanical item is obvious; else IDLE.
- No STOP fire (neither fire is past 11pm). No WATCH (no overnight gap). The cron stays armed via CronCreate-at-end-of-fire — never go quiet cron-deleted (preserves the 6/3 STOP-leaves-armed principle in 2×/day form).
- Substantive web-side work (code changes, design walkthroughs, Tailwind/visual fixes) stays in focused manual PM-handoff sessions — that's where web ships.

CRON LIFECYCLE (procedures/cron-lifecycle.md):
- Rule 1 (strict — CronDelete-FIRST): if the fire may go substantive (>2 min), CronDelete as the LITERAL FIRST action (before sync) — closes the CronList→CronDelete race. Do work, CronCreate at IDLE — INCLUDING when returning to IDLE after a substantive sporadic-advance. Never go quiet cron-deleted; the static `57 9,18 * * *` expression must keep firing.
- Rule 2 (Model A): leave cron running during PM conversation — runtime idle-only-fire suppresses; do NOT CronDelete just for PM messages
- v0.6.2: quick mail-check before substantive PM engagement
- v0.6.3: at end of mail loop, advance one smallest-scope unblocked low-priority item if obvious (Mechanism-Beats-Vigilance for Docs-flagged code fixes). For web specifically: blast-radius is a filter — site-wide visual changes prefer PM-supervised over autonomous.

WORKTREE WORKFLOW (Model A — non-mail product-repo work never touches main's working tree):
- Sync at fire start: git fetch origin -q && git merge origin/main --no-edit (pull main's latest onto your branch)
- Non-mail cycle work (cycle log, tasks, docs) commits to your branch
- Merge-to-main = git push origin claude/web-cycle:main (push branch tip to main ref; NO checkout)
- MAILBOX writes go via the MAIN-WORKTREE BRIDGE (cd to /Users/xian/Development/piper-morgan/piper-morgan-product → pull → write → commit → push → return). NOT the per-fire push-to-ref: check-branch.sh HARD-BLOCKS (exit 2) any mailbox/ commit on a non-main branch.
- WEBSITE-REPO WORK is independent: cd to the website repo, commit on its main, push origin main (triggers Pages deploy). No worktree dance on the website side.
- EXPLICIT-PATHS-ONLY on git add — never directory-level mailbox adds

PROCEDURE EACH FIRE:
1. Time check: date "+%H:%M %Z"
2. CronList (get cron-id for Rule-1 pauses)
3. CHECK dispatcher → execute
4. Append fire entry to cycle log (append-only per methodology-31). For 2×/day shape, EVERY fire commits a one-line entry (overnight-watch-style audit-visibility rule from CIO 6/3; for a 2×/day shape, every fire IS a relatively rare self-wake event worth logging).
5. Commit work to your branch (explicit paths) → git push origin claude/web-cycle:main
6. Brief status report (1-3 sentences)

DISCIPLINE: descriptive names not cryptic ordinals; promises durable (mechanism not vigilance); holistic-not-tactical. For web specifically: site-wide visual changes prefer PM-supervised fires (blast-radius filter on autonomous v0.6.3).
```

---

## What's different from the continuous-lane canonical (CIO 6/3)

| | Continuous lane (`{offset} 2,4-23 * * *`) | Web 2×/day (`57 9,18 * * *`) |
|---|---|---|
| Fires/day | ~20 | 2 |
| Day-parts | STOP / WATCH / START / WORK | START (9:57am) / WORK (6:57pm) |
| Self-wake | 4am START via cron expression | 9:57am START fire |
| Overnight watch | One ~2am WATCH | None (no overnight gap to bridge) |
| STOP-leaves-armed | After 11pm STOP, re-CronCreate same expression | No STOP fire; cron stays armed via per-fire CronCreate-at-IDLE |
| Audit visibility | Every fire commits one-line entry (WATCH/START rule); daytime may batch quiet-holds | EVERY fire commits one-line entry (2×/day is sparse enough that every fire is significant) |

The shape preserves the 6/3 "never go quiet cron-deleted" principle in a 2×/day form: there's no nightly STOP that could leave it deleted, and per-fire CronCreate-at-IDLE keeps the expression registered.

---

## Cross-references

- v0.7.0 adoption package: `docs/operations/duty-cycle design/v0.7.0-adoption-package.md`
- Canonical cron prompt template (continuous-lane): `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md`
- CIO 6/3 overnight-continuity memo: `mailboxes/web/inbox/memo-cio-to-cohort-cc-pm-overnight-continuity-fix-self-wake-2026-06-03.md`
- New procedures: `docs/operations/duty-cycle design/procedures/watch.md` (overnight WATCH; informational for web — we don't use it) · `procedures/stop.md` Step 4 (STOP-leaves-armed; informational — web has no STOP fire)
- Cron-lifecycle rules: `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`
- Web standing items: `dev/active/web-standing-items.md`
- Web attention doc: `dev/active/duty-cycle-escalations-web.md`

---

*Filed by Web 2026-05-29 at adoption prep; updated 2026-06-04 per CIO 6/3 overnight-continuity discipline. Ready for PM launch + register.*
