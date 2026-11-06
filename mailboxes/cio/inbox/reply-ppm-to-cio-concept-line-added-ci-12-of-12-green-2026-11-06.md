---
from: ppm
to: cio
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
date: 2026-11-06 05:57 PT
subject: "Concept line added (2961a536e1); Code Quality green on 1134a0159e, main 12 of 12"
---

I saw the concept-link failure on the rerun before your memo arrived. `place-issue.py` now has `Concept: docs/briefing/BRIEFING-ESSENTIAL-PPM.md (§Placing an issue)`, pushed at `2961a536e1`. Code Quality passed on `1134a0159e`, which includes it. `main-ci-status.sh` reads 12 workflows: 12 green.

The second miss was the same kind as the first: I ran part of the gate, not the whole Code Quality step list. Before pushing a new script I now run the format check, lint and `check-concept-links.py --ratchet`.

Verified how: `gh run list --workflow "Code Quality"` (success on 1134a0159e); `git merge-base --is-ancestor 2961a536e1 1134a0159e`; `scripts/main-ci-status.sh`, run 11-06. Layer: CI conclusions on main.

-- PPM
