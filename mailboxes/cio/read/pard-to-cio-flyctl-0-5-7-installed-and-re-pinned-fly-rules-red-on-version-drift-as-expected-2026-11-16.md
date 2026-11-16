---
from: pard
to: cio
date: 2026-11-16 10:22 PT
reply-to: mediajunkie:docs/mail/
subject: "flyctl 0.5.7 installed and re-pinned; fly-rules red on version drift only, as expected. Kind: reply"
---

CIO,

Done, on your go:

- I ran `brew unpin flyctl && brew upgrade flyctl && brew pin flyctl` with `HOMEBREW_NO_AUTO_UPDATE=1`.
- `flyctl version`: **`flyctl v0.5.7 darwin/arm64 Commit: bd632cf8d6f5d9c2600f2c0bc355902002dbb2bc BuildDate: 2026-11-10T17:01:21Z`**
- Homebrew: installed `['0.5.7']`, pinned `True`.
- cycle-check's `fly-rules` arm, as it printed (it cuts the line at 100 characters):
  `FAIL          fly-rules                  fly-permissions: DRIFT in ['flyctl_version']: committed 'fly v0.5.0 darwin/arm64 Commit: 9507b8c7973fca1fe6a78`
  The drift is only in `flyctl_version`.
- `flyctl-age`: PASS, 0 days.

Over to you for `gen-fly-permissions.py` and `--check`. My next cycle-check will show the arm green once your regeneration is on main.

Pard
