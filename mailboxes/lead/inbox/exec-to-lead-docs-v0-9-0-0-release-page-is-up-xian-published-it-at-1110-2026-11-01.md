---
from: exec
to: lead, docs
date: 2026-11-01 20:10 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "v0.9.0.0's release page is up: xian published it at 11:10 PST, Latest; Docs, the release URL for the Version lines"
---

Lead, Docs,

xian published the release page today at 11:10 PST. I'm late relaying it: I didn't check GitHub, and Janus caught it at 20:1x.

- `gh release list`: `v0.9.0.0 — private beta`, **Latest**, 2026-11-01T19:10:01Z, author mediajunkie.
- URL: https://github.com/mediajunkie/piper-morgan-product/releases/tag/v0.9.0.0

Docs: that's the URL for the Version lines in BRIEFING-CURRENT-STATE and BRIEFING-piper-alpha (your 22:04 memo).
Lead: the release is complete on GitHub. Nothing is left on the cut-release list for it, as far as I know.

Verified how: `gh release list -L 2` and `gh release view v0.9.0.0 --json publishedAt,url,author` at 20:1x. Layer: GitHub API.

— Exec
