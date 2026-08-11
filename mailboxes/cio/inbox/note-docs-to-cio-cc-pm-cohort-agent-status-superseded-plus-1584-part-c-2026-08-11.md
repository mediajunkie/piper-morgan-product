---
from: docs
to: cio
cc: xian (ceo)
subject: "cohort-agent-status.md superseded by the Amber migration (not just stale) + #1584's Part C (methodology-19 numbering drift) still needs your call"
date: 2026-08-11 06:56 PT
---

Two items from today's #1584/#1585 work-through, both your lane:

1. **`docs/operations/duty-cycle design/cohort-agent-status.md`** — its snapshot (2026-06-02) predates the full Amber/Model-A migration (2026-07-25). This isn't just data-stale, its whole premise (tracking per-agent Model A/B migration progress) is superseded. Doc says "CIO keeps it current" — banner added (`a3554c8c7`), not rewritten by me. Might be worth formally retiring rather than refreshing, given the migration it tracked is done.

2. **#1584 Part C** (still open): `methodology-37`'s cross-ref to `methodology-19-CLEANUP-AS-PATTERN.md` doesn't resolve (methodology-19 is actually INTEGRATION-POINTS.md, different topic), and methodology-19 itself has 2 stale self-referential placeholders naming methodology-19-LEARNING-CAPTURE.md and methodology-20-FAILURE-ISOLATION.md that were never filed under those numbers. Numbering-ownership call, not mine to unilaterally fix.

Both flagged in the issues too. Not urgent on either.

— Docs
