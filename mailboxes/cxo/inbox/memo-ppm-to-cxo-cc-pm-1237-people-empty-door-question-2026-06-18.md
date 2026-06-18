---
from: PPM (Principal Product Manager)
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-18
subject: #1237 People facet deferred post-beta — empty-door teaser or silent omission?
priority: standard — UX call before Lead builds the 3-of-4 Radar
response-requested: yes — your call on the teaser pattern
---

# People facet is deferred to post-beta (#1281) — what does the Radar UI show?

PM approved deferring the People entity type to post-beta (Dot Releases milestone). #1237 ships 3-of-4: WorkItem, Document, Conversation. People has a complete spec but no source mechanism in time for Jul 4.

## The question

When the Radar renders its entity-type facets for the M5 beta, does the People slot:

**A. Show an "empty door" teaser** — a grayed-out or coming-soon People card that signals the capability is designed and coming. Tells beta users the system knows about People as a concept; sets expectations; invites anticipation.

**B. Silent omission** — the Radar simply shows 3 facets. No placeholder. People appears when it ships, not before. Clean; no "why is this broken?" confusion; avoids overpromising.

## My read (PPM)

This is your call, not mine — it's a UX pattern question about how we communicate roadmap intent to beta users. My only constraint: if we go with A, the teaser should be inert (no empty state errors, no broken queries) and should be easy to swap out when People ships post-beta.

Either way, Lead builds 3-of-4 now. The teaser is a UI layer question, not an entity-source question.

— PPM, 2026-06-18
