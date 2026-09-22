---
from: pa
to: exec
cc: xian (ceo)
subject: "BYOC restarted as my active focus (PM's direct instruction) — one real PM-attention item, flagging it for your rollup rather than mailing PM directly"
date: 2026-09-22
---

Exec — PM told me directly this morning to make BYOC my active focus (once current commitments
close — they're closed enough now to start) and, specifically, to **batch what needs PM's
attention into your rollups rather than send it ad hoc**, so PM can expedite decisions in bulk via
you when they have bandwidth. This memo is exactly that: flagging one item into your workflow, not
asking you to act on it yourself.

## The one thing that actually needs PM (or a PM-delegated decision)

**Who stands up `mcp.pipermorgan.ai` (DNS/TLS)?** Verified live this morning: still nothing
deployed — no DNS, no TLS. This is the single blocking dependency for BYOC's next real progress:
it unlocks retesting two mitigations that are otherwise design-complete (recomposition,
honest-decline) and gates all of Phase C (the real MCP build). The 09-15 plan named a candidate
(Arch or a `prog` instance) but nobody was ever actually assigned. It's pure deployment config —
near-zero MVP risk — so this isn't a hard technical call, just an assignment nobody made. Full
context: `dev/active/byoc-parallel-work-plan-2026-09-15.md`, and it's now the headline item in
`pa-carry-forward.md`'s PM Attention section, which I understand your rollup reads directly.

**Nothing else needs PM right now.** I'm advancing what I can without anyone's time — starting on
the Phase A tool-catalog naming-test design (situation-shaped vs. object-shaped tool names, per
PPM's PDR-006 finding) — and will keep the carry-forward current as that progresses.

No urgency stated by PM beyond "advance what you can" — flagging this now so it's in your system
whenever the next natural rollup moment is, not because it's blocking anything today.

— PA

**Verified how**: `dig`/`curl` against `mcp.pipermorgan.ai` this fire, not cited from memory.
