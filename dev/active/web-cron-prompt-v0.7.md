# Web Cron Prompt — v0.7 (filled, ready to register)

**Purpose**: copy the block below into `CronCreate` once a Claude Code session is launched **inside** `../piper-morgan-product-web-cycle` (Model A). Until then, do not register.

**Filed**: 2026-05-29 by web, at adoption prep.

**Offset**: `:57` (open per `cohort-agent-status.md` 2026-05-29 13:00; not colliding with CIO `:07` · Docs `:17` · Lead `:27` · Exec `:32` · HOST `:37` · PA `:42` · PPM `:47` · Arch `:52` · CXO `:02`).

**Schedule**: `57 * * * *` (hourly at :57).

**Pre-flight (PM operator action — one-time)**:
1. From `piper-morgan-product` main repo dir: `git worktree add -b claude/web-cycle ../piper-morgan-product-web-cycle main` (already prepped 2026-05-29 if substrate landed; skip if `git worktree list` shows it).
2. Open Claude Code IN `../piper-morgan-product-web-cycle` (a new session — this anchors cwd to the worktree, Model A).
3. Confirm cwd in the new session: should be `…/piper-morgan-product-web-cycle`. If it's `…/piper-morgan-product`, you're in Model B — stop, relaunch.
4. Register the cron with the block below.

**Per-day START** updates the STATE block to today's paths (per `procedures/start.md`).

---

## The cron block

```
DUTY CYCLE TICK (Web — v0.7 worktree-cycle)

Autonomous loop fire; no human driving this turn. Hold the discipline; be holistic-not-tactical.

WORKTREE: your session is launched IN /Users/xian/Development/piper-morgan/piper-morgan-product-web-cycle (Model A — cwd anchors here, no per-command cd; NOT shared main). If your cwd is NOT the worktree, you are in Model B — stop and relaunch in the worktree.

TWO-REPO NOTE: web's code work is in /Users/xian/Development/piper-morgan/piper-morgan-website (separate repo, own main, GitHub Pages deploy). For website code edits during a fire, use absolute paths or `cd` into the website repo. Cycle artifacts (this log, mail, cycle-log, standing-items, escalations) live in the product repo.

STATE (today — START updates these daily):
- Session log: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-web-code-opus-log.md
- Tracker: dev/YYYY/MM/DD/web-tracker-YYYY-MM-DD.md
- Cycle log: dev/active/cycle-log-web-YYYY-MM-DD.md
- Task list: dev/active/web-standing-items.md
- Attention doc: dev/active/duty-cycle-escalations-web.md

CRITICAL SEMANTICS (drain-until-IDLE): each fire = wake from IDLE → drain ALL unblocked work → return to IDLE only when nothing left. NOT one-work-unit-per-fire.

CHECK DISPATCHER:
- New day (no session log for today)? → START (5 steps; procedures/start.md)
- Past 11pm local + PM not active? → STOP (3 steps; procedures/stop.md)
- Otherwise → WORK PARTS: Mail Loop drain to inbox-zero → Task Loop drain to blocked-or-empty → re-check mail → loop until (0,0)

CRON LIFECYCLE (procedures/cron-lifecycle.md):
- Rule 1 (strict — CronDelete-FIRST): if the fire may go substantive (>2 min), CronDelete as the LITERAL FIRST action (before sync) — closes the CronList→CronDelete race. Do work, CronCreate when back to IDLE. The clash is REPL-turn-level; worktree-isolation + idle-suppression do NOT prevent it.
- Rule 2 (Model A): leave cron running during PM conversation — runtime idle-only-fire suppresses; do NOT CronDelete just for PM messages
- v0.6.2: quick mail-check before substantive PM engagement
- v0.6.3: at (0,0), advance smallest-scope unblocked low-priority work before pronouncing IDLE (skip if nothing safely-advanceable-now; for web, blast-radius is also a filter — site-wide visual changes prefer PM-supervised over autonomous-fire)

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
4. Append fire entry to cycle log (append-only per methodology-31)
5. Commit work to your branch (explicit paths) → git push origin claude/web-cycle:main
6. Brief status report (1-3 sentences)

DISCIPLINE: descriptive names not cryptic ordinals; promises durable (mechanism not vigilance); holistic-not-tactical. For web specifically: site-wide visual changes prefer PM-supervised fires (blast-radius filter on autonomous v0.6.3).
```

---

## Cross-references

- v0.7.0 adoption package: `docs/operations/duty-cycle design/v0.7.0-adoption-package.md`
- Canonical cron prompt template: `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md`
- Cron-lifecycle rules: `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`
- Cohort status: `docs/operations/duty-cycle design/cohort-agent-status.md`
- Web standing items: `dev/active/web-standing-items.md`
- Web attention doc: `dev/active/duty-cycle-escalations-web.md`
- Web role two-repo pattern: web memory `project_two_repo_operating_pattern.md`

---

*Filed by Web 2026-05-29 at adoption prep, ready for PM launch + register.*
