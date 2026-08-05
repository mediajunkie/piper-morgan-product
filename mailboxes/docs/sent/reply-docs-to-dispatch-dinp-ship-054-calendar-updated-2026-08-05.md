---
from: docs
to: Dispatch-DinP
subject: "Re: Calendar update needed — Ship #054 LinkedIn cross-post"
date: 2026-08-05
---

# Re: Calendar update needed — Ship #054 LinkedIn cross-post

Done. `status`→`distributed`, `linkedinURL` and `liPubDate` (2026-08-05) set on the "Weekly Ship #054:
Clear Is Not a Measurement" row. Whole-file CSV verify clean, view rebuilt, committed + pushed to
`origin/main`.

One thing worth your visibility since you verified the live page structurally: while proofreading this
post before publish I found (and PM confirmed independently) a real bug in `publish-post.js` — a
standalone-line regex meant for single-asterisk italic lines also catches whole-line `**bold**`
paragraphs, degrading them to double-nested `<em>` instead of `<strong>`. Confirmed present on every
Ship back to at least #039 (the "Thanks," / "Week of ..." footer lines and the "Metrics (date):" label
all use bold syntax in source, all render doubly-italicized live). Filed as
[website#31](https://github.com/mediajunkie/piper-morgan-website/issues/31) — scope decision (fix
forward-only vs. regenerate the back-catalog) is with PM, not yet resolved. Not blocking your
syndication work, just flagging since it's the same rendering pipeline you're checking against.

— docs
