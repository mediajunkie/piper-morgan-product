---
last_updated: 2026-09-14
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-14 (10:37 fire, complete)

**Cron**: `a03890a3` · `7 10,16,22 * * *` · armed at 2026-09-09 22:45 STOP · expires ~2026-09-16
22:45. **Approaching the ~48h proactive re-arm window — re-arm at tonight's STOP or tomorrow's
START if still outside it then.**
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## Today's shape so far: a morning of real cross-role instrumentation findings, cleanly resolved

**Exec's "seven roles dark" escalation self-corrected to "a two"** (Fable model-tier ceiling on
arch+web, four others self-recovered) — Exec's own root cause: cadence-blind + pattern-blind
hand-rolled comparison overriding a correctly-calibrated instrument. My own seat was never
actually affected (just swept into a comparison that didn't apply to my cadence).

**Pard answered my own 08-29 rate-limit question with real data**: model-tier ceilings wedge
persistent sessions that inherit a model; seats that pin `--model` at launch are immune. Engaged
substantively, correctly scoped the fix as provisioning-level, not `duty-cycle-tick`'s to build.

**Catalogued three real causes of "silence"** (Lead's ask) directly in `duty-cycle-freeze-check.sh`'s
header — signed-out session, classifier outage, model-tier-ceiling-with-session-restart — each with
its actual remedy. Comment-only, full suite 32/32.

## Open, needs a look

- **Issue #1798** (standing-item 7z): hook PostToolUse migration + common-dir move. Not urgent.
- **Standing-item 7x**: Exec's 2 remaining process items (archive `mailboxes/*/read/`; change the
  PM-cc rule). Not started.
- **Standing-item 7y**: NO-DAY-CLOSE streak detector. Correctly gated on cohort data.
- **NEW watch, not mine**: if PM wants `duty-cycle-tick` roles protected against model-tier
  ceilings the way Klatch/Terminus already are, that's a launch-configuration decision across
  ~10 seats — Pard's/PM's call, flagged but not actioned.

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
- **NEW (09-14): a durable "here's what actually happened" catalog belongs in the artifact a
  future confused reader will actually open, not a memo that scrolls away.** Lead's ask was small
  but the placement mattered more than the content — the freeze-check's own header, not a new doc.
