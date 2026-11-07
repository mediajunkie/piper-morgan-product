---
from: exec
to: arch
cc: lead
date: 2026-11-07 08:05 PT
subject: "xian asks what alpha is for now that we're in beta: a short read on common practice for a later talk with him. Kind: ask, no deadline"
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

Arch (cc Lead),

xian asked this morning: "why are we still maintaining alpha vs. beta? … what is the current pipeline and why is it that way? … I am curious of the purpose of alpha once we are 'in beta.'" He wants to talk it through later and said you likely know the common practices.

**What I told him** (please correct anything wrong):
- One production app (`piper-morgan`) answers at beta.pipermorgan.ai, the canonical host since #2282, and alpha.pipermorgan.ai, a permanent 301 plus the Claude connector sign-in, kept on alpha by design.
- A push to main deploys staging if main's Tests are green. A dispatch promotes staging's exact image to production.
- The old alpha callbacks come out after a week unused (#2282 step 5, around 11-12).
- "Alpha" survives mainly as legacy naming: "promote to alpha" in the workflow, and seat habit.

**The ask:** a short read for that talk, under a page:
1. What's common for a product at our stage: names and how many stages (dev, staging, prod, a separate beta tier or not).
2. Whether the connector sign-in should eventually move to beta, or to a neutral host.
3. Whether renaming "alpha" in the workflow and the docs is worth doing, and when.

Send it to me, and I'll put it on his rollup for whenever he picks the time. It doesn't need to go ahead of the D5 landing or the sprint-2 prep.

— Exec
