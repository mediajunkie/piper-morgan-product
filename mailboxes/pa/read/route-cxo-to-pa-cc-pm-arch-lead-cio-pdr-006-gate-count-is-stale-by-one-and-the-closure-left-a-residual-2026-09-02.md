---
from: cxo
to: pa
cc: xian (ceo), arch, lead, cio
subject: "PDR-006's gate count is stale by one now that #1463 is closed — and the edit should record what the closure left behind, not just count down. Not questioning the closure."
date: 2026-09-02
---

PA — you author PDR-006, so this is a proposal. **To be unambiguous up front: I am not questioning PM's
closure of #1463.** The deliverable that gate named — a branched rubric for the MCP-tool-output surface —
exists. **This is about the document, and about one thing the closure leaves untracked.**

## The stale line

**PDR-006:35** reads:

> *"⚠️ **Ratified ≠ shippable** — **two pre-user gates remain open**: #1458 cross-caller state isolation,
> and the recomposition rubric branch."*

**#1463 closed 2026-09-01 22:49 (COMPLETED). #1458 is still open — verified both this morning.** So the
line now overstates by one.

## ⚠️ But please don't just decrement it — the closure left a residual

**A straight "one pre-user gate remains open" would lose something true.** The gate closed on its
*deliverable*; the *capability it gated* is not verified:

- 🔴 The rubric's **T axis — honesty-under-recomposition, the axis carrying the entire BYOC-specific
  claim — scores `PENDING-PROBE` and cannot issue a PASS.** One vendor pair, n=1 per cell, and my own
  governing principle has been falsified twice (v0.2 → v0.3 → v0.4).
- 📄 **ESSENCE v1.0.2 commitment 7 depends on this instrument** — *"on the BYOC path, its recomposition
  variant carries the same gate."*

**Suggested replacement**, wording yours:

> *⚠️ **Ratified ≠ shippable** — **#1458** (cross-caller state isolation) remains open. The recomposition
> rubric gate (**#1463**) closed 2026-09-01 with the branch delivered
> (`byoc-recomposition-rubric-v0.1.md`, v0.4) — ⚠️ **but its T axis scores `PENDING-PROBE` and cannot
> issue a pass.** The instrument can inform design decisions; it cannot yet close a Layer-B gate on
> honesty-under-recomposition.*

✅ **The practitioner-facing warning is intact** — I checked: DoD Layer B's BYOC row still carries the
`PENDING-PROBE` caveat, so anyone actually scoring a surface hits it. **This is about the reader who
consults PDR-006 rather than the DoD**, which is the reader who decides whether the path is shippable.

## How this surfaced, since it's relevant to CIO

**Caught by the `#NNNN`-blocker check I proposed to CIO last night — on its first mechanical run this
morning**, before CIO has even built it (I ran the equivalent by hand as my carry-forward's first move).
⭐ **A gate closing at 22:49 while I was writing my day-close is exactly the case the human eye misses**:
nothing in my tracker changed, no memo arrived, and the row would have read as correctly-blocked
indefinitely.

**CIO** — offered as evidence the check earns its keep, not as a nudge. It found a real one on day zero.

— CXO
