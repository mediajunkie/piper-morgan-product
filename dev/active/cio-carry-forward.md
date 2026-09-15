---
last_updated: 2026-09-14
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-14 (16:37 fire, complete)

**Cron**: `a03890a3` · `7 10,16,22 * * *` · armed at 2026-09-09 22:45 STOP · expires ~2026-09-16
22:45. **Not yet within the ~48h proactive re-arm window (still ~54h out) — will be by tonight's
STOP or definitely by tomorrow's 10:xx fire. Check and re-arm at the first fire that's within 48h.**
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## Today's shape so far: the Fable-ceiling incident traced to its real root cause

**10:37**: Exec's "seven roles dark" alert self-corrected to "a two" (Fable model-tier ceiling on
arch+web). Pard answered my own 08-29 rate-limit question with real data. Catalogued three real
causes of "silence" (Lead's ask) in `duty-cycle-freeze-check.sh`'s header.

**16:37**: Janus's retrospective + Exec's analysis traced the ceiling to its actual source — Lead's
30 Saturday subagent dispatches, all inheriting Lead's Fable tier by default (a fan-out inherits
the dispatcher's model), exhausting the tier that arch and web then got refused against, though
neither of them dispatched anything. Lead owned it immediately and adopted explicit model-pinning
for all future dispatches. **Checked my own exposure**: one dispatch this week, inherited Sonnet
not Fable, wasn't part of this incident — but adopted the same "pin explicitly, never inherit"
discipline for my own future dispatches regardless. Deliberately did NOT write this into CLAUDE.md
as a cohort default — Exec's memo frames that as still open (decide before Thursday), not ruled.

## Open, needs a look

- **Issue #1798** (standing-item 7z): hook PostToolUse migration + common-dir move. Not urgent.
- **Standing-item 7x**: Exec's 2 remaining process items (archive `mailboxes/*/read/`; change the
  PM-cc rule). Not started.
- **Standing-item 7y**: NO-DAY-CLOSE streak detector. Correctly gated on cohort data.
- **Watch, not mine**: whether "subagent dispatches pin a cheaper tier by default" becomes an
  actual cohort ruling before Thursday — if it does and needs writing into CLAUDE.md's Subagents
  section, that's a natural pickup for me as the one who's been tracking the thread.

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
- **My own heartbeat compliance** — clean today, v1.34/v1.35 self-check working as designed.
- **My own future subagent dispatches** — adopted explicit model-pinning today; watch whether I
  actually follow through on the next real dispatch rather than defaulting back to omission.

## Standing corrections to myself

- **A syntax-checked script is not a tested script.** (recurring.)
- **Before filing a new methodology entry, check the existing corpus for the same test under
  different words.** (09-12/13.)
- **A fix for an invisible-success problem can itself be invisible-success-shaped.** (09-12/13.)
- **Test a fix against the actual live mechanism before calling it shipped.** (09-13.)
- **A compound `git add && git commit` in one Bash call silently bypasses any PreToolUse hook
  that reads `git diff --cached`.** (09-13.)
- **When accepting an interim state after finding a bug, name it as an interim in the artifact
  itself and document what it doesn't fix.** (09-13.)
- **A durable "here's what actually happened" catalog belongs in the artifact a future confused
  reader will actually open, not a memo that scrolls away.** (09-14.)
- **NEW (09-14): when a colleague owns a real mistake publicly, check your own exposure to the
  same class of error before just crediting them.** Lead's dispatch-inheritance mistake wasn't
  unique to Lead — it's available to anyone who calls Agent/Task without a model argument. I
  hadn't hit it this week, but I would have eventually without the check.
- **NEW (09-14): don't write a still-open cross-role decision into a durable doc as if it were
  settled, even when you personally agree with the likely outcome.** Exec explicitly framed the
  dispatch-tier-pinning question as pending a decision before Thursday — CLAUDE.md waits for that,
  not my own read of where it's heading.
