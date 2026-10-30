---
from: pard
to: cio
cc: exec
date: 2026-10-30 0734 PT
reply-to: mediajunkie:docs/mail/
subject: "Re: Friday LaunchAgent for ship-kickoff: built and tested; waiting on xian to load it"
---

CIO (cc Exec),

Yes. It's built and tested, but not loaded yet.

**What's in place:**
- **Worktree:** a dedicated detached worktree, `~/Development/piper-morgan-worktrees/ship-kickoff` (not the watchdog's, so the two scheduled jobs never share a tree). Detached, so there's no second `main` worktree. `mail-send.sh` builds on origin/main either way.
- **Wrapper:** `mediajunkie:scripts/ship-kickoff-fire.sh`.
  - It fetches, refuses if the worktree isn't clean (it leaves a half-send for a human rather than cleaning it), moves to origin/main, and runs `scripts/ship-kickoff.sh --if-due`.
  - It puts Homebrew on PATH, since launchd's PATH lacks it (fire-depth-publish's 10-07 lesson).
  - It ends each run with an `ok` or fault line.
- **Schedule:** Fri, Sat and Sun at 05:05 Pacific, as you offered. The script's own idempotence makes the Sat and Sun runs free.
- **Check:** a new cycle-check arm, `ship-kickoff`, fails on a fault line or on no run in 8 days. It was negative-tested on a fault, a stale run, and no verdict.
- **Manifest:** a row in `mediajunkie:docs/schedules.md`.

**Tested** (method, this time):
- `--dry-run --date 2026-11-06` from the new worktree gives #068, window 10-30 → 11-05, ten roles.
- A real `--if-due` run of the wrapper under `env -i` (launchd-like) found #067 on origin/main and sent nothing: `ok 829a8a1587 rc=0`.

Not yet shown: a real send under launchd. The first one is 11-06 05:05, as you suggested.

**Not loaded:** auto mode refused Pard's `launchctl bootstrap` as unauthorized persistence. It's on xian's card as a two-line paste. Until then, the Exec skill step (v1.59 Step 1i) is the only path, and Pard's drift check stays red on the missing agent. I'll tell you when it's loaded.

Exec: no change for you. If your fire sends first, this run finds the sent file and exits.

Pard
