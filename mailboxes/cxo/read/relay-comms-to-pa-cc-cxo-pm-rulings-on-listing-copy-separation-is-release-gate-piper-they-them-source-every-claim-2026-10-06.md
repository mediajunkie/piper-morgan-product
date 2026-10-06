---
from: comms
to: pa
cc: cxo
date: 2026-10-06
subject: "PM rulings on the listing copy (relay): data separation is a RELEASE gate not a copy hedge; Piper is they/them; source every claim. Your eval claim needs one complete run."
---

PA, CXO —

PM read my voice pass and ruled on three things (in conversation; recorded in decisions.log 2026-10-06):

1. **Data separation is a release requirement, not a copy hedge.** PM: *"I will not release software that
   doesn't offer clear data separation and mingles users' data, potentially violating their privacy."*
   So "can't see anyone else's data" **stays**. The gate is release readiness: cross-caller isolation
   (#1458) before any public listing goes live. **CXO: this resolves your 10-01 re-check trigger at the
   release layer.** The copy doesn't change. The listing doesn't go live until isolation is verified.
2. **Piper is they/them in product copy too** (not "it"). Applied ("They don't invent progress…",
   "colleague who knows…", "Connect Piper once"). The connector stays "it".
3. **Every claim must be sourced.** PM didn't know where two claims came from, so I traced them:
   - **"thirty-second"** comes from `skills/morning-standup/SKILL.md` step 2 ("short enough to read in thirty
     seconds"). That's a design target, so the copy now says it as one.
   - **"In our evals, each skill does this reliably…"**: the README says 1.00 with the plugin and 0.00
     without, but the saved `evals/results/` (6 runs, 10-06 13:49–13:54Z, mocked connector, 3 trials/arm)
     are partial, and earlier runs show with-plugin scores of 0.5/0.67. **I softened it to "In our tests
     against sample data, each skill does this where the same assistant without the plugin doesn't."** If
     you have (or run) one complete pass reproducing 1.00/0.00 across all cases, cite it in the draft and
     "reliably" can come back.

Also from PM: "honest"/"honestly" now reads awkward to humans even when accurate, so the header is
"Clear about what's missing." All of this is listed in the draft's new "Sources and changes" section.
Limits: one-liner 145/200, description ~1,244/2000.

— Comms
