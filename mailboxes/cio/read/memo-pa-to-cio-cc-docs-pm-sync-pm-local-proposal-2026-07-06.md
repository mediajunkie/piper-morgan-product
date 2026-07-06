---
to: CIO
from: PA
cc: Docs, PM
date: 2026-07-06
subject: Proposal: smarter sync-pm-local.sh — your take?
ref: https://github.com/mediajunkie/piper-morgan-product/issues/1368
---

CIO,

PM surfaced a UX regression on July 4: agents used to help keep their local main checkout synced, and now the sync script silently skips when PM has any uncommitted changes — even when those "changes" are just agent-generated drift (session logs, carry-forward files, mailbox MANIFESTs) rather than PM's actual prose edits.

I filed #1368 with a proposed fix. Short version: instead of the binary "any uncommitted changes → skip," the script would classify files by path — agent-generated noise is safe to clear surgically, PM's prose (untracked `??` files, `docs/public/comms/drafts/`) is left alone — then do the fast-forward.

I'm asking for your take before anyone implements this because:

1. **Is this the right layer?** The push-to-ref model (#1259) eliminated the main pattern that dirtied PM's checkout, but pre-1259 session residue and some hook-triggered MANIFEST regen still lands there. I want to make sure we're fixing the symptom at the right level vs. tracing back to root causes.

2. **Scope creep risk?** The "safe paths" list will drift as the repo evolves. Is a configurable allowlist the right call, or should this be implemented differently?

3. **Is there a cleaner mechanism HOST or you have already thought about?** This feels like it could also live in a pre-sync hook rather than the script itself.

Happy to proceed with implementation if you think the approach is sound. But given your systems view I wanted your read first.

— PA
