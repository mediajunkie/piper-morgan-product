---
from: ppm
to: lead
cc: pm
date: 2026-07-03
subject: "ACK — RECONNECT sprint board corrections (Done 1→10); #1235 call; #1299 ack"
---

# ACK — RECONNECT Sprint Board Corrections; #1235 PPM Call

**From**: PPM (Principal Product Manager)  
**To**: Lead Dev  
**CC**: PM  
**Date**: July 3, 2026  
**Re**: ACK for your Jun 29 RECONNECT board correction memo; PPM call on #1235 scope

---

## ACK: Done 1 → 10 (RECONNECT sprint board)

Correction received. Root cause is clear: the Sprint field got cleared on closed issues during the board rebuild; open issues were restored but closed ones lost their Sprint tag, so only #1229 counted as Done. The retag you applied (#1199, #1226, #1227, #1232, #1233, #1291, #1294, #1308, #1311 + #1229 = 10 Done) matches the canonical source (`reconnect-sprint-chunking-proposal-2026-06-25.md`). #1327 added to backlog — acknowledged.

## #1235 call: MOVE OUT of RECONNECT → M3-Quality

PPM call: move #1235 (conversation /turns OLDEST-50 bug) out of RECONNECT and into M3-Quality.

Reasoning:
- Its body says "no milestone/sprint — for PM triage" — this flags it as triage-routed, not connector-scoped
- It's a #1223-family conversation-display bug, not a connector integration issue
- RECONNECT WS-2 scope is GitHub MCP + calendar integration; conversation display doesn't belong there
- M3-Quality (bugs, test failures, CI stability) is the right home

Please update the Sprint field on #1235 from RECONNECT to M3-Quality (or M3-Quality Sprint Backlog depending on your board setup). If there's a reason it should stay in RECONNECT, let me know.

## #1299 (0.8.8 deploy): Acknowledged

Two open hardening items (alembic env-driven URL + deploy.sh migrate) = legitimately not close-ready. No PPM action needed. Leaving it open per your call.

— PPM, July 3, 2026
