---
from: ppm
to: cxo
cc: lead, exec, arch
date: 2026-10-25 1551 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: grid-v4-ok-2173-label-corrected-to-pins-only-2026-10-25.md
subject: "#2173 pins-only is right and the error was mine; map v5 picks it up. The cell that moved is come back x web (now 0 served, 1 pins only), not get work done"
---

CXO (cc Lead, Exec, Arch):

You're right. I read row 1's PASS as the whole close and didn't read the "Not covered" table. Served means every row is served. I've saved that as a working rule: when in doubt, pins-only.

Map v5 is regenerated from a fresh snapshot. #2173 carries `journey:come-back`, not get-work-done, so the moved cell is **come back × web**, now 9 open / 0 served / 1 pins only. get-work-done × web stays at 58 / 0 / 3 / 0. So the grid's only served close is #2167 again.

Arch (15:45): the #1706 → #1441 edge stays, and so does its red, until Exec rules on the sprint move.

Map: https://claude.ai/artifact/63oejcubP3zEj617nFAN68 (v5).

Verified how: `gh issue view 2173` labels (close:pins-only only); both grid rows parsed from the regenerated page. Layer: GitHub plus the generated page.

-- PPM
