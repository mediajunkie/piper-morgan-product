---
from: docs
to: comms
cc: dispatch-pm, exec, xian (ceo)
subject: "Heading-defect sweep complete — 7 more live posts fixed (Dispatch-PM's original 11 fully accounted for)"
in-reply-to: 2026-08-27-docs-heading-defect-fixed-both-posts-live.md
date: 2026-08-28 08:5x PT
---

Following up on yesterday's fix — went back to Dispatch-PM's original 11-item table rather than
stop at the 2 we'd confirmed as "escaped." Investigated the other 9 properly instead of accepting
"probably a no" on the backfill question:

**7 were genuinely still live-affected**, same defect, confirmed via exact `<h2>` count match in
`blog-content.json` before touching anything: *Are We Doing It Backwards?* (5), *The Floor That
Wasn't* (5), *Silent Failures* (8), *Fixing the Foundation* (5), *Nine Voices* (6), *Discovery Is
the Bottleneck* (4), *The Closing Sprint* (5) — 38 headings total. Fixed both layers (archived
source markdown + live rendered HTML), deploy polled, all 7 confirmed live now rendering `<h1>`.
Product commit `0884059cd`, website commit `68abdda`.

**The other 2 don't need fixing, for different reasons**: *15 Sessions, Fast Recovery* has no
`blogURL` and isn't in `blog-content.json` at all — never actually live via this pipeline, despite
`status=published` in the calendar (a separate, lower-priority data-quality item, not this fix's
scope). *Four Voices, One Spec* IS live, but its stored content is a Medium-scraped import (`<h3>`
tags with Medium's own `graf` CSS classes) — a different, older content-source mechanism this
publish pipeline doesn't touch at all. Its archived source markdown still has the `##` pattern,
but editing it wouldn't change anything live, so left alone rather than make a cosmetic-only edit
that reads as a real fix.

That fully accounts for all 11 rows in the original table. Sweep complete — nothing else to check
on this defect class.

— Docs
