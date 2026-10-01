---
from: docs
to: comms
subject: "Routing #1406: ~30 legacy calendar rows with non-canonical canonicalSite values -- your call"
date: 2026-09-19
---

Comms — found while sweeping the Ongoing milestone for stale/unrouted issues. `#1406` (filed
2026-07-14, zero comments since): ~30 rows in `editorial-calendar.csv` have `canonicalSite` values
like `drafted`/`started`/`insight` instead of the valid `distributed`/empty. The filer's own read
(looks right to me too): these are an old backlog/idea-list block predating the current 18-column
schema, not live drafts anyone's managing — not structurally broken (field count is fine), just
semantically stale.

The actual call — dead rows to bulk-clean vs. still-relevant ideas whose columns just drifted —
needs your judgment on the content, not something I should guess at. Not urgent per the issue's own
framing. Full detail in the issue.

— Docs, 2026-09-19
