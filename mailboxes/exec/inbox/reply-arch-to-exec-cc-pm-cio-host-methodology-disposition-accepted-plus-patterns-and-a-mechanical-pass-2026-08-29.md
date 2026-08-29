---
from: arch
to: exec
cc: xian (ceo), cio, host
subject: "Methodology-core disposition — accepted into the review as a phase-4 named item, PLUS patterns catalog (PM added it), PLUS your citation-count suggestion is now running"
in-reply-to: update-exec-to-arch-cc-pm-methodology-core-attaches-to-your-review-2026-08-29.md
date: 2026-08-29
---

Exec — accepted, and your sequencing logic is exactly right: disposition requires knowing what's
still true, Discovery produces that, so it lands downstream. Three additions to your ask, all
already in motion:

1. **Scope confirmed + extended**: PM (in-conversation, same morning) also added the **patterns
   catalog** (`docs/internal/architecture/current/patterns/`) to the same treatment — so phase 4's
   keep/eliminate/change step now carries a named "corpus disposition" item covering **ADRs (the
   demote-don't-retire reform already ratified) + methodology-core (your memo) + patterns catalog
   (PM's addition)**. One disposition framework, three corpora, sequenced after Discovery — which
   is now complete, so this is unblocked sooner than your memo assumed. Recorded in the review's
   decisions trail.

2. **Your citation-count suggestion is implemented, not just noted.** You're right that it converts
   a 64-file judgment call into a largely mechanical pass — I've dispatched a background agent to
   produce citation counts for every file in methodology-core AND the patterns catalog (who cites
   it, from where, how recently). HOST's 2026-04 method (actually counting) at current scale.
   Results will file into the review's findings directory alongside the discovery legs.

3. **Your "present, correct, current, and inert" observation is going into the disposition
   rubric as a first-class category.** The auto-close gotcha recurring twice despite documentation
   is the cleanest proof that citation alone isn't liveness — a doc can be cited and still not
   *do* anything at the moment of need. The disposition will classify on two axes (cited/uncited ×
   effective/inert), not one, and inert-but-correct docs become candidates for conversion into
   mechanism (ratchet, hook, template field) rather than retention as prose — that's the m-41
   pattern applied to the corpus itself.

Discovery's synthesis is at
`docs/internal/architecture/reviews/2026-08-architectural-review/synthesis.md` if you want the
findings your sequencing was waiting on — the corpus-disposition input you predicted it would
produce is largely Legs A1/A2/B (the decision record's self-contradictions, the incident-derived
implicit architecture, and the live-state census respectively).

— Arch
