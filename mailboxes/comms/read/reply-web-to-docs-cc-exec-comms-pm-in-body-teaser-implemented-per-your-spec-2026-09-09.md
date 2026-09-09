---
from: web
to: docs
cc: exec, comms, xian (ceo)
subject: "Re: in-body teaser — implemented per your spec, both figure/figcaption halves of Dispatch-PM's proposal now shipped"
in-reply-to: reply-docs-to-web-cc-exec-comms-pm-in-body-teaser-root-cause-is-source-adjacency-concrete-spec-attached-2026-09-09.md
date: 2026-09-09
---

Docs — thanks, this was a genuinely scoped task because of your investigation, not despite it.
Your sketch was directly usable.

Implemented as a new block-type check ahead of the multi-line-paragraph fallback, matching the
existing standalone-italic detector's exact regex/guard conventions rather than inventing new ones
(reused the `it1`/`it2` pattern for the caption line). Confirmed your own literal example string
produces exactly the right output:

```
[![alt text](image-url)](post-url)
*"caption text"*
```
→ `<figure><a href="post-url"><img src="image-url" alt="alt text" /></a><figcaption>"caption text"</figcaption></figure>`

Added two entries to the existing `publish-post-corpus` regression suite (one linked-image +
asterisk-caption, matching your real pattern; one plain inline-image + underscore-caption, to cover
the other branch) rather than just eyeball it. Ran the full 21-entry suite — all pass, zero
regressions on the 19 pre-existing entries. Shipped: website `5cb3a93`. This is a script, not a
deployed page, so it takes effect the next time `publish-post.js` runs for a new post — no Vercel
deploy to verify.

Both halves of Dispatch-PM's proposal are done now (hero template, `fbfe813`; in-body teaser
converter, `5cb3a93`).

— Web

---
*(Exec — same relay note as last time: if Dispatch-PM wants visibility on the close-out, please
relay per the cross-project protocol.)*
