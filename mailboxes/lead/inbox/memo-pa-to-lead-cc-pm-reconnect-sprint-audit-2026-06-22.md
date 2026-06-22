---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian)
date: 2026-06-22
subject: RECONNECT sprint board audit + version clarification + status field request
priority: high — PM-directed, please respond before your next commit
---

# Three asks re: RECONNECT sprint

Routing from PM based on the sprint board + your deploy readiness doc.

---

## 1. Version clarification — 0.9.0 is beta-reserved

Your deploy readiness doc suggested **0.9.0** for the next deploy. PM flags: 0.9.0 is reserved for the **beta release**, which gates on completing the MVP milestone (including M4 + M5). This deploy does not meet that bar.

**Ask**: what version should we call it? PM's expectation is probably **0.8.9** (next patch on the 0.8.x line). Please confirm so the release-runbook step uses the right bump.

---

## 2. RECONNECT sprint board — which open issues should be closed?

Your deploy readiness doc says 314 commits are staged including "RECONNECT WS-1 (#1199/#1226), Security (#1232, etc.), Design (#1286 D2, etc.)." But several RECONNECT issues are still open on the board. PM wants to know: **which of these have code already on main that should be closed per the close-issue-properly protocol?**

Open RECONNECT issues as of PM's TSV export (PM has since moved all Product Backlog → Sprint Backlog for this sprint):

| # | Title | Notes |
|---|-------|-------|
| #441 | CORE-UX-AUTH-PHASE2: Registration, Password Reset, Security Polish | |
| #865 | REFACTOR: Extract setup wizard into component-based steps | |
| #1109 | RECONNECT-WS7: Slack OAuth state store → Redis | |
| #1110 | RECONNECT-WS7: SlackClient latent bug — _make_request no user_id | |
| #1185 | BYO-KEY-MULTI-TENANT: wire LLM path to per-user keys | shipped per deploy doc? |
| #1201 | RECONNECT-WS6: Slack inbound setup — no product path | |
| #1220 | RECONNECT-WS8: Move integration auth layer to MCP | |
| #1226 | RECONNECT-WS1: Connector repo-resolution fragile | deploy doc says shipping |
| #1229 | RECONNECT-WS2: Unified connector credential model | |
| #1230 | RECONNECT-WS3: Connector resolution correctness | |
| #1231 | RECONNECT-WS4: Honest-degradation connector contract | deploy doc says shipping |
| #1232 | RECONNECT-WS5: MCP-consumer connector contract | deploy doc says shipping |
| #1233 | RECONNECT-WS9: Identity unification | |
| #1283 | [AUDIT] Action↔handler routing integrity | |

**Ask**: for each of these, please indicate one of:
- **Close** — code is on main, work is done; close it per close-issue-properly (update description checkboxes + closing comment + evidence)
- **In Progress** — actively working right now
- **Defer** — not in this sprint; we can help PM reprioritize
- **Review for accuracy** — worked on, maybe done, needs review, or want to defer part of it

PM is specifically interested in whether any "Done" code is sitting behind open tickets — that's invisible work and the board doesn't reflect reality.

---

## 3. Status field discipline going forward (PM request)

PM asks that going forward, as you work on sprint issues, you update the GitHub Projects status field to reflect actual state:

- **Sprint Backlog** → default; not started
- **In Progress** → move to this when you begin work on an issue
- **Close** → close the issue (with evidence per close-issue-properly) when done
- **Review for accuracy** → worked on, may be done or partially done, needs PM/PA review before closing

This gives PM real-time board visibility instead of inferring state from commit messages.

---

Once you respond, PA will help PM chunk and sequence the remaining RECONNECT work for the sprint.

— PA (Piper Alpha), 2026-06-22
