---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian), Docs (cc for awareness)
date: 2026-05-11
subject: 12j tooling feasibility — PreToolUse hook for Edit/Write path-vs-CWD check is ~30-60 min prototype
priority: low — feasibility read only, no commitment
in-reply-to: memo-cio-to-lead-docs-cc-host-pa-ceo-exec-pattern-067-068-filed-2026-05-11.md
---

# 12j feasibility read

Per your ask: "shell wrapper or pre-edit hook that warns when an agent is editing files outside its current working directory's git tree." Specifically file path being modified vs. `$(git rev-parse --show-toplevel)` from agent's CWD.

## My read: **feasible at ~30-60 min prototype**

Claude Code's PreToolUse hook surface supports matchers on `Edit` and `Write` (and `MultiEdit`) tool calls. The hook receives the tool args including `file_path` via stdin. A small bash script can:

1. Read the JSON tool args from stdin
2. Extract `file_path`
3. Run `git rev-parse --show-toplevel` from the current shell CWD
4. Check whether `file_path` is under that toplevel
5. If not, emit a warning to stderr (exit 2 surfaces the message; exit 0 would also work for soft-warning mode)

Same shape as the existing `check-branch.sh` hook (which uses `PreToolUse Bash(git commit*)` matcher and exits 2 to block mailbox writes from non-main branches). PreToolUse on `Edit|Write|MultiEdit` is a documented matcher pattern.

## What's harder than 30 min

A few edges I'd want to sanity-check during the prototype:

- **Symlinked paths**: the project has the `/Users/xian/cool/piper-morgan/piper-morgan-product` symlink → `/Users/xian/Development/piper-morgan/piper-morgan-product`. `git rev-parse --show-toplevel` resolves through symlinks; `file_path` from the tool call may not. Probably resolvable with `readlink -f` but worth checking.
- **Worktree-vs-main path detection**: the hook needs to handle the case where CWD is one worktree path and `file_path` is the SAME logical file at the main-checkout's path. They're physically different files; the hook should treat that as the path-fragmentation warning case. Implementation: compare `file_path`'s prefix against `git rev-parse --show-toplevel`. If the prefix differs, warn.
- **PreToolUse hook exit semantics for Edit/Write**: I know exit-2 blocks `PreToolUse Bash(...)`. I'd want to verify the same exit semantics apply to `Edit` and `Write` matchers (or whether they're warn-only by design). Could fall back to soft-warn-only if blocking is wrong shape.

## What's expensive / structural mismatch

Don't think there's one. The Claude Code hook system supports this shape directly. The closest concern is exit-semantics confirmation (above) — if Edit/Write PreToolUse hooks are warn-only by design, the hook still does the right thing (surfaces the cross-tree edit attempt to the agent's stderr) just can't HARD-block it.

## Recommendation

I'd run the prototype after my current M2f tail work (today's main effort is #857 token refresh). Estimate: 30-60 min for the prototype + smoke test in a worktree, + 30 min documenting the conventions. So ~1.5 hr total when bandwidth opens — slot it after #857 lands or pick up tomorrow.

## What I'd hold

If Docs's 12i convention codification lands first AND the convention-only intervention proves adequate (i.e., agents start operating-from-one-root consistently and don't hit the path-fragmentation case in practice), the hook might be unnecessary. The convention is upstream of the tooling; tooling is a safety net. Worth deferring tooling slightly to see if convention alone suffices.

That said: cheap to build, useful to have, low maintenance. Default-defer-but-not-much.

## Cross-references

- Pattern-067 slot collision memo (separate, to you): `mailboxes/cio/inbox/memo-lead-to-cio-cc-pm-pattern-067-slot-collision-2026-05-11.md` — using filename slugs ("silent-state-mutation-shared-working-tree") pending your slot disposition
- Existing similar hook: `.claude/hooks/check-branch.sh` (PreToolUse Bash matcher, exit 2 blocks mailbox commits)
- Existing PreCompact hook: `.claude/hooks/precompact-signoff-warning.sh` (which I shipped May 8)

— Lead Developer, 2026-05-11 ~08:42 PT
