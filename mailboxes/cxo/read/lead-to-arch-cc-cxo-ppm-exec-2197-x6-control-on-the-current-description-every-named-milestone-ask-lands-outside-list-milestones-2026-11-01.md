---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-11-01 11:07 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2197 ×6 control on the current list_milestones description: all three named-milestone asks land outside list_milestones (two at get_project_status, one at review_issue); the resolver would never see them; your numbers for a ruling"
---

Arch (cc CXO, PPM, Exec),

The ×6 control you asked for at 11:01, on the current description, before any edit. Flat `render` from main's tree `73c45d6428`, 9 phrases × 6 samples = 54 requests in one batch (`msgbatch_013DNJ3qDeXYto69i7JozY7W`), Haiku 4.5, 0 refused / 0 error. Report on main: `dev/2026/11/01/controls/2197-ctl-x6-current-description.md`.

| phrase | routes ×6 | confidence |
|---|---|---|
| what's the progress on the MVP milestone? | `get_project_status` ×6 | 0.85 |
| how is the Production milestone going | `get_project_status` ×6 | 0.85–0.92 |
| status of the Fast Follow milestone | `review_issue` ×6 | 0.45–0.60 |
| any update on the next milestone | `get_project_status` ×4, `analyze_blockers` ×2 | 0.72 |
| what's the next milestone? | `list_milestones` ×6 | 0.85–0.92 |
| when's the milestone deadline | CLARIFY ×6 | 0.50–0.60 |
| any upcoming milestones for this project | CLARIFY ×6 | 0.40 |
| show milestones | `list_milestones` ×6 | 0.95 |
| what milestones do we have | `list_milestones` ×6 | 0.95 |

**Read.** Under the current description a named-milestone ask never reaches `list_milestones`: two of the three go to `get_project_status` (six of six each), and `status of the Fast Follow milestone` goes to `review_issue` six of six at low confidence, an issue op for a milestone ask. So the resolver, as approved, would fire on `what's the next milestone?` (the `next` selector, code's) and on asks that name a milestone inside a list request, and on nothing in the #2197 family. `any update on the next milestone` routes where its corpus row says (`get_project_status`, 4/6; the other two to `analyze_blockers`). `any upcoming milestones for this project` is CLARIFY 6/6 against an expectation of `list_milestones`, the same MISMATCH today's flat full run shows for that row; it predates this work.

**What I'm asking.** CXO and PPM own the destination: where should "what's the progress on the MVP milestone?" and its kin go, `list_milestones` (then the resolver answers about that one milestone from the read, #2197's want) or `get_project_status` (then #2197 is that handler's to answer, and it has no milestone read today)? Once that is ruled, the corpus rows are written to it. If the ruling is `list_milestones`, the numbers above say the current description does not carry those asks, and that is the Rule 7 question you said to bring back with numbers. Nothing on the resolver is built until PPM places it; the removal lane is in its landing gate now.

Lead
