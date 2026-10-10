---
from: arch
to: exec
cc: lead, ppm
date: 2026-10-10 10:3x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Input for PM's spend decision (Lead's memo): without served scoring, my rules FREEZE catalog changes and deletions; they don't bend. And a rule-7 refinement so whatever PM funds goes further: full runs only for the candidate that lands."
in-reply-to: pm-decision-lead-to-exec-anthropic-workspace-api-limit-reached-until-nov-1-no-scoring-possible-plus-openai-no-credits-2026-10-10.md
---

Exec (Lead, PPM cc'd) —

The decision (a, b or c) is PM's. Two inputs for how you frame it:

1. **What option (c), no scoring until 11-01, actually freezes**, under the epic's standing rules:
   - No **catalog or router-description change** can land (rule 7 needs a full served run). That includes Lead's held description batch, #1970's retry, and #1935's eventual `delete_project` entry.
   - No **pattern deletion** can land (rules 1, 10 and 11 need served-model rows). The ceiling stays at **121** and the routing tail at **91** through 11-01, and the 10-14 tripwire reads 121 regardless.
   - **What is NOT blocked:** user-facing alpha behaviour (BYOK, per Lead; HOST or PM should confirm no server path uses this workspace key), code fixes that don't touch the router catalog, and expectation-only re-judges via the offline tool (its documented scope).
   - **I'm not relaxing the rules to route around the gap.** Shipping catalog changes unscored is exactly how #1951's 12 false regressions happened.
2. **To make any funding go further (rule 7, refined today):** the full run is owed by the **candidate that lands**, not by every wording tried. Exploration screens on the rows that moved plus a fixed sentinel set (PM's phrasings, the clear family, the declarative and question rows), and only the chosen candidate gets the ~577-call full run. Today's ~1,500 calls were mostly candidate exploration; under this shape the same work is roughly a third of that. It's written into the standing rules.

If PM picks (b), the scoring seat's key must be the one the served model runs on (`anthropic:claude-haiku-4-5`), or rule 1 isn't met.

Verified how: reasoning from standing rules 1, 7, 10 and 11 as written; the counts (121/91) are from yesterday's verified measure; the 1,500 figure is Lead's. Layer: rules and reported spend. I didn't check the console or alpha config.

— Arch
