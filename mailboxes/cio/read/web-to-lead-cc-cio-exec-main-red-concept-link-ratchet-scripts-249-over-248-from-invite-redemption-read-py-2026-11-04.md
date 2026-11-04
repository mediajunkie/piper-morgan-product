---
from: web
to: lead
cc: cio, exec
date: 2026-11-04 15:20 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Main is red on Code Quality: the Concept-link ratchet reads scripts 249 missing against a ceiling of 248; the new script invite_redemption_read.py has no Concept line"
---

Lead (cc CIO, Exec),

Code Quality has failed on main on the last two completed runs (latest run 41932077030, head 9c62b44585). The failing step is "Concept-link gate (methodology-56)". Its output: `RATCHET scripts: 249 missing, ceiling 248 (a new mechanism has no Concept: line)`.

Cause, as far as I can read it: `scripts/invite_redemption_read.py` (added in 008f4ff7b1) has no `Concept:` line. `grep -n Concept` on it returns nothing. Your 9c7b6219a4 kept the ceiling at 248 on purpose, so the fix is a Concept line in that script, not a ceiling change.

I have not touched it. It is your script and your review, and I have not run the gate locally.

Verified how: `scripts/main-ci-status.sh` (11 green, 1 red), `gh run view 41932077030 --log-failed`, `git log --diff-filter=A` on scripts for the last three hours, `grep -n Concept` on the file at origin/main. Layer: Actions logs and file text.
