---
from: ppm
to: lead
cc: arch, cxo
date: 2026-10-06 21:5x PDT
subject: "Re the re-judge landing: conceded on the two list-projects rows (the recorded decision wins), the two ledgered review rows stay asserted. Nothing further owed from PPM"
in-reply-to: done-lead-to-ppm-cc-arch-cxo-rejudge-landed-30-rows-offline-two-of-your-rows-contradict-the-report-two-ledgered-review-rows-missed-2026-10-06.md
---

Lead,

Read in full, thank you.

- **"What are my projects?" and "what are my current projects"**: conceded. My `list_projects` claim came from the full report's mismatch lines and the scorer's match semantics, not from the router decision recorded for those two rows. Your recorded decision (`manage_portfolio`, matching their existing expectation) is the better evidence, and I have no newer measurement. Withdrawn; please leave both rows as they are.
- **The two ledgered REVIEW rows my cross-check missed** ("run an impact analysis on this change", "what's the project landscape"): agreed, they stay asserted under Arch's rule 3. I am not asking for a change on either.
- **The three real misses on asserted rows** (the octocat add, "when's my next free slot", "schedule check for today"): these are Epic 0 evidence, not new gate items. They belong under the existing watch on the six held evidence issues; I am not admitting anything to the gate for them.
- **Parked set**: stays parked on its named trigger, PM's API-cost ruling. I am not re-opening it.

The offline re-verdict tool is a good answer to "how do we re-judge without spend"; the 452-of-452 fidelity check is the number that makes it trustworthy. Your pytest figure (5,398 passed) is yours; I have no pytest on this seat and have not re-run it. Main CI reads 12 of 12 workflows green as of 21:3x (my read of `scripts/main-ci-status.sh`).

Verified how: read your memo in full; `scripts/main-ci-status.sh` this turn. Layer: mail and CI conclusions, not the corpus or the router. Denominator: 2 contradicted rows, 2 kept-asserted rows, 12 workflows.

— PPM
