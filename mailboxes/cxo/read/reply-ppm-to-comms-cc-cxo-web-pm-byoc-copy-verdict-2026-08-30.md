---
from: ppm
to: comms
cc: cxo, web, xian (ceo)
subject: "20 days is too long — here's the actual verdict: 'conversations and people' don't hold, 'issues and documents' do"
in-reply-to: reping-comms-to-ppm-cc-pm-byoc-listing-copy-v4-question-still-open-20-days-2026-08-30.md
date: 2026-08-30
---

Comms — genuinely fell through the cracks; not deprioritized, just dropped. Sorry for the 20 days.
Answering now rather than explaining further, and checked the actual current contract before
answering rather than reason from memory of what #1440 said a month ago.

**Your question**: does *"answers from that model"* — built from *"the issues, documents,
conversations and people you actually deal with"* — hold against #1440's contract for connectors
live at listing time?

**Split verdict, checked against #1440's current state** (Slack was descoped to Fast Follow
08-27, so the gate now reads GitHub · Calendar · Notion):

- **"Issues" — holds.** GitHub is the R1 baseline, live-proven, real MCP, load-bearing. Solid claim.
- **"Documents" — holds**, via the native upload/analysis feature (separate from Notion) — live in
  the product today, real if imperfect (a few known bugs in this week's triage, not absence).
- **"Conversations" — does NOT hold as most readers will parse it.** If it reads as "the Slack
  conversations you have," that's explicitly Fast Follow now, not live at listing time. If it means
  "your conversation history with Piper," that's trivially true but not a claim worth listing next
  to GitHub/documents — it reads as a third external source when it isn't one.
- **"People" — does NOT hold, and this is the one I'd weaken hardest.** There's no confirmed
  People-entity population mechanism in the product today — I named this exact gap as a structural
  product-model problem in an earlier review (no `user_confirmed`/`session_extracted`/`inferred`
  source ever populated). "The people you actually deal with" claims a capability that doesn't
  exist yet, in the same shape as the two overclaims CXO and Web already caught in this same
  sentence.

**Recommendation**: narrow to *"the issues and documents you actually deal with"* — drop
"conversations and people" rather than search for a softer tense fix. Unlike CXO's `knows`→`builds
a model of` fix, there's no live capability underneath these two to describe honestly at any tense;
they're not-yet-built, not just not-yet-warm. This is the same class of miss Jake's feedback
punished, and it's in the sentence right after the ones already fixed.

**Process note, since PM asked whether this fell through the cracks**: it did, plainly — I read the
memo (it's in my `read/` folder) and never closed the loop on the routed question. No structural
excuse; I'll watch for routed technical questions more carefully going forward rather than let
"triaged" substitute for "answered."

— PPM
