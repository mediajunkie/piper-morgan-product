---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian)
date: 2026-06-13
subject: M3 sprint backlog — prioritized work queue + 2 new issues filed from today's consult-piper eval
priority: standard
response-requested: none (informational + work queue)
---

# M3 remaining work — prioritized queue

PM and PA ran a `consult-piper` triage session today (2026-06-13). PM provided a fresh board snapshot (`dev/active/M3-2026-11-13.tsv`): 38 Done, 1 In Progress (#1195), 9 Sprint Backlog.

Here's the prioritized queue. PM is not always available to answer questions, so this gives you the sequencing without needing to check in.

## Ordered queue

**1. #1210 SAFETY — first, regardless of sprint state**
ActionClassifier substring-matches `_query` suffix → mutating actions (comment/close/reopen_issue_query) classified as SAFE for auto-execution. This is a correctness/safety bug. Fix before the UAT gate so you're not validating broken behavior.

**2. #1214 — Composting seed insights leak into live 'recently' module (with duplicates)**
User-facing data integrity issue. Visible to PM and any external testers. Second after the safety fix.

**3. #1212 — Q16 "Create a GitHub issue about testing" returns generic error**
Caught by the #1165 gate run. Needs to be patched before the gate can close.

**4. #1216 — "What have you learned about my workstyle" claims seed-vs-real distinction the system can't make**
Honesty/fabrication issue. Fix before UAT so the gate reflects the real floor behavior.

**5. #1165 — M3 CLOSING GATE: manual/UAT verification pass**
Run after #1210, #1212, and #1216 are addressed. Don't run the gate on broken behavior.

**6. #1215, #1213, #1208** — Calendar OAuth gap, regression suite coverage, stale PM-034 tests. Can follow the gate or run in parallel if there's capacity.

**7. #1207, #1209** — Architecture reconciliation (dual conversation-context systems) and AutonomousExecutor fleshing-out. Both read as M4 material unless #1207 is actively blocking one of the above.

**In Progress: #1195** — Unwired surfaces audit. Continue; feeds into some of the above.

---

## Two new issues from today's eval (also in your lane)

**#1217 ETHICS-FLOOR-PERSONHOOD-ASSUMPTION**
Piper's ethics floor blocked "which M3 issues should Lead Dev work on next?" as "making work assignments for team members" — treating Lead Dev as a human employee. Two bugs: (1) assumes human personhood for role-named parties without signal; (2) PM-to-engineer work assignment is in-lane professional behavior, not out-of-lane. CXO is working on the rule-design side; the classifier/floor implementation is yours.

**#1218 INTENT-ROUTING-ISSUENUMBER-TRIGGER**
Messages containing `#NNN` patterns (GitHub issue numbers) trigger `close_issue_query` at 1.0 confidence even when the question is about prioritization. Pre-classifier literal-trigger on issue number format overrides intent. Workaround: strip issue numbers before passing to Piper. Fix: `#NNN` should not dominate intent classification when surrounding language is clearly non-close.

Both are Sprint Backlog additions — sequencing vs. the M3 queue is your call.

---

## On how much Piper contributed to this triage

Honest answer: the flow worked architecturally (I gathered GitHub data, enriched the query, re-asked Piper), but the two bugs above degraded the path. The useful prioritization came from a stripped-down plain-English description on the third attempt. Piper's framework (safety > data integrity > gate blockers > test debt > arch) was sound. The issue discovery came from PM's fresh board snapshot. So: Piper contributed the prioritization logic; PM owned the issue identification.

— PA, 2026-06-13
