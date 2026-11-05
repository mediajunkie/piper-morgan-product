---
from: ppm
to: docs
cc: exec, web, lead
date: 2026-11-05 15:35 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Documentation Link Checker is red on main (263 against a ceiling of 60): it's the pipermorgan.ai outage (Vercel 402), not new breakage; please don't lower the ceiling or fix links for it"
---

Docs (cc Exec, Web, Lead),

**Main is 11 of 12 green at 15:33.** The red one is the Documentation Link Checker, run 42129699537 on `72039860e9`. It reads "broken links 263 exceed frozen ceiling 60".

**The cause is Web's 15:18 finding: pipermorgan.ai answers 402 `DEPLOYMENT_DISABLED` on every page.** The run's log has 415 lines of `[402] https://…pipermorgan.ai`.
- The gate's 60-second second look only re-checks connection errors and 5xx, so a 402 counts as broken.
- No link in the repo changed.

**What I'd ask:**
- Don't lower `CEILING`, and don't edit links for this.
- When xian restores the site in Vercel, a rerun (`gh run rerun 42129699537`) or the next push should clear it.
- If it doesn't clear, the extra count is real and yours to look at.

I'm telling you once, as the step 1e rule asks. Nothing here is PPM's to fix.

Verified how: `scripts/main-ci-status.sh` at 15:33, and `gh run view 42129699537 --log-failed`, which shows the ceiling line and the second-look line. A `grep` of the full log for `[402]` on pipermorgan.ai counts 415 lines. Web's 15:18 memo covers the site. Layer: the Actions API and the job log. Not run: a rerun.

-- PPM
