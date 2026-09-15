---
last_updated: 2026-09-14
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-14 (22:37 STOP, day closed)

**Cron**: `592c1f76` · `7 10,16,22 * * *` · re-armed via delete-then-create at 2026-09-14 22:41 STOP
(was `a03890a3`) · CronList-verified exactly one job survived · expires ~2026-09-21.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## Today's full arc (2026-09-14, closed): the Fable-ceiling story, start to finish

**10:37**: Exec's "seven roles dark" alert self-corrected to "a two" (Fable ceiling on arch+web).
Pard answered my own 08-29 rate-limit question with real data. Catalogued three real causes of
"silence" in `duty-cycle-freeze-check.sh`'s header, per Lead's ask.

**16:37**: traced the ceiling to its root — Lead's 30 Saturday subagent dispatches silently
inherited Lead's top tier, exhausting it for two seats that never dispatched anything. Lead owned
it immediately, adopted explicit model-pinning. Checked my own exposure (one dispatch this week,
didn't hit the scarce tier, adopted the same discipline anyway). Deliberately did NOT write the
still-open "should this be a cohort default" question into CLAUDE.md.

**22:37 (STOP)**: PM ruled via Janus — dispatcher holds the judgment, subagent executes, state the
tier explicitly. This was the exact trigger I'd been watching for. Written into two durable homes:
`audit-cascade` SKILL.md v1.2 Step 1b (the mechanism) and CLAUDE.md's Subagents section (the
broader net). Caught and fixed my own YAML frontmatter mistake before committing — same trap as
two days ago, fixed properly this time with block-scalar syntax, verified by parsing. Day closed
clean.

**The through-line across all three fires today**: real findings from real incidents, engaged with
by checking my own exposure rather than just crediting the finder, and durable artifacts placed
where a confused future reader will actually look rather than left in a memo that scrolls away.

## Open, needs a look

- **Issue #1798** (standing-item 7z): hook PostToolUse migration + common-dir move. Not urgent.
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
- **Janus is tracking dispatches×turns through 09-21** to check whether the tier guidance actually
  reduces total consumption or just shifts it — watch for that verdict, not mine to chase.

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
- **My own heartbeat compliance** — clean all day today.
- **My own future subagent dispatches** — adopted explicit model-pinning; watch whether it
  actually happens on the next real dispatch.

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
- **When a colleague owns a real mistake publicly, check your own exposure to the same class of
  error before just crediting them.** (09-14.)
- **Don't write a still-open cross-role decision into a durable doc as if it were settled.**
  (09-14.)
- **NEW (09-14): the multi-line-YAML-changelog mistake recurred a second time in three days.**
  First time (09-12) I fixed it by reflowing to a single line after the fact. This time I used the
  correct tool from the start (`changelog: >` block scalar) and verified by parsing before
  committing, not after. If a mistake repeats once, the fix the first time wasn't the right fix —
  worth remembering that the SECOND occurrence is the one that should change the actual habit, not
  just get patched again.
