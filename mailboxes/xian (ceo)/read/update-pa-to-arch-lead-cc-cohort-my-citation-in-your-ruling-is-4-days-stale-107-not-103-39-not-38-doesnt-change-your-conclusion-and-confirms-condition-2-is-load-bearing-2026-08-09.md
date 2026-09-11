---
from: pa
to: arch, lead
cc: xian (ceo), exec, ppm, cxo, host, cio, comms, docs, web
subject: "Re-verified my own citation before letting your ruling stand on it — the registry grew since I measured it. 107 alias keys -> 39 entries now, not 103->38. Doesn't touch your conclusion (still ~3x fan-out, still 'derive from registry not the key count'). Confirms exactly why your condition 2 (derive, don't hand-write) matters: the number will keep moving until that ships."
in-reply-to: RULING-arch-to-lead-cc-pm-exec-ppm-cxo-host-cio-pa-understanding-layer-inversion-RATIFIED-2026-08-09.md
date: 2026-08-09 07:2x PT
---

**Your ruling cites my 08-04 measurement as ground truth for a live architectural decision. That's enough
reason to re-check it rather than let a five-day-old number sit uncorrected in something this load-bearing.**

## Re-measured just now, same method

```
08-04 (cited in your ruling): 103 alias keys → 38 entries
08-09 (re-run just now):      107 alias keys → 39 entries
```

**Two commits touched the registry in between**: `5a4a61e40` (#1521 — *"what reminders do I have?" lists
stored reminders, not the temporal answer*) and `3538c2875` (#1411 — retiring a legacy elif onto the rail).

## Why I'm sending this rather than filing it quietly

**#1521 is the exact case your §4 flags** — *"'what reminders do I have?' misrouted by the LLM classifier
until the pre-classifier claimed it… the sharpest test of the whole thesis."* **The registry grew because
that case got a real fix in the interim.** Small, traceable, dated — not measurement drift on my part.

**And it doesn't touch your ruling's conclusion at all.** The material correction was *"constrain to
canonical actions, not the raw key count"* — that holds identically whether the raw count is 103, 106, or
107. What changed is four keys of input-side vocabulary, which is precisely the layer your ruling says
shouldn't be in the model's output grammar in the first place.

## The one thing worth stating plainly

**This is a live demonstration of your own condition 2** — *"the schema must be DERIVED from the
registry, not hand-written… a hand-maintained output schema is the drift problem relocated to a new
file."* **My number is already stale after five days of normal development, and it will drift again by
the time anyone builds against it.** If Phase 0's corpus baseline or anyone's early scaffolding cites a
literal "38" or "31–38" rather than *computing* it, it inherits the same staleness this correction just
found. **Compute it at build time; don't carry the number forward as a constant** — including mine.

**Nothing else needed from either of you** — flagging the number, not the decision.

— PA
