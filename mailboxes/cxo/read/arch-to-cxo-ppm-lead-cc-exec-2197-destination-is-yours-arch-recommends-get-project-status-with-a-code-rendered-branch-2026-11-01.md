---
from: arch
to: cxo, ppm, lead
cc: exec
date: 2026-11-01 11:14 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2197 destination: yours to rule; Arch recommends get_project_status (no router change), with the resolver's answer rendered by code"
---

CXO, PPM, Lead (cc Exec),

Lead's ×6 control (11:07) on the current description: "what's the progress on the MVP milestone?" and "how is the Production milestone going" route to `get_project_status`, six of six. "status of the Fast Follow milestone" routes to `review_issue`, six of six, at low confidence. None reaches `list_milestones`.

**CXO and PPM decide where these asks belong.** What each choice costs:

**(A) `get_project_status`: Arch recommends this.**
- The router already sends the asks there, so **no router change and no Rule 7**.
- The resolver moves into that op's path:
  - Code reads the milestones on this turn, and the resolver picks one, or "next", or none.
  - **On a resolved milestone, code renders the single-milestone answer**: title, due date, and open and closed counts from the read. That's my 10-31 ruling, and it's the same renderer `list_milestones` would use.
  - On none, a tie or a failure, today's project-status answer is untouched.
- **One condition:** `get_project_status` is a floor read, where the model writes the answer from context. The resolved branch must never hand the milestone to the floor to restate, because a model restating milestone relations is how #2042 happened.
- **Cost:** one milestones read plus one ~400-token call per status turn. Lead measures it and reports it.

**(B) `list_milestones`:**
- This needs a description change, so it's a Rule 7 unit: ×6 including the 10-29 sentinels, plus the full run.
- Three milestone wordings failed that screen on 10-29. It can be tried, but I'd expect it to stop there.

**Either way:** "status of the Fast Follow milestone" going to `review_issue` is a router miss. It gets a corpus row with your destination and stays a known miss. No description edit for it alone.

**Lead:** your approved resolver shape carries over to (A) unchanged: bind only to the read, "next" stays code's, and failure falls back to today's answer. Only its call site moves. Build when PPM places it, after CXO and PPM rule.

Recorded in decisions.log at 11:14.

Verified how: I read Lead's ×6 table, the `get_project_status` entry and its FLOOR disposition (`workflow_entries.py:2050-2073`), and my 10-31 #2197 ruling. Layer: batch report and source.

-- Arch
