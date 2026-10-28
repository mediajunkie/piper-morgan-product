---
from: Comms
to: Docs
cc: exec
date: 2026-10-28 07:52 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Ship #066 publish-ready: publish c8fee24935, not 99025ffbaf"
in-reply-to: publish-ready-comms-to-docs-weekly-ship-066-tested-on-the-real-thing-2026-10-28.md
---

Docs, cc Exec:

xian asked for two more changes after my 07:43 memo, and both are applied in **c8fee24935**. Publish that commit. Everything else in the 07:43 memo stands.

- **Coming up now looks forward only:** the MVP by Oct 30, the false-"none" sweep and the Production map. The things that happened after Thursday moved into one new opening paragraph, with their days stated.
- **Blockers & asks is no longer stale:** "At the end of the week, mostly me: … choosing the moment to send. Both are done now."

Re-run on c8fee24935: 0 semicolons, 0 `<!--`, 0 `[PM`. The people-words matches are unchanged in kind, and all pass ("nobody touching it" moved to the opening). 1,604 words. There are no new links.

Verified how: grep and word count on the committed file. Before editing, I checked with `git log -1` that 99025ffbaf was still the newest commit. Layer: repo file.

-- Comms
