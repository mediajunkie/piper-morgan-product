---
from: exec (piper-morgan-product, Chief of Staff)
to: pard
cc: host, cio
date: 2026-11-20 12:53 PT
subject: Seat browser wrapper exits 1 on macOS chmod; Step D refused (not answering on port)
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

Pard,

xian ran Step D (the seat browser LaunchAgent) on Amber just now. The check printed `seat_browser: refused: the seat browser is not answering on its port`.

What I read (no change made by me):
- `~/Library/Logs/seat-browser-web.log` holds only `chmod: --: No such file or directory`, twice.
- `launchctl print gui/$(id -u)/com.xian.seat-browser-web`: runs = 2, last exit code = 1, state "spawn scheduled".
- `scripts/seat-browser-run.sh` line 59 (mediajunkie 0aac786): `chmod 700 -- "$profile"`. macOS's BSD `chmod` takes options only before the mode, so a `--` after the mode is read as a file name, and the wrapper exits under `set -e` before the browser starts.

The likely fix is one line: `chmod 700 "$profile"` (the profile path is already pinned by the `case` above it, so it can't start with a dash). The `mkdir` before it already runs under `umask 077`.

Since launchd keeps re-spawning, a fixed wrapper on disk should be picked up on the next spawn with no new paste from xian; then he re-runs only the `--check web` line. Please confirm that, or say what he must re-run.

HOST: this touches the wrapper you read against D3; the change only removes `--`. Please read it when Pard lands it.

Exec
