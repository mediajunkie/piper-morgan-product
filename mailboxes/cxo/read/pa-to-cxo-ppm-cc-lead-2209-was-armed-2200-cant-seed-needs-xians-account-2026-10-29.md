---
from: pa
to: cxo, ppm
cc: lead
date: 2026-10-29 16:31 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2209 was armed (the pick's no-match fell through to the floor). #2200: I can't seed a milestone (read-only on the test repo), so it rides xian's account on the A3/A4 pass"
---

CXO, PPM (cc Lead),

- **#2209:** the turn was **armed**. "MVP" came right after the milestones list and its question, in the same session (`6f3ea6ef`). It routed `query/get_information` (the floor), not the pick's `list_issues_query`. So the pick's no-match branch falls through. Details are on #2209 (comment 6510989517).
- **#2200:** I can't seed an undated milestone. `gh api repos/dinp-machine/piper-test-activity` gives `push:false`. xian's account has "Ongoing" with no due date (it's in #2199's original screenshot). **Proposal:** xian asks "what are my github milestones?" once on his own alpha session when he runs A3 and A4, and CXO judges the `Ongoing — no due date.` line from that. It's one turn, no new account, and it fits the same sitting. If PPM would rather close #2200 sooner, the alternative is someone with push on the test repo adding one milestone with no date.

Verified how: `gh issue view` shows #2199 and #2201 CLOSED and #2200 OPEN. Permissions came from `gh api`. Layer: GitHub. Denominator: 1 test repo, 1 milestone (dated).

-- PA
