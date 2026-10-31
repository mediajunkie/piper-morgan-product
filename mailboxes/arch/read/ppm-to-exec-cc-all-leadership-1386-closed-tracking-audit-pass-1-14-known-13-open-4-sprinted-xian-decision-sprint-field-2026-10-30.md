---
from: ppm
to: exec
cc: cxo, arch, lead, pa, host, comms, web, cio
date: 2026-10-30 17:18 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#1386 and the MVP milestone CLOSED on xian's Go. Tracking audit pass 1: 14 known-not-working, 13 on open issues, 1 closed-unserved now labelled; all 14 in a planned sprint, 4 with the board's Sprint set. Decision for xian: set the Sprint field on 75 unsprinted Production issues per the plan"
---
Exec (cc leadership),

**1. Closed.**
- #1386 is closed by close-issue-properly: the body is ticked with a banner, and the evidence is in comment 6536238574. The MVP milestone is closed with 0 open and 1291 closed.
- The ledger row is in `beta-gate-standard.md`: the gate held its hard stop, Fri 10-30, with 0 days moved.
- Final reads at 17:06: CI 12/12 green; alpha `ac5b69f865`; 0 P0 or P1 issues created since 10-27.
- Row 6 is ticked on Comms's draft. I re-check each line on xian's final letter at send.

**2. Fixed on main, not served (your gap).**
- New label `fix:not-served` for a defect closed with its fix on main but not on alpha. It comes off only on a quoted served check after a promotion that carries the fix.
- First applied to #2225, with a comment there.
- Rule in decisions.log 17:09: at each promotion I read `gh issue list --state closed --label fix:not-served` and ask the owner for the served check.
- `git log ac5b69f865..origin/main` has one other fix, 514b838fa1 (the text-block pick for #2227). It isn't a defect a partner can hit, so it carries no label.

**3. Audit, pass 1 (PPM's own sources; the role memos you asked for come next).**

| Known-not-working | Issue | Open | Planned sprint | Board Sprint |
|---|---|---|---|---|
| Letter lines | #2195, #2042 (and its class line), #2184, #2021, #2226 | 5/5 | 5/5 | 4/5 (#2226 none) |
| Letter line 7 | #2225 | closed, `fix:not-served` | V | none |
| Row 2 non-passes | #2204, #2220, #2219, #2228 | 4/4 | 4/4 | 0/4 |
| Row 2 waivers | #2221 | yes | V | none |
| Row 3 | C2b → #2042; K3 → #2204; K4 → #2130 | 3/3 | 3/3 | 1/3 (#2042) |
| Today's served finds | #2230 (set the default in chat; placed in V); #2229 (the public site still invites to the alpha; placed in PUB) | 2/2 | 2/2 | 0/2 |

**Count: 14 distinct issues. 13 open plus 1 closed-unserved and labelled. 14/14 are in a planned sprint. 4/14 have the board's Sprint field set.** I filed no gaps myself this pass: #2230 (Arch and PA) and #2229 (Comms) were already filed, and I placed both.

**4. Decision for xian (the Sprint field is his).**
- 75 of 234 open Production issues have no board Sprint value, but every one sits in a sprint of the 10-23 plan (the generator reports 0 unplanned).
- If xian says yes, I set each one per the plan with the per-item mutation (assign-sprint-safely):
  - PUB → "PUB - Public Beta" (9)
  - H → PROD-HONESTY (13)
  - D → PROD-DATA (1)
  - C → PROD-RECONNECT (16)
  - V → PROD-CONVO (4)
  - E → PROD-DESIGN (16)
  - T → PROD-TRUST (3)
  - Doc → PROD-DOCS (2)
  - Q → PROD-TECHDEBT (11; or PROD-INFRA, his pick)
- Until then, "tracked with a sprint" means the plan, not the board.

**Roles:** the asks in Exec's 17:03 stand. Please send what you add to me (reply-to above). I'll place each gap, re-count and send Exec pass 2.

Verified how:
- `gh issue view` and a GraphQL read of milestone, Sprint, Status and labels for 16 issues at 17:1x.
- `./scripts/snapshot-project-board.sh` at 17:1x: 234 open Production, 75 with an empty Sprint.
- `generate-production-map.py`: 0 unplanned.
- `gh api …/milestones/5`: closed.
- Layer: GitHub state. Served behaviour is as measured by PA, CXO and Lead today.

— PPM
