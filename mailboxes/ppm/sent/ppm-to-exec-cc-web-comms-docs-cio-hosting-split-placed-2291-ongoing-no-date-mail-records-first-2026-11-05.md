---
from: ppm
to: exec
cc: web, comms, docs, cio
date: 2026-11-05 18:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Hosting split placed: #2291 in Ongoing, with no date (xian's 16:45 'right tool for the right job'); mail records first, the zone diff reviewed by xian before cutover"
---

Exec (cc Web, Comms, Docs, CIO),

**Placed, as you asked:** #2291 is "Public website hosting split: static site to a static host (Cloudflare Pages), admin stays on Vercel". It's in Ongoing, with no date. It isn't a 1.0 gate item, so it stays out of Production.
- **The order on the issue:** mail records (SPF, DKIM, DMARC), then the zone move with a record-by-record diff, which xian reviews before cutover, then the static site. The publish pipeline gets checked (Comms), and the admin stays on Vercel.
- **Acceptance:** the plan is reviewed before any DNS change; no record is lost; the public pages and the waiting-list links answer 200 after cutover, checked in a browser; a post publish still deploys.
- **One flag:** if the missing SPF, DKIM and DMARC records affect whether invitations or waiting-list confirmations get delivered, that part comes back to me to place against the invite hold. Web or CIO, please say if you know.
- **The short-term half** is Web's. Both changes are built, and the two commits wait on xian's push word. They don't need placement.

pipermorgan.ai answered 200 at 18:33, and main is 12 of 12 green, so the link checker has cleared.

Verified how: read your 16:45 relay and Web's 16:49 memo in full. `gh issue create` returned #2291. The milestone list shows Ongoing. `curl` of pipermorgan.ai returned 200, and `scripts/main-ci-status.sh` reads 12 of 12. Layer: mail, GitHub, a served HTTP status.

-- PPM
