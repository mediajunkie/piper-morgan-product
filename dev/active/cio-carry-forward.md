---
last_updated: 2026-09-13
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-13 (16:37 fire, complete)

**Cron**: `a03890a3` · `7 10,16,22 * * *` · armed at 2026-09-09 22:45 STOP · expires ~2026-09-16.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## Today's headline: caught my own fix silently broken before it shipped

**Lead confirmed alive** — this morning's stale-role concern resolved to a genuine sign-out +
classifier outage, not a dead cron. Cron survived and was rotated on resume.

**The broad-staging hook decision (WARN, Arch's reasons 1+2) executed — then tested before
trusting it.** The exit-0 implementation produced ZERO visible output to the agent (hook fired
correctly per its own log, but PreToolUse exit 0 doesn't surface stderr here). **Reverted to exit
2 (BLOCK) same-fire** as the safe, confirmed-working state. Found two more real issues along the
way: (1) editing a `.claude/hooks/*.sh` file in a worktree has zero effect until synced via
`scripts/sync-pm-local.sh` — documented in the hook's own header; (2) this hook has the identical
time-of-check/time-of-use bug `check-branch.sh` had before its July fix (a compound `git add &&
git commit` silently bypasses it). Both real fixes (PostToolUse migration, common-dir move) filed
as standing-item 7z, deliberately deferred rather than rushed.

**Also fixed same-fire**: Exec's belt-honesty finding — `duty-cycle-freeze-check.sh`'s STALE line
now states its own limitation (can't distinguish a stop from a stall/wedge/gated-commit-path).

**The lesson worth carrying, stated plainly**: I almost shipped a silently broken safety
mechanism today — the exact failure class this whole week has been about — and the only thing
that caught it was actually running the test instead of trusting that the fix looked right. Worth
remembering next time a fix "looks obviously correct."

## Open, needs a look

- **Standing-item 7z**: hook PostToolUse migration + common-dir move. Not urgent — current BLOCK
  state is safe and matches existing behavior. Needs a careful, non-rushed pass.
- **Standing-item 7x**: Exec's 2 remaining process items (archive `mailboxes/*/read/`; change the
  PM-cc rule). Not started.
- **Standing-item 7y**: NO-DAY-CLOSE streak detector. Correctly gated on cohort data.

## Still watching, not acting

- **7t (scope guard)**: narrowed to one PM decision — bypass the required status check for the
  bot's actor, or remove it.
- **Standing-item 7u (Pard's LaunchAgent proposal)**: sent my "adopt" read Sept 10; watching for
  Exec's read and PM's word.
- **#1744**: will show up in future live scope-drift-check runs as a correct, expected flag.
- **#1746**: filed Sept 11 (mail-send.sh reconcile + split-call rename hazard). Watching for
  Pard's response.

## Open, non-blocking

- **Standing-items 7a/7b/7c** — 7a raised directly to PM in chat 08-31, no reply yet; 7b Docs-
  owned; 7c needs HOST+Docs concurrence, low priority.
- **Chess-board day-close commit wiring** — second half of PM's cadence ruling. Not built.

## Watch

- **#1731** — PPM's reconcile-sequencing hypothesis, unconfirmed, not actively chasing.
- **The 1 still-held worktree** (`agent-af6f27891de682d61`) — inconclusive, correctly held.
- **The RACI/responsibility-notation backlog item** (Themis relay, filed 09-02) — still not started.
- **The `mailboxes/*/MANIFEST.md` sibling-basename false-strand warning** — hit repeatedly this
  week, confirmed harmless every time, not mine to fix.
- **My own heartbeat compliance** — practiced twice this fire, both genuinely verified clean.

## Standing corrections to myself

- **A syntax-checked script is not a tested script.** (recurring — the sharpest instance yet
  today: a hook fix that read as obviously correct and was completely non-functional.)
- **Never split a mailbox rename across two `mail-send.sh` calls.** (09-11, #1746.)
- **Before filing a new methodology entry, check the existing corpus for the same test under
  different words.** (09-12/13.)
- **A fix for an invisible-success problem can itself be invisible-success-shaped.** (09-12,
  confirmed again 09-13 — this is now three instances of me personally shipping this exact
  pattern in three days: my own heartbeat gap, my own grace-window sizing, and now a hook fix
  that looked right and did nothing.)
- **NEW (09-13): test a fix against the actual live mechanism before calling it shipped, not
  just against your own worktree's copy of the file.** A push to origin/main is necessary, not
  sufficient — `.claude/hooks/*.sh` specifically needs a main-checkout sync to actually take
  effect, and I only found this because I tested rather than assumed.
- **NEW (09-13): a compound `git add && git commit` in one Bash call silently bypasses any
  PreToolUse hook that reads `git diff --cached` — the index is empty when the hook fires.**
  Stage in one call, commit standalone in the next, whenever you actually need a PreToolUse gate
  to see what you're about to commit — not just for git's own hooks, for any Claude-Code hook
  reading index state.
