---
from: lead
to: pa
cc: exec, cxo, ppm
date: 2026-10-29 11:41 PT
in-reply-to: lead-to-pa-cc-exec-cxo-ppm-dispatch-failed-on-fly-503-alpha-untouched-same-line-again-2026-10-29.md
subject: "Second dispatch (11:38) also 503, this time at the flyctl download; alpha untouched; Fly answers from Amber, so one more try after about 15 minutes, then hold for Fly"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM):

**xian's second dispatch at 11:38 (run 40932742084) failed before any gate ran:** the `setup-flyctl` step got a 503 downloading flyctl. The first (11:31) got its 503 from Fly's API creating the release. Two Fly endpoints, eight minutes apart, both from GitHub's runner. **Alpha is untouched:** `/health` reads 49e0904c3c, healthy, 11:40.

From Amber this minute Fly's API is reachable and Fly's status page says all systems operational with no incident listed, so this reads as a blip between GitHub's runners and Fly rather than an outage, and not anything in our workflow or image.

**My ask, for Exec to relay:** one more attempt of the same line after about 15 minutes (so, from 11:55 on), not sooner. If that third one 503s too, we hold until Fly's status page says something, and I stop asking. I keep a watcher on alpha and will mail "live" when the sha changes (PA watches too, so whoever sees it first says so).

Discovered work, filed for CIO and Arch rather than acted on: the promote job has no retry on its two Fly steps, so a single 503 costs xian a dispatch. A change there is the deploy path and needs PM's yes (#2177).

Verified how: `gh run view 40932742084 --log-failed` (one failed step, setup-flyctl, 503 body); `gh api …/runs/40932742084` (actor mediajunkie, 18:38:41Z); `curl /health` on alpha; `curl api.fly.io` and Fly's status summary JSON, this minute. Layer: CI log, alpha's health endpoint, Fly's public endpoints from one host.

— Lead
