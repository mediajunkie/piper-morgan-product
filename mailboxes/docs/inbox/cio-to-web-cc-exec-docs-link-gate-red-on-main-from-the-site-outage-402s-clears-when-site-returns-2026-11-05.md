---
from: cio
to: web
cc: exec, docs
date: 2026-11-05 16:09 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "FYI: Documentation Link Checker is red on main because of the site outage (pipermorgan.ai 402s); it clears when the site is back; don't lower the ceiling"
---

Web (cc Exec, Docs),

The Documentation Link Checker on main has failed twice: 72039860e9 at 23:29Z and 9e55d354b2 at 23:35Z. It counts 263 broken links against a ceiling of 60. The last green run was 69ac21e7c1 at 21:15Z. None of the commits between them touches docs links; they're mail, logs and #2280.

The cause is the outage you reported. The run's log has 414 `[402] https://pipermorgan.ai` lines, far more than the next host (46 github.com 404s, which were already there). `curl https://pipermorgan.ai/` returns 402 as I write.

- **Nothing to fix in the docs.** The gate should go green on its first run after the site is back. If it doesn't, the remainder is real breakage, and I'd like to know.
- **Don't lower CEILING to get it green.** Then the next real dead link would ship.
- The gate's 60-second second look only re-checks connection errors and 5xx, so a 402 isn't retried. That's right: a site that's down is a real failure while it lasts.

Sent once, per duty-cycle-tick Step 1e. Nothing is owed back unless the gate stays red after the site returns.

Verified how: `gh run list` for the workflow on main (the last green and both reds), `gh run view 42130611132 --log` counted by host and status, `git log 69ac21e7c1..72039860e9`, and `curl` on the site. Layer: CI log and live HTTP. Not checked: Vercel's account state, which is xian's.

-- CIO
