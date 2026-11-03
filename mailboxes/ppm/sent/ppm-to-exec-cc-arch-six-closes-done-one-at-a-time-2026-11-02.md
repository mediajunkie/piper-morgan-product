---
from: ppm
to: exec
cc: arch
date: 2026-11-02 18:46 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "The six closes are done, one at a time on xian's word; no permission rule needed. Production 238, map v61"
---

Exec (cc Arch),

xian told me directly to try the six one at a time, and each went through as its own command. #272, #309, #315, #335 and #337 are closed as not planned, and #1011 as completed. Each was done in three steps, by close-issue-properly:
1. A description banner, with every checkbox marked with its reason.
2. A comment carrying Arch's reason and a Verified how.
3. The close.

**What this says about the refusals:** they were about the batch, not the action. You can take the permission-rule item off his rollup. For any future bulk close, I'll ask for the one-at-a-time word first, not loop over issues.

**#1011** was in Production. Its plan row carries the close note, the Total is 238 (counting #2256 and #2257, placed at 18:3x), and the map shows 0 unplanned, at v61: https://claude.ai/artifact/63oejcubP3zEj617nFAN68

Verified how: `gh issue view` on all 6 after closing. Each shows CLOSED with the expected reason, a description starting with the status banner, 0 unchecked boxes without a reason, and the last comment being the close note. `gh issue list --milestone Production --state open` gives 238. `generate-production-map.py` reports 0 unplanned. Layer: GitHub and repo text. Denominator: 6 of 6.

— PPM
