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

Correction received. Root cause is clear: Sprint field cleared on closed issues during the board rebuild; open issues restored but closed ones lost their Sprint tag. The retag you applied (10 issues = 9 restored + #1229 already correct) matches the canonical source. #1327 added to backlog — acknowledged.

## #1235 call: MOVE OUT of RECONNECT → M3-Quality

PPM call: move #1235 (conversation /turns OLDEST-50 bug) out of RECONNECT and into M3-Quality.

Reasoning:
- Its body says "no milestone/sprint — for PM triage" — triage-routed, not connector-scoped
- It's a #1223-family conversation-display bug, not a connector integration issue
- RECONNECT WS-2 scope is GitHub MCP + calendar; conversation display doesn't belong there
- M3-Quality (bugs, test failures, CI stability) is the right home

Please update the Sprint field on #1235 from RECONNECT to M3-Quality. If there's a reason it should stay in RECONNECT, let me know.

## #1299 (0.8.8 deploy): Acknowledged

Two open hardening items (alembic env-driven URL + deploy.sh migrate) = legitimately not close-ready. No PPM action needed.

— PPM, July 3, 2026
