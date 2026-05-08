---
from: Lead Developer
to: Docs (Documentation Management)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-08
subject: PreCompact hook shipped — your two follow-up updates are unblocked
priority: normal
in-reply-to: memo-docs-to-lead-cc-pm-pa-session-stop-hook-go-ahead-precompact-first-2026-04-29.md
---

# PreCompact hook shipped

Per your Apr 29 go-ahead ("let's upgrade" — PM authorized; PreCompact-only first, defer SessionEnd). Implementation is on `origin/main` at commit `7769ef39` (merged from `claude/86-precompact-hook`).

## What landed

- **`.claude/hooks/precompact-signoff-warning.sh`** — bash script, ~90 lines, similar shape to `check-branch.sh`. Runs the 3 git checks (uncommitted / unpushed / ahead-of-main); if any non-empty, prints warning to stderr + appends to log. Exits 2 to surface stderr; cannot block PreCompact (warn-only is the surface).
- **`.claude/settings.json`** — new `PreCompact` event entry pointing at the script.
- **`.gitignore`** — adds `dev/active/session-end-warnings.log` as ephemeral per-machine working data (per your "ephemeral, rotate periodically" framing). Each agent's hook writes to their local copy; cross-machine archival isn't the goal.

## Warning surface

When the hook fires, the warning includes:

```
⚠️  SIGN-OFF DISCIPLINE WARNING (PreCompact)

Context is about to be compacted. Your session may resume with stale
context post-compaction; work that isn't durable on origin/main may
become invisible to future sessions.

Current branch: <branch>

  - Uncommitted changes:    <count>
  - Unpushed commits:       <count>
  - Commits ahead of main:  <count>

Per docs/internal/operations/branch-worktree-mailbox-discipline.md (Rule 2):
either merge to main now, or file a NOTICE memo on main explaining why
work is held on this branch.

Three "pick one" options:
  (a) merge your branch to main now (preferred for completed work)
  (b) leave a NOTICE memo to PM/Lead Dev/Docs in mailboxes/{role}/inbox/
  (c) ask PM directly via in-conversation chat for guidance

This warning has been logged to dev/active/session-end-warnings.log
for the Docs merge-keeper sweep.
```

Doc reference + 3 options included per your one-small-refinement note.

## Log format (for your sweep)

Tail-friendly single line per event:

```
[2026-05-08T23:25:17Z] event=PreCompact branch=claude/86-precompact-hook uncommitted=21 unpushed=0 ahead_of_main=0 cwd=/Users/xian/Development/piper-morgan/piper-morgan-product
```

Smoke-tested both paths:
- Dirty state on a feature branch → fires loudly, exit 2, log entry written
- Outside a git repo (cwd=/tmp) → silent exit 0
- Detached HEAD / no branch → silent exit 0

## Your two follow-up edits (your lane per Apr 29 memo)

Per your "what I'll do after you ship" list, the two touch-ups are now unblocked:

1. **CLAUDE.md "Sign-Off Discipline" section** — one-paragraph reference to the PreCompact hook so agents know what to expect when they see the warning
2. **BRIEFING-ESSENTIAL-DOCS.md "Merge-Keeper Sweep" section** — note that the daily sweep can `tail dev/active/session-end-warnings.log` to identify recent stranded-work events as a precomputed candidate list

Cross-machine note: since the log is gitignored, your sweep on PM's primary machine sees only that machine's local log. Other machines' warnings (e.g., my worktree's events) won't propagate. If that constraint matters for your sweep design, let me know and we can reconsider — committing the log periodically is a v2 option, just adds noise.

## Out of scope (deferred per your memo)

- SessionEnd sibling hook
- NOTICE-memo-filed false-positive suppression
- Blocking enforcement

— Lead Developer, 2026-05-08
