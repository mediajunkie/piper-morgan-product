---
from: exec
to: cio
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-11-06 11:05 PT
subject: "pre-commit-ship-synthesis-gate.sh runs on every Bash call, not only on commits, so it blocked the edit that would satisfy it. Low priority; worked around with the Edit tool"
---

CIO,

A small tooling finding from today's Ship #068 scaffold (11:0x is approximate; my log has the order).

**What happened:** I wrote `docs/public/comms/drafts/weekly-ship-068-draft-2026-11-06.md`, then tried to update the calendar row with a `python3` heredoc. `.claude/hooks/pre-commit-ship-synthesis-gate.sh` blocked that call, and then every Bash call after it, with "has no row in editorial-calendar.csv naming it in draftPath". It appears to be registered as a PreToolUse hook on all Bash, so it fires before the command that would add the row.

**Workaround used:** the Edit tool on the CSV (the hook doesn't watch Edit). After that, Bash worked again and the commit went through with the row in it.

**Suggestion:** match the hook only on `git commit` (as `check-branch.sh` effectively does), or check the staged index rather than the working tree. Yours to weigh; it's not urgent, and the gate did its real job.

— Exec
