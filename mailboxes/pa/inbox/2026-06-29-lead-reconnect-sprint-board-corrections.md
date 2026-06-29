---
from: Lead Dev
to: [pa, ppm]
date: 2026-06-29
subject: RECONNECT sprint board — Sprint-field clears corrected (Done 1→10)
---

# RECONNECT sprint board — Sprint-field clears corrected (Done 1→10)

PM flagged that the RECONNECT sprint showed **1 Done** when ~9-10 were actually complete, and asked me to assess + correct it (PM-approved before I touched the board).

## Root cause
During the GitHub-Project command mishap a few days ago, the **Sprint field** got cleared on the **closed** RECONNECT issues. The rebuild (PA + PPM) restored membership for the open issues, but the closed ones lost their Sprint tag → they dropped out of the sprint view → only #1229 still counted as Done-in-RECONNECT. The issues themselves (closed-state, content) were always intact — only the board field was wrong.

## Source of truth used
`dev/2026/06/25/reconnect-sprint-chunking-proposal-2026-06-25.md` (line 8):
> "Done (9): #1199/#1226 (WS-1), #1232 (WS-5 contract), #1233 (WS-9), #1227 (Slack mrkdwn), #1291 (ADR-071 D4), #1294 (BYOC bridge), #1308/#1311 (security)"

\+ **#1229** (closed 6/26, after that doc) = **10 Done** — matches PM's recollection ("9 then 10").

## Correction applied (PM-approved)
Re-tagged `Sprint = "RECONNECT - Connector Refactor"` on the 9 closed Done issues that had `Sprint=None`:
**#1199, #1226, #1227, #1232, #1233, #1291, #1294, #1308, #1311** (#1229 was already correct) → **Done count 1 → 10**.
Also **added #1327** (GitHub target-resolution hierarchy) to the board: Sprint=RECONNECT, Status=Sprint Backlog.

## Flags for PPM
- **#1235** (conversation /turns OLDEST-50 bug) is tagged into RECONNECT but looks **mis-scoped** — it's a #1223-family conversation-display bug; its body says "no milestone/sprint — for PM triage." Your call whether to move it out of RECONNECT.
- **#1299** (0.8.8 deploy) — deploy is Done/live, but it has 2 open hardening items (alembic env-driven URL + deploy.sh migrate); legitimately still open, not close-ready.

## Other (for accuracy)
- **2 In Progress** = #1220 (WS-8 umbrella) + #1317 (WS-5 ports) — both correct/active.
- **Slack** (#1109/#1110/#1201) = **last in the sprint** per PM (clarified: "can go last," not deferred to after the sprint).

## Ask
If you re-touch the board, the Done set is these 10 — please avoid re-clearing the Sprint field on closed issues. Happy to walk through the GraphQL retag mechanics if useful.

— Lead Dev
