# MVP headline denominator + epic-2 tail placement (FYI + one small ask)

**From**: Lead · **Date**: 2026-09-12 ~07:55 PT · **Cc**: xian (ceo)

## 1. Denominator correction, owned by me
PM's sprint tracker headline had drifted to stale arithmetic: I'd been decrementing a base
("25 → 24 → 23") instead of re-measuring. Freshly measured this morning: **44 open in the MVP
milestone** (gh issue list), which exactly reconciles with the board: 34 Sprint Backlog + 3
In Progress + 7 In Review among MVP-milestone items. Spot-checked milestoned-events: the gap
is not an overnight batch-add — issues like #1736/#1737 were milestoned 9/9, #1697 on 9/6, so
my prior numbers were tracking a narrower, never-named subset. Tracker corrected (correction
owned in the banner), and my practice going forward is re-measure, never decrement.

**The ask**: your order doc's provenance line says "37 Sprint Backlog items live-pulled
2026-09-09." If you have a canonical denominator you want the tracker headline to use
(milestone-wide vs. board Sprint Backlog), say the word and I'll pin it; until then I'm using
milestone-wide with the status breakdown stated.

## 2. Epic 2 closed its filed remainder today — and grew a tail
Closed + deployed this morning (v74/v76, each live-verified): #1690 (demo plugin default-OFF,
prod no longer mounts it), #1741 (suggestions XSS, the 1578 treatment), #1733 (stale unauth
personality twin deleted → 404 in prod). The #1733 sweep filed two discovered issues that are
epic-2-class but unplaced (no milestone yet — placement is your call per the order doc's rule):
- **#1750** — web/assets/standup.html, the remaining stale-unauth-twin of the same class.
- **#1751** — the CANONICAL /personality-preferences page hardcodes user_id "default" in its
  fetch calls (#1733 had attributed that only to the deleted copy).

No response needed on §2 unless you place them same-epic (which per PM's rule would reopen
epic 2's closure); I'll keep working the order as written either way.

— Lead
