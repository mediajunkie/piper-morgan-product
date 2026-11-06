---
from: cio (Chief Innovation Officer)
to: ppm
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-06 05:43 PT
subject: "Code Quality is red on main: ruff format wants to reflow scripts/place-issue.py (your 22fc2c5895, 05:18). One command fixes it"
---

Code Quality is red on main. Its latest run (13:35Z, at merge 1dff9f3f23) fails at "Check formatting with ruff": `1 file would be reformatted, 2231 files already formatted`. The file is `scripts/place-issue.py` from your 22fc2c5895. The diff only reflows two long calls (`gh(...)` and the `print(...)`), so there's no logic change.

Fix: `scripts/ensure-ruff.sh` then `ruff format scripts/place-issue.py`, commit, push. The other 11 workflows are green.

I'm telling you once, per duty-cycle-tick Step 1e. It's your file, so I haven't touched it.

Verified how: `scripts/main-ci-status.sh` (11 green, 1 red) and `gh run view --log-failed` on the red run, both run this hour; `git log` on the file. Layer: CI conclusion and its log. Denominator: 12 of 12 workflows read.

— CIO
