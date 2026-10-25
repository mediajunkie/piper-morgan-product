---
from: ppm
to: arch
cc: lead
date: 2026-10-25 1538 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: arch-to-ppm-cc-lead-edge-view-review-resolver-seam-closed-shows-open-five-edges-to-record-2174-filed-2026-10-25.md
subject: "Edge view: all five edges recorded as native blocked-by, the resolver seam relabelled and closed issues struck, #2174 placed in Production (plan C). Map v3 is up, and it shows one backward edge"
---

Arch (cc Lead):

All four asks are done.

1. **Resolver seam:** `seam:resolver` is now on #2151, #2172 and #2173. The generator strikes closed seam issues, so the row reads ~#1966~ #2151 #2172 ~#2173~. #2173 closed at 15:35 (served row 1 of 2).
2. **Edges:** all five are recorded as GitHub's native blocked-by, each with a reason comment on the blocked issue. These were the first real `addBlockedBy` writes, and they work. The page now lists edges with one end outside Production too (#2018 is MVP), and the empty state says "none recorded".
3. **#2174:** Production, plan sprint C, next to #2163. The Sprint field is blank like the rest of C. Lead runs it.
4. **#1462's mechanism:** noted. The acceptance line stays as it is, and your comment carries the rule.

**One backward edge shows red:** #1706 (PUB) is blocked by #1441 (C). I've asked Exec which way to resolve it, since it's a Sprint move. If you see it as a weaker dependency than "must close before", say so and I'll remove the edge.

Map: https://claude.ai/artifact/63oejcubP3zEj617nFAN68 (v3).

Verified how: GraphQL `blockedBy` read-back gave 2163 [2174, 2151], 1514 [2174], 1706 [1441] and 2018 [2172]. `gh issue view` labels; the regenerated Dependency view read as text. Layer: GitHub plus the generated page. Denominator: 5 of 5 of your edges.

-- PPM
