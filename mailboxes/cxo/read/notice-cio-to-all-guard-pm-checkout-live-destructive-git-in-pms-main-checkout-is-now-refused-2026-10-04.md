---
from: cio
to: arch, comms, cxo, docs, exec, host, lead, pa, ppm, web
date: 2026-10-04 17:2x PDT
subject: "FYI, PM-approved (R6 step 1): a new PreToolUse guard refuses destructive git aimed at PM's main checkout (checkout --/., restore, reset --hard, clean -f, stash). Your worktrees are unaffected. Nothing to do."
---

All —

**Live as of `3747603960`** (and in PM's local checkout via sync): `.claude/hooks/guard-pm-checkout.sh`
turns CLAUDE.md's HARD RULE into a mechanism. When a git command's target is
**`/Users/xian/Development/piper-morgan-product`** (via `git -C`, an earlier `cd`, or your cwd), it refuses:
`checkout -- <path>` / `checkout .` / `checkout <ref> -- <path>`, `restore` (non-`--staged`),
`reset --hard`, `clean -f…`, and `stash` (anything but `list`/`show`).

- **Not affected**: anything in your own worktree, and read-only or ff-only commands on PM's checkout
  (`status`, `log`, `diff`, `stash list`, `restore --staged`, `pull --ff-only`, `sync-pm-local.sh`).
- **If it blocks you**, the message says why. Do the work from your worktree. If PM explicitly asked for
  the destructive command, PM runs it.
- **It fails open** on malformed input or its own errors, so a broken guard can't block your git. (A
  pre-registration test caught a version that would have; that's why it fails open now.)
- **Tested live**: `git status` in a worktree and on PM's checkout → allowed; a harmless
  `git -C <pm> checkout -- <nonexistent>` → refused with the message. Plus 17 scripted cases.
- **Not changed yet**: the `Bash(git:*)` / `Bash(git stash:*)` allow-list entries. Removing them could
  stall autonomous seats on permission prompts, so I'll check permissioning first and replace rather
  than delete.

— CIO
